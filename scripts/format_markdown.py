#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from notegen_paths import (
    REPO_ROOT,
    classify_content_path,
    iter_content_markdown,
    load_notegenignore,
    to_posix,
)


def format_markdown_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines) + "\n"


def staged_content_markdown() -> list[Path]:
    result = subprocess.run(
        [
            "git",
            "-c",
            "core.quotepath=false",
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=ACMR",
            "--",
            "*.md",
        ],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    ignore_patterns = load_notegenignore()
    files: list[Path] = []

    for line in result.stdout.splitlines():
        path = to_posix(line)
        if classify_content_path(path, ignore_patterns) is not None:
            files.append(REPO_ROOT / path)

    return files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--staged",
        action="store_true",
        help="format only content markdown files currently staged for commit",
    )
    args = parser.parse_args()

    changed = 0
    files = staged_content_markdown() if args.staged else iter_content_markdown()

    for path in files:
        if not path.exists():
            continue

        original = path.read_text(encoding="utf-8")
        formatted = format_markdown_text(original)

        if formatted != original:
            path.write_text(formatted, encoding="utf-8")
            changed += 1

    if changed:
        print(f"Formatted {changed} markdown file(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
