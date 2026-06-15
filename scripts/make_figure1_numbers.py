#!/usr/bin/env python3
"""Generate Fig. 1 values only."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tme.tables import compute_all
from tme.io_utils import write_csv, write_json


def main() -> None:
    data = compute_all(ROOT)
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    write_json(out / "figure1_numbers.json", data["figure1_rows"])
    write_csv(out / "figure1_numbers.csv", data["figure1_rows"], ["order", "key", "label", "source", "L", "Lambda", "I"])
    print(f"Wrote {out / 'figure1_numbers.csv'}")


if __name__ == "__main__":
    main()
