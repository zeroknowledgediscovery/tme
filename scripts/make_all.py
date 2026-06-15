#!/usr/bin/env python3
"""Generate all manuscript calculation outputs."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tme.tables import write_outputs


def main() -> None:
    data = write_outputs(ROOT)
    out = ROOT / "outputs"
    print(f"Wrote outputs to {out}")
    print("Figure 1 values:")
    for row in data["figure1_rows"]:
        print(f"  {row['order']:>2}. {row['key']:<24} Lambda={row['Lambda']:.6g} L={row['L']:.6g}")


if __name__ == "__main__":
    main()
