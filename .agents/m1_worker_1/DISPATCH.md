# Dispatch for Milestone 1 Worker

## Assigned Milestone
Milestone 1 (Requirement R1): Reconstruct Experiment Specification & 3-Way Reconciliation.

## Mandatory Integrity Warning
> DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective
Implement and verify the authoritative 3-way reconciliation script and artifacts that reconcile Specification vs Implementation vs Parquet Data across all 8 architectures ($A_0$–$A_{5.3}$), 5 policies ($\text{POL-01}$–$\text{POL-05}$), 40 configurations per cell (1,600 cells), 4 screening gates, and 11 KPIs.

## Key Inputs & References
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md`
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md`
- Explorer reports:
  - `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/m1_explorer_1/reconciliation_report.md`
  - `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/m1_explorer_2/gates_and_mechanisms_report.md`
  - `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/m1_explorer_3/discrepancies_report.md`
- Codebase and data:
  - `simulations/design_discovery/stage2_architecture_screening.py`
  - `audit_artifacts/execution/STAGE_2_RESULTS.parquet`
  - `audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json`

## Tasks
1. Execute an independent verification script `audit_artifacts/execution/verify_stage2_3way_reconciliation.py` (or verify via Python execution) that programmatically checks all parameters, dimensions, gate compliance rates, Pareto non-dominated sets (178 non-dominated candidates), and discrepancy registers.
2. Compile and publish the consolidated 3-way reconciliation tables in markdown format ready for incorporation into the final validation report.
3. Verify that all 8 architectures and 5 policies are formally mapped with exact mathematical definitions, code references, and empirical parquet values.
4. Record build/test verification results in `handoff.md`.

## Working Directory
`/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/m1_worker_1`
