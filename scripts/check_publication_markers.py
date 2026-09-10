#!/usr/bin/env python3
"""Block internal editorial markers from public and source-facing files."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRECTORIES = ("articles", "content", "public")
ROOT_FILES = ("index.html", "how-we-work.html", "support.html", "script.js", "feedback.js")
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".md", ".txt", ".yaml", ".yml"}

FORBIDDEN_PATTERNS = (
    ("internal editorial marker", re.compile(r"\[(?:INTERNAL|END\s+INTERNAL\s+NOTE)\b", re.I)),
    ("unresolved TK marker", re.compile(r"\[TK(?:\b|[\s:—-])", re.I)),
    ("unresolved verification marker", re.compile(r"\[VERIFY(?:\b|[\s:—-])", re.I)),
    ("missing-source marker", re.compile(r"\[SOURCE\s+NEEDED(?:\b|[\s:—-])", re.I)),
    ("do-not-publish instruction", re.compile(r"\bNOT\s+FOR\s+PUBLICATION\b", re.I)),
    ("removal instruction", re.compile(r"\bREMOVE\s+BEFORE\s+PUBLICATION\b", re.I)),
    (
        "publication approval is false",
        re.compile(r"[\"']?publication_approved[\"']?\s*[:=]\s*(?:false|no)\b", re.I),
    ),
    ("internal-draft status", re.compile(r"[\"']?status[\"']?\s*[:=]\s*[\"']?internal[_-]draft\b", re.I)),
    ("internal HTML comment", re.compile(r"<!--\s*INTERNAL\b", re.I)),
)


def publication_files(root: Path = ROOT) -> list[Path]:
    files: set[Path] = set()
    for directory in SCAN_DIRECTORIES:
        base = root / directory
        if base.exists():
            files.update(path for path in base.rglob("*") if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES)
    for filename in ROOT_FILES:
        path = root / filename
        if path.is_file():
            files.add(path)
    return sorted(files)


def find_violations(root: Path = ROOT) -> list[tuple[Path, int, str]]:
    violations: list[tuple[Path, int, str]] = []
    for path in publication_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for label, pattern in FORBIDDEN_PATTERNS:
                if pattern.search(line):
                    violations.append((path.relative_to(root), line_number, label))
    return violations


def main() -> int:
    violations = find_violations()
    if not violations:
        print("Publication-marker check passed.")
        return 0

    print("Publication-marker check failed. Resolve these internal markers before publication:", file=sys.stderr)
    for path, line_number, label in violations:
        print(f"- {path}:{line_number}: {label}", file=sys.stderr)
    print("Passing this check does not itself grant publication approval.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
