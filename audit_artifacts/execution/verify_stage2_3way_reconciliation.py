#!/usr/bin/env python3
"""
Master Stage 2 3-Way Reconciliation & Verification Script
Adversarial Validation Audit of Stage 2 Architecture & Redistribution Policy Screening

This script programmatically verifies:
1. Complete Dataset Integrity: 1,600 rows, 25 columns, 0 null/NaN/inf values.
2. Exact Stratified Balance: 8 architectures x 5 policies x 40 candidates per cell.
3. Gate Compliance Rates:
   - Gate 1 (Peg RMSE <= 0.05): 100.0% (1,600/1,600) [Degenerate Pass]
   - Gate 2 (Reset Churn <= 5.0): 92.0% (1,472/1,600)
   - Gate 3 (Validator CR >= 0.80): 0.0% (0/1,600) [Sub-Scale Artifact]
   - Gate 4 (Solvency Survival >= 99% / Haircut Prob <= 0.01): 19.94% (319/1,600)
   - Joint Non-Subscale Gates (G1 + G2 + G4): 19.75% (316/1,600)
4. Multi-Objective Vector Optimization & Pareto Non-Dominated Frontier (5 Canonical Objectives):
   - Objectives: haircut_prob (MIN), tail_cvar_99 (MIN), reset_churn_annual (MIN), validator_cr_min (MAX), avax_burned_total (MAX).
   - Exact 178 Pareto non-dominated configurations across active objectives.
   - Architecture A0 has exactly 0 non-dominated candidates (universally dominated).
   - Policy POL-04 has exactly 28 non-dominated candidates (Pareto Frontier Extreme Point).
5. Complete 14-Parameter Behavioral Parameter Audit (BPA) summary statistics.
6. Complete 11-KPI empirical profiles across all 8 architectures and 5 policies.
"""

import os
import sys
import json
import numpy as np
import pandas as pd

def run_verification():
    print("=" * 80)
    print("STAGE 2: 3-WAY RECONCILIATION & DATASET INTEGRITY VERIFICATION SUITE")
    print("=" * 80)

    # 1. Load Parquet Dataset and Manifest
    parquet_path = "audit_artifacts/execution/STAGE_2_RESULTS.parquet"
    manifest_path = "audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json"
    
    if not os.path.exists(parquet_path):
        raise FileNotFoundError(f"Missing parquet dataset: {parquet_path}")
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Missing manifest: {manifest_path}")

    df = pd.read_parquet(parquet_path)
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    print(f"[+] Loaded Parquet Dataset: {parquet_path}")
    print(f"    Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"[+] Loaded Manifest: {manifest_path}")

    # Check 1: Dimensions and Data Integrity
    assert df.shape[0] == 1600, f"Expected 1,600 rows, got {df.shape[0]}"
    assert df.shape[1] == 25, f"Expected 25 columns, got {df.shape[1]}"
    
    null_counts = df.isnull().sum().sum()
    na_counts = df.isna().sum().sum()
    inf_counts = np.isinf(df.select_dtypes(include=[np.number])).sum().sum()
    
    assert null_counts == 0, f"Found {null_counts} null values"
    assert na_counts == 0, f"Found {na_counts} NA values"
    assert inf_counts == 0, f"Found {inf_counts} infinite values"
    print("[PASS] Check 1: Dataset Integrity (1,600 rows, 25 columns, 0 null/NaN/inf).")

    # Check 2: Stratification Balance
    arch_counts = df["arch_id"].value_counts().sort_index()
    policy_counts = df["policy_id"].value_counts().sort_index()
    cell_counts = df.groupby(["arch_id", "policy_id"]).size()

    assert len(arch_counts) == 8, f"Expected 8 architectures, got {len(arch_counts)}"
    assert (arch_counts == 200).all(), f"Each architecture must have 200 rows, got:\n{arch_counts}"
    assert len(policy_counts) == 5, f"Expected 5 policies, got {len(policy_counts)}"
    assert (policy_counts == 320).all(), f"Each policy must have 320 rows, got:\n{policy_counts}"
    assert len(cell_counts) == 40, f"Expected 40 cells, got {len(cell_counts)}"
    assert (cell_counts == 40).all(), f"Each [arch, policy] cell must have exactly 40 rows"
    print("[PASS] Check 2: Stratified Allocation (8 Archs x 5 Policies x 40 Configs = 1,600 Balanced Cells).")

    # Check 3: Gate Compliance Calculations
    g1_pass = (df["peg_rmse"] <= 0.05)
    g2_pass = (df["reset_churn_annual"] <= 5.0)
    g3_pass = (df["validator_cr_min"] >= 0.80)
    g4_pass = (df["haircut_prob"] <= 0.01)
    joint_124_pass = g1_pass & g2_pass & g4_pass

    print("\n--- Diagnostic Screening Gate Results ---")
    print(f"Gate 1 (Peg RMSE <= 0.05):           {g1_pass.sum():4d} / 1600 ({g1_pass.mean()*100:6.2f}%)")
    print(f"Gate 2 (Reset Churn <= 5.0):         {g2_pass.sum():4d} / 1600 ({g2_pass.mean()*100:6.2f}%)")
    print(f"Gate 3 (Validator CR >= 0.80):       {g3_pass.sum():4d} / 1600 ({g3_pass.mean()*100:6.2f}%)")
    print(f"Gate 4 (Solvency Survival >= 99%):   {g4_pass.sum():4d} / 1600 ({g4_pass.mean()*100:6.2f}%)")
    print(f"Joint G1 + G2 + G4 Pass:             {joint_124_pass.sum():4d} / 1600 ({joint_124_pass.mean()*100:6.2f}%)")

    assert g1_pass.sum() == 1600, f"Gate 1 pass count mismatch: {g1_pass.sum()}"
    assert g2_pass.sum() == 1472, f"Gate 2 pass count mismatch: {g2_pass.sum()}"
    assert g3_pass.sum() == 0, f"Gate 3 pass count mismatch: {g3_pass.sum()}"
    assert g4_pass.sum() == 319, f"Gate 4 pass count mismatch: {g4_pass.sum()}"
    assert joint_124_pass.sum() == 316, f"Joint G1+G2+G4 pass count mismatch: {joint_124_pass.sum()}"
    print("[PASS] Check 3: Gate Compliance Rates match exact canonical values.")

    # Check 4: Gate Breakdown by Architecture
    print("\n--- Gate Compliance Breakdown by Architecture ---")
    arch_names = {
        0: "A0 (Dual-Class Reset)",
        1: "A1 (Continuous Amort)",
        2: "A2 (Solvency Buffer)",
        3: "A3 (Floating Junior)",
        4: "A4 (Zero Controller)",
        5: "A5.1 (Convertible Debt)",
        6: "A5.2 (Protocol AMM)",
        7: "A5.3 (Multi-LST Basket)"
    }
    for aid, aname in arch_names.items():
        sub = df[df["arch_id"] == aid]
        g1_cnt = (sub["peg_rmse"] <= 0.05).sum()
        g2_cnt = (sub["reset_churn_annual"] <= 5.0).sum()
        g3_cnt = (sub["validator_cr_min"] >= 0.80).sum()
        g4_cnt = (sub["haircut_prob"] <= 0.01).sum()
        j_cnt = ((sub["peg_rmse"] <= 0.05) & (sub["reset_churn_annual"] <= 5.0) & (sub["haircut_prob"] <= 0.01)).sum()
        print(f"Arch {aid:d} [{aname:24s}]: G1={g1_cnt:3d}/200, G2={g2_cnt:3d}/200, G3={g3_cnt:3d}/200, G4={g4_cnt:3d}/200, Joint={j_cnt:3d}/200")
        if aid == 2:
            assert g4_cnt == 194 and j_cnt == 191
        elif aid == 7:
            assert g4_cnt == 125 and j_cnt == 125
        else:
            assert g4_cnt == 0 and j_cnt == 0

    print("[PASS] Check 4: Architecture gate distributions verified (A2: 194 pass G4, A5.3: 125 pass G4, others: 0).")

    # Check 5: Multi-Objective Vector Optimization and Pareto Non-Dominated Frontier
    # 5 Canonical Objectives from DECISION_FRAMEWORK.md and EXPERIMENTAL_LADDER.md:
    # 1. haircut_prob (MIN)
    # 2. tail_cvar_99 (MIN)
    # 3. reset_churn_annual (MIN)
    # 4. validator_cr_min (MAX -> MIN -validator_cr_min)
    # 5. avax_burned_total (MAX -> MIN -avax_burned_total)
    
    objs = np.column_stack([
        df["haircut_prob"].values,
        df["tail_cvar_99"].values,
        df["reset_churn_annual"].values,
        -df["validator_cr_min"].values,
        -df["avax_burned_total"].values
    ])
    
    n_candidates = len(df)
    is_dominated = np.zeros(n_candidates, dtype=bool)
    
    for i in range(n_candidates):
        diff = objs - objs[i]
        # Candidate j dominates candidate i if all diff <= 0 (j is at least as good in all dims)
        # and any diff < 0 (j is strictly better in at least one dim)
        dominates = (np.all(diff <= 1e-9, axis=1)) & (np.any(diff < -1e-9, axis=1))
        if np.any(dominates):
            is_dominated[i] = True

    is_non_dominated = ~is_dominated
    df["is_non_dominated"] = is_non_dominated
    total_non_dominated = is_non_dominated.sum()
    print(f"\n--- Multi-Objective Vector Optimization Results ---")
    print(f"Total Non-Dominated Configurations: {total_non_dominated} / 1600 ({total_non_dominated/1600*100:.2f}%)")

    # Non-dominated breakdown by Architecture
    print("\nNon-Dominated Candidates by Architecture:")
    for aid, aname in arch_names.items():
        cnt = df[df["arch_id"] == aid]["is_non_dominated"].sum()
        print(f"  Arch {aid} [{aname:24s}]: {cnt:3d} / 200 ({cnt/200*100:5.2f}%)")
    
    # Non-dominated breakdown by Policy
    policy_names = {
        0: "POL-01 (Static Reference)",
        1: "POL-02 (Countercyclical)",
        2: "POL-03 (Reserve Priority)",
        3: "POL-04 (Burn Maximizer)",
        4: "POL-05 (State Softmax)"
    }
    print("\nNon-Dominated Candidates by Policy:")
    for pid, pname in policy_names.items():
        cnt = df[df["policy_id"] == pid]["is_non_dominated"].sum()
        print(f"  Policy {pid} [{pname:24s}]: {cnt:3d} / 320 ({cnt/320*100:5.2f}%)")

    assert total_non_dominated == 178, f"Expected 178 non-dominated candidates, got {total_non_dominated}"
    assert df[df["arch_id"] == 0]["is_non_dominated"].sum() == 0, "A0 must have 0 non-dominated candidates"
    assert df[df["policy_id"] == 3]["is_non_dominated"].sum() == 28, "POL-04 must have exactly 28 non-dominated candidates"
    print("[PASS] Check 5: Pareto non-dominated set verified (178 total, 0 in A0, 28 in POL-04).")

    # Check 6: Summary of Parameter and KPI Statistics
    print("\n--- Parameter Distributions (14 Parameters) ---")
    param_cols = ["R", "R_prime", "H_d", "H_u", "omega_burn", "omega_val", "omega_res", "omega_l1", "K_p", "K_i", "B_target", "kappa_dd", "arch_id", "policy_id"]
    for col in param_cols:
        print(f"  {col:15s}: Min={df[col].min():10.4f}, Mean={df[col].mean():10.4f}, Max={df[col].max():10.4f}, Std={df[col].std():10.4f}")

    print("\n--- KPI Distributions (11 Metrics) ---")
    kpi_cols = ["peg_rmse", "max_depeg", "haircut_prob", "tail_cvar_99", "recovery_time_days", "validator_cr_min", "validator_insolvency_prob", "avax_burned_total", "reset_churn_annual", "rate_volatility", "reserve_depletion_prob"]
    for col in kpi_cols:
        print(f"  {col:26s}: Min={df[col].min():12.6f}, Mean={df[col].mean():12.6f}, Max={df[col].max():12.6f}")

    print("\n" + "=" * 80)
    print("ALL VERIFICATION CHECKS PASSED PERFECTLY (100.00% PROGRAMMATIC RECONCILIATION)")
    print("=" * 80)

if __name__ == "__main__":
    run_verification()
