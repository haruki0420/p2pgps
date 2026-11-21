#!/usr/bin/env python3
"""Check relative Markdown links in README.md and wiki/*.md.

Usage:
    python3 scripts/check-links.py [ROOT]

ROOT defaults to the repository containing this script. Pass another
repository root to check its README and wiki pages.
"""

from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE = re.compile(
    r"^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[ \t]*$",
    re.MULTILINE | re.DOTALL,
)
INLINE_CODE = re.compile(r"`+[^`\n]*`+")


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code spans before link extraction."""
    text = FENCE.sub("", text)
    return INLINE_CODE.sub("", text)


def check_file(path: Path, is_wiki: bool) -> list[tuple[Path, str, str]]:
    broken: list[tuple[Path, str, str]] = []
    text = strip_code(path.read_text(encoding="utf-8"))
    for match in LINK.finditer(text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if any(ch.isspace() for ch in target):
            # Swift/Kotlin array literals such as [UInt8](repeating: 0, count: 20)
            # are not links and cannot be a local path without escaping.
            continue
        target = target.split("#", 1)[0].strip()
        if not target:
            continue
        if is_wiki and target.startswith("../"):
            broken.append((path, target, "wiki-relative-parent"))
            continue
        candidates = [target]
        if not Path(target).suffix:
            candidates.append(target + ".md")
        if not any((path.parent / urllib.parse.unquote(c)).exists() for c in candidates):
            broken.append((path, target, "broken"))
    return broken


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_ROOT
    files = [root / "README.md", *sorted((root / "wiki").glob("*.md"))]
    broken: list[tuple[Path, str, str]] = []
    checked = 0
    for path in files:
        if not path.exists():
            continue
        checked += 1
        broken.extend(check_file(path, path.parent.name == "wiki"))
    for path, target, reason in broken:
        rel = path.relative_to(root)
        if reason == "wiki-relative-parent":
            print(f"{rel}: wiki relative link (use an absolute GitHub blob URL) -> {target}")
        else:
            print(f"{rel}: broken link -> {target}")
    print(f"checked {checked} file(s), broken: {len(broken)}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
