# Dispatch for Worker M6

## Assigned Milestone
Milestone 6 (Requirement R6): Deliver Formal Adversarial Validation Report & Update Provenance.

## Mandatory Integrity Warning
> DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective
Synthesize the verified evidence, empirical statistics, mathematical proofs, and test results from Milestones M1 through M5 into the master deliverable:
1. Deliver the authoritative, comprehensive adversarial validation report at:
   `/home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/reports/STAGE_2_ADVERSARIAL_VALIDATION.md`
   The report MUST include all 17 required sections:
   - Section 1: Executive Summary & Epistemic Verdict
   - Section 2: Audit Charter, Scope & Boundary Conditions
   - Section 3: 3-Way Reconciliation: Specification vs Implementation vs Actual Outputs
   - Section 4: Dataset Integrity & Parquet Schema Verification (1,600 cells)
   - Section 5: Common Random Numbers (CRN) & Stochastic Stream Audit
   - Section 6: End-to-End KPI Mathematical Audit (Formula, Implementation, Parquet)
   - Section 7: Objective Direction & Sign Convention Verification
   - Section 8: Screening Gate Compliance Audit
   - Section 9: Formal Pareto Dominance & Trade-off Analysis (A0–A5.3)
   - Section 10: Redistribution Policy Screening Audit (POL-01–POL-05, Burn vs OpEx)
   - Section 11: Monte Carlo Sampling Error & Confidence Bounds (500 Paths)
   - Section 12: Stage-1 Analytical Pruning Selection Bias Audit
   - Section 13: Sensitivity to Provisional Jump Intensity ($\lambda = 15.00\text{ yr}^{-1}$)
   - Section 14: Error, Anomaly & Nuance Register
   - Section 15: Master Epistemic Classification Table (assigning exactly one of [`VERIFIED`, `CONDITIONALLY SUPPORTED`, `SCREENING-ONLY`, `STATISTICALLY INCONCLUSIVE`, `UNSUPPORTED`, `CONTRADICTED`, `INVALID`] to each architecture and policy)
   - Section 16: Provenance, Metadata & Environment Cryptographic Manifest (git SHA, Python/dependency versions, dataset SHA-256 hashes, random seeds)
   - Section 17: Final Formal Gate Recommendation (`PROCEED TO STAGE 3` with conditionality on A2 / A5.3 / A5.2 and POL-02 / POL-03 / POL-05).
2. Update `RESEARCH_STATE.yaml`:
   - Record the audit completion status (`audit_status: "VERIFIED"`), commit hash, dataset hashes, and next stage (`stage3_global_sensitivity_analysis`) under `stage2_architecture_screening`.
   - STRICT CONSTRAINT: Do NOT alter any canonical economic parameters or equations.
3. Write `simulations/design_discovery/test_stage2_final_report_validation.py` to verify that all 17 sections, file references, dataset hashes, and gate decisions in the report are complete and parseable.

## Key Inputs & Verified Deliverables
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md`
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md`
- M1 Deliverables: `.agents/m1_worker_1/m1_reconciliation_deliverable.md`
- M2 Deliverables: `.agents/worker_m2_gen2/m2_dataset_crn_report.md`
- M3 Deliverables: `.agents/worker_m3/m3_kpi_math_report.md`
- M4 Deliverables: `.agents/worker_m4/m4_dominance_policy_report.md`
- M5 Deliverables: `.agents/worker_m5/m5_statistical_bias_report.md`
- `RESEARCH_STATE.yaml`

## Working Directory
`/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m6`
