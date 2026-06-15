"""Symbolic generation scale calculations.

The entropy-rate values used here are imported constants from the NERO workflow.
This module does not regenerate NERO text entropy estimates.
"""

from __future__ import annotations

import math
from .scale import Lambda_from_L


def human_sentence_scale(N_V: float, N_G: float, q_human: float = 1.0) -> dict[str, float]:
    """Sentence-scale human rare-valid lift.

    I_H + 1 = q_H * N_V / N_G.
    """
    if N_V <= 0 or N_G <= 0 or q_human < 0:
        raise ValueError("N_V and N_G must be positive; q_human must be nonnegative")
    I_plus_1 = q_human * N_V / N_G
    if I_plus_1 <= 0:
        raise ValueError("I_plus_1 must be positive")
    L = math.log10(I_plus_1)
    return {
        "N_V": N_V,
        "N_G": N_G,
        "q_human": q_human,
        "delta_star": N_G / N_V,
        "I_plus_1": I_plus_1,
        "I": I_plus_1 - 1.0,
        "L": L,
        "Lambda": Lambda_from_L(L),
    }


def gpt_sentence_scale(
    N_V: float,
    N_G: float,
    n_star_characters: int,
    H_gpt_bits_per_character: float,
    H_human_bits_per_character: float,
    rho_n_star: float = 0.0,
    q_human: float = 1.0,
) -> dict[str, float]:
    """Sentence-scale GPT rare-valid lift using an AEP-style support correction.

    log2(q_GPT/q_H) = n_star * (H_GPT - H_H) + rho_n_star.
    I_GPT + 1 = (q_GPT/q_H) * q_H * N_V / N_G.
    """
    human = human_sentence_scale(N_V, N_G, q_human=q_human)
    exponent = n_star_characters * (H_gpt_bits_per_character - H_human_bits_per_character) + rho_n_star
    q_ratio = 2.0 ** exponent
    I_plus_1 = human["I_plus_1"] * q_ratio
    L = math.log10(I_plus_1)
    return {
        "N_V": N_V,
        "N_G": N_G,
        "n_star_characters": n_star_characters,
        "H_gpt_bits_per_character": H_gpt_bits_per_character,
        "H_human_bits_per_character": H_human_bits_per_character,
        "rho_n_star": rho_n_star,
        "q_ratio_gpt_to_human": q_ratio,
        "log2_q_ratio_gpt_to_human": exponent,
        "I_plus_1": I_plus_1,
        "I": I_plus_1 - 1.0,
        "L": L,
        "Lambda": Lambda_from_L(L),
    }


def symbolic_sensitivity(
    N_V: float,
    N_G: float,
    n_star_characters: int,
    H_gpt_bits_per_character: float,
    H_human_bits_per_character: float,
    rho_values: list[float],
    q_human: float = 1.0,
) -> list[dict[str, float]]:
    """Return GPT symbolic scale values across finite-length slack values."""
    return [
        gpt_sentence_scale(
            N_V=N_V,
            N_G=N_G,
            n_star_characters=n_star_characters,
            H_gpt_bits_per_character=H_gpt_bits_per_character,
            H_human_bits_per_character=H_human_bits_per_character,
            rho_n_star=rho,
            q_human=q_human,
        )
        for rho in rho_values
    ]
