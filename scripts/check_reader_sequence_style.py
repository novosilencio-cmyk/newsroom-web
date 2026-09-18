#!/usr/bin/env python3
"""Guard reader-facing text against compressed arrow chains.

Action arrows inside links remain allowed. The rule targets explanatory prose,
labels and headings where an arrow is used as shorthand for meaning.
"""
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

class ArrowParser(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.stack = []
        self.violations = []

    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if "→" not in data:
            return
        if any(tag in {"a","button","script","style","code","pre"} for tag in self.stack):
            return
        compact = " ".join(data.split())
        self.violations.append(f"{self.path.relative_to(ROOT)}: {compact}")

def main():
    violations=[]
    for path in sorted(PUBLIC.rglob("*.html")):
        parser=ArrowParser(path)
        parser.feed(path.read_text(encoding="utf-8"))
        violations.extend(parser.violations)
    if violations:
        print("Reader-sequence style check failed:")
        for item in violations:
            print(f"- {item}")
        return 1
    print("Reader-sequence style check passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
