import unittest
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tme.symbolic import human_sentence_scale, gpt_sentence_scale


class TestSymbolic(unittest.TestCase):
    def test_human_sentence_scale(self):
        out = human_sentence_scale(5e21, 1e7)
        self.assertAlmostEqual(out["I_plus_1"], 5e14)
        self.assertAlmostEqual(out["L"], 14.69897, places=5)
        self.assertAlmostEqual(out["Lambda"], 1.19587, places=5)

    def test_gpt_sentence_scale(self):
        out = gpt_sentence_scale(5e21, 1e7, 100, 0.74, 0.77, 0.0)
        self.assertAlmostEqual(out["q_ratio_gpt_to_human"], 0.125)
        self.assertAlmostEqual(out["I_plus_1"] / 6.25e13, 1.0, places=12)
        self.assertAlmostEqual(out["Lambda"], 1.17014, places=5)


if __name__ == "__main__":
    unittest.main()
