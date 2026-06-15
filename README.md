# TME: Thermodynamic Measure of Intelligence manuscript calculations

This repository contains a small, auditable code collection for reproducing the numerical calibration values used in the manuscript **Thermodynamic Measure of Intelligence**.

The code generates the values used for:

- Fig. 1 example scale values.
- Table I velocity-selection demon calculations.
- Table II numerical thermodynamic-intelligence scale.
- Appendix C scale calculations.
- Derived JSON/CSV/LaTeX tables for direct manuscript use.

The repository is intentionally lightweight. It uses only the Python standard library. The GPT/human entropy-rate estimates are not recomputed here; they are treated as imported constants from the NERO workflow and are recorded in `inputs/symbolic_entropy_inputs.json`. The NERO repository should be cited for the human/GPT entropy-rate estimation pipeline and raw/derived text analysis outputs.

## Quick start

From the repository root:

```bash
python scripts/make_all.py
```

This writes outputs into `outputs/`:

```text
figure1_numbers.csv
figure1_numbers.json
table1_velocity_demon.csv
table1_velocity_demon.tex
table2_scale.csv
table2_scale.tex
manuscript_constants.json
appendix_c_reproduction.json
```

Run tests with:

```bash
python -m unittest discover -s tests
```

## Inputs

The manuscript assumptions are stored as explicit JSON files in `inputs/`:

- `figure1_examples.json`: example categories and ordering used in Fig. 1.
- `controller_inputs.json`: fixed-feedback and repeated-control assumptions.
- `demon_inputs.json`: Maxwell-demon and velocity-selection parameters.
- `symbolic_entropy_inputs.json`: symbolic-scale parameters, including the NERO-derived entropy-rate values.

The symbolic defaults are:

- `N_V = 5e21`: finite-resolution estimate of interpretable English sentence-scale strings.
- `N_G = 1e7`: illustrative high-quality sentence-scale target-set cardinality.
- `n_star = 100`: character-scale sentence length after the 27-symbol coarse-graining.
- `H_human = 0.77` bits/character: Gutenberg prose entropy-rate estimate from NERO.
- `H_gpt = 0.74` bits/character: GPT-5 long-form prose entropy-rate estimate from NERO.
- `rho = 0`: central finite-length AEP slack value.

Sensitivity to `rho`, `N_V`, and `N_G` can be explored by editing the input JSON files or by importing `tme.symbolic` directly.

## Scope

This code reproduces numerical scale calculations. It does not prove the manuscript theorems and does not regenerate the NERO entropy-rate estimates from raw text. The intent is to make every number plotted or tabulated in the TME manuscript traceable to a named formula and an explicit parameter file.

## Suggested manuscript data/code availability sentence

> The code used to reproduce the numerical scale calculations in Fig. 1, Table I, Table II, and Appendix C is available in the public TME calculation repository. The entropy-rate estimates used for the symbolic GPT-human comparison are imported from the NERO workflow, which maps text to a common 27-symbol alphabet and applies the nonparametric entropy-rate estimator described in Appendix B. Derived CSV and LaTeX files containing the plotted and tabulated values are provided with the TME repository.
