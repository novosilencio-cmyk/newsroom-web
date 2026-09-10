from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_publication_markers.py"
SPEC = importlib.util.spec_from_file_location("publication_markers", SCRIPT)
assert SPEC and SPEC.loader
publication_markers = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publication_markers)


class PublicationMarkerTests(unittest.TestCase):
    def write_public_article(self, root: Path, content: str) -> None:
        article = root / "public" / "articles" / "example.html"
        article.parent.mkdir(parents=True)
        article.write_text(content, encoding="utf-8")

    def test_reader_ready_copy_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_public_article(root, "<p>A documented opening.</p>")
            self.assertEqual(publication_markers.find_violations(root), [])

    def test_internal_note_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_public_article(root, "[INTERNAL EDITORIAL NOTE — REMOVE BEFORE PUBLICATION]")
            violations = publication_markers.find_violations(root)
            self.assertGreaterEqual(len(violations), 2)

    def test_unresolved_markers_fail(self) -> None:
        for marker in ("[TK: date]", "[VERIFY: figure]", "[SOURCE NEEDED]"):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_public_article(root, marker)
                self.assertTrue(publication_markers.find_violations(root))

    def test_false_approval_metadata_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_public_article(root, 'publication_approved: false')
            self.assertTrue(publication_markers.find_violations(root))

    def test_internal_note_in_documentation_is_not_a_publish_surface(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            documentation = root / "docs" / "standard.md"
            documentation.parent.mkdir(parents=True)
            documentation.write_text("[INTERNAL EDITORIAL NOTE]", encoding="utf-8")
            self.assertEqual(publication_markers.find_violations(root), [])


if __name__ == "__main__":
    unittest.main()
