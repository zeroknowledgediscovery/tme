# TME: Thermodynamic Measure of Intelligence manuscript calculations

This repository contains a small, auditable code collection for reproducing the numerical calibration values used in the manuscript **Thermodynamic Measure of Intelligence**.

The central scope distinction is:

- **TME computes manuscript-scale quantities**: rare-valid lift `I`, log scale `L = log10(I + 1)`, compressed scale `Lambda = log10(L + 1)`, controller examples, Maxwell-demon examples, velocity-selection demon values, and manuscript-ready CSV/JSON/LaTeX outputs.
- **TME does not recompute the GPT/human entropy-rate estimates from raw text.** Those empirical entropy-rate values are imported from the workflow in https://github.com/zeroknowledgediscovery/nero and recorded as input constants.
- **https://github.com/zeroknowledgediscovery/nero is the source repository for the GPT/human text entropy-rate analysis.** Cite https://github.com/zeroknowledgediscovery/nero for the preprocessing, corpus handling, GPT/human text analysis, and entropy-rate estimates used as symbolic inputs here.

The code generates the values used for Fig. 1, Table I, Table II, Appendix C, and derived JSON/CSV/LaTeX outputs for direct manuscript use.

## What is computed here, and what is imported?

| Quantity | Computed in TME? | Source / formula |
| --- | --- | --- |
| Passive baseline | Yes | `I = 0`, `L = 0`, `Lambda = 0` |
| Fixed-feedback controller | Yes | `I = alpha - 1`, with `alpha` range from `inputs/controller_inputs.json` |
| Repeated dynamic controller | Yes | `I + 1 approx 2^m`, with stage range from `inputs/controller_inputs.json` |
| Maxwell demon, single entropy reduction | Yes | `L = (Delta S / k_B) / ln(10)`, with constants from `inputs/demon_inputs.json` |
| Velocity-selection demon | Yes | Maxwell-Boltzmann tail calculation in `src/tme/demons.py`, with parameters from `inputs/demon_inputs.json` |
| Human symbolic scale | Yes, from symbolic assumptions | `I_H + 1 = q_H N_V / N_G`; `N_V`, `N_G`, and `q_H` are manuscript assumptions in `inputs/symbolic_entropy_inputs.json` |
| GPT-5 symbolic scale | Yes, from imported entropy rates | `log2(q_GPT/q_H) = n_star (H_GPT - H_H) + rho`; `H_GPT` and `H_H` are imported from https://github.com/zeroknowledgediscovery/nero and recorded in `inputs/symbolic_entropy_inputs.json` |
| GPT/human entropy-rate estimation from raw or generated text | No | Performed in https://github.com/zeroknowledgediscovery/nero, not in TME |

## Symbolic GPT/human calculation

TME uses the following symbolic-scale calculation.

For the expert-human symbolic row,

    I_H + 1 = q_H N_V / N_G.

The current default inputs are recorded in `inputs/symbolic_entropy_inputs.json`:

    N_V = 5e21
    N_G = 1e7
    q_H = 1

Thus

    I_H + 1 = 5e14,
    L_H = log10(5e14),
    Lambda_H = log10(L_H + 1).

For the GPT-5 symbolic row, TME imports the entropy-rate estimates from https://github.com/zeroknowledgediscovery/nero:

    H_human = 0.77 bits/character
    H_gpt = 0.74 bits/character

TME then applies the finite-resolution symbolic correction

    log2(q_GPT / q_H) = n_star * (H_gpt - H_human) + rho_n_star.

With the default central values

    n_star = 100
    rho_n_star = 0

this gives

    log2(q_GPT / q_H) = 100 * (0.74 - 0.77) = -3,
    q_GPT / q_H = 2^-3 = 0.125,
    I_GPT + 1 = (I_H + 1) * 0.125 = 6.25e13.

TME then computes

    L_GPT = log10(I_GPT + 1),
    Lambda_GPT = log10(L_GPT + 1).

The entropy-rate values themselves are not produced by TME. They should be traced to https://github.com/zeroknowledgediscovery/nero and to the provenance file `inputs/nero_entropy_provenance.json`.

## Quick start

From the repository root:

    python scripts/make_all.py

This writes outputs into `outputs/`:

    figure1_numbers.csv
    figure1_numbers.json
    table1_velocity_demon.csv
    table1_velocity_demon.tex
    table2_scale.csv
    table2_scale.tex
    manuscript_constants.json
    appendix_c_reproduction.json

Run tests with:

    python -m unittest discover -s tests

## Inputs

The manuscript assumptions are stored as explicit JSON files in `inputs/`:

- `figure1_examples.json`: example categories and ordering used in Fig. 1.
- `controller_inputs.json`: fixed-feedback and repeated-control assumptions.
- `demon_inputs.json`: Maxwell-demon and velocity-selection parameters.
- `symbolic_entropy_inputs.json`: symbolic-scale parameters, including entropy-rate values derived from https://github.com/zeroknowledgediscovery/nero.
- `nero_entropy_provenance.json`: provenance metadata for entropy-rate values imported from https://github.com/zeroknowledgediscovery/nero.

The symbolic defaults are:

- `N_V = 5e21`: finite-resolution estimate of interpretable English sentence-scale strings.
- `N_G = 1e7`: illustrative high-quality sentence-scale target-set cardinality.
- `n_star = 100`: character-scale sentence length after the 27-symbol coarse-graining.
- `H_human = 0.77` bits/character: Gutenberg prose entropy-rate estimate from https://github.com/zeroknowledgediscovery/nero.
- `H_gpt = 0.74` bits/character: GPT-5 long-form prose entropy-rate estimate from https://github.com/zeroknowledgediscovery/nero.
- `rho = 0`: central finite-length AEP slack value.

Sensitivity to `rho`, `N_V`, and `N_G` can be explored by editing the input JSON files or by importing `tme.symbolic` directly.

## Scope

This code reproduces numerical scale calculations. It does not prove the manuscript theorems and does not regenerate the entropy-rate estimates from raw text; those estimates are produced by https://github.com/zeroknowledgediscovery/nero. The intent is to make every number plotted or tabulated in the TME manuscript traceable to a named formula, an explicit parameter file, and, where needed, a named external provenance source.

## Suggested manuscript data/code availability sentence

The code used to reproduce the numerical scale calculations in Fig. 1, Table I, Table II, and Appendix C is available in the public TME calculation repository. The GPT-human entropy-rate estimates used as symbolic inputs are imported from https://github.com/zeroknowledgediscovery/nero, which performs the text preprocessing and entropy-rate estimation described in Appendix B. TME records these imported values, applies the finite-resolution symbolic-scale formulas, and provides derived CSV, JSON, and LaTeX outputs for the plotted and tabulated manuscript values.
