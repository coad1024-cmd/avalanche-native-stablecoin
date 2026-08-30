"""
Automated Conservation Law and Thermodynamic Invariant Checker
Governing Standard: BCRG Senior Engineering Principles (Invariant Assertion Gates)
"""
from typing import Dict, Any, Tuple
import math

MACHINE_EPSILON: float = 1e-12

def verify_primary_solvency_invariant(V_A: float, V_B: float, S_index: float, alpha: float = 1.0) -> Tuple[bool, float]:
    """
    Checks Primary Solvency Invariant:
    | alpha * V_A(t) + V_B(t) - (1 + alpha) * S(t) | <= 1e-12
    """
    lhs = alpha * V_A + V_B
    rhs = (1.0 + alpha) * S_index
    gap = abs(lhs - rhs)
    return (gap <= MACHINE_EPSILON), gap

def verify_sub_tranche_parity_invariant(V_A_prime: float, V_B_prime: float, V_A: float) -> Tuple[bool, float]:
    """
    Checks Subordinated Tranche Conservation:
    | V_A'(t) + V_B'(t) - 2 * V_A(t) | <= 1e-12
    """
    lhs = V_A_prime + V_B_prime
    rhs = 2.0 * V_A
    gap = abs(lhs - rhs)
    return (gap <= MACHINE_EPSILON), gap

def verify_step_conservation(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes full multi-invariant conservation audit on a single simulation state row.
    """
    solv_ok, solv_gap = verify_primary_solvency_invariant(
        state_dict["V_A"],
        state_dict["V_B"],
        state_dict["S_index"]
    )
    sub_ok, sub_gap = verify_sub_tranche_parity_invariant(
        state_dict["V_A_prime"],
        state_dict["V_B_prime"],
        state_dict["V_A"]
    )
    
    all_ok = solv_ok and sub_ok
    return {
        "is_conserved": all_ok,
        "primary_solvency_ok": solv_ok,
        "solvency_gap": solv_gap,
        "sub_tranche_ok": sub_ok,
        "sub_tranche_gap": sub_gap
    }
