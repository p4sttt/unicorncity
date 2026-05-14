from __future__ import annotations

import json
from fnmatch import fnmatch
from pathlib import Path, PurePosixPath


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHANGELOG_PATH = "changelog.jsonl"

SERVICE_PATHS = {
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    ".gitlab-ci.yml",
    ".notegenignore",
    "notegen.config.json",
    DEFAULT_CHANGELOG_PATH,
    "changelog.json",
}

SERVICE_DIRS = {
    ".agents",
    ".codex",
    ".git",
    ".githook",
    ".githooks",
    ".obsidian",
    ".venv",
    ".vscode",
    "scripts",
}


def to_posix(path: str | Path) -> str:
    return str(PurePosixPath(str(path).replace("\\", "/")))


def load_notegenignore(root: Path = REPO_ROOT) -> list[str]:
    ignore_path = root / ".notegenignore"
    if not ignore_path.exists():
        return []

    patterns: list[str] = []
    for raw_line in ignore_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return patterns


def changelog_path(root: Path = REPO_ROOT) -> str:
    config_path = root / "notegen.config.json"
    if not config_path.exists():
        return DEFAULT_CHANGELOG_PATH

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return DEFAULT_CHANGELOG_PATH

    path = config.get("changelogPath")
    if isinstance(path, str) and path.strip():
        return to_posix(path.strip())
    return DEFAULT_CHANGELOG_PATH


def _matches_ignore(path: str, pattern: str) -> bool:
    path = to_posix(path).lstrip("/")
    pattern = pattern.lstrip("/")

    if pattern.endswith("/"):
        dirname = pattern.rstrip("/")
        return path == dirname or path.startswith(f"{dirname}/")

    if "/" in pattern:
        return fnmatch(path, pattern)

    return any(fnmatch(part, pattern) for part in path.split("/"))


def is_service_path(path: str, ignore_patterns: list[str] | None = None) -> bool:
    normalized = to_posix(path).lstrip("/")
    parts = normalized.split("/")

    if normalized in SERVICE_PATHS:
        return True
    if any(part in SERVICE_DIRS or part.startswith(".") for part in parts):
        return True

    patterns = ignore_patterns if ignore_patterns is not None else load_notegenignore()
    return any(_matches_ignore(normalized, pattern) for pattern in patterns)


def classify_content_path(
    path: str, ignore_patterns: list[str] | None = None
) -> str | None:
    normalized = to_posix(path).lstrip("/")

    if is_service_path(normalized, ignore_patterns):
        return None

    parts = PurePosixPath(normalized).parts
    if "assets" in parts:
        return "asset"
    if normalized.endswith(".ipynb"):
        return "note"
    if not normalized.endswith(".md"):
        return None

    name = PurePosixPath(normalized).name

    if name == "_index.md":
        return "topic"
    return "note"


def iter_content_markdown(root: Path = REPO_ROOT) -> list[Path]:
    ignore_patterns = load_notegenignore(root)
    files: list[Path] = []

    for path in root.rglob("*.md"):
        rel = to_posix(path.relative_to(root))
        if classify_content_path(rel, ignore_patterns) is not None:
            files.append(path)

    return sorted(files)
