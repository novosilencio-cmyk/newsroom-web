import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_norwegian_editorial_style import find_violations, NorwegianProseParser, APPROVED_PHRASES  # noqa: E402


class NorwegianEditorialStyleTest(unittest.TestCase):
    def test_editor_approval_is_scoped_to_exact_text_and_article(self):
        article = "public/articles/amediastiftelsen-aschehoug-2026.html"
        phrase = APPROVED_PHRASES[article][0]
        allowed = NorwegianProseParser(ROOT / article)
        allowed.feed(f'<html lang="nb"><p>{phrase}</p></html>')
        self.assertEqual([], allowed.violations)
        changed = NorwegianProseParser(ROOT / article)
        changed.feed(f'<html lang="nb"><p>{phrase} og nye ord</p></html>')
        self.assertEqual(1, len(changed.violations))
        elsewhere = NorwegianProseParser(ROOT / "public/other.html")
        elsewhere.feed(f'<html lang="nb"><p>{phrase}</p></html>')
        self.assertEqual(1, len(elsewhere.violations))

    def test_reader_facing_norwegian_prose_reaches_full_score(self):
        self.assertEqual([], find_violations())


if __name__ == "__main__":
    unittest.main()
