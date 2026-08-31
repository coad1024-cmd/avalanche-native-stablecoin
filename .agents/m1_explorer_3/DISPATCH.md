# Dispatch for Milestone 1 Explorer 3

## Assigned Milestone
Milestone 1 (Requirement R1): Reconstruct Experiment Specification & 3-Way Reconciliation — Discrepancies, Nuances & Anomaly Register.

## Objective
Audit and document every parameter, gate, formula, or configuration discrepancy between theoretical specification, Python implementation, and parquet output.

## Key References
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md`
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md`
- `audit_artifacts/design_discovery/EXPERIMENTAL_LADDER.md`
- `audit_artifacts/design_discovery/OBJECTIVES_AND_CONSTRAINTS.md`
- `audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json`
- `simulations/design_discovery/stage2_architecture_screening.py`
- `audit_artifacts/reports/STAGE_2_ARCHITECTURE_SCREENING.md`
- Survey outputs in `.agents/teamwork_preview_explorer_survey_1/survey_specs.md`, `.agents/teamwork_preview_explorer_survey_2/survey_codebase.md`, `.agents/teamwork_preview_explorer_survey_3/survey_data.md`

## Focus Area for Explorer 3
- Enumerate and explain all discrepancies:
  1. Secondary AMM peg SDE degeneracy (peg RMSE = 0.0).
  2. Validator coverage sub-scale factor (1M sAVAX test vault vs 1,450 validator network OpEx).
  3. A1/A3/A4 deficit condition check against 1.0 vs $V_A$.
  4. A2 upward reset omission in simulation loop.
  5. A5.3 synthetic basket asset dynamics ($20\%$ basket volatility assumption).
  6. Any other implementation vs specification divergences.

## Output Requirements
- Working directory: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/m1_explorer_3`
- Write detailed investigation report to `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/m1_explorer_3/discrepancies_report.md`
- Write `handoff.md` and `progress.md`.
