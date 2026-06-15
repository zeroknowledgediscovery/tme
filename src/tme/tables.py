"""Build manuscript-ready numeric tables and figure values."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from .controllers import fixed_feedback_range, repeated_binary_control_range
from .demons import entropy_reduction_demon, velocity_selection_table, range_from_velocity_rows
from .symbolic import human_sentence_scale, gpt_sentence_scale, symbolic_sensitivity
from .scale import Lambda_from_L, L_from_I
from .io_utils import read_json, write_json, write_csv


def fmt_float(x: float, digits: int = 3) -> str:
    if x == 0:
        return "0"
    ax = abs(x)
    if 1e-3 <= ax < 1e4:
        return f"{x:.{digits}g}"
    return f"{x:.{digits}e}"


def fmt_range(a: float, b: float, digits: int = 3) -> str:
    return f"{fmt_float(a, digits)}--{fmt_float(b, digits)}"


def load_inputs(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    return {
        "controllers": read_json(root / "inputs" / "controller_inputs.json"),
        "demons": read_json(root / "inputs" / "demon_inputs.json"),
        "symbolic": read_json(root / "inputs" / "symbolic_entropy_inputs.json"),
        "figure1": read_json(root / "inputs" / "figure1_examples.json"),
    }


def compute_all(root: str | Path) -> dict[str, Any]:
    """Compute all manuscript calibration values from input JSON files."""
    inputs = load_inputs(root)

    # Controllers.
    ff_in = inputs["controllers"]["fixed_feedback"]
    fixed = fixed_feedback_range(ff_in["alpha_min"], ff_in["alpha_max"])
    rep_in = inputs["controllers"]["repeated_dynamic_control"]
    repeated = repeated_binary_control_range(rep_in["binary_stages_min"], rep_in["binary_stages_max"])

    # Demons.
    pc = inputs["demons"]["physical_constants"]
    maxwell_in = inputs["demons"]["maxwell_single_entropy_reduction"]
    maxwell = entropy_reduction_demon(maxwell_in["deltaS_J_per_K"], pc["kB_J_per_K"])

    vel_in = inputs["demons"]["velocity_selection"]
    vel_rows = velocity_selection_table(
        epsilons=vel_in["epsilons"],
        N_sparse=vel_in["N_sparse"],
        N_one_mm3_air=vel_in["N_one_mm3_air"],
        T_K=pc["T_K"],
        molecular_mass_kg=pc["nitrogen_molecular_mass_kg"],
        kB_J_per_K=pc["kB_J_per_K"],
        half_chamber_factor=vel_in["one_shot_half_chamber_factor"],
    )
    vel_sparse_range = range_from_velocity_rows(vel_rows, "L_sparse")
    vel_1mm3_range = range_from_velocity_rows(vel_rows, "L_one_mm3")

    # Symbolic.
    sent = inputs["symbolic"]["sentence_scale"]
    human = human_sentence_scale(sent["N_V"], sent["N_G"], sent.get("q_human", 1.0))
    gpt = gpt_sentence_scale(
        N_V=sent["N_V"],
        N_G=sent["N_G"],
        n_star_characters=sent["n_star_characters"],
        H_gpt_bits_per_character=sent["H_gpt_bits_per_character"],
        H_human_bits_per_character=sent["H_human_bits_per_character"],
        rho_n_star=sent.get("rho_n_star", 0.0),
        q_human=sent.get("q_human", 1.0),
    )
    sensitivity = symbolic_sensitivity(
        N_V=sent["N_V"],
        N_G=sent["N_G"],
        n_star_characters=sent["n_star_characters"],
        H_gpt_bits_per_character=sent["H_gpt_bits_per_character"],
        H_human_bits_per_character=sent["H_human_bits_per_character"],
        rho_values=inputs["symbolic"]["sensitivity"].get("rho_values", []),
        q_human=sent.get("q_human", 1.0),
    )

    # Compact rows used in Fig. 1 / Table II.
    sources = {
        "passive_baseline": {"I": 0.0, "L": 0.0, "Lambda": 0.0},
        "fixed_feedback_midpoint": {"L": fixed["L_mid"], "Lambda": fixed["Lambda_mid"], "I": 10 ** fixed["L_mid"] - 1},
        "repeated_control_midpoint": {"L": repeated["L_mid"], "Lambda": repeated["Lambda_mid"], "I": 10 ** repeated["L_mid"] - 1},
        "velocity_sparse_midpoint": {"L": vel_sparse_range["L_mid"], "Lambda": vel_sparse_range["Lambda_mid"], "I": 10 ** vel_sparse_range["L_mid"] - 1},
        "gpt5_symbolic": gpt,
        "human_symbolic": human,
        "maxwell_single_entropy": maxwell,
        "velocity_1mm3_midpoint": {"L": vel_1mm3_range["L_mid"], "Lambda": vel_1mm3_range["Lambda_mid"], "I": math.inf},
    }

    fig_rows = []
    for i, ex in enumerate(inputs["figure1"]["examples"]):
        src = sources[ex["source"]]
        fig_rows.append({
            "order": i + 1,
            "key": ex["key"],
            "label": ex["label"],
            "source": ex["source"],
            "L": src["L"],
            "Lambda": src["Lambda"],
            "I": src.get("I", float("nan")),
        })

    table2_rows = [
        {
            "example_regime": "Passive matter / passive gas",
            "calculation_basis": "Baseline dynamics, P = P0.",
            "I_display": "0",
            "L_min": 0.0,
            "L_max": 0.0,
            "Lambda_min": 0.0,
            "Lambda_max": 0.0,
            "sort_L_mid": 0.0,
        },
        {
            "example_regime": "Narrow fixed-feedback controller",
            "calculation_basis": "Constant rare-valid lift, P(V_delta) = alpha delta, with alpha = 2--10^2.",
            "I_display": f"{fmt_float(fixed['I_min'])}--{fmt_float(fixed['I_max'])}",
            "L_min": fixed["L_min"],
            "L_max": fixed["L_max"],
            "Lambda_min": fixed["Lambda_min"],
            "Lambda_max": fixed["Lambda_max"],
            "sort_L_mid": fixed["L_mid"],
        },
        {
            "example_regime": "Repeated dynamic controller",
            "calculation_basis": "Sequential binary lift over 7--10 controlled stages, I + 1 approx 2^7--2^10.",
            "I_display": f"{fmt_float(repeated['I_min'])}--{fmt_float(repeated['I_max'])}",
            "L_min": repeated["L_min"],
            "L_max": repeated["L_max"],
            "Lambda_min": repeated["Lambda_min"],
            "Lambda_max": repeated["Lambda_max"],
            "sort_L_mid": repeated["L_mid"],
        },
        {
            "example_regime": "100-particle velocity-selection demon",
            "calculation_basis": "Maxwell-Boltzmann velocity selection with N = 100 particles and epsilon = 2--5.",
            "I_display": f"10^{vel_sparse_range['L_min']:.3g}--10^{vel_sparse_range['L_max']:.3g}",
            "L_min": vel_sparse_range["L_min"],
            "L_max": vel_sparse_range["L_max"],
            "Lambda_min": vel_sparse_range["Lambda_min"],
            "Lambda_max": vel_sparse_range["Lambda_max"],
            "sort_L_mid": vel_sparse_range["L_mid"],
        },
        {
            "example_regime": "GPT-5 symbolic generation",
            "calculation_basis": "Central sentence-scale rare-valid lift with N_V = 5e21, N_G = 1e7, n_star = 100, H_H = 0.77, H_GPT5 = 0.74, rho_100 = 0.",
            "I_display": f"{fmt_float(gpt['I_plus_1'])}",
            "L_min": gpt["L"],
            "L_max": gpt["L"],
            "Lambda_min": gpt["Lambda"],
            "Lambda_max": gpt["Lambda"],
            "sort_L_mid": gpt["L"],
        },
        {
            "example_regime": "Expert human symbolic generation",
            "calculation_basis": "Same sentence-scale calculation with q_H approx 1: I_H + 1 = N_V/N_G.",
            "I_display": f"{fmt_float(human['I_plus_1'])}",
            "L_min": human["L"],
            "L_max": human["L"],
            "Lambda_min": human["Lambda"],
            "Lambda_max": human["Lambda"],
            "sort_L_mid": human["L"],
        },
        {
            "example_regime": "Maxwell demon with Delta S = 1e-19 J/K",
            "calculation_basis": "Fluctuation-theorem scale with Delta S/k_B computed from the exact Boltzmann constant.",
            "I_display": f"~10^{maxwell['L']:.0f}",
            "L_min": maxwell["L"],
            "L_max": maxwell["L"],
            "Lambda_min": maxwell["Lambda"],
            "Lambda_max": maxwell["Lambda"],
            "sort_L_mid": maxwell["L"],
        },
        {
            "example_regime": "Velocity-selection demon in 1 mm^3 air",
            "calculation_basis": "Maxwell-Boltzmann velocity selection with N = 2.44e16 and epsilon = 2--5.",
            "I_display": f"10^({vel_1mm3_range['L_min']:.3e})--10^({vel_1mm3_range['L_max']:.3e})",
            "L_min": vel_1mm3_range["L_min"],
            "L_max": vel_1mm3_range["L_max"],
            "Lambda_min": vel_1mm3_range["Lambda_min"],
            "Lambda_max": vel_1mm3_range["Lambda_max"],
            "sort_L_mid": vel_1mm3_range["L_mid"],
        },
    ]
    table2_rows.sort(key=lambda r: r["sort_L_mid"])

    return {
        "inputs": inputs,
        "controllers": {"fixed_feedback": fixed, "repeated_dynamic_control": repeated},
        "demons": {"maxwell_single_entropy": maxwell, "velocity_selection_rows": vel_rows, "velocity_sparse_range": vel_sparse_range, "velocity_1mm3_range": vel_1mm3_range},
        "symbolic": {"human": human, "gpt5": gpt, "gpt5_rho_sensitivity": sensitivity},
        "figure1_rows": fig_rows,
        "table2_rows": table2_rows,
    }


def write_outputs(root: str | Path) -> dict[str, Any]:
    """Compute values and write all CSV/JSON/LaTeX outputs."""
    root = Path(root)
    out_dir = root / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = compute_all(root)

    write_json(out_dir / "appendix_c_reproduction.json", data)
    write_json(out_dir / "figure1_numbers.json", data["figure1_rows"])
    write_csv(out_dir / "figure1_numbers.csv", data["figure1_rows"], ["order", "key", "label", "source", "L", "Lambda", "I"])

    vel_fields = [
        "epsilon", "v_c_m_per_s", "q", "phi", "N_sparse_selected", "L_sparse", "Lambda_sparse",
        "N_one_mm3_selected_1e14", "Q_one_mm3_excess_1e_minus_6_J", "L_one_mm3_1e14", "Lambda_one_mm3"
    ]
    write_csv(out_dir / "table1_velocity_demon.csv", data["demons"]["velocity_selection_rows"], vel_fields)
    write_csv(out_dir / "table2_scale.csv", data["table2_rows"])

    constants = {
        "symbolic": data["symbolic"],
        "controllers": data["controllers"],
        "maxwell_single_entropy": data["demons"]["maxwell_single_entropy"],
        "velocity_sparse_range": data["demons"]["velocity_sparse_range"],
        "velocity_1mm3_range": data["demons"]["velocity_1mm3_range"],
    }
    write_json(out_dir / "manuscript_constants.json", constants)
    (out_dir / "table1_velocity_demon.tex").write_text(make_table1_tex(data["demons"]["velocity_selection_rows"]), encoding="utf-8")
    (out_dir / "table2_scale.tex").write_text(make_table2_tex(data["table2_rows"]), encoding="utf-8")
    return data


def make_table1_tex(rows: list[dict[str, float]]) -> str:
    lines = []
    lines.append(r"\begin{tabular}{rrrrrrrrr}")
    lines.append(r"\hline")
    lines.append(r"$\epsilon$ & $v_c$ (m/s) & $q$ & $\phi$ & $N^{100}_{\rm sel}$ & $L_{100}$ & $N^{1\,\mathrm{mm}^3}_{\rm sel}/10^{14}$ & $Q^{1\,\mathrm{mm}^3}_{\rm excess}/10^{-6}\,\mathrm{J}$ & $L_{1\,\mathrm{mm}^3}/10^{14}$ \\")
    lines.append(r"\hline")
    for r in rows:
        lines.append(
            f"{r['epsilon']:.0f} & {r['v_c_m_per_s']:.0f} & {r['q']:.3g} & {r['phi']:.3f} & "
            f"{r['N_sparse_selected']:.3g} & {r['L_sparse']:.3g} & {r['N_one_mm3_selected_1e14']:.3g} & "
            f"{r['Q_one_mm3_excess_1e_minus_6_J']:.3g} & {r['L_one_mm3_1e14']:.3g} \\")
    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    return "\n".join(lines) + "\n"


def make_table2_tex(rows: list[dict[str, Any]]) -> str:
    lines = []
    lines.append(r"\begin{tabular}{p{0.23\linewidth}p{0.45\linewidth}p{0.14\linewidth}p{0.10\linewidth}}")
    lines.append(r"\hline")
    lines.append(r"Example / regime & Calculation basis & $I$ & $\Lambda$ \\")
    lines.append(r"\hline")
    for r in rows:
        lam = f"{r['Lambda_min']:.3f}" if abs(r['Lambda_min'] - r['Lambda_max']) < 1e-12 else f"{r['Lambda_min']:.3f}--{r['Lambda_max']:.3f}"
        lines.append(f"{r['example_regime']} & {r['calculation_basis']} & {r['I_display']} & {lam} \\")
    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    return "\n".join(lines) + "\n"
