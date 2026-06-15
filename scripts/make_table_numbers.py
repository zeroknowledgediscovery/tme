#!/usr/bin/env python3
"""Generate table CSV and LaTeX outputs."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tme.tables import compute_all, make_table1_tex, make_table2_tex
from tme.io_utils import write_csv


def main() -> None:
    data = compute_all(ROOT)
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    write_csv(out / "table1_velocity_demon.csv", data["demons"]["velocity_selection_rows"])
    write_csv(out / "table2_scale.csv", data["table2_rows"])
    (out / "table1_velocity_demon.tex").write_text(make_table1_tex(data["demons"]["velocity_selection_rows"]), encoding="utf-8")
    (out / "table2_scale.tex").write_text(make_table2_tex(data["table2_rows"]), encoding="utf-8")
    print(f"Wrote table outputs to {out}")


if __name__ == "__main__":
    main()
