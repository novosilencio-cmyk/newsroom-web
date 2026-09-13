import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_norwegian_editorial_style import find_violations  # noqa: E402


class NorwegianEditorialStyleTest(unittest.TestCase):
    def test_reader_facing_norwegian_prose_reaches_full_score(self):
        self.assertEqual([], find_violations())


if __name__ == "__main__":
    unittest.main()
