"""
Pytest Suite for Stage 2 3-Way Reconciliation & Adversarial Audit Verification
"""

import os
import json
import pytest
import numpy as np
import pandas as pd

PARQUET_PATH = "audit_artifacts/execution/STAGE_2_RESULTS.parquet"
MANIFEST_PATH = "audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json"

@pytest.fixture(scope="module")
def stage2_df():
    assert os.path.exists(PARQUET_PATH), f"Missing dataset: {PARQUET_PATH}"
    return pd.read_parquet(PARQUET_PATH)

@pytest.fixture(scope="module")
def stage2_manifest():
    assert os.path.exists(MANIFEST_PATH), f"Missing manifest: {MANIFEST_PATH}"
    with open(MANIFEST_PATH, "r") as f:
        return json.load(f)

def test_dataset_dimensions_and_integrity(stage2_df):
    """Verify 1,600 rows x 25 columns and zero missing/NaN/inf values."""
    assert stage2_df.shape == (1600, 25)
    assert stage2_df.isnull().sum().sum() == 0
    assert stage2_df.isna().sum().sum() == 0
    num_df = stage2_df.select_dtypes(include=[np.number])
    assert np.isinf(num_df).sum().sum() == 0

def test_stratification_balance(stage2_df):
    """Verify exact 2D stratification: 8 archs x 5 policies x 40 configs."""
    arch_counts = stage2_df["arch_id"].value_counts().sort_index()
    policy_counts = stage2_df["policy_id"].value_counts().sort_index()
    cell_counts = stage2_df.groupby(["arch_id", "policy_id"]).size()

    assert len(arch_counts) == 8
    assert (arch_counts == 200).all()
    assert len(policy_counts) == 5
    assert (policy_counts == 320).all()
    assert len(cell_counts) == 40
    assert (cell_counts == 40).all()

def test_screening_gate_compliance_rates(stage2_df):
    """Verify programmatic pass rates for all four diagnostic screening gates."""
    g1 = stage2_df["peg_rmse"] <= 0.05
    g2 = stage2_df["reset_churn_annual"] <= 5.0
    g3 = stage2_df["validator_cr_min"] >= 0.80
    g4 = stage2_df["haircut_prob"] <= 0.01
    joint = g1 & g2 & g4

    assert g1.sum() == 1600, "Gate 1 (Peg RMSE) must pass 1,600/1,600"
    assert g2.sum() == 1472, "Gate 2 (Reset Churn) must pass 1,472/1,600 (92.0%)"
    assert g3.sum() == 0, "Gate 3 (Validator CR) must pass 0/1,600 (0.0% due to sub-scale)"
    assert g4.sum() == 319, "Gate 4 (Solvency) must pass 319/1,600 (19.94%)"
    assert joint.sum() == 316, "Joint G1+G2+G4 must pass 316/1,600 (19.75%)"

def test_architecture_gate_distribution(stage2_df):
    """Verify architecture-level gate breakdowns."""
    # A2 Solvency Buffer
    a2 = stage2_df[stage2_df["arch_id"] == 2]
    assert (a2["haircut_prob"] <= 0.01).sum() == 194
    assert ((a2["peg_rmse"] <= 0.05) & (a2["reset_churn_annual"] <= 5.0) & (a2["haircut_prob"] <= 0.01)).sum() == 191

    # A5.3 Multi-LST Basket
    a53 = stage2_df[stage2_df["arch_id"] == 7]
    assert (a53["haircut_prob"] <= 0.01).sum() == 125
    assert ((a53["peg_rmse"] <= 0.05) & (a53["reset_churn_annual"] <= 5.0) & (a53["haircut_prob"] <= 0.01)).sum() == 125

    # Other architectures fail Gate 4 100%
    for aid in [0, 1, 3, 4, 5, 6]:
        sub = stage2_df[stage2_df["arch_id"] == aid]
        assert (sub["haircut_prob"] <= 0.01).sum() == 0

def test_pareto_dominance_and_frontier_counts(stage2_df):
    """Verify multi-objective Pareto non-dominated set (178 total, 0 in A0, 28 in POL-04)."""
    objs = np.column_stack([
        stage2_df["haircut_prob"].values,
        stage2_df["tail_cvar_99"].values,
        stage2_df["reset_churn_annual"].values,
        -stage2_df["validator_cr_min"].values,
        -stage2_df["avax_burned_total"].values
    ])
    
    n_candidates = len(stage2_df)
    is_dominated = np.zeros(n_candidates, dtype=bool)
    
    for i in range(n_candidates):
        diff = objs - objs[i]
        dominates = (np.all(diff <= 1e-9, axis=1)) & (np.any(diff < -1e-9, axis=1))
        if np.any(dominates):
            is_dominated[i] = True

    non_dom = ~is_dominated
    assert non_dom.sum() == 178, f"Expected 178 non-dominated candidates, got {non_dom.sum()}"
    
    # A0 must have 0 non-dominated candidates
    assert (stage2_df[non_dom]["arch_id"] == 0).sum() == 0
    
    # POL-04 must have exactly 28 non-dominated candidates
    assert (stage2_df[non_dom]["policy_id"] == 3).sum() == 28

def test_parameter_bounds(stage2_df):
    """Verify that sampled parameters conform to canonical boundary constraints."""
    assert (stage2_df["R"] >= 0.01).all() and (stage2_df["R"] <= 0.20).all()
    assert (stage2_df["R_prime"] >= 0.005).all() and (stage2_df["R_prime"] <= 0.10).all()
    assert (stage2_df["R"] > stage2_df["R_prime"]).all()  # Filter F2 check
    assert (stage2_df["H_d"] >= 0.05).all() and (stage2_df["H_d"] <= 0.60).all()
    assert (stage2_df["H_u"] >= 1.10).all() and (stage2_df["H_u"] <= 3.50).all()
    assert (stage2_df["K_p"] >= 0.01).all() and (stage2_df["K_p"] <= 0.60).all()
    assert (stage2_df["K_i"] >= 0.001).all() and (stage2_df["K_i"] <= 0.10).all()
    assert (stage2_df["B_target"] >= 0.0001).all() and (stage2_df["B_target"] <= 0.30).all()
    assert (stage2_df["kappa_dd"] >= 0.05).all() and (stage2_df["kappa_dd"] <= 0.80).all()
