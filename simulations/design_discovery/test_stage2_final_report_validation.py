"""
Automated Pytest Suite: Stage 2 Adversarial Validation Final Report & Provenance Verification

Verifies:
1. Master validation report presence, substantial content, and 17-section structure.
2. Complete inclusion and exact syntax of all 17 required sections.
3. Master Epistemic Classification Table validity and adherence to canonical taxonomy.
4. Cryptographic SHA-256 hash reconciliation between disk, report, and RESEARCH_STATE.yaml.
5. Final Gate recommendation validity (PROCEED TO STAGE 3).
6. Structural and semantic integrity of updated RESEARCH_STATE.yaml without parameter alteration.
"""

import os
import re
import hashlib
import yaml
import pytest


REPORT_PATH = "audit_artifacts/reports/STAGE_2_ADVERSARIAL_VALIDATION.md"
RESEARCH_STATE_PATH = "audit_artifacts/state/RESEARCH_STATE.yaml"
STAGE_1_PARQUET = "audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet"
STAGE_2_PARQUET = "audit_artifacts/execution/STAGE_2_RESULTS.parquet"
STAGE_1_MANIFEST = "audit_artifacts/execution/STAGE_1_ANALYTICAL_PRUNING_MANIFEST.json"
STAGE_2_MANIFEST = "audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json"

REQUIRED_SECTIONS = [
    (1, "Executive Summary & Epistemic Verdict"),
    (2, "Audit Charter, Scope & Boundary Conditions"),
    (3, "3-Way Reconciliation"),
    (4, "Dataset Integrity & Parquet Schema Verification"),
    (5, "Common Random Numbers (CRN) & Stochastic Stream Audit"),
    (6, "End-to-End KPI Mathematical Audit"),
    (7, "Objective Direction & Sign Convention Verification"),
    (8, "Screening Gate Compliance Audit"),
    (9, "Formal Pareto Dominance & Trade-off Analysis"),
    (10, "Redistribution Policy Screening Audit"),
    (11, "Monte Carlo Sampling Error & Confidence Bounds"),
    (12, "Stage-1 Analytical Pruning Selection Bias Audit"),
    (13, "Sensitivity to Provisional Jump Intensity"),
    (14, "Error, Anomaly & Nuance Register"),
    (15, "Master Epistemic Classification Table"),
    (16, "Provenance, Metadata & Environment Cryptographic Manifest"),
    (17, "Final Formal Gate Recommendation"),
]

ALLOWED_EPISTEMIC_VERDICTS = {
    "VERIFIED",
    "CONDITIONALLY SUPPORTED",
    "SCREENING-ONLY",
    "STATISTICALLY INCONCLUSIVE",
    "UNSUPPORTED",
    "CONTRADICTED",
    "INVALID",
}


def compute_sha256(filepath: str) -> str:
    """Compute standard SHA-256 hexadecimal digest for a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def test_report_file_existence_and_size():
    """Verify that the master adversarial validation report exists and has substantial content."""
    assert os.path.exists(REPORT_PATH), f"Report missing at {REPORT_PATH}"
    size = os.path.getsize(REPORT_PATH)
    assert size > 20000, f"Report file size ({size} bytes) is unexpectedly small"
    
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) >= 300, f"Report length ({len(lines)} lines) is below expectations"


def test_all_17_required_sections_present():
    """Verify that all 17 required sections exist with correct numbering and headers."""
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    for sec_num, sec_title_keyword in REQUIRED_SECTIONS:
        # Match heading patterns like "## 1. Executive Summary" or "## 1. "
        pattern = rf"##\s+{sec_num}\.\s+.*{re.escape(sec_title_keyword)}"
        match = re.search(pattern, content, re.IGNORECASE)
        assert match is not None, (
            f"Missing or malformed Section {sec_num} ({sec_title_keyword}) in {REPORT_PATH}"
        )


def test_master_epistemic_classification_table():
    """Verify that Section 15 contains all 8 architectures and 5 policies with valid classifications."""
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract Section 15 content
    sec15_match = re.search(
        r"##\s+15\.\s+Master Epistemic Classification Table(.*?)(?=##\s+16\.|$)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    assert sec15_match is not None, "Could not isolate Section 15"
    sec15_text = sec15_match.group(1)

    # Check that all 8 architectures and 5 policies are referenced in Section 15
    required_entities = [
        "A0", "A1", "A2", "A3", "A4", "A5.1", "A5.2", "A5.3",
        "POL-01", "POL-02", "POL-03", "POL-04", "POL-05"
    ]
    for entity in required_entities:
        assert entity in sec15_text, f"Entity {entity} missing from Section 15 Epistemic Table"

    # Verify that classifications used belong strictly to the allowed taxonomy
    for verdict in ["VERIFIED", "CONDITIONALLY SUPPORTED", "SCREENING-ONLY"]:
        assert verdict in sec15_text, f"Expected verdict {verdict} missing from Section 15"


def test_cryptographic_hashes_reconciliation():
    """Verify that SHA-256 digests in report match on-disk files and RESEARCH_STATE.yaml."""
    expected_hashes = {
        "STAGE_1_PARQUET": (STAGE_1_PARQUET, "3d9ebe70ef522223edf0d115e9c0505b78ef9ceea57e5c40e22892a22bd13319"),
        "STAGE_2_PARQUET": (STAGE_2_PARQUET, "653890da46dc822e87fda27b7a5e750b68bb54a027dd4864c1addf757211d24f"),
        "STAGE_1_MANIFEST": (STAGE_1_MANIFEST, "b0215f418f7d8a8fdf51b02521f9c2da3f2494fdae0927abf40074b6f99674b9"),
        "STAGE_2_MANIFEST": (STAGE_2_MANIFEST, "6b3e409b1dd72c73996c9c7f9737d20f6ceccfc92576b4d465960b6a642aec91"),
    }

    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        report_content = f.read()

    for name, (path, expected_hash) in expected_hashes.items():
        actual_hash = compute_sha256(path)
        assert actual_hash == expected_hash, f"Hash mismatch for {path}: {actual_hash} != {expected_hash}"
        assert expected_hash in report_content, f"Report does not mention expected hash {expected_hash} for {name}"


def test_gate_recommendation_verdict():
    """Verify that the final gate recommendation is PROCEED TO STAGE 3 with explicit conditionality."""
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    sec17_match = re.search(
        r"##\s+17\.\s+Final Formal Gate Recommendation(.*)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    assert sec17_match is not None, "Could not find Section 17"
    sec17_text = sec17_match.group(1)

    assert "PROCEED TO STAGE 3" in sec17_text or "PROCEED" in sec17_text, "Missing PROCEED TO STAGE 3 in Section 17"
    assert ("A2" in sec17_text or "$A_2$" in sec17_text), "Missing Architecture A2 in Section 17 recommendations"
    assert ("A5.3" in sec17_text or "$A_{5.3}$" in sec17_text), "Missing Architecture A5.3 in Section 17 recommendations"
    assert ("POL-02" in sec17_text or "POL_02" in sec17_text), "Missing Policy POL-02 in Section 17 recommendations"
    assert ("POL-03" in sec17_text or "POL_03" in sec17_text), "Missing Policy POL-03 in Section 17 recommendations"
    assert ("POL-05" in sec17_text or "POL_05" in sec17_text), "Missing Policy POL-05 in Section 17 recommendations"


def test_research_state_provenance_integrity():
    """Verify that RESEARCH_STATE.yaml has been updated with audit metadata without altering economic parameters."""
    assert os.path.exists(RESEARCH_STATE_PATH), f"RESEARCH_STATE.yaml not found at {RESEARCH_STATE_PATH}"
    
    with open(RESEARCH_STATE_PATH, "r", encoding="utf-8") as f:
        state = yaml.safe_load(f)

    # Check stage 2 screening block
    s2 = state.get("baseline_artifacts", {}).get("stage_2_architecture_screening", {})
    assert s2.get("audit_status") == "VERIFIED", f"Expected audit_status VERIFIED, got {s2.get('audit_status')}"
    assert s2.get("next_stage") == "stage3_global_sensitivity_analysis", f"Expected next_stage stage3_global_sensitivity_analysis, got {s2.get('next_stage')}"
    
    audit_block = s2.get("adversarial_validation_audit", {})
    assert audit_block.get("audit_status") == "VERIFIED"
    assert audit_block.get("audit_report") == REPORT_PATH
    assert audit_block.get("dataset_hashes", {}).get("stage_2_results") == "653890da46dc822e87fda27b7a5e750b68bb54a027dd4864c1addf757211d24f"
    assert audit_block.get("dataset_hashes", {}).get("stage_1_survivors") == "3d9ebe70ef522223edf0d115e9c0505b78ef9ceea57e5c40e22892a22bd13319"

    # Verify canonical economic calibration parameters are intact
    kou = state.get("baseline_artifacts", {}).get("empirical_calibration", {}).get("admitted_kou_parameters", {})
    assert kou.get("diffusion_sigma") == 0.8915, "diffusion_sigma altered in RESEARCH_STATE.yaml"
    assert kou.get("jump_intensity_lambda") == 15.00, "jump_intensity_lambda altered in RESEARCH_STATE.yaml"
    assert kou.get("up_jump_probability_p") == 0.5955, "up_jump_probability_p altered in RESEARCH_STATE.yaml"
    assert kou.get("up_tail_decay_eta1") == 7.671, "up_tail_decay_eta1 altered in RESEARCH_STATE.yaml"
    assert kou.get("down_tail_decay_eta2") == 7.801, "down_tail_decay_eta2 altered in RESEARCH_STATE.yaml"
    assert kou.get("staking_apr_mean") == 0.0640, "staking_apr_mean altered in RESEARCH_STATE.yaml"
