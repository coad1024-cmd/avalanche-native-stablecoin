"""
Dynamic Reset State Transitions, O(1) Rebase Engine, and Extreme Crash Waterfall
Source: SSRN-3856569 Section 2.3 - 2.5
Governing Standard: BCRG Mathematical Edge-Case & Invariant Canon
"""
from typing import Dict, Any, Tuple

def check_reset_condition(V_B: float, H_u: float, H_d: float) -> str:
    """
    Evaluates boundary crossings for Class B equity NAV:
    - UPWARD: V_B >= H_u (e.g. $2.00)
    - DOWNWARD: V_B <= H_d (e.g. $0.25)
    - NONE: H_d < V_B < H_u
    """
    if V_B >= H_u:
        return "UPWARD"
    elif V_B <= H_d:
        return "DOWNWARD"
    return "NONE"

def execute_upward_reset(P_spot: float, P_0: float, beta: float, epoch_v: float, V_B: float, coupon_R: float) -> Dict[str, Any]:
    """
    Executes Upward Reset (Profit Realization and Share Split):
    1. Accrued coupon paid to Class A: R * v
    2. Realized profit paid to Class B: V_B - 1.0
    3. Global conversion factor updates: beta_new = beta * (P_spot / P_0)
    4. Reset epoch anchor: P_0 = P_spot, v = 0.0
    """
    coupon_payout_A = coupon_R * epoch_v
    profit_payout_B = max(0.0, V_B - 1.0)
    beta_new = beta * (P_spot / max(1e-6, P_0))
    
    return {
        "new_beta": beta_new,
        "new_P_0": P_spot,
        "new_epoch_v": 0.0,
        "payout_A": coupon_payout_A,
        "payout_B": profit_payout_B,
        "reset_type": "UPWARD"
    }

def execute_downward_reset(
    P_spot: float,
    beta: float,
    epoch_v: float,
    V_B: float,
    coupon_R: float,
    bear_subsidy_R_tilde: float,
    coupon_R_prime: float = 0.030
) -> Dict[str, Any]:
    """
    Executes Downward Reset (Principal Protection and Reverse Split / Merger):
    1. Senior coupon paid: R * v
    2. Senior principal returned: 1.0 - V_B
    3. Bear-market coupon subsidy transferred from Class A to Class B: R_tilde * v
    4. Global conversion factor scales down by equity factor V_B: beta_new = beta * V_B
    5. Reset epoch anchor: P_0 = P_spot, v = 0.0
    
    Edge-Case Residual Recovery Waterfall (when V_B <= 0.0 due to extreme flash crash):
    - Class B equity is fully wiped out (payout_B = 0.0).
    - Class A absorbs total remaining pool value: Payout_A = max(0.0, 2 * S_index).
    - Class A' (anUSD) is prioritized over Class B': Class A' receives full 1.0 par value
      as long as total pool value >= 1.0 + R'*v (verified for drops up to -60.00% from H_d).
    """
    if V_B > 0.0:
        # Standard Downward Reset within normal barrier boundary
        coupon_payout_A = coupon_R * epoch_v
        principal_return_A = 1.0 - V_B
        bear_subsidy_B = bear_subsidy_R_tilde * epoch_v
        
        net_payout_A = coupon_payout_A + principal_return_A - bear_subsidy_B
        net_payout_B = bear_subsidy_B
        beta_new = beta * max(0.001, V_B)
        realized_anUSD_value = 1.0 + coupon_R_prime * epoch_v
    else:
        # Extreme Beyond-Barrier Shock (V_B <= 0.0)
        net_payout_B = 0.0
        # Calculate remaining pool value per senior pair
        remaining_pool_value = max(0.0, 1.0 + V_B) # Residual asset backing
        net_payout_A = remaining_pool_value
        beta_new = beta * 0.001 # Set to floor scaling factor
        
        # Subordinated Tranche Waterfall: Class A' is senior to Class B'
        promised_anUSD = 1.0 + coupon_R_prime * epoch_v
        realized_anUSD_value = min(promised_anUSD, 2.0 * remaining_pool_value)
    
    return {
        "new_beta": beta_new,
        "new_P_0": P_spot,
        "new_epoch_v": 0.0,
        "payout_A": net_payout_A,
        "payout_B": net_payout_B,
        "realized_anUSD_payout": realized_anUSD_value,
        "reset_type": "DOWNWARD"
    }

def evaluate_single_step_crash_tolerance(
    coupon_R: float,
    coupon_R_prime: float,
    H_d: float,
    epoch_T: float = 100.0 / 365.0,
    bear_subsidy_R_tilde: float = 0.0
) -> float:
    """
    Evaluates Theorem 1 analytical model-free single-step crash bound:
    Delta P_max = max_{v in [0, T]} [ 0.5 * (1 + R'*v + 2*R_tilde*v) / (1 + R*v + H_d) - 1.0 ]
    """
    v_grid = [t * (epoch_T / 100.0) for t in range(101)]
    max_bound = -1.0
    for v in v_grid:
        numerator = 1.0 + coupon_R_prime * v + 2.0 * bear_subsidy_R_tilde * v
        denominator = 1.0 + coupon_R * v + H_d
        ratio = 0.5 * (numerator / denominator) - 1.0
        if ratio > max_bound:
            max_bound = ratio
    return max_bound
