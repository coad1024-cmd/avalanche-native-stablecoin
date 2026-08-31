# Dispatch for Worker M2 (Generation 2)

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
   - Verify path generation isolation, environmental vs candidate-specific randomness streams, Kou SDE jump paths ($N=500$, $T=365$, $\Delta t=1.0$, seed=2026).
   - Run an independent bit-for-bit reproducibility test across representative sampled candidate runs under the identical seed (e.g., sample candidates across architectures and policies to verify bit-for-bit match max abs diff = 0.0 without executing a full 800,000-path brute force).
3. Check and reconcile cryptographic SHA-256 checksums across all on-disk parquet files and `RESEARCH_STATE.yaml`.

## Deliverables
- Working directory: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m2_gen2`
- Independent verification script: `/home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/execution/verify_stage2_crn_and_dataset.py`
- Automated test suite: `simulations/design_discovery/test_stage2_crn_dataset_integrity.py`
- Comprehensive report: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m2_gen2/m2_dataset_crn_report.md`
- `handoff.md` and `progress.md`.
