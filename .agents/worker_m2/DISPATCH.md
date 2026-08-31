# Dispatch for Worker M2

## Assigned Milestone
Milestone 2 (Requirement R2): Verify 1,600-Configuration Dataset Integrity & Genuine CRN Implementation.

## Mandatory Integrity Warning
> DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective
Execute a rigorous first-principles verification of `STAGE_2_RESULTS.parquet` and the Common Random Numbers (CRN) simulation pipeline:
1. Programmatically inspect `STAGE_2_RESULTS.parquet` and execution logs to verify:
   - Exact architecture (8) and policy (5) balance across all 40 candidate configurations (1,600 unique cells).
   - Candidate IDs, missing cells, duplicated cells, failed/silently discarded paths, and NaN/inf/null values.
2. Verify Common Random Numbers (CRN):
   - Inspect and audit seed management in `simulations/design_discovery/stage2_architecture_screening.py`.
   - Verify path generation isolation, environmental vs candidate-specific randomness streams, Kou SDE jump paths ($N=500$, $T=365$, $\Delta t=1.0$).
   - Run an independent bit-for-bit reproducibility test across candidate runs under the identical seed.
3. Check and reconcile cryptographic SHA-256 checksums across all on-disk parquet files and `RESEARCH_STATE.yaml`.

## Key Inputs & References
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md`
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md`
- `audit_artifacts/execution/STAGE_2_RESULTS.parquet`
- `audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet`
- `audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json`
- `simulations/design_discovery/stage2_architecture_screening.py`
- M1 Deliverable: `.agents/m1_worker_1/m1_reconciliation_deliverable.md`

## Deliverables
- Working directory: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m2`
- Independent verification script: `/home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/execution/verify_stage2_crn_and_dataset.py`
- Automated test suite: `simulations/design_discovery/test_stage2_crn_dataset_integrity.py`
- Comprehensive report: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m2/m2_dataset_crn_report.md`
- `handoff.md` and `progress.md`.

## 2026-08-31T07:34:21Z
You are Worker M2 for Milestone 2 (Requirement R2: Verify 1,600-Configuration Dataset Integrity & Genuine CRN Implementation).
Your working directory is: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m2
Read instructions in: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m2/DISPATCH.md
Read the authoritative user request: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md
Read PROJECT.md: /home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md

MANDATORY INTEGRITY WARNING:
> DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your mission:
1. Programmatically inspect `STAGE_2_RESULTS.parquet` and execution logs for 1,600-cell balance (8 archs x 5 policies x 40 configs), 0 NaNs/nulls/infs/dropped paths.
2. Programmatically verify CRN stream isolation and bit-for-bit reproducibility test under identical seed (2026).
3. Check all cryptographic hashes against RESEARCH_STATE.yaml.
4. Deliver:
   - Verification script: `audit_artifacts/execution/verify_stage2_crn_and_dataset.py`
   - Test suite: `simulations/design_discovery/test_stage2_crn_dataset_integrity.py`
   - Master report: `.agents/worker_m2/m2_dataset_crn_report.md`
   - `handoff.md` and `progress.md`. Send message to parent when finished.

