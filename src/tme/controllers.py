"""Controller-scale calculations."""

from __future__ import annotations

import math
from .scale import L_from_I, Lambda_from_I, Lambda_from_L


def fixed_feedback(alpha: float) -> dict[str, float]:
    """Constant likelihood-factor amplification: P(V_delta) = alpha * delta.

    Returns I = alpha - 1, L = log10(alpha), and Lambda.
    """
    if alpha < 1:
        raise ValueError("alpha must be at least 1")
    I = alpha - 1.0
    L = math.log10(alpha)
    return {"alpha": alpha, "I": I, "L": L, "Lambda": Lambda_from_L(L)}


def fixed_feedback_range(alpha_min: float, alpha_max: float) -> dict[str, float]:
    """Endpoint and midpoint summary for a fixed-feedback alpha range."""
    low = fixed_feedback(alpha_min)
    high = fixed_feedback(alpha_max)
    L_min, L_max = sorted([low["L"], high["L"]])
    L_mid = 0.5 * (L_min + L_max)
    return {
        "alpha_min": alpha_min,
        "alpha_max": alpha_max,
        "I_min": min(low["I"], high["I"]),
        "I_max": max(low["I"], high["I"]),
        "L_min": L_min,
        "L_max": L_max,
        "L_mid": L_mid,
        "Lambda_min": Lambda_from_L(L_min),
        "Lambda_max": Lambda_from_L(L_max),
        "Lambda_mid": Lambda_from_L(L_mid),
    }


def repeated_binary_control(stages: int) -> dict[str, float]:
    """Sequential binary improvements: I + 1 = 2^stages."""
    if stages < 0:
        raise ValueError("stages must be nonnegative")
    I_plus_1 = 2.0 ** stages
    I = I_plus_1 - 1.0
    L = math.log10(I_plus_1)
    return {"stages": stages, "I_plus_1": I_plus_1, "I": I, "L": L, "Lambda": Lambda_from_L(L)}


def repeated_binary_control_range(stages_min: int, stages_max: int) -> dict[str, float]:
    """Endpoint and midpoint summary for repeated binary control."""
    low = repeated_binary_control(stages_min)
    high = repeated_binary_control(stages_max)
    L_min, L_max = sorted([low["L"], high["L"]])
    L_mid = 0.5 * (L_min + L_max)
    return {
        "stages_min": stages_min,
        "stages_max": stages_max,
        "I_min": min(low["I"], high["I"]),
        "I_max": max(low["I"], high["I"]),
        "L_min": L_min,
        "L_max": L_max,
        "L_mid": L_mid,
        "Lambda_min": Lambda_from_L(L_min),
        "Lambda_max": Lambda_from_L(L_max),
        "Lambda_mid": Lambda_from_L(L_mid),
    }
