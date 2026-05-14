#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import UTC, datetime
from pathlib import PurePosixPath

from notegen_paths import (
    REPO_ROOT,
    changelog_path,
    classify_content_path,
    load_notegenignore,
    to_posix,
)


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)", re.DOTALL)
TITLE_RE = re.compile(r'^\s*title\s*:\s*(?P<value>.+?)\s*$', re.MULTILINE)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        cwd=REPO_ROOT,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def commit_timestamp(commit: str = "HEAD") -> str:
    raw = git("show", "-s", "--format=%cI", commit).stdout.strip()
    parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    return parsed.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def current_timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def changed_paths(
    commit: str = "HEAD", staged: bool = False
) -> list[tuple[str, str | None, str]]:
    if staged:
        output = git(
            "diff",
            "--cached",
            "-M",
            "--name-status",
            "--diff-filter=ACDMR",
        ).stdout
    else:
        output = git(
            "diff-tree",
            "--root",
            "-r",
            "-M",
            "--no-commit-id",
            "--name-status",
            commit,
        ).stdout

    changes: list[tuple[str, str | None, str]] = []
    for line in output.splitlines():
        parts = line.split("\t")
        if not parts:
            continue

        status = parts[0]
        status_code = status[0]

        if status_code == "A" and len(parts) == 2:
            changes.append(("created", None, parts[1]))
        elif status_code == "M" and len(parts) == 2:
            changes.append(("updated", None, parts[1]))
        elif status_code == "D" and len(parts) == 2:
            changes.append(("deleted", None, parts[1]))
        elif status_code == "R" and len(parts) == 3:
            changes.append(("renamed", parts[1], parts[2]))

    return changes


def read_file_at(commit: str, path: str) -> str | None:
    result = git("show", f"{commit}:{path}", check=False)
    if result.returncode != 0:
        return None
    return result.stdout


def read_index_file(path: str) -> str | None:
    result = git("show", f":{path}", check=False)
    if result.returncode != 0:
        return None
    return result.stdout


def fallback_title(path: str) -> str:
    stem = PurePosixPath(path).stem
    return stem.replace("-", " ").replace("_", " ").strip().title()


def extract_title(text: str | None, path: str) -> str:
    if text:
        frontmatter = FRONTMATTER_RE.search(text)
        source = frontmatter.group(1) if frontmatter else text
        title = TITLE_RE.search(source)
        if title:
            value = title.group("value").strip()
            if (
                len(value) >= 2
                and value[0] == value[-1]
                and value[0] in {"'", '"'}
            ):
                value = value[1:-1]
            if value:
                return value

    return fallback_title(path)


def content_for_change(
    action: str, old_path: str | None, path: str, staged: bool
) -> str | None:
    if staged:
        if action == "deleted":
            return read_file_at("HEAD", path)
        return read_index_file(path) or (
            read_file_at("HEAD", old_path) if old_path else None
        )

    if action == "deleted":
        return read_file_at("HEAD^", path)
    return read_file_at("HEAD", path) or (
        read_file_at("HEAD^", old_path) if old_path else None
    )


def normalize_markdown_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines) + "\n"


def is_format_only_change(
    action: str, old_path: str | None, path: str, staged: bool
) -> bool:
    if action != "updated" or old_path is not None:
        return False

    before = read_file_at("HEAD", path) if staged else read_file_at("HEAD^", path)
    after = read_index_file(path) if staged else read_file_at("HEAD", path)
    if before is None or after is None:
        return False

    return normalize_markdown_text(before) == normalize_markdown_text(after)


def parent_index_path(path: str) -> str | None:
    posix_path = PurePosixPath(path)
    parts = posix_path.parts

    if "assets" in parts:
        asset_index = parts.index("assets")
        parent = PurePosixPath(*parts[:asset_index])
    else:
        parent = posix_path.parent

    if posix_path.name == "_index.md":
        parent = parent.parent

    if str(parent) in {"", "."}:
        return None
    return to_posix(parent / "_index.md")


def topic_for_path(path: str, action: str, staged: bool) -> str | None:
    index_path = parent_index_path(path)
    if not index_path:
        return None

    if staged:
        text = read_index_file(index_path)
        if text is None:
            text = read_file_at("HEAD", index_path)
    else:
        text = read_file_at("HEAD", index_path)
        if text is None and action == "deleted":
            text = read_file_at("HEAD^", index_path)

    if text is None:
        return fallback_title(str(PurePosixPath(index_path).parent))
    return extract_title(text, index_path)


def existing_events(path: str) -> set[str]:
    changelog = REPO_ROOT / path
    if not changelog.exists():
        return set()
    return set(changelog.read_text(encoding="utf-8").splitlines())


def build_events(staged: bool = False) -> list[dict[str, object]]:
    timestamp = current_timestamp() if staged else commit_timestamp()
    default_source = "pre-commit" if staged else "post-commit"
    source = os.environ.get("CHANGELOG_SOURCE", default_source)
    ignore_patterns = load_notegenignore()
    events: list[dict[str, object]] = []

    for action, old_path, path in changed_paths(staged=staged):
        path = to_posix(path)
        old_path = to_posix(old_path) if old_path else None

        kind = classify_content_path(path, ignore_patterns)
        if kind is None and old_path:
            kind = classify_content_path(old_path, ignore_patterns)
        if kind is None:
            continue

        if is_format_only_change(action, old_path, path, staged):
            continue

        content = None if kind == "asset" else content_for_change(action, old_path, path, staged)
        event: dict[str, object] = {
            "timestamp": timestamp,
            "action": action,
            "kind": kind,
            "path": path,
        }

        if old_path:
            event["oldPath"] = old_path

        event["title"] = extract_title(content, path)

        topic = topic_for_path(path, action, staged)
        if topic:
            event["topic"] = topic

        event["source"] = source
        events.append(event)

    return events


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--staged",
        action="store_true",
        help="build changelog events from the staged index instead of HEAD",
    )
    args = parser.parse_args()

    changelog_relpath = changelog_path()
    changelog = REPO_ROOT / changelog_relpath
    seen = existing_events(changelog_relpath)
    lines: list[str] = []

    for event in build_events(staged=args.staged):
        line = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
        if line not in seen:
            lines.append(line)
            seen.add(line)

    if lines:
        with changelog.open("a", encoding="utf-8") as handle:
            for line in lines:
                handle.write(line + "\n")
        print(f"Appended {len(lines)} changelog event(s) to {changelog_relpath}.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
