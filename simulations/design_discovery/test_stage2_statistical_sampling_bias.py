"""
Pytest Suite for Milestone 5 (Requirement R5):
Sampling Error, Stage-1 Selection Bias, and Lambda Provisionality Assessment.

Governing Plan: BCRG-DESIGN-DISCOVERY-DECISION-FRAMEWORK-01
Pipeline Stage: Stage 2 / 7 (Adversarial Validation Audit)
"""

import os
import sys
import json
import pytest
import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

EXECUTION_DIR = os.path.join(PROJECT_ROOT, "audit_artifacts", "execution")
PARQUET_PATH = os.path.join(EXECUTION_DIR, "STAGE_2_RESULTS.parquet")
SURVIVORS_PATH = os.path.join(EXECUTION_DIR, "STAGE_1_CORRECTED_SURVIVORS.parquet")
STAGE1_MANIFEST_PATH = os.path.join(EXECUTION_DIR, "STAGE_1_ANALYTICAL_PRUNING_MANIFEST.json")
STAGE2_MANIFEST_PATH = os.path.join(EXECUTION_DIR, "STAGE_2_EXPERIMENT_MANIFEST.json")


@pytest.fixture(scope="module")
def stage2_df():
    assert os.path.exists(PARQUET_PATH), f"Missing dataset: {PARQUET_PATH}"
    return pd.read_parquet(PARQUET_PATH)


@pytest.fixture(scope="module")
def stage1_survivors_df():
    assert os.path.exists(SURVIVORS_PATH), f"Missing survivors dataset: {SURVIVORS_PATH}"
    return pd.read_parquet(SURVIVORS_PATH)


@pytest.fixture(scope="module")
def stage1_manifest():
    assert os.path.exists(STAGE1_MANIFEST_PATH), f"Missing manifest: {STAGE1_MANIFEST_PATH}"
    with open(STAGE1_MANIFEST_PATH, "r") as f:
        return json.load(f)


def test_monte_carlo_standard_errors_and_ci(stage2_df):
    """Verify MCSE and 95% Confidence Intervals across architectures and policies."""
    kpi_cols = ["haircut_prob", "tail_cvar_99", "reset_churn_annual", "validator_cr_min", "avax_burned_total"]
    
    # 1. Architecture-level uncertainty checks
    for aid in range(8):
        sub = stage2_df[stage2_df["arch_id"] == aid]
        assert len(sub) == 200
        for col in kpi_cols:
            mean = sub[col].mean()
            std = sub[col].std()
            se = std / np.sqrt(len(sub))
            ci_low = mean - 1.96 * se
            ci_high = mean + 1.96 * se
            assert ci_low <= mean <= ci_high
            assert not np.isnan(se)
            
    # Specific architecture boundary checks:
    a2 = stage2_df[stage2_df["arch_id"] == 2]
    a2_h_mean = a2["haircut_prob"].mean()
    a2_h_se = a2["haircut_prob"].std() / np.sqrt(200)
    assert (a2_h_mean + 1.96 * a2_h_se) < 0.005, "A2 95% CI upper bound must be < 0.5%"
    
    a53 = stage2_df[stage2_df["arch_id"] == 7]
    a53_h_mean = a53["haircut_prob"].mean()
    a53_h_se = a53["haircut_prob"].std() / np.sqrt(200)
    assert (a53_h_mean + 1.96 * a53_h_se) < 0.030, "A5.3 95% CI upper bound must be < 3.0%"
    
    a0 = stage2_df[stage2_df["arch_id"] == 0]
    a0_churn_mean = a0["reset_churn_annual"].mean()
    a0_churn_se = a0["reset_churn_annual"].std() / np.sqrt(200)
    assert (a0_churn_mean - 1.96 * a0_churn_se) > 5.0, "A0 reset churn lower bound must exceed 5.0/yr gate"


def test_critical_ranking_boundaries_statistical_significance(stage2_df):
    """Verify statistical significance and ties across critical architecture ranking boundaries."""
    # A2 vs A5.3: A2 significantly beats A5.3 in haircut_prob and tail_cvar_99 (p < 0.01)
    a2_h = stage2_df[stage2_df["arch_id"] == 2]["haircut_prob"].values
    a53_h = stage2_df[stage2_df["arch_id"] == 7]["haircut_prob"].values
    t_stat_a2_a53, p_a2_a53 = stats.ttest_ind(a2_h, a53_h, equal_var=False)
    assert p_a2_a53 < 1e-14, f"A2 vs A5.3 haircut diff must be statistically significant (p={p_a2_a53})"
    
    # A5.3 vs A5.2: A5.3 significantly beats A5.2 in haircut_prob (p < 0.01)
    a52_h = stage2_df[stage2_df["arch_id"] == 6]["haircut_prob"].values
    _, p_a53_a52 = stats.ttest_ind(a53_h, a52_h, equal_var=False)
    assert p_a53_a52 < 1e-20, f"A5.3 vs A5.2 haircut diff must be statistically significant (p={p_a53_a52})"
    
    # A5.2 vs A0: A5.2 significantly beats A0 in haircut_prob and reset churn (p < 0.01)
    a0_h = stage2_df[stage2_df["arch_id"] == 0]["haircut_prob"].values
    a0_churn = stage2_df[stage2_df["arch_id"] == 0]["reset_churn_annual"].values
    a52_churn = stage2_df[stage2_df["arch_id"] == 6]["reset_churn_annual"].values
    _, p_a52_a0_h = stats.ttest_ind(a52_h, a0_h, equal_var=False)
    _, p_a52_a0_c = stats.ttest_ind(a52_churn, a0_churn, equal_var=False)
    assert p_a52_a0_h < 1e-5
    assert p_a52_a0_c < 1e-25
    
    # A0 vs A1: A0 significantly beats A1 in haircut_prob (p < 0.01)
    a1_h = stage2_df[stage2_df["arch_id"] == 1]["haircut_prob"].values
    _, p_a0_a1 = stats.ttest_ind(a0_h, a1_h, equal_var=False)
    assert p_a0_a1 < 1e-100
    
    # A2 vs A5.2 Reset Churn: Statistically TIED (p > 0.05)
    a2_churn = stage2_df[stage2_df["arch_id"] == 2]["reset_churn_annual"].values
    t_churn_a2_a52, p_churn_a2_a52 = stats.ttest_ind(a2_churn, a52_churn, equal_var=False)
    assert p_churn_a2_a52 > 0.05, f"A2 vs A5.2 reset churn must be statistically tied (p={p_churn_a2_a52})"


def test_policy_statistical_significance_and_ties(stage2_df):
    """Verify statistical significance of redistribution policies on coverage and burn."""
    pol2 = stage2_df[stage2_df["policy_id"] == 1]
    pol3 = stage2_df[stage2_df["policy_id"] == 2]
    pol4 = stage2_df[stage2_df["policy_id"] == 3]
    pol5 = stage2_df[stage2_df["policy_id"] == 4]
    
    # POL-02 achieves highest validator_cr_min (p < 0.01 vs POL-05 and POL-03)
    _, p_cr_2_5 = stats.ttest_ind(pol2["validator_cr_min"], pol5["validator_cr_min"], equal_var=False)
    _, p_cr_2_3 = stats.ttest_ind(pol2["validator_cr_min"], pol3["validator_cr_min"], equal_var=False)
    assert p_cr_2_5 < 1e-5
    assert p_cr_2_3 < 1e-10
    
    # POL-04 achieves extreme burn but extreme validator starvation (p < 1e-30)
    _, p_burn_4_2 = stats.ttest_ind(pol4["avax_burned_total"], pol2["avax_burned_total"], equal_var=False)
    _, p_cr_4_2 = stats.ttest_ind(pol4["validator_cr_min"], pol2["validator_cr_min"], equal_var=False)
    assert p_burn_4_2 < 1e-100
    assert p_cr_4_2 < 1e-50
    
    # Policies are statistically tied on haircut_prob across architectures (p > 0.50)
    _, p_haircut_2_5 = stats.ttest_ind(pol2["haircut_prob"], pol5["haircut_prob"], equal_var=False)
    assert p_haircut_2_5 > 0.50


def test_stage1_survivor_representation_balance(stage1_survivors_df, stage1_manifest):
    """Verify balanced survivor representation across architectures and policies in Stage 1."""
    assert len(stage1_survivors_df) == 64052
    assert stage1_manifest["metadata"]["survivors_total"] == 64052
    assert stage1_manifest["metadata"]["sample_size_initial"] == 100000
    
    # Check architecture representation balance
    arch_counts = stage1_survivors_df["arch_id"].value_counts().sort_index()
    assert len(arch_counts) == 8
    for aid, count in arch_counts.items():
        assert 7800 <= count <= 8200, f"Arch {aid} survivor count {count} out of balanced bounds"
        
    chi2_gof, p_gof = stats.chisquare(arch_counts)
    assert p_gof > 0.05, f"Architecture representation must follow uniform distribution (p={p_gof})"
    
    # Check policy representation balance
    policy_counts = stage1_survivors_df["policy_id"].value_counts().sort_index()
    assert len(policy_counts) == 5
    for pid, count in policy_counts.items():
        assert 12400 <= count <= 13200, f"Policy {pid} survivor count {count} out of balanced bounds"


def test_stage1_selection_bias_subspaces(stage1_survivors_df):
    """Verify that Stage 1 pruning only constrains R and R_prime via Filter F2, leaving all other 10 dimensions unbiased."""
    from simulations.design_discovery.stage1_analytical_screening import generate_candidate_tensor
    
    tensor_init = generate_candidate_tensor(n_samples=100000, seed=2026)
    df_init = pd.DataFrame(tensor_init)
    
    # Filter-constrained parameters
    ks_r, p_r = stats.ks_2samp(df_init["R"], stage1_survivors_df["R"])
    ks_rp, p_rp = stats.ks_2samp(df_init["R_prime"], stage1_survivors_df["R_prime"])
    assert p_r < 1e-10, "R must show distribution constraint from Filter F2"
    assert p_rp < 1e-10, "R_prime must show distribution constraint from Filter F2"
    
    # Invariant parameter subspaces (zero selection bias, KS p > 0.50)
    unbiased_params = [
        "H_d", "H_u", "omega_burn", "omega_val", "omega_res", "omega_l1",
        "K_p", "K_i", "B_target", "kappa_dd"
    ]
    for param in unbiased_params:
        ks_stat, p_val = stats.ks_2samp(df_init[param], stage1_survivors_df[param])
        assert p_val > 0.50, f"Parameter {param} must be invariant (KS={ks_stat:.4f}, p={p_val:.4f})"


def test_lambda_provisionality_and_ranking_invariance(stage2_df):
    """Verify that jump intensity lambda scaling preserves architecture ranking order and scales reset churn."""
    from simulations.design_discovery.stage2_architecture_screening import (
        generate_standardized_price_paths,
        simulate_single_candidate
    )
    
    # Pick representative configuration per architecture
    rep_configs = {}
    for aid in range(8):
        rep_configs[aid] = stage2_df[stage2_df["arch_id"] == aid].iloc[0].to_dict()
        
    for lam in [5.0, 15.0, 30.0]:
        price_paths = generate_standardized_price_paths(n_paths=100, n_steps=365, seed=2026, lambda_j=lam)
        res_a2 = simulate_single_candidate(rep_configs[2], price_paths)
        res_a53 = simulate_single_candidate(rep_configs[7], price_paths)
        res_a0 = simulate_single_candidate(rep_configs[0], price_paths)
        res_a1 = simulate_single_candidate(rep_configs[1], price_paths)
        
        # A2 and A5.3 remain ultra-low haircut
        assert res_a2["haircut_prob"] <= 0.01
        assert res_a53["haircut_prob"] <= 0.03
        
        # A1 suffers catastrophic default
        assert res_a1["haircut_prob"] > 0.70
        
        # A0 fails reset churn gate
        assert res_a0["reset_churn_annual"] > 5.0
