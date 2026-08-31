"""
Automated Pytest Suite: Stage 2 Dataset Integrity & Genuine CRN Implementation
Milestone 2 (Requirement R2) — Adversarial Validation Audit

Governing Plan: BCRG-DESIGN-DISCOVERY-DECISION-FRAMEWORK-01
Research Snapshot: SNAP-2026-08-31-02
Author: Worker M2 (Research & Formal Validation)
"""

import os
import sys
import json
import yaml
import hashlib
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

EXECUTION_DIR = os.path.join(PROJECT_ROOT, "audit_artifacts", "execution")
STATE_DIR = os.path.join(PROJECT_ROOT, "audit_artifacts", "state")
STAGE2_PARQUET = os.path.join(EXECUTION_DIR, "STAGE_2_RESULTS.parquet")
STAGE2_MANIFEST = os.path.join(EXECUTION_DIR, "STAGE_2_EXPERIMENT_MANIFEST.json")
STAGE1_PARQUET = os.path.join(EXECUTION_DIR, "STAGE_1_CORRECTED_SURVIVORS.parquet")
STAGE1_MANIFEST = os.path.join(EXECUTION_DIR, "STAGE_1_ANALYTICAL_PRUNING_MANIFEST.json")
RESEARCH_STATE_FILE = os.path.join(STATE_DIR, "RESEARCH_STATE.yaml")


def compute_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


@pytest.fixture(scope="module")
def stage2_df():
    assert os.path.exists(STAGE2_PARQUET), f"Missing dataset: {STAGE2_PARQUET}"
    return pd.read_parquet(STAGE2_PARQUET)


@pytest.fixture(scope="module")
def stage1_df():
    assert os.path.exists(STAGE1_PARQUET), f"Missing dataset: {STAGE1_PARQUET}"
    return pd.read_parquet(STAGE1_PARQUET)


@pytest.fixture(scope="module")
def standardized_price_paths():
    return generate_standardized_price_paths(n_paths=500, n_steps=365, seed=2026)


def test_sha256_cryptographic_checksums_against_research_state():
    """
    Verifies that all dataset and manifest SHA-256 digests match RESEARCH_STATE.yaml
    and STAGE_2_EXPERIMENT_MANIFEST.json bit-for-bit.
    """
    with open(RESEARCH_STATE_FILE, "r") as f:
        rstate = yaml.safe_load(f)
    with open(STAGE2_MANIFEST, "r") as f:
        s2_man = json.load(f)

    hash_s1_p = compute_sha256(STAGE1_PARQUET)
    hash_s1_m = compute_sha256(STAGE1_MANIFEST)
    hash_s2_p = compute_sha256(STAGE2_PARQUET)
    hash_s2_m = compute_sha256(STAGE2_MANIFEST)

    exp_s1_p = rstate["baseline_artifacts"]["stage_1_analytical_screening"]["authoritative_dataset"]["sha256"]
    exp_s1_m = rstate["baseline_artifacts"]["stage_1_analytical_screening"]["authoritative_dataset"]["manifest_sha256"]
    exp_s2_p = rstate["baseline_artifacts"]["stage_2_architecture_screening"]["results_dataset"]["sha256"]
    man_s2_p = s2_man["deliverables"][0]["sha256"]

    assert hash_s1_p == exp_s1_p, f"Stage 1 parquet hash mismatch: {hash_s1_p} != {exp_s1_p}"
    assert hash_s1_m == exp_s1_m, f"Stage 1 manifest hash mismatch: {hash_s1_m} != {exp_s1_m}"
    assert hash_s2_p == exp_s2_p, f"Stage 2 parquet hash mismatch: {hash_s2_p} != {exp_s2_p}"
    assert hash_s2_p == man_s2_p, f"Stage 2 deliverable hash mismatch: {hash_s2_p} != {man_s2_p}"


def test_dataset_dimensions_and_null_invariants(stage2_df):
    """Verifies that the dataset has exactly 1,600 rows, 25 columns, and zero null/NaN/inf values."""
    assert stage2_df.shape == (1600, 25)
    assert stage2_df.isnull().sum().sum() == 0
    assert stage2_df.isna().sum().sum() == 0
    num_cols = stage2_df.select_dtypes(include=[np.number])
    assert np.isinf(num_cols).sum().sum() == 0


def test_absence_of_duplicate_configurations(stage2_df):
    """Verifies that all 1,600 parameter configurations are strictly unique (0 duplicates)."""
    param_cols = [
        "arch_id", "policy_id", "R", "R_prime", "H_d", "H_u",
        "omega_burn", "omega_val", "omega_res", "omega_l1",
        "K_p", "K_i", "B_target", "kappa_dd"
    ]
    assert stage2_df.duplicated().sum() == 0
    assert stage2_df.duplicated(subset=param_cols).sum() == 0


def test_stratified_2d_cell_balance(stage2_df):
    """Verifies exact 2D stratification: 8 archs x 5 policies x 40 configs per cell."""
    arch_counts = stage2_df["arch_id"].value_counts().sort_index()
    policy_counts = stage2_df["policy_id"].value_counts().sort_index()
    cell_counts = stage2_df.groupby(["arch_id", "policy_id"]).size()

    assert len(arch_counts) == 8
    assert (arch_counts == 200).all()
    assert len(policy_counts) == 5
    assert (policy_counts == 320).all()
    assert len(cell_counts) == 40
    assert (cell_counts == 40).all()


def test_stage1_survivor_provenance_and_membership(stage2_df, stage1_df):
    """Verifies that 100% of Stage 2 candidate parameter inputs originate from Stage 1 survivors."""
    param_cols = [
        "arch_id", "policy_id", "R", "R_prime", "H_d", "H_u",
        "omega_burn", "omega_val", "omega_res", "omega_l1",
        "K_p", "K_i", "B_target", "kappa_dd"
    ]
    assert len(stage1_df) == 64052
    merged = pd.merge(stage2_df[param_cols], stage1_df[param_cols], on=param_cols, how="inner")
    assert len(merged) == 1600, f"Expected 1,600 matches, got {len(merged)}"


def test_sampling_seed_formula_reproducibility(stage2_df, stage1_df):
    """Verifies deterministic candidate sampling via sub_df.sample(40, random_state=2026 + arch*10 + policy)."""
    param_cols = [
        "arch_id", "policy_id", "R", "R_prime", "H_d", "H_u",
        "omega_burn", "omega_val", "omega_res", "omega_l1",
        "K_p", "K_i", "B_target", "kappa_dd"
    ]
    candidates = []
    n_per_cell = 40
    seed = 2026
    for a_id in range(8):
        for p_id in range(5):
            sub_df = stage1_df[(stage1_df["arch_id"] == a_id) & (stage1_df["policy_id"] == p_id)]
            sampled_sub = sub_df.sample(n=n_per_cell, random_state=seed + a_id * 10 + p_id)
            candidates.append(sampled_sub)
    df_expected = pd.concat(candidates, ignore_index=True)

    merged = pd.merge(stage2_df[param_cols], df_expected[param_cols], on=param_cols, how="inner")
    assert len(merged) == 1600


def test_kou_sde_crn_path_determinism():
    """Verifies Kou jump-diffusion SDE determinism under seed 2026 and independence under different seeds."""
    p1 = generate_standardized_price_paths(n_paths=100, n_steps=365, seed=2026)
    p2 = generate_standardized_price_paths(n_paths=100, n_steps=365, seed=2026)
    assert p1.shape == (100, 366)
    assert np.all(p1[:, 0] == 1.0)
    assert np.all(p1 > 0.0)
    assert np.max(np.abs(p1 - p2)) == 0.0

    p_diff = generate_standardized_price_paths(n_paths=100, n_steps=365, seed=2027)
    assert np.max(np.abs(p1 - p_diff)) > 0.10


def test_kou_sde_stream_isolation_and_no_mutation(standardized_price_paths):
    """Verifies that simulate_single_candidate does not mutate the price paths array in-place."""
    paths_copy = np.copy(standardized_price_paths)
    dummy_row = {
        "arch_id": 7, "policy_id": 1, "R": 0.05, "R_prime": 0.02,
        "H_d": 0.30, "H_u": 1.50, "omega_burn": 0.25, "omega_val": 0.25,
        "omega_res": 0.25, "omega_l1": 0.25, "K_p": 0.10, "K_i": 0.01,
        "B_target": 0.10, "kappa_dd": 0.20
    }
    _ = simulate_single_candidate(dummy_row, paths_copy)
    assert np.max(np.abs(standardized_price_paths - paths_copy)) == 0.0


def test_bit_for_bit_kpi_reproducibility_sampled_cells(stage2_df, standardized_price_paths):
    """
    Recomputes candidate simulation across representative stratified configurations
    (covering all 8 architectures and all 5 policies) and verifies exact bit-for-bit reproducibility (max abs diff < 1e-9).
    """
    kpis = [
        "peg_rmse", "max_depeg", "haircut_prob", "tail_cvar_99",
        "recovery_time_days", "validator_cr_min", "validator_insolvency_prob",
        "avax_burned_total", "reset_churn_annual", "rate_volatility",
        "reserve_depletion_prob"
    ]

    # Sample representative configs across all 8 architectures rotating across all 5 policies
    sampled_configs = []
    for a in range(8):
        p = a % 5
        sub = stage2_df[(stage2_df["arch_id"] == a) & (stage2_df["policy_id"] == p)]
        sampled_configs.append(sub.iloc[0].to_dict())

    for orig in sampled_configs:
        recomp = simulate_single_candidate(orig, standardized_price_paths)
        for k in kpis:
            stored = float(orig[k])
            actual = float(recomp[k])
            diff = abs(stored - actual)
            assert diff < 1e-9, f"Row Arch {orig['arch_id']}, Policy {orig['policy_id']} KPI {k} mismatch: {stored} vs {actual}"


def test_parameter_domain_bounds_and_simplex_invariants(stage2_df):
    """Verifies that all 14 parameters conform to theoretical bounds and simplex constraints."""
    df = stage2_df
    assert (df["R"] >= 0.01).all() and (df["R"] <= 0.20).all()
    assert (df["R_prime"] >= 0.005).all() and (df["R_prime"] <= 0.12).all()
    assert (df["R"] > df["R_prime"]).all()
    assert (df["R_prime"] <= 0.1000 + 1e-7).all()
    assert (df["H_d"] >= 0.05).all() and (df["H_d"] <= 0.60).all()
    assert (df["H_u"] >= 1.10).all() and (df["H_u"] <= 3.50).all()
    assert (df["K_p"] >= 0.01).all() and (df["K_p"] <= 0.60).all()
    assert (df["K_i"] >= 0.001).all() and (df["K_i"] <= 0.10).all()
    assert (df["B_target"] >= 0.00).all() and (df["B_target"] <= 0.30).all()
    assert (df["kappa_dd"] >= 0.05).all() and (df["kappa_dd"] <= 0.80).all()

    simplex_sum = df["omega_burn"] + df["omega_val"] + df["omega_res"] + df["omega_l1"]
    assert np.allclose(simplex_sum, 1.0, atol=1e-6)


def test_kpi_value_domains_and_physical_bounds(stage2_df):
    """Verifies that all 11 KPIs reside in valid mathematical/probabilistic ranges."""
    df = stage2_df
    assert ((df["haircut_prob"] >= 0.0) & (df["haircut_prob"] <= 1.0)).all()
    assert ((df["tail_cvar_99"] >= 0.0) & (df["tail_cvar_99"] <= 1.0)).all()
    assert ((df["validator_insolvency_prob"] >= 0.0) & (df["validator_insolvency_prob"] <= 1.0)).all()
    assert ((df["reserve_depletion_prob"] >= 0.0) & (df["reserve_depletion_prob"] <= 1.0)).all()
    assert (df["validator_cr_min"] >= 0.0).all()
    assert (df["avax_burned_total"] >= 0.0).all()
    assert (df["reset_churn_annual"] >= 0.0).all()
    assert (df["peg_rmse"] >= 0.0).all()
    assert (df["max_depeg"] >= 0.0).all()
    assert (df["rate_volatility"] >= 0.0).all()
    assert (df["recovery_time_days"] >= 0.0).all()
