"""
Empirical Adversarial Verification Suite - Challenger 1
Mathematical Invariants, Plant Gain, Crash Bounds, Stability Proofs & Failure Manifolds
"""

import math
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List

def test_domain_1_balance_sheet_closure(n_samples: int = 10000) -> Dict[str, Any]:
    """
    Stress tests the Double-Entry Balance Sheet Closure Identity:
    Published: A(t) = D_senior(t) + E_B(t) + B(t) + D_insolvency(t)
    """
    rng = np.random.default_rng(42)
    
    published_errors = []
    corrected_errors = []
    regimes_tested = {"surplus": 0, "buffer_covered": 0, "insolvent": 0}
    
    for _ in range(n_samples):
        # Generate random state
        P_spot = rng.uniform(5.0, 150.0)
        C_savax = rng.uniform(100.0, 1_000_000.0)
        B_res = rng.uniform(0.0, 500_000.0)
        N_A = rng.uniform(100.0, 500_000.0)
        N_Ap = N_A * 0.5
        N_Bp = N_A * 0.5
        v = rng.uniform(0.0, 0.5)
        R = 0.073
        R_prime = 0.030
        
        V_A = 1.0 + R * v
        V_Ap = 1.0 + R_prime * v
        V_Bp = 2.0 * V_A - V_Ap
        
        # Assets
        A_collateral = C_savax * P_spot
        A_total = A_collateral + B_res
        
        # Senior Debt
        D_senior = N_A * V_A + 0.5 * (N_Ap * V_Ap + N_Bp * V_Bp)
        
        # Classify regime
        if A_collateral >= D_senior:
            regimes_tested["surplus"] += 1
        elif A_total >= D_senior:
            regimes_tested["buffer_covered"] += 1
        else:
            regimes_tested["insolvent"] += 1
            
        # Published definitions:
        E_B_pub = max(0.0, A_total - D_senior - B_res) # = max(0, A_collateral - D_senior)
        B_pub = B_res
        D_insolv_pub = max(0.0, D_senior - A_total)
        RHS_pub = D_senior + E_B_pub + B_pub + D_insolv_pub
        err_pub = abs(A_total - RHS_pub)
        published_errors.append(err_pub)
        
        # Corrected definitions:
        E_B_corr = max(0.0, A_collateral - D_senior)
        collateral_shortfall = max(0.0, D_senior - A_collateral)
        B_unalloc = max(0.0, B_res - collateral_shortfall)
        D_insolv_corr = max(0.0, D_senior - A_total)
        RHS_corr = D_senior + E_B_corr + B_unalloc - D_insolv_corr
        err_corr = abs(A_total - RHS_corr)
        corrected_errors.append(err_corr)
        
    pub_errs = np.array(published_errors)
    corr_errs = np.array(corrected_errors)
    
    pub_failures = np.sum(pub_errs > 1e-8)
    corr_failures = np.sum(corr_errs > 1e-8)
    
    return {
        "n_samples": n_samples,
        "regimes_tested": regimes_tested,
        "published_formula_max_err": float(np.max(pub_errs)),
        "published_formula_failures": int(pub_failures),
        "published_formula_failure_rate": float(pub_failures / n_samples),
        "corrected_formula_max_err": float(np.max(corr_errs)),
        "corrected_formula_failures": int(corr_failures)
    }

def test_domain_2_crash_bounds_theorems() -> Dict[str, Any]:
    """
    Stress tests Theorem 1 and Theorem 2 crash bounds.
    """
    # 1. Theorem 1 Model-Free Flash Crash Invariance:
    # Delta P*_crit = 0.5 * (1 + R'v + 2*R_tilde*v) / (1 + Rv + H_d) - 1.0
    results_t1 = []
    for Hd in [0.15, 0.20, 0.25, 0.30, 0.35, 1.00]:
        for v in [0.0, 0.25, 0.50]:
            for R_tilde in [0.0, 0.05, 0.10]:
                crit_drop = 0.5 * (1.0 + 0.03 * v + 2.0 * R_tilde * v) / (1.0 + 0.073 * v + Hd) - 1.0
                results_t1.append({
                    "Hd": Hd, "v": v, "R_tilde": R_tilde, "crit_drop": crit_drop
                })
                
    # 2. Theorem 2 A2 Solvency Buffer Extension:
    # Initial state: 1 pair minted with 2 units of collateral index S=1.00
    # At barrier Hd=0.25, collateral index is S = (1 + 0.25)/2 = 0.625
    # Value of collateral at barrier is 0.625 * 2 * P0 = 1.25 * P0 per pair
    # Senior claim is 1.0 * P0 (or 0.5 A' + 0.5 B' = 1.0 A claim)
    # If buffer B_res = b_res * TVL_0 (where TVL_0 = 2 * P0):
    # Total assets post-jump: 1.25 * P0 * (1 + Delta P) + b_res * (2 * P0) >= 1.0 * P0
    # 1 + Delta P >= (1.0 - 2 * b_res) / 1.25 = 0.80 - 1.6 * b_res
    # Delta P >= -0.20 - 1.6 * b_res ???
    # WAIT: Why is Senior claim 1.0 when 1 unit of A' is backed by 2 units of pool?
    # Let's verify the exact per-share payout formula:
    # 1 Token A is backed by (1 + Rv + V_B)/2 of collateral index S.
    # 1 Token A' (anUSD) is backed by (1 + Rv + V_B) of collateral index.
    # At Hd=0.25, backing per anUSD is 1.25 * (1 + Delta P).
    # Zero haircut requires 1.25 * (1 + Delta P) + (B_res / N_Ap) >= 1.0
    # 1 + Delta P >= (1.0 - b_res_per_Ap) / 1.25 = 0.80 - 0.80 * b_res_per_Ap
    # Delta P >= -0.20 - 0.80 * b_res_per_Ap ???
    # WAIT! Why does 1.25 * (1 + Delta P) = 0.50?
    # In A0 dual-tranche: 2 units of Class A ($2) split into 1 A' ($1) and 1 B' ($1).
    # So 1 unit of A' requires 2 units of Class A, which has 2 * (1 + Rv + Hd) backing!
    # So backing per unit of A' is 2 * (1.25) * (1 + Delta P) = 2.50 * (1 + Delta P)!
    # 2.50 * (1 + Delta P) >= 1.00 => 1 + Delta P >= 1.0 / 2.50 = 0.40 => Delta P >= -0.60 (-60.00%)!
    # With Buffer B_res added:
    # 2.50 * (1 + Delta P) + (B_res / N_Ap) >= 1.00
    # 1 + Delta P >= (1.00 - B_res / N_Ap) / 2.50 = 0.40 - (B_res / N_Ap) / 2.50
    # Delta P >= -0.60 - (B_res / N_Ap) / 2.50!
    
    # If B_res is expressed as fraction of Senior Debt (N_Ap * $1.00):
    # b_senior = B_res / (N_Ap * 1.00)
    # Delta P*_crit = -0.60 - b_senior / 2.50
    # At b_senior = 0.15 (15% of Senior Debt): Delta P*_crit = -0.60 - 0.15 / 2.50 = -0.60 - 0.06 = -66.00%!
    # At b_senior = 0.375 (37.5% of Senior Debt): Delta P*_crit = -0.60 - 0.375 / 2.50 = -0.60 - 0.15 = -75.00%!
    # If B_res is expressed as fraction of Initial Collateral at Barrier (2.50 * P0 * N_Ap):
    # b_barrier = B_res / (2.50 * P0 * N_Ap)
    # Delta P*_crit = -0.60 - b_barrier!
    # So to get Delta P*_crit = -75.00%, b_barrier must be 0.15 (15% of collateral value at barrier)!
    
    results_t2 = []
    for b_frac in [0.00, 0.05, 0.10, 0.15, 0.20, 0.25]:
        # Case A: b_frac of barrier collateral (2.50 * N_Ap)
        drop_barrier_def = -0.60 - b_frac
        # Case B: b_frac of senior debt (1.00 * N_Ap)
        drop_senior_def = -0.60 - b_frac / 2.50
        # Case C: from Par (4.00 * N_Ap)
        drop_from_par_barrier = -0.75 - b_frac
        drop_from_par_senior = -0.75 - b_frac / 4.00
        results_t2.append({
            "b_frac": b_frac,
            "drop_if_b_is_barrier_collateral": drop_barrier_def,
            "drop_if_b_is_senior_debt": drop_senior_def,
            "drop_from_par_barrier": drop_from_par_barrier,
            "drop_from_par_senior": drop_from_par_senior
        })
        
    return {"theorem_1": pd.DataFrame(results_t1), "theorem_2": pd.DataFrame(results_t2)}

def test_domain_3_and_4_plant_transfer_and_stability() -> Dict[str, Any]:
    """
    Stress tests the CPMM plant transfer function, damping ratio formulas, and Kd=0 proof.
    """
    alpha_elasticity = 5_000_000.0 # USD
    tau_arb_days = 5.55 # days
    tau_arb_yr = 5.55 / 365.0 # yr
    Kp = 0.150
    Ki_day = 0.020 # per day
    Ki_yr = 0.020 # if treated as per yr
    Kd = 0.005
    
    liquidity_tiers = [1.5e6, 10.0e6, 30.0e6]
    
    plant_analysis = []
    
    for L in liquidity_tiers:
        K_amm = alpha_elasticity / L # 3.333, 0.500, 0.1667
        
        # 1. Continuous Time in DAYS:
        a2_d = 1.0
        a1_d = (1.0 / tau_arb_days) + K_amm * Kp # 0.18018 + K_amm * 0.15
        a0_d = K_amm * Ki_day # K_amm * 0.020
        wn_d = math.sqrt(a0_d)
        zeta_exact_d = a1_d / (2.0 * wn_d)
        roots_d = np.roots([a2_d, a1_d, a0_d])
        
        # 2. Continuous Time in YEARS (if Ki=0.020 yr^-2, tau=0.0152 yr):
        a2_y = 1.0
        a1_y = (1.0 / tau_arb_yr) + K_amm * Kp # 65.7658 + K_amm * 0.15
        a0_y = K_amm * Ki_yr # K_amm * 0.020
        wn_y = math.sqrt(a0_y)
        zeta_exact_y = a1_y / (2.0 * wn_y)
        roots_y = np.roots([a2_y, a1_y, a0_y])
        
        # 3. Flawed formula in deliverable text:
        # zeta = (1 + K_dc * Kp) / (2 * sqrt(K_dc * Ki)) where K_dc = K_amm * tau_yr
        K_dc_y = K_amm * tau_arb_yr
        zeta_flawed_text_y = (1.0 + K_dc_y * Kp) / (2.0 * math.sqrt(K_dc_y * Ki_yr))
        
        # 4. Phase Margin PM with delay tau_delay = 300s = 300 / 86400 days = 0.003472 days:
        tau_delay_days = 300.0 / 86400.0
        # Solve for gain crossover frequency omega_gc where |L(j*w)| = 1
        # |L(jw)| = K_amm * sqrt(Kp^2 * w^2 + Ki^2) / (w * sqrt(w^2 + (1/tau)^2))
        w_grid = np.logspace(-3, 2, 10000)
        mag_L = (K_amm * np.sqrt(Kp**2 * w_grid**2 + Ki_day**2)) / (w_grid * np.sqrt(w_grid**2 + (1.0/tau_arb_days)**2))
        idx_gc = np.argmin(np.abs(mag_L - 1.0))
        w_gc_d = w_grid[idx_gc]
        
        # PM in degrees
        angle_controller = np.arctan2(Kp * w_gc_d, Ki_day) * 180.0 / np.pi
        angle_plant = -90.0 - np.arctan2(w_gc_d, (1.0 / tau_arb_days)) * 180.0 / np.pi
        angle_delay = - (w_gc_d * tau_delay_days) * 180.0 / np.pi
        pm_deg = 180.0 + angle_controller + angle_plant + angle_delay
        
        # Noise amplification calculation for Kd:
        # Variance of discrete derivative: 2 * sigma_noise^2 / dt^2
        # dt = 2.0s = 2.0 / 86400 days = 2.315e-5 days
        sigma_noise = 0.003 # 30 bps price noise
        dt_days = 2.0 / 86400.0
        deriv_noise_std = math.sqrt(2.0) * sigma_noise / dt_days # in 1/day units
        kd_rate_noise_std = Kd * deriv_noise_std
        
        plant_analysis.append({
            "L_USD": L,
            "K_amm": K_amm,
            "zeta_days_exact": round(zeta_exact_d, 3),
            "wn_rad_per_day": round(wn_d, 4),
            "poles_days": [round(r, 4) for r in roots_d],
            "zeta_years_exact": round(zeta_exact_y, 2),
            "zeta_flawed_text_formula": round(zeta_flawed_text_y, 2),
            "w_gc_rad_day": round(w_gc_d, 4),
            "PM_degrees_300s_delay": round(pm_deg, 2),
            "kd_actuator_noise_std_pp": round(kd_rate_noise_std * 100.0, 2)
        })
        
    return {"analysis": pd.DataFrame(plant_analysis)}

def test_domain_5_failure_manifolds() -> Dict[str, Any]:
    """
    Stress tests the failure boundary definitions and Euclidean distance metric.
    """
    # Let's test boundary distance for nominal parameter vector theta_0
    # theta = [H_d, H_u, K_p, K_i, kappa_dd]
    theta_0 = np.array([0.25, 2.00, 0.150, 0.020, 0.350])
    weights = np.array([0.10, 0.50, 0.05, 0.010, 0.100]) # normalizers
    
    # Boundary 1: H_d = 0.10 (Crash boundary threshold too low)
    dist_Hd = abs(theta_0[0] - 0.10) / weights[0]
    
    # Boundary 2: K_p = 0.00 (Unstable / Undamped)
    dist_Kp = abs(theta_0[1] - 0.00) / weights[2]
    
    # Boundary 3: K_i = 0.00 (Loss of Integral action)
    dist_Ki = abs(theta_0[3] - 0.00) / weights[3]
    
    # Composite distance:
    min_dist = min(dist_Hd, dist_Kp, dist_Ki)
    
    return {
        "theta_0": theta_0.tolist(),
        "normalized_distance_to_Hd_fail": dist_Hd,
        "normalized_distance_to_Kp_fail": dist_Kp,
        "normalized_distance_to_Ki_fail": dist_Ki,
        "min_safety_margin": min_dist,
        "satisfies_20pct_safe_gate": min_dist >= 0.20
    }

if __name__ == "__main__":
    print("=================================================================")
    print("1. DOMAIN 1: BALANCE SHEET STOCK-FLOW INVARIANT AUDIT")
    print("=================================================================")
    d1 = test_domain_1_balance_sheet_closure(10000)
    print(f"Total Samples Tested: {d1['n_samples']}")
    print(f"Regimes Sampled: {d1['regimes_tested']}")
    print(f"Published Formula Max Error: ${d1['published_formula_max_err']:,.2f}")
    print(f"Published Formula Failures: {d1['published_formula_failures']} ({d1['published_formula_failure_rate']*100:.1f}%)")
    print(f"Corrected Formula Max Error: ${d1['corrected_formula_max_err']:.2e}")
    print(f"Corrected Formula Failures: {d1['corrected_formula_failures']} (0.00%)")
    
    print("\n=================================================================")
    print("2. DOMAIN 2: THEOREM 1 & THEOREM 2 CRASH BOUNDS AUDIT")
    print("=================================================================")
    d2 = test_domain_2_crash_bounds_theorems()
    print("Theorem 1 Critical Drops:")
    print(d2["theorem_1"].head(10).to_string(index=False))
    print("\nTheorem 2 Solvency Extension Sizing:")
    print(d2["theorem_2"].to_string(index=False))
    
    print("\n=================================================================")
    print("3. DOMAIN 3 & 4: PLANT GAIN, STABILITY, DAMPING & KD=0 PROOF")
    print("=================================================================")
    d3 = test_domain_3_and_4_plant_transfer_and_stability()
    print(d3["analysis"].to_string(index=False))
    
    print("\n=================================================================")
    print("4. DOMAIN 5: FAILURE BOUNDARIES & SAFETY DISTANCE AUDIT")
    print("=================================================================")
    d5 = test_domain_5_failure_manifolds()
    print(f"Nominal Parameters: {d5['theta_0']}")
    print(f"Minimum Safety Distance Margin: {d5['min_safety_margin']:.2f}")
    print(f"Passes 20% Safe Gate (dist >= 0.20): {d5['satisfies_20pct_safe_gate']}")
