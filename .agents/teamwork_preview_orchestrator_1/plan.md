# Execution Plan: Stage 2 Adversarial Validation Audit

## Objective
Execute an independent first-principles adversarial validation audit of the completed Stage 2 Architecture & Redistribution Policy Screening in `coad1024-cmd/avalanche-native-stablecoin` on branch `research/first-principles-adversarial-audit`.

## Architecture of the Audit Team
1. **Phase 0: Survey & Discovery (Top-Level Orchestrator)**
   - Spawn Explorers to survey:
     - Explorer 1 (Spec & Ladder): `audit_artifacts/design_discovery/` specs, Stage 1 manifests, Stage 2 manifests, historical report.
     - Explorer 2 (Codebase & Sim Engine): `src/` simulation engine, runner scripts, KPI calculation modules, statistical routines.
     - Explorer 3 (Data & Artifacts): `audit_artifacts/execution/` parquet files, manifests, logs, environment.
2. **Phase 1: Milestone M1 — Specification Reconstruction & 3-Way Reconciliation (R1)**
   - Reconstruct 8 architectures, 5 policies, 40 configurations (1,600 cells), 500 MC paths, screening gates, KPI definitions.
   - Perform 3-way reconciliation: Specification vs Implementation vs Actual Outputs.
3. **Phase 2: Milestone M2 — Dataset Integrity & Genuine CRN Implementation (R2)**
   - Programmatically inspect `STAGE_2_RESULTS.parquet` (1,600 cells, NaN/inf checks, candidate balance).
   - Verify Common Random Numbers (seed management, randomness isolation, reproducibility test).
4. **Phase 3: Milestone M3 — End-to-End KPI Calculation & Objective Directions (R3)**
   - Mathematical formulation $\to$ code implementation $\to$ parquet storage $\to$ report synthesis.
   - Verify Peg RMSE, reset count, validator coverage, solvency survival probability, subsidy, burn, yield, reserves.
   - Audit for algebraic tautologies, look-ahead bias, scaling/annualization, path averaging, inverted directions.
5. **Phase 4: Milestone M4 — Architecture & Policy Classification Audit (R4)**
   - Disentangle Screening Gate failure from Mathematical Pareto Dominance.
   - Formally audit A0-A5.3 and POL-01 to POL-05.
6. **Phase 5: Milestone M5 — Sampling Error, Selection Bias, & Lambda Provisionality (R5)**
   - MC standard errors & 95% CIs across 500 paths.
   - Audit Stage-1 selection bias & provisional $\lambda=15.00\text{ yr}^{-1}$ sensitivity.
7. **Phase 6: Milestone M6 — Deliver Formal Adversarial Validation Report & Provenance (R6)**
   - Write comprehensive report at `audit_artifacts/reports/STAGE_2_ADVERSARIAL_VALIDATION.md` (all 17 required sections).
   - Update `RESEARCH_STATE.yaml` with audit state, commit hash, dataset hashes, and explicit gate decision (`PROCEED TO STAGE 3` or `HOLD STAGE 3`).

## Gating and Verification Strategy
- Every milestone executes: Explorer(s) -> Worker -> Reviewer(s) -> Challenger(s) -> Forensic Auditor (`teamwork_preview_auditor`).
- Strict AND gate: All must pass with zero integrity violations.
