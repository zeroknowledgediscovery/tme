"""Common scale transformations for rare-valid lift.

Definitions:
    I: rare-valid probability lift.
    L = log10(I + 1).
    Lambda = log10(log10(I + 1) + 1) = log10(L + 1).
"""

from __future__ import annotations

import math


def validate_nonnegative(value: float, name: str) -> None:
    if value < 0:
        raise ValueError(f"{name} must be nonnegative; got {value!r}")


def L_from_I(I: float) -> float:
    """Return L = log10(I + 1)."""
    validate_nonnegative(I, "I")
    return math.log10(I + 1.0)


def Lambda_from_L(L: float) -> float:
    """Return Lambda = log10(L + 1)."""
    validate_nonnegative(L, "L")
    return math.log10(L + 1.0)


def Lambda_from_I(I: float) -> float:
    """Return Lambda = log10(log10(I + 1) + 1)."""
    return Lambda_from_L(L_from_I(I))


def I_from_L(L: float) -> float:
    """Return I = 10^L - 1."""
    validate_nonnegative(L, "L")
    return 10.0 ** L - 1.0


def L_range_midpoint(L_min: float, L_max: float) -> float:
    """Midpoint of a range on the L = log10(I+1) scale."""
    validate_nonnegative(L_min, "L_min")
    validate_nonnegative(L_max, "L_max")
    if L_min > L_max:
        L_min, L_max = L_max, L_min
    return 0.5 * (L_min + L_max)


def sci10_from_L(L: float, sigfigs: int = 3) -> str:
    """Format I + 1 = 10^L as a compact scientific string.

    For moderate L, returns a decimal scientific notation. For extremely large L,
    returns a power-of-ten form such as ``10^3146`` or ``10^(2.29e15)``.
    """
    validate_nonnegative(L, "L")
    if L < 12:
        return f"{10.0 ** L:.{sigfigs}g}"
    if L < 1e6:
        return f"10^{L:.{sigfigs}g}"
    return f"10^({L:.{sigfigs}e})"


def range_summary_from_L(L_min: float, L_max: float) -> dict[str, float]:
    """Return L/Lambda endpoints and midpoint for a range."""
    if L_min > L_max:
        L_min, L_max = L_max, L_min
    return {
        "L_min": L_min,
        "L_max": L_max,
        "L_mid": L_range_midpoint(L_min, L_max),
        "Lambda_min": Lambda_from_L(L_min),
        "Lambda_max": Lambda_from_L(L_max),
        "Lambda_mid": Lambda_from_L(L_range_midpoint(L_min, L_max)),
    }
