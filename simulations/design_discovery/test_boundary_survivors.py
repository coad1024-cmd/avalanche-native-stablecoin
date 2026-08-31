"""
Boundary-Survivor Sensitivity & Analytical Pruning Validator.
Validates Stage 1 filter boundary behavior and performs epsilon-perturbation tests.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any


def derive_plant_damping_ratio(K_p: float, K_i: float, L_amm: float = 1.5e6, 
                               tau_arb_days: float = 5.55, alpha_flow: float = 1.0e7) -> Tuple[float, float, float]:
    """
    Rigorously derives the closed-loop damping ratio zeta, natural frequency omega_n,
    and DC gain K_dc from the physical secondary AMM plant and PI feedback controller.
    
    Plant: G_plant(s) = K_dc / (tau_arb * s + 1)
    Controller: C(s) = (K_p * s + K_i) / s
    Characteristic Eq: tau_arb * s^2 + (1 + K_dc * K_p) * s + K_dc * K_i = 0
    """
    tau_arb = tau_arb_days / 365.25  # in years
    K_dc = (alpha_flow * tau_arb) / L_amm  # Dimensionless plant DC gain
    
    omega_n = np.sqrt(K_dc * K_i / tau_arb)
    zeta = (1.0 + K_dc * K_p) / (2.0 * np.sqrt(tau_arb * K_dc * K_i))
    
    return zeta, omega_n, K_dc


def test_filter_boundary_perturbations() -> Dict[str, Any]:
    """
    Evaluates points at epsilon-distances around every candidate pruning boundary
    to ensure valid candidates are not erroneously discarded.
    """
    epsilons = [1e-5, 1e-4, 1e-3, 1e-2]
    results = {}
    
    # 1. Test R vs R' Boundary (Yield Spread)
    r_base = 0.05
    results["yield_spread_boundary"] = []
    for eps in epsilons:
        # Candidate A: R = R' + eps (Valid senior premium)
        r_valid = r_base + eps
        r_prime_valid = r_base
        valid_pass = bool(r_valid > r_prime_valid)
        
        # Candidate B: R = R' - eps (Inverted yield spread: senior earns less than borrow rate)
        r_invalid = r_base - eps
        r_prime_invalid = r_base
        invalid_pass = bool(r_invalid > r_prime_invalid)
        
        results["yield_spread_boundary"].append({
            "eps": eps,
            "valid_candidate (R > R')": valid_pass,
            "invalid_candidate (R < R')": invalid_pass,
            "economic_rationale": "Senior fixed claim must earn positive spread over benchmark borrow rate to prevent senior capital run."
        })
        
    # 2. Test Simplex Weight Conservation Boundary
    results["simplex_boundary"] = []
    for eps in epsilons:
        # Valid: exactly sums to 1.0
        w_valid = np.array([0.65, 0.20, 0.00, 0.15])
        pass_valid = bool(np.abs(np.sum(w_valid) - 1.0) < 1e-7)
        
        # Incomplete allocation: sum = 1 - eps (Yield leaked)
        w_leak = np.array([0.65 - eps, 0.20, 0.00, 0.15])
        pass_leak = bool(np.abs(np.sum(w_leak) - 1.0) < 1e-7)
        
        # Over-allocation: sum = 1 + eps (Unbacked yield created)
        w_over = np.array([0.65 + eps, 0.20, 0.00, 0.15])
        pass_over = bool(np.abs(np.sum(w_over) - 1.0) < 1e-7)
        
        results["simplex_boundary"].append({
            "eps": eps,
            "valid_simplex_pass": pass_valid,
            "leak_pass": pass_leak,
            "over_pass": pass_over,
            "economic_rationale": "Simplex sum != 1.0 violates double-entry token conservation."
        })
        
    # 3. Test Reset Barrier Ordering Boundary (H_d < 1.0 < H_u)
    results["barrier_ordering_boundary"] = []
    for eps in epsilons:
        # Candidate A: H_d = 1.0 - eps, H_u = 1.0 + eps (Microscopic valid ordering)
        hd_valid = 1.0 - eps
        hu_valid = 1.0 + eps
        ordering_valid = bool((0.0 < hd_valid < 1.0) and (hu_valid > 1.0))
        
        # Candidate B: H_d = 1.0 + eps (Inverted reset barrier: downward reset triggered above par)
        hd_inverted = 1.0 + eps
        ordering_inverted = bool(0.0 < hd_inverted < 1.0)
        
        results["barrier_ordering_boundary"].append({
            "eps": eps,
            "ordering_valid": ordering_valid,
            "ordering_inverted": ordering_inverted,
            "economic_rationale": "Downward reset barrier H_d >= 1.0 violates parity normalization definition V0 = $1.0."
        })
        
    # 4. Test Damping Ratio Stability Boundary across Liquidity Tiers
    results["damping_stability_grid"] = []
    liquidity_levels = [500_000, 1_500_000, 5_000_000, 30_000_000]
    for L in liquidity_levels:
        for kp in [0.01, 0.15, 0.50]:
            for ki in [0.001, 0.02, 0.08]:
                zeta, wn, kdc = derive_plant_damping_ratio(kp, ki, L_amm=L)
                results["damping_stability_grid"].append({
                    "liquidity_L": L,
                    "K_p": kp,
                    "K_i": ki,
                    "K_dc": float(kdc),
                    "omega_n": float(wn),
                    "zeta": float(zeta),
                    "is_overdamped": bool(zeta >= 1.0)
                })
                
    return results


if __name__ == "__main__":
    res = test_filter_boundary_perturbations()
    print("=== DAMPING RATIO PHYSICAL DERIVATION SAMPLE ===")
    df_damp = pd.DataFrame(res["damping_stability_grid"])
    print(df_damp.head(12).to_string())
    print("\nMin zeta observed across grid:", df_damp["zeta"].min())
    print("Max zeta observed across grid:", df_damp["zeta"].max())
    print("All points overdamped (zeta >= 1.0)?", (df_damp["zeta"] >= 1.0).all())
    print("\n=== YIELD SPREAD BOUNDARY PERTURBATION TEST ===")
    for item in res["yield_spread_boundary"]:
        print(f"  eps={item['eps']:1.0e} | Valid candidate passed: {item['valid_candidate (R > R\')']} | Invalid candidate passed: {item['invalid_candidate (R < R\')']}")
    print("\n=== SIMPLEX BOUNDARY PERTURBATION TEST ===")
    for item in res["simplex_boundary"]:
        print(f"  eps={item['eps']:1.0e} | Valid pass: {item['valid_simplex_pass']} | Leak pass: {item['leak_pass']} | Over pass: {item['over_pass']}")
