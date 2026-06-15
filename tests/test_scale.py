import math
import unittest

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tme.scale import L_from_I, Lambda_from_I, Lambda_from_L, I_from_L


class TestScale(unittest.TestCase):
    def test_passive(self):
        self.assertEqual(L_from_I(0), 0)
        self.assertEqual(Lambda_from_I(0), 0)

    def test_inverse(self):
        for L in [0, 1, 3.2, 14.699]:
            self.assertAlmostEqual(L_from_I(I_from_L(L)), L, places=10)

    def test_lambda(self):
        self.assertAlmostEqual(Lambda_from_L(14.699), math.log10(15.699), places=12)


if __name__ == "__main__":
    unittest.main()
