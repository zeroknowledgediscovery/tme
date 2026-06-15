import unittest
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tme.demons import entropy_reduction_demon, velocity_selection_demon, mb_tail_q, mb_excess_phi


class TestDemons(unittest.TestCase):
    def test_entropy_reduction_scale(self):
        out = entropy_reduction_demon(1e-19)
        self.assertAlmostEqual(out["deltaS_over_kB"], 7242.970516, places=3)
        self.assertAlmostEqual(out["Lambda"], 3.4978, places=3)

    def test_mb_tail_values(self):
        self.assertAlmostEqual(mb_tail_q(2.0), 0.261464, places=5)
        self.assertAlmostEqual(mb_excess_phi(2.0), 1.652, places=3)

    def test_velocity_sparse(self):
        out = velocity_selection_demon(N=100, epsilon=2.0)
        self.assertAlmostEqual(out["N_selected"], 13.0732, places=3)
        self.assertAlmostEqual(out["L"], 9.38, places=2)


if __name__ == "__main__":
    unittest.main()
