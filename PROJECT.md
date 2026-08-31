# Project: Stage 2 Architecture & Redistribution Policy Screening Adversarial Validation Audit

## Architecture
- **Audit Domain**: Independent first-principles adversarial validation audit of Stage 2 Architecture & Redistribution Policy Screening in `coad1024-cmd/avalanche-native-stablecoin`.
- **Target Branch**: `research/first-principles-adversarial-audit`.
- **Core Invariants & Rules**:
  - Zero tolerance for prior agent unverified claims (SOURCE-CRITICALITY RULE).
  - Strict separation of Screening Gate Failure vs. Mathematical Pareto Dominance.
  - Strict preservation of historical outputs (`STAGE_2_RESULTS.parquet`, `STAGE_2_EXPERIMENT_MANIFEST.json`).
  - Strict non-modification of canonical economic parameters.
  - Verification across 1,600 configuration cells ($8 \times 5 \times 40$), 500 Kou SDE CRN paths, and 11 KPI metrics.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Specification Reconstruction & 3-Way Reconciliation | Map experimental ladder, manifests, code, Stage 1 inputs; reconcile Spec vs Impl vs Data | M1 | R1 |
| 2 | Parameter & Gate Discrepancy Matrix | Enumerate every discrepancy across gates, formulas, and parameters | M1 | R1 |
| 3 | 1,600-Configuration Dataset Integrity | Programmatic verification of 1,600 cells ($8 \times 5 \times 40$), 0 NaN/inf/null/dropped | M2 | R2 |
| 4 | CRN & Seed Stream Verification | Verify Kou SDE path isolation, randomness streams, bit-for-bit reproducibility | M2 | R2 |
| 5 | KPI Mathematical & Implementation Audit | Line-by-line verification of Peg RMSE, Reset Churn, Coverage, Solvency, Subsidy, Burn, Yield, Reserves | M3 | R3 |
| 6 | Objective Direction & Bias Check | Verify minimize/maximize alignments, look-ahead bias, scaling/annualization, path aggregation | M3 | R3 |
| 7 | Architecture Dominance Formal Proofs/Refutations | Audit A0–A5.3, proving gate failure vs Pareto dominance for all rejected architectures | M4 | R4 |
| 8 | Redistribution Policy Trade-Off Audit | Audit POL-01–POL-05, evaluating POL-04 frontier extreme vs unmitigated failure | M4 | R4 |
| 9 | Monte Carlo Sampling Error & Uncertainty Bounds | Compute MC standard errors & 95% CIs across 500 paths to establish statistical significance | M5 | R5 |
| 10 | Stage-1 Analytical Pruning Selection Bias | Audit survivor distributions from $N_0=100,000 \to 64,052$ for subspace elimination bias | M5 | R5 |
| 11 | Provisional Lambda Sensitivity Evaluation | Assess architecture/policy ranking dependence on $\lambda = 15.00\text{ yr}^{-1}$ | M5 | R5 |
| 12 | 17-Section Formal Validation Report Delivery | Synthesize and write `audit_artifacts/reports/STAGE_2_ADVERSARIAL_VALIDATION.md` | M6 | R6 |
| 13 | Epistemic Classification Table | Assign formal epistemic status to every architecture and policy outcome | M6 | R6 |
| 14 | Research State & Cryptographic Provenance Update | Update `RESEARCH_STATE.yaml` with commit, hashes, and final gate verdict | M6 | R6 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Reconstruct Experiment Specification & 3-Way Reconciliation (R1) | Reconstruct 8 architectures, 5 policies, 40 configs, 500 MC paths; 3-way reconciliation (Spec vs Impl vs Data) | None | DONE |
| 2 | Dataset Integrity & Genuine CRN Verification (R2) | Programmatic audit of `STAGE_2_RESULTS.parquet`, balance, NaN/inf checks, CRN reproducibility | M1 | IN_PROGRESS |
| 3 | End-to-End KPI Calculation & Objective Direction Audit (R3) | Audit mathematical formulas, implementation code, parquet storage, sign conventions, biases | M1 | PLANNED |
| 4 | Architecture & Policy Classification Audit (R4) | Formal audit of A0–A5.3 and POL-01–POL-05; disentangle gate failure from Pareto dominance | M2, M3 | PLANNED |
| 5 | Sampling Error, Selection Bias & Lambda Sensitivity (R5) | Monte Carlo uncertainty quantification (500 paths), Stage 1 selection bias, $\lambda=15$ sensitivity | M2, M3 | PLANNED |
| 6 | Deliver Formal Validation Report (17 Sections) & Provenance (R6) | Comprehensive report at `audit_artifacts/reports/STAGE_2_ADVERSARIAL_VALIDATION.md`, update `RESEARCH_STATE.yaml` | M1, M2, M3, M4, M5 | PLANNED |

## Interface Contracts
### M1 ↔ M2, M3, M4, M5, M6
- Baseline parameter mapping, gate threshold definitions, candidate index definitions, and 3-way reconciliation tables.

### M2 & M3 ↔ M4 & M5
- Verified raw dataset, verified KPI formulas, column names, sign conventions, clean dataset handles, and reproducible CRN seeds.

### M4 & M5 ↔ M6
- Proven Pareto dominance/gate failure matrix, policy trade-off classifications, MC confidence intervals, selection bias verdicts, lambda sensitivity matrices, and epistemic classifications.

## Code Layout
- `audit_artifacts/reports/STAGE_2_ADVERSARIAL_VALIDATION.md`: Master 17-section adversarial validation report deliverable.
- `RESEARCH_STATE.yaml`: Provenance, cryptographic checksums, audit history, and Stage 2 gate status.
- `.agents/`: Agent workspaces and audit metadata (no raw data or modified source code here).
- `simulations/design_discovery/`: Simulation engine, runner scripts, verification scripts.
- `audit_artifacts/execution/`: Execution manifests and parquet datasets.
