"""
Primary and Secondary Tranche Mathematical Formulations
Source: SSRN-3856569 (Cao et al., 2021) "Designing Stablecoins"
"""
import math
from typing import Tuple

def compute_normalized_pool_index(P_spot: float, beta: float, P_0: float) -> float:
    """Computes S(t) = P(t) / (beta(t) * P_0)"""
    return P_spot / (beta * P_0)

def evaluate_primary_navs(S_index: float, epoch_v: float, coupon_R: float) -> Tuple[float, float]:
    """
    Computes Net Asset Values for Primary Tranches:
    V_A(t) = 1.0 + R * v(t)
    V_B(t) = 2 * S(t) - V_A(t)
    """
    V_A = 1.0 + coupon_R * epoch_v
    V_B = 2.0 * S_index - V_A
    return V_A, V_B

def evaluate_secondary_navs(V_A: float, epoch_v: float, coupon_R_prime: float, coupon_R: float) -> Tuple[float, float]:
    """
    Computes Net Asset Values for Secondary Sub-Tranches:
    V_A'(t) = 1.0 + R' * v(t) (anUSD Stablecoin)
    V_B'(t) = 2 * V_A(t) - V_A'(t) = 1.0 + (2R - R') * v(t) (High Yield Tranche)
    """
    V_A_prime = 1.0 + coupon_R_prime * epoch_v
    V_B_prime = 2.0 * V_A - V_A_prime
    return V_A_prime, V_B_prime

def compute_effective_leverage(S_index: float, V_B: float) -> float:
    """
    Effective leverage of Class B:
    Lambda_B = 2 * S(t) / V_B(t)
    """
    if V_B <= 0.001:
        return 50.0  # Cap maximum theoretical leverage
    return (2.0 * S_index) / V_B

def verify_solvency_invariant(V_A: float, V_B: float, S_index: float, epsilon: float = 1e-12) -> Tuple[bool, float]:
    """
    Asserts strict value conservation invariant: |V_A + V_B - 2*S| == 0
    """
    gap = abs(V_A + V_B - 2.0 * S_index)
    return (gap <= epsilon), gap
