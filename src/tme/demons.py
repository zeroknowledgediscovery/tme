"""Maxwell-demon and velocity-selection calculations."""

from __future__ import annotations

import math
from .scale import Lambda_from_L

K_B_EXACT = 1.380649e-23


def entropy_reduction_demon(deltaS_J_per_K: float, kB_J_per_K: float = K_B_EXACT) -> dict[str, float]:
    """Fluctuation-theorem scale for an entropy-reducing trajectory.

    L = log10(I + 1) = (Delta S / kB) / ln(10).
    """
    if deltaS_J_per_K <= 0:
        raise ValueError("deltaS_J_per_K must be positive")
    ratio = deltaS_J_per_K / kB_J_per_K
    L = ratio / math.log(10.0)
    return {
        "deltaS_J_per_K": deltaS_J_per_K,
        "deltaS_over_kB": ratio,
        "L": L,
        "Lambda": Lambda_from_L(L),
    }


def mb_tail_q(epsilon: float) -> float:
    """Three-dimensional Maxwell-Boltzmann kinetic-energy tail q(epsilon).

    x = m v^2/(2 k_B T) follows Gamma(shape=3/2, scale=1).
    q(epsilon) = P(x > epsilon).
    """
    if epsilon < 0:
        raise ValueError("epsilon must be nonnegative")
    root = math.sqrt(epsilon)
    return math.erfc(root) + (2.0 / math.sqrt(math.pi)) * root * math.exp(-epsilon)


def upper_gamma_3half(epsilon: float) -> float:
    """Upper incomplete gamma Gamma(3/2, epsilon)."""
    root = math.sqrt(epsilon)
    return 0.5 * math.sqrt(math.pi) * math.erfc(root) + root * math.exp(-epsilon)


def upper_gamma_5half(epsilon: float) -> float:
    """Upper incomplete gamma Gamma(5/2, epsilon), via recurrence."""
    return 1.5 * upper_gamma_3half(epsilon) + (epsilon ** 1.5) * math.exp(-epsilon)


def mb_conditional_mean_x(epsilon: float) -> float:
    """E[x | x > epsilon] for x ~ Gamma(3/2, 1)."""
    denom = upper_gamma_3half(epsilon)
    if denom <= 0:
        raise ValueError("tail probability underflowed to zero")
    return upper_gamma_5half(epsilon) / denom


def mb_excess_phi(epsilon: float) -> float:
    """Excess dimensionless kinetic energy above thermal mean 3/2."""
    return mb_conditional_mean_x(epsilon) - 1.5


def cutoff_speed_m_per_s(epsilon: float, T_K: float, molecular_mass_kg: float, kB_J_per_K: float = K_B_EXACT) -> float:
    """Cutoff speed v_c = sqrt(2 k_B T epsilon / m)."""
    if T_K <= 0 or molecular_mass_kg <= 0:
        raise ValueError("T_K and molecular_mass_kg must be positive")
    return math.sqrt(2.0 * kB_J_per_K * T_K * epsilon / molecular_mass_kg)


def velocity_selection_demon(
    N: float,
    epsilon: float,
    T_K: float = 300.0,
    molecular_mass_kg: float = 4.65e-26,
    kB_J_per_K: float = K_B_EXACT,
    half_chamber_factor: float = 0.5,
) -> dict[str, float]:
    """Velocity-selection demon scale.

    Uses the one-shot half-chamber protocol:
        N_sel = (N/2) q(epsilon)
        Q_excess = (N/2) q(epsilon) phi(epsilon) k_B T
        L = log10(I + 1) = (N/2) q(epsilon) phi(epsilon) / ln(10)
    """
    if N <= 0:
        raise ValueError("N must be positive")
    if not (0 < half_chamber_factor <= 1):
        raise ValueError("half_chamber_factor must be in (0, 1]")
    q = mb_tail_q(epsilon)
    phi = mb_excess_phi(epsilon)
    selected = half_chamber_factor * N * q
    Q_excess = half_chamber_factor * N * q * phi * kB_J_per_K * T_K
    L = half_chamber_factor * N * q * phi / math.log(10.0)
    return {
        "epsilon": epsilon,
        "v_c_m_per_s": cutoff_speed_m_per_s(epsilon, T_K, molecular_mass_kg, kB_J_per_K),
        "q": q,
        "phi": phi,
        "N": N,
        "N_selected": selected,
        "Q_excess_J": Q_excess,
        "L": L,
        "Lambda": Lambda_from_L(L),
    }


def velocity_selection_table(
    epsilons: list[float],
    N_sparse: float,
    N_one_mm3_air: float,
    T_K: float = 300.0,
    molecular_mass_kg: float = 4.65e-26,
    kB_J_per_K: float = K_B_EXACT,
    half_chamber_factor: float = 0.5,
) -> list[dict[str, float]]:
    """Rows corresponding to manuscript Table I."""
    rows = []
    for eps in epsilons:
        sparse = velocity_selection_demon(N_sparse, eps, T_K, molecular_mass_kg, kB_J_per_K, half_chamber_factor)
        one = velocity_selection_demon(N_one_mm3_air, eps, T_K, molecular_mass_kg, kB_J_per_K, half_chamber_factor)
        rows.append({
            "epsilon": eps,
            "v_c_m_per_s": one["v_c_m_per_s"],
            "q": one["q"],
            "phi": one["phi"],
            "N_sparse_selected": sparse["N_selected"],
            "L_sparse": sparse["L"],
            "Lambda_sparse": sparse["Lambda"],
            "N_one_mm3_selected": one["N_selected"],
            "N_one_mm3_selected_1e14": one["N_selected"] / 1e14,
            "Q_one_mm3_excess_J": one["Q_excess_J"],
            "Q_one_mm3_excess_1e_minus_6_J": one["Q_excess_J"] / 1e-6,
            "L_one_mm3": one["L"],
            "L_one_mm3_1e14": one["L"] / 1e14,
            "Lambda_one_mm3": one["Lambda"],
        })
    return rows


def range_from_velocity_rows(rows: list[dict[str, float]], L_key: str) -> dict[str, float]:
    """Endpoint/midpoint summary for velocity-selection rows by an L column."""
    values = [row[L_key] for row in rows]
    L_min, L_max = min(values), max(values)
    L_mid = 0.5 * (L_min + L_max)
    return {
        "L_min": L_min,
        "L_max": L_max,
        "L_mid": L_mid,
        "Lambda_min": Lambda_from_L(L_min),
        "Lambda_max": Lambda_from_L(L_max),
        "Lambda_mid": Lambda_from_L(L_mid),
    }
