#!/usr/bin/env python3
"""Check the current Norwegian editorial exercise rule.

The rule applies to reader-facing Norwegian prose. Verbatim source titles retain
their original wording because editorial style can never overrule source truth.
"""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
FORBIDDEN = re.compile(r"\bikke\b", re.IGNORECASE)
VERBATIM_EXEMPTIONS = (
    "Eldrebølgen kom ikke overraskende",
)


class NorwegianProseParser(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.path = path
        self.lang_stack: list[str] = [""]
        self.tag_stack: list[str] = []
        self.violations: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        inherited = self.lang_stack[-1]
        current = values.get("lang") or inherited
        if values.get("data-language-panel") == "no":
            current = "nb"
        self.lang_stack.append(current.lower())
        self.tag_stack.append(tag)
        if self._is_norwegian:
            for name in ("content", "title", "aria-label", "alt"):
                value = values.get(name)
                if value:
                    self._check(value, f"<{tag} {name}>")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if self.tag_stack:
            self.tag_stack.pop()
            self.lang_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._is_norwegian:
            self._check(data, f"<{self.tag_stack[-1] if self.tag_stack else 'document'}>")

    @property
    def _is_norwegian(self) -> bool:
        return self.lang_stack[-1] in {"nb", "nn", "no"}

    def _check(self, text: str, location: str) -> None:
        editorial_text = text
        for source_title in VERBATIM_EXEMPTIONS:
            editorial_text = editorial_text.replace(source_title, "")
        if FORBIDDEN.search(editorial_text):
            compact = " ".join(text.split())
            self.violations.append(f"{self.path.relative_to(ROOT)} {location}: {compact}")


def find_violations() -> list[str]:
    violations: list[str] = []
    for path in sorted(PUBLIC.rglob("*.html")):
        parser = NorwegianProseParser(path)
        parser.feed(path.read_text(encoding="utf-8"))
        violations.extend(parser.violations)
    return violations


def main() -> int:
    violations = find_violations()
    if violations:
        print("Norwegian editorial style gate failed:")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("Norwegian editorial style gate passed: 100/100.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
