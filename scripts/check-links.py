#!/usr/bin/env python3
"""Check relative Markdown links in README.md and wiki/*.md."""

from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def check_file(path: Path) -> list[tuple[Path, str]]:
    broken: list[tuple[Path, str]] = []
    text = path.read_text(encoding="utf-8")
    for match in LINK.finditer(text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0].strip()
        if not target:
            continue
        candidates = [target]
        if not Path(target).suffix:
            candidates.append(target + ".md")
        if not any((path.parent / urllib.parse.unquote(c)).exists() for c in candidates):
            broken.append((path, target))
    return broken


def main() -> int:
    files = [ROOT / "README.md", *sorted((ROOT / "wiki").glob("*.md"))]
    broken: list[tuple[Path, str]] = []
    for path in files:
        if path.exists():
            broken.extend(check_file(path))
    for path, target in broken:
        print(f"{path.relative_to(ROOT)}: broken link -> {target}")
    print(f"checked {len(files)} file(s), broken: {len(broken)}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
