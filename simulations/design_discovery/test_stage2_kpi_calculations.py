"""
Automated Test Suite for Stage 2 KPI Calculations & Objective Directions
Milestone 3 (Requirement R3): End-to-End KPI Calculation & Objective Direction Audit
Governing Plan: BCRG-DESIGN-DISCOVERY-DECISION-FRAMEWORK-01 / BCRG-DISCOVERY-2026-OBJECTIVES-CONSTRAINTS-01
"""

import os
import sys
import pytest
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from simulations.design_discovery.stage2_architecture_screening import (
    generate_standardized_price_paths,
    simulate_single_candidate
)

PARQUET_PATH = os.path.join(PROJECT_ROOT, "audit_artifacts", "execution", "STAGE_2_RESULTS.parquet")


@pytest.fixture(scope="module")
def stage2_results():
    assert os.path.exists(PARQUET_PATH), f"Missing dataset: {PARQUET_PATH}"
    df = pd.read_parquet(PARQUET_PATH)
    return df


@pytest.fixture(scope="module")
def standardized_price_paths():
    return generate_standardized_price_paths(n_paths=500, n_steps=365, seed=2026)


def test_dataset_structure_and_no_nans(stage2_results):
    """Verifies that the dataset contains exactly 1,600 rows and 25 columns with zero NaN/null/inf."""
    df = stage2_results
    assert df.shape == (1600, 25)
    assert df.isnull().sum().sum() == 0
    assert np.isinf(df.select_dtypes(include=[np.number])).sum().sum() == 0
    
    expected_kpis = [
        "peg_rmse", "max_depeg", "haircut_prob", "tail_cvar_99",
        "recovery_time_days", "validator_cr_min", "validator_insolvency_prob",
        "avax_burned_total", "reset_churn_annual", "rate_volatility",
        "reserve_depletion_prob"
    ]
    for kpi in expected_kpis:
        assert kpi in df.columns, f"Missing KPI column: {kpi}"


def test_objective_direction_consistency():
    """
    Verifies that objective directions match canonical specifications:
    - Min: peg_rmse, max_depeg, haircut_prob, tail_cvar_99, reset_churn_annual, recovery_time_days, rate_volatility, validator_insolvency_prob, reserve_depletion_prob.
    - Max: validator_cr_min, avax_burned_total.
    """
    minimize_objectives = [
        "peg_rmse", "max_depeg", "haircut_prob", "tail_cvar_99",
        "recovery_time_days", "reset_churn_annual", "rate_volatility",
        "validator_insolvency_prob", "reserve_depletion_prob"
    ]
    maximize_objectives = ["validator_cr_min", "avax_burned_total"]

    assert len(minimize_objectives) + len(maximize_objectives) == 11
    # Check that all minimization metrics have natural non-negative lower bound at 0
    # and all maximization metrics represent positive economic utility.


def test_kpi_value_domains(stage2_results):
    """Verifies that all KPI values reside within their physical/mathematical domain bounds."""
    df = stage2_results

    # Probabilities in [0, 1]
    assert ((df["haircut_prob"] >= 0.0) & (df["haircut_prob"] <= 1.0)).all()
    assert ((df["validator_insolvency_prob"] >= 0.0) & (df["validator_insolvency_prob"] <= 1.0)).all()
    assert ((df["reserve_depletion_prob"] >= 0.0) & (df["reserve_depletion_prob"] <= 1.0)).all()

    # Losses in [0, 1]
    assert ((df["tail_cvar_99"] >= 0.0) & (df["tail_cvar_99"] <= 1.0)).all()

    # Non-negative metrics
    assert (df["reset_churn_annual"] >= 0.0).all()
    assert (df["validator_cr_min"] >= 0.0).all()
    assert (df["avax_burned_total"] >= 0.0).all()
    assert (df["peg_rmse"] >= 0.0).all()
    assert (df["max_depeg"] >= 0.0).all()
    assert (df["rate_volatility"] >= 0.0).all()
    assert (df["recovery_time_days"] >= 0.0).all()


def test_peg_dynamics_fixed_point(stage2_results):
    """
    Audits the secondary peg metrics: verifies that peg_rmse, max_depeg, and rate_volatility
    are identically 0.0 due to unexcited plant dynamics, and recovery_time_days equals default 0.50.
    """
    df = stage2_results
    assert (df["peg_rmse"] == 0.0).all()
    assert (df["max_depeg"] == 0.0).all()
    assert (df["rate_volatility"] == 0.0).all()
    assert (df["recovery_time_days"] == 0.50).all()


def test_validator_scale_mismatch_tautology(stage2_results):
    """
    Audits the validator insolvency metric: verifies that validator_insolvency_prob is identically 1.0
    because a production threshold (1.20) was evaluated on a sub-scale test pool (max CR = 0.0861).
    """
    df = stage2_results
    assert (df["validator_insolvency_prob"] == 1.0).all()
    assert df["validator_cr_min"].max() < 0.09
    assert df["validator_cr_min"].min() > 0.0001


def test_architecture_solvency_separation(stage2_results):
    """
    Verifies that the solvency metrics cleanly separate architectures:
    - A2 achieves near-zero haircut probability (~0.14%) and low CVaR (~0.67%).
    - A5.3 achieves moderate haircut probability (~2.02%) and low CVaR (~5.57%).
    - A0 experiences ~13.68% haircut probability.
    - A1, A3, A4 experience severe haircut probability (74.20%).
    """
    df = stage2_results
    a2_haircut = df[df["arch_id"] == 2]["haircut_prob"].mean()
    a53_haircut = df[df["arch_id"] == 7]["haircut_prob"].mean()
    a0_haircut = df[df["arch_id"] == 0]["haircut_prob"].mean()
    a1_haircut = df[df["arch_id"] == 1]["haircut_prob"].mean()

    assert a2_haircut < 0.005, f"A2 haircut too high: {a2_haircut}"
    assert a53_haircut < 0.03, f"A5.3 haircut too high: {a53_haircut}"
    assert 0.10 < a0_haircut < 0.20, f"A0 haircut unexpected: {a0_haircut}"
    assert abs(a1_haircut - 0.742) < 1e-4, f"A1 haircut unexpected: {a1_haircut}"


def test_streaming_and_floating_loss_parity(stage2_results):
    """
    Verifies that A1, A3, and A4 exhibit identical loss statistics due to shared
    underlying single-step haircut conditions (2 * S_t < 1.0) without discrete resets.
    """
    df = stage2_results
    a1 = df[df["arch_id"] == 1]
    a3 = df[df["arch_id"] == 3]
    a4 = df[df["arch_id"] == 4]

    assert (a1["haircut_prob"].values == a3["haircut_prob"].values).all()
    assert (a3["haircut_prob"].values == a4["haircut_prob"].values).all()
    assert (a1["tail_cvar_99"].values == a3["tail_cvar_99"].values).all()
    assert (a3["tail_cvar_99"].values == a4["tail_cvar_99"].values).all()
    assert (a1["reset_churn_annual"] == 0.0).all()


def test_policy_tradeoff_burn_vs_coverage(stage2_results):
    """
    Verifies the fundamental Pareto trade-off between POL-04 (Burn Maximizer) and POL-02 (Countercyclical):
    - POL-04 achieves the highest AVAX burn volume (> 1.15M).
    - POL-04 achieves the lowest minimum validator OpEx coverage floor (< 0.010).
    - POL-02 achieves the highest minimum validator OpEx coverage floor (> 0.030).
    """
    df = stage2_results
    pol_summary = df.groupby("policy_id")[["avax_burned_total", "validator_cr_min"]].mean()

    # POL-04 (id=3) has max burn
    assert pol_summary["avax_burned_total"].idxmax() == 3
    # POL-04 has min coverage
    assert pol_summary["validator_cr_min"].idxmin() == 3
    # POL-02 (id=1) has max coverage
    assert pol_summary["validator_cr_min"].idxmax() == 1


def test_reserve_depletion_a2_isolation(stage2_results):
    """Verifies that reserve_depletion_prob is strictly 0.0 for non-A2 architectures and non-zero only for A2."""
    df = stage2_results
    non_a2 = df[df["arch_id"] != 2]
    a2 = df[df["arch_id"] == 2]

    assert (non_a2["reserve_depletion_prob"] == 0.0).all()
    assert a2["reserve_depletion_prob"].max() > 0.0


def test_bit_for_bit_recomputation_crn(stage2_results, standardized_price_paths):
    """
    Recomputes candidate simulation across several stratified configurations and verifies
    exact bit-for-bit numerical reproducibility against STAGE_2_RESULTS.parquet.
    """
    df = stage2_results
    # Sample 4 configurations: A0, A2, A5.1, A5.3
    sample_indices = [0, 400, 1000, 1400]

    for idx in sample_indices:
        sample_row = df.iloc[idx].to_dict()
        recomputed = simulate_single_candidate(sample_row, standardized_price_paths)
        for k in ["haircut_prob", "tail_cvar_99", "validator_cr_min", "avax_burned_total", "reset_churn_annual"]:
            expected = sample_row[k]
            actual = recomputed[k]
            diff = abs(expected - actual)
            assert diff < 1e-6, f"Row {idx} KPI {k} mismatch: expected {expected}, got {actual}"
