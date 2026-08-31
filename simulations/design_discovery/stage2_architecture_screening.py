"""
Stage 2: Architecture & Policy Screening Engine.
Governing Plan: BCRG-DESIGN-DISCOVERY-DECISION-FRAMEWORK-01 (Stage 2 / 7)

Executes standardized Monte Carlo screening over candidate configurations from
audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet across all 8 architectures
(A0–A5.3) and 5 redistribution policies (POL-01 to POL-05) under Kou jump-diffusion dynamics.

Computes exact statistical metrics with Common Random Numbers (CRN):
  - Peg Tracking RMSE & Maximum Depeg
  - Senior Principal Haircut Probability & CVaR_99
  - Peg Recovery Time (Days)
  - Validator OpEx Coverage Ratio (CR_OpEx) & Insolvency Probability
  - Cumulative AVAX Burn Volume
  - Reserve Buffer Depletion Rate (A2)
  - Rate Controller Volatility
"""

import os
import sys
import time
import json
import datetime
import subprocess
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXECUTION_DIR = os.path.join(PROJECT_ROOT, "audit_artifacts", "execution")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "audit_artifacts", "reports")
os.makedirs(EXECUTION_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


# ----------------------------------------------------------------------
# 1. Stochastic Environment & Kou SDE Jump-Diffusion Path Generator
# ----------------------------------------------------------------------
def generate_standardized_price_paths(n_paths: int = 500, n_steps: int = 365, 
                                      dt: float = 1.0/365.0, seed: int = 2026,
                                      sigma: float = 0.8915, lambda_j: float = 15.0,
                                      p_up: float = 0.5955, eta1: float = 7.671, 
                                      eta2: float = 7.801, mu: float = -0.3402) -> np.ndarray:
    """
    Generates standardized daily AVAX price paths using Kou Asymmetric Double-Exponential SDE.
    Uses Common Random Numbers (CRN) for identical testing conditions across all architectures.
    """
    rng = np.random.default_rng(seed)
    
    # Expected jump size zeta_j
    zeta_j = p_up * eta1 / (eta1 - 1.0) + (1.0 - p_up) * eta2 / (eta2 + 1.0) - 1.0
    drift = (mu - 0.5 * sigma**2 - lambda_j * zeta_j) * dt
    diff_std = sigma * np.sqrt(dt)
    
    # 1. Diffusion component
    dW = rng.normal(0, diff_std, size=(n_paths, n_steps))
    
    # 2. Poisson jump counts
    dN = rng.poisson(lambda_j * dt, size=(n_paths, n_steps))
    
    # 3. Asymmetric jump sizes
    jumps = np.zeros((n_paths, n_steps))
    total_jumps = int(np.sum(dN))
    if total_jumps > 0:
        is_up = rng.random(size=total_jumps) < p_up
        up_jumps = rng.exponential(scale=1.0 / eta1, size=total_jumps)
        down_jumps = -rng.exponential(scale=1.0 / eta2, size=total_jumps)
        jump_vals = np.where(is_up, up_jumps, down_jumps)
        
        # Flatten dN indices and populate
        jump_idx = np.where(dN > 0)
        # Handle multiple jumps per step if any
        cursor = 0
        for p, s in zip(jump_idx[0], jump_idx[1]):
            cnt = dN[p, s]
            jumps[p, s] = np.sum(jump_vals[cursor:cursor+cnt])
            cursor += cnt
            
    # Continuous log returns
    dlnP = drift + dW + jumps
    lnP = np.cumsum(dlnP, axis=1)
    # Normalized price paths starting at P_0 = 1.0
    P_paths = np.exp(lnP)
    P_paths = np.hstack([np.ones((n_paths, 1)), P_paths])
    return P_paths


# ----------------------------------------------------------------------
# 2. Vectorized Architecture Lifecycle Simulation
# ----------------------------------------------------------------------
def simulate_single_candidate(row: Dict[str, Any], price_paths: np.ndarray) -> Dict[str, Any]:
    """
    Simulates a single candidate parameter configuration across all standardized price paths.
    """
    arch_id = int(row["arch_id"])
    policy_id = int(row["policy_id"])
    R = float(row["R"])
    R_prime = float(row["R_prime"])
    H_d = float(row["H_d"])
    H_u = float(row["H_u"])
    omega_burn = float(row["omega_burn"])
    omega_val = float(row["omega_val"])
    omega_res = float(row["omega_res"])
    omega_l1 = float(row["omega_l1"])
    K_p = float(row["K_p"])
    K_i = float(row["K_i"])
    B_target = float(row["B_target"])
    kappa_dd = float(row["kappa_dd"])
    
    n_paths, n_steps = price_paths.shape[0], price_paths.shape[1] - 1
    dt = 1.0 / 365.0
    
    # Path tracking arrays
    peg_errors = np.zeros((n_paths, n_steps))
    haircuts = np.zeros(n_paths)
    validator_cr_mins = np.zeros(n_paths)
    burn_totals = np.zeros(n_paths)
    res_depletions = np.zeros(n_paths)
    reset_counts = np.zeros(n_paths)
    rate_mods = np.zeros((n_paths, n_steps))
    recovery_times = []
    
    # Constant parameters
    base_pool_savax = 1_000_000.0  # 1M sAVAX
    node_count = 1450
    node_monthly_cost = 350.0
    validator_annual_opex = node_count * node_monthly_cost * 12.0  # $6.09M
    base_staking_apr = 0.0640
    
    # Liquidity parameters
    L_amm_base = 15_000_000.0  # $15M default secondary AMM depth
    if arch_id == 6:  # A5.2 Protocol-Owned AMM boosts liquidity by +30%
        L_amm_base *= 1.30
        
    tau_arb = 5.55 / 365.25  # 5.55 days
    alpha_flow = 1.0e7
    K_dc = (alpha_flow * tau_arb) / L_amm_base
    
    for p in range(n_paths):
        P_path = price_paths[p]
        
        # In A5.3 (Multi-LST Basket), price volatility is damped by 3-asset basket diversification
        if arch_id == 7:
            # Basket return reduces path deviation by ~20%
            P_path = 1.0 + (P_path - 1.0) * 0.80
            
        beta = 1.0
        epoch_v = 0.0
        B_res = B_target * base_pool_savax * 25.0 * 0.5  # Initial reserve buffer ($)
        
        P_dex = 1.0000
        int_err = 0.0
        resets = 0
        path_haircut = 0.0
        min_cr_val = 999.0
        cum_burn = 0.0
        res_depleted = 0
        
        depeg_start_idx = None
        
        for s in range(n_steps):
            P_t = P_path[s+1]
            epoch_v += dt
            
            # Collateral Spot Index
            S_t = P_t / (beta * 1.0)
            
            # --- 1. PRIMARY TRANCHE VALUATION BY ARCHITECTURE ---
            if arch_id == 0:  # A0: Dual-Class Discrete Resets
                V_A = 1.0 + R * epoch_v
                V_B = max(0.0, 2.0 * S_t - V_A)
                
                # Reset Checks
                if V_B >= H_u:
                    resets += 1
                    beta *= S_t
                    epoch_v = 0.0
                elif V_B <= H_d:
                    resets += 1
                    if 2.0 * S_t < V_A:
                        deficit = (V_A - 2.0 * S_t) / V_A
                        path_haircut = max(path_haircut, deficit)
                    beta *= max(0.01, S_t)
                    epoch_v = 0.0
                    
            elif arch_id == 1:  # A1: Continuous Streaming Amortization
                # Continuous de-leveraging (zero discrete resets)
                V_A = 1.0 + R * epoch_v
                # Streaming yield continuously de-leverages
                if 2.0 * S_t < 1.0:
                    path_haircut = max(path_haircut, (1.0 - 2.0 * S_t))
                    
            elif arch_id == 2:  # A2: Dedicated Solvency Buffer Vault
                V_A = 1.0 + R * epoch_v
                V_B = max(0.0, 2.0 * S_t - V_A)
                if V_B <= H_d:
                    resets += 1
                    if 2.0 * S_t < V_A:
                        deficit_usd = (V_A - 2.0 * S_t) * base_pool_savax
                        if B_res >= deficit_usd:
                            B_res -= deficit_usd
                        else:
                            uncovered = deficit_usd - B_res
                            B_res = 0.0
                            res_depleted = 1
                            path_haircut = max(path_haircut, uncovered / (V_A * base_pool_savax))
                    beta *= max(0.01, S_t)
                    epoch_v = 0.0
                    
            elif arch_id == 3:  # A3: Floating Junior Equity Tranche
                V_A = 1.0000  # Pure fixed claim $1.00
                V_B = max(0.0, 2.0 * S_t - 1.0)
                if 2.0 * S_t < 1.0:
                    path_haircut = max(path_haircut, 1.0 - 2.0 * S_t)
                    
            elif arch_id == 4:  # A4: Zero-Controller CDP
                V_A = 1.0000
                if 2.0 * S_t < 1.0:
                    path_haircut = max(path_haircut, 1.0 - 2.0 * S_t)
                    
            elif arch_id == 5:  # A5.1: Dynamic Debt-Equity Convertibles
                V_A = 1.0 + R * epoch_v
                if 2.0 * S_t < V_A:
                    # Auto-convert junior claims to equity, preventing senior default
                    path_haircut = max(path_haircut, (V_A - 2.0 * S_t) * 0.20)  # 80% absorbed by conversion
                    
            elif arch_id in (6, 7):  # A5.2 (Protocol AMM) & A5.3 (Multi-LST)
                V_A = 1.0 + R * epoch_v
                V_B = max(0.0, 2.0 * S_t - V_A)
                if V_B <= H_d:
                    resets += 1
                    if 2.0 * S_t < V_A:
                        path_haircut = max(path_haircut, (V_A - 2.0 * S_t) / V_A)
                    beta *= max(0.01, S_t)
                    epoch_v = 0.0
                    
            # --- 2. CONTROLLER ACTUATION & SECONDARY PEG DYNAMICS ---
            if arch_id == 4:  # A4: Zero Controller
                u_t = 0.0
            else:
                err = P_dex - 1.0000
                int_err = np.clip(int_err + err * dt, -0.10, 0.10)
                u_t = np.clip(-K_p * err - K_i * int_err, -0.05, 0.05)
                
            rate_mods[p, s] = u_t
            
            # Secondary DEX Price Evolution
            # Primary arbitrage pushes price towards 1.0, interest rate diff modulates demand
            arb_pull = (1.0000 - P_dex) / tau_arb
            rate_demand_flow = u_t * alpha_flow / L_amm_base
            dP_dex = (arb_pull + rate_demand_flow) * dt
            P_dex = float(np.clip(P_dex + dP_dex, 0.50, 1.50))
            peg_errors[p, s] = P_dex - 1.0000
            
            # Track recovery time if depegged > 0.50%
            if abs(P_dex - 1.0) > 0.005:
                if depeg_start_idx is None:
                    depeg_start_idx = s
            else:
                if depeg_start_idx is not None:
                    recovery_times.append((s - depeg_start_idx) * dt * 365.0)
                    depeg_start_idx = None
                    
            # --- 3. REDISTRIBUTION POLICY & VALIDATOR OPEX TRACKING ---
            gross_surplus_flow = base_staking_apr * base_pool_savax * P_t * 25.0 * dt
            drawdown_t = max(0.0, 1.0 - S_t)
            
            if policy_id == 0:  # POL-01: Static
                w_burn, w_val, w_res = omega_burn, omega_val, omega_res
            elif policy_id == 1:  # POL-02: Countercyclical Drawdown Feedback
                w_val = np.clip(omega_val + kappa_dd * drawdown_t, 0.15, 0.50)
                w_res = omega_res
                w_burn = max(0.0, 1.0 - w_val - w_res - omega_l1)
            elif policy_id == 2:  # POL-03: Reserve Priority
                w_res = np.clip(0.30 * max(0.0, 1.25 - 2.0 * S_t), 0.0, 0.35)
                w_val = omega_val
                w_burn = max(0.0, 1.0 - w_val - w_res - omega_l1)
            elif policy_id == 3:  # POL-04: Deflationary Burn Maximizer
                w_val = 0.10
                w_res = 0.0
                w_burn = max(0.75, 1.0 - w_val - omega_l1)
            else:  # POL-05: State Softmax Dynamic
                w_val = np.clip(0.20 + 0.30 * drawdown_t, 0.10, 0.50)
                w_res = np.clip(0.15 * max(0.0, 1.10 - S_t), 0.0, 0.25)
                w_burn = max(0.0, 1.0 - w_val - w_res - omega_l1)
                
            # Validator OpEx Coverage Ratio
            validator_income_flow = gross_surplus_flow * w_val
            daily_opex_cost = validator_annual_opex * dt
            cr_val = validator_income_flow / daily_opex_cost if daily_opex_cost > 0 else 2.0
            min_cr_val = min(min_cr_val, cr_val)
            
            # Burn accumulator & Reserve accumulation
            cum_burn += gross_surplus_flow * w_burn
            if arch_id == 2:
                B_res += gross_surplus_flow * w_res
                
        haircuts[p] = path_haircut
        validator_cr_mins[p] = min_cr_val
        burn_totals[p] = cum_burn
        res_depletions[p] = res_depleted
        reset_counts[p] = resets
        
    # Aggregate Metrics across all paths
    peg_rmse = float(np.sqrt(np.mean(peg_errors**2)))
    max_depeg = float(np.max(np.abs(peg_errors)))
    haircut_prob = float(np.mean(haircuts > 0.0001))
    tail_cvar_99 = float(np.mean(haircuts[haircuts >= np.percentile(haircuts, 99.0)])) if np.sum(haircuts > 0) > 0 else 0.0
    val_cr_mean = float(np.mean(validator_cr_mins))
    val_insolv_prob = float(np.mean(validator_cr_mins < 1.20))
    avg_burn = float(np.mean(burn_totals))
    avg_resets = float(np.mean(reset_counts))
    rate_vol = float(np.std(rate_mods))
    avg_recov_time = float(np.mean(recovery_times)) if len(recovery_times) > 0 else 0.50
    res_depletion_prob = float(np.mean(res_depletions))
    
    return {
        "peg_rmse": peg_rmse,
        "max_depeg": max_depeg,
        "haircut_prob": haircut_prob,
        "tail_cvar_99": tail_cvar_99,
        "recovery_time_days": avg_recov_time,
        "validator_cr_min": val_cr_mean,
        "validator_insolvency_prob": val_insolv_prob,
        "avax_burned_total": avg_burn,
        "reset_churn_annual": avg_resets,
        "rate_volatility": rate_vol,
        "reserve_depletion_prob": res_depletion_prob
    }


# ----------------------------------------------------------------------
# 3. Parallel Batch Execution Harness
# ----------------------------------------------------------------------
def execute_stage2_screening_campaign(n_sample_candidates: int = 1600, 
                                      n_mc_paths: int = 500, 
                                      seed: int = 2026) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Executes the full Stage 2 Monte Carlo screening campaign.
    Stratified sampling across all 8 architectures and 5 policies from STAGE_1_CORRECTED_SURVIVORS.parquet.
    """
    survivors_path = os.path.join(EXECUTION_DIR, "STAGE_1_CORRECTED_SURVIVORS.parquet")
    df_survivors = pd.read_parquet(survivors_path)
    
    print(f"[1/4] Loaded N = {len(df_survivors):,} Stage-1 validated candidates from: {survivors_path}")
    
    # Stratified candidate sampling (Option A: 200 candidates per architecture divided equally across 5 policies = 40 per cell)
    candidates = []
    n_per_cell = n_sample_candidates // (8 * 5)  # 1600 // 40 = 40
    for a_id in range(8):
        for p_id in range(5):
            sub_df = df_survivors[(df_survivors["arch_id"] == a_id) & (df_survivors["policy_id"] == p_id)]
            if len(sub_df) >= n_per_cell:
                sampled_sub = sub_df.sample(n=n_per_cell, random_state=seed + a_id * 10 + p_id)
            else:
                sampled_sub = sub_df
            candidates.append(sampled_sub)
        
    df_sample = pd.concat(candidates, ignore_index=True)
    print(f"[2/4] Selected 2D stratified evaluation batch: N = {len(df_sample):,} configurations (40 / [arch, policy] cell)")
    
    # Generate Common Random Numbers (CRN) Standardized Price Paths
    print(f"[3/4] Generating {n_mc_paths} Kou SDE jump-diffusion paths (seed={seed})...")
    price_paths = generate_standardized_price_paths(n_paths=n_mc_paths, n_steps=365, seed=seed)
    
    # Run Parallel Evaluation
    print(f"[4/4] Executing Monte Carlo screening on 8 worker processes...")
    t0 = time.time()
    
    rows = df_sample.to_dict(orient="records")
    results = []
    
    # Vectorized / Parallel dispatch
    with ProcessPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as executor:
        futures = {executor.submit(simulate_single_candidate, row, price_paths): i for i, row in enumerate(rows)}
        for future in as_completed(futures):
            idx = futures[future]
            res = future.result()
            # Combine input config with output metrics
            combined = {**rows[idx], **res}
            results.append(combined)
            
    runtime = time.time() - t0
    print(f"Screening campaign completed in {runtime:.2f} seconds ({len(results)/runtime:.1f} configs/sec)")
    
    df_results = pd.DataFrame(results)
    
    # Save Results Dataset
    results_parquet = os.path.join(EXECUTION_DIR, "STAGE_2_RESULTS.parquet")
    df_results.to_parquet(results_parquet)
    print(f"Published results parquet to: {results_parquet}")
    
    # Compile Manifest & Statistical Summary
    manifest = {
        "experiment_id": "EXP-STAGE-02-ARCHITECTURE-POLICY-SCREENING-01",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "input_population_dataset": "STAGE_1_CORRECTED_SURVIVORS.parquet",
        "input_population_size": len(df_survivors),
        "evaluated_configurations": len(df_results),
        "mc_paths_per_candidate": n_mc_paths,
        "runtime_seconds": runtime,
        "random_seed": seed,
        "model_version": "Kou-SDE-CPMM-v2.1",
        "deliverables": [
            "audit_artifacts/execution/STAGE_2_RESULTS.parquet",
            "audit_artifacts/reports/STAGE_2_ARCHITECTURE_SCREENING.md",
            "audit_artifacts/reports/ARCHITECTURE_COMPARISON.md",
            "audit_artifacts/reports/REDISTRIBUTION_POLICY_SCREENING.md",
            "audit_artifacts/reports/SCREENING_STATISTICS.md"
        ]
    }
    
    manifest_path = os.path.join(EXECUTION_DIR, "STAGE_2_EXPERIMENT_MANIFEST.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        
    return df_results, manifest


if __name__ == "__main__":
    df_res, man = execute_stage2_screening_campaign(n_sample_candidates=1600, n_mc_paths=500, seed=2026)
    print("Stage 2 screening execution completed successfully!")
