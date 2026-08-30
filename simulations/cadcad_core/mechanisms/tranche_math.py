"""
Primary and Secondary Tranche Mathematical Formulations
Source: SSRN-3856569 (Cao et al., 2021) "Designing Stablecoins"
Governing Standard: BCRG Mathematical & Singularity Edge-Case Canon
"""
import math
from typing import Tuple

def compute_normalized_pool_index(P_spot: float, beta: float, P_0: float) -> float:
    """
    Computes normalized collateral pool index S(t):
    S(t) = P(t) / (beta(t) * P_0)
    """
    if beta <= 0.0 or P_0 <= 0.0:
        raise ValueError(f"Invalid state parameters: beta={beta}, P_0={P_0}")
    return P_spot / (beta * P_0)

def evaluate_primary_navs(S_index: float, epoch_v: float, coupon_R: float, alpha: float = 1.0) -> Tuple[float, float]:
    """
    Computes Net Asset Values for Primary Tranches:
    V_A(t) = 1.0 + R * v(t)
    V_B(t) = (1 + alpha) * S(t) - alpha * V_A(t)
    """
    V_A = 1.0 + coupon_R * epoch_v
    V_B = (1.0 + alpha) * S_index - alpha * V_A
    return V_A, V_B

def evaluate_secondary_navs(V_A: float, epoch_v: float, coupon_R_prime: float, coupon_R: float) -> Tuple[float, float]:
    """
    Computes Net Asset Values for Secondary Sub-Tranches:
    V_A'(t) = 1.0 + R' * v(t) (anUSD Stablecoin, approx $1.0000)
    V_B'(t) = 2 * V_A(t) - V_A'(t) = 1.0 + (2R - R') * v(t) (Leveraged High Yield Tranche)
    """
    V_A_prime = 1.0 + coupon_R_prime * epoch_v
    V_B_prime = 2.0 * V_A - V_A_prime
    return V_A_prime, V_B_prime

def compute_effective_leverage(S_index: float, V_B: float, alpha: float = 1.0) -> float:
    """
    Computes effective financial leverage of Class B with singularity guards:
    Lambda_B(S) = (1 + alpha) * S(t) / V_B(t)
    
    Singularity Edge Cases:
    1. V_B <= 0.001 (Deep underwater / wiped out): Capped smoothly at 50.0x maximum theoretical leverage.
    2. S -> infinity (Extreme bull market): Asymptotically approaches (1 + alpha) / (1 + alpha) = 1.0x (unleveraged).
    """
    if V_B <= 0.001:
        return 50.0  # Singularity ceiling
    raw_leverage = ((1.0 + alpha) * S_index) / V_B
    return max(1.0, min(50.0, raw_leverage))
