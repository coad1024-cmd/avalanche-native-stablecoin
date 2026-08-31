# Original User Request

## 2026-08-31T07:14:02Z

# Teamwork Project Prompt — Draft

> Status: Launched
> Goal: Craft prompt → get user approval → delegate to teamwork_preview
> Requested team: Full multi-agent adversarial audit team (Research & Formal Validation)

Execute an independent first-principles adversarial validation audit of the completed Stage 2 Architecture & Redistribution Policy Screening in `coad1024-cmd/avalanche-native-stablecoin` on branch `research/first-principles-adversarial-audit`. The objective is to rigorously determine whether the conclusions, rankings, and "dominated" classifications reported by Stage 2 are genuinely supported by underlying code, experiment manifests, parquet datasets, and statistical evidence, without relying on prior agent claims.

Working directory: /home/hash/Hub/Projects/avalanche-native-stablecoin
Integrity mode: development

## Scope and Boundary Constraints (STRICT)

- **DO NOT** run Stage 3 GSA (Global Sensitivity Analysis).
- **DO NOT** run NSGA-II or multi-objective parameter optimization.
- **DO NOT** redesign protocol mechanisms or alter canonical economic model equations.
- **DO NOT** silently modify historical Stage 2 outputs (`STAGE_2_RESULTS.parquet`, `STAGE_2_EXPERIMENT_MANIFEST.json`).
- **SOURCE-CRITICALITY RULE**: Treat all prior reports, claims registers, manifests, and classifications as audit targets rather than established truth.
- **STOP RULE**: Terminate immediately upon generating the validation report, logging provenance, and updating research state.

## Reference Material
- Canonical Specifications: `audit_artifacts/design_discovery/EXPERIMENTAL_LADDER.md`, `audit_artifacts/design_discovery/DECISION_FRAMEWORK.md`, `audit_artifacts/design_discovery/OBJECTIVES_AND_CONSTRAINTS.md`
- Stage 1 Provenance: `audit_artifacts/execution/STAGE_1_ANALYTICAL_PRUNING_MANIFEST.json`, `audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet`
- Stage 2 Targets: `audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json`, `audit_artifacts/execution/STAGE_2_RESULTS.parquet`, `audit_artifacts/reports/STAGE_2_ARCHITECTURE_SCREENING.md`
- Codebase: Simulation engine, runner scripts, KPI calculation modules, and statistical routines in `src/` / `audit_artifacts/`

---

## Requirements

### R1. Reconstruct Experiment Specification & Reconcile Discrepancies
Independently reconstruct the formal specification of Stage 2 from the experimental ladder, manifests, code, and Stage 1 inputs (8 architectures, 5 policies, 40 configurations = 1,600 cells; 500 MC paths; time horizon; timestep; random seeds; CRN architecture; screening gates; KPI definitions; objective directions). Perform a 3-way reconciliation:
47154\text{SPECIFICATION} \quad \text{vs} \quad \text{IMPLEMENTATION} \quad \text{vs} \quad \text{ACTUAL OUTPUTS}47154
Record every parameter, gate, or configuration discrepancy.

### R2. Verify 1,600-Configuration Dataset Integrity & Genuine CRN Implementation
Programmatically inspect `STAGE_2_RESULTS.parquet` and execution logs to verify:
- Exact architecture (8) and policy (5) balance across all 40 candidate configurations (1,600 unique cells).
- Check for candidate IDs, missing cells, duplicated cells, failed/silently discarded paths, and NaN/inf values.
- Verify Common Random Numbers (CRN): verify seed management, path generation isolation, environmental vs candidate-specific randomness streams, and run an independent reproducibility test.

### R3. End-to-End KPI Calculation & Objective Direction Audit
Audit every Stage 2 KPI from mathematical formulation $\to$ code implementation $\to$ parquet storage $\to$ report synthesis.
- KPIs to verify: Peg RMSE, reset count, validator coverage, solvency survival probability, subsidy, burn, yield, and reserve metrics.
- Check specifically for: algebraic tautologies, denominator cancellations, look-ahead bias, incorrect unit scaling/annualization, aggregation errors across MC paths, survivorship bias, and inverted objective directions.

### R4. Audit Architecture (A0–A5.3) and Policy (POL-01–POL-05) Classifications
- Formally audit every architecture classified as DOMINATED (A0, A1, A3, A4, A5.1) vs RETENTION (A2, A5.2, A5.3).
- **Strict Distinction**: Disentangle **FAILED SCREENING GATE** from **MATHEMATICALLY PARETO-DOMINATED**. For any claimed Pareto dominance, verify dominating candidate, all objectives, strict improvement dimension, and non-worsening dimensions.
- Audit redistribution policies (POL-01 to POL-05), specifically testing whether POL-04 reflects a legitimate Pareto trade-off (burn vs coverage) or unmitigated failure, and whether POL-02, POL-03, POL-05 are robust survivors.

### R5. Sampling Error, Stage-1 Selection Bias, and Lambda Provisionality
- **Monte Carlo Sampling Error**: Quantify Monte Carlo standard errors and 95% confidence intervals across 500 paths to determine if ranking differences are statistically distinguishable or effectively tied.
- **Stage-1 Selection Bias**: Audit whether Stage 1 analytical pruning disproportionately eliminated parameter subspaces favorable to specific architectures or policies.
- **Provisional Lambda Evaluation**: Evaluate whether architecture/policy rankings depend materially on the provisional jump intensity $\lambda = 15.00\text{ yr}^{-1}$ without running a new broad GSA.

### R6. Deliver Formal Adversarial Validation Report & Update Provenance
- Deliver the comprehensive audit report at: `audit_artifacts/reports/STAGE_2_ADVERSARIAL_VALIDATION.md` structured with all 17 required sections including executive summary, reconciliation tables, Pareto proofs/refutations, error registers, epistemic classification table, and explicit recommendation (`PROCEED TO STAGE 3` or `HOLD STAGE 3`).
- Record audit metadata (git SHA, Python/dependency versions, dataset hashes, random seeds, auditor config) and update `RESEARCH_STATE.yaml` without altering canonical economic parameters.

---

## Acceptance Criteria

### Execution & Dataset Integrity
- [ ] Direct programmatic verification of `STAGE_2_RESULTS.parquet` confirming presence/absence of all 1,600 configuration cells (8 architectures × 5 policies × 40 candidates).
- [ ] Explicit check for NaN, null, infinite, or silently dropped simulation runs across all Monte Carlo paths.
- [ ] Reproducibility check of the Common Random Numbers (CRN) stream verifying identical shock sequences across comparable candidates.

### KPI & Mathematical Validation
- [ ] Line-by-line code audit of KPI formulas (Peg RMSE, Reset Count, Validator Coverage, Solvency, Subsidy, Burn, Yield) reconciled with theoretical definitions.
- [ ] Verification that objective directions (minimize vs maximize) match `OBJECTIVES_AND_CONSTRAINTS.md` and `DECISION_FRAMEWORK.md`.
- [ ] Check for look-ahead bias, units/annualization errors, and path averaging bias in stored results.

### Dominance & Epistemic Classification
- [ ] Mathematical Pareto dominance verification vs Screening Gate failure for every rejected architecture (, A_1, A_3, A_4, A_{5.1}$).
- [ ] Rigorous trade-off vs failure audit for redistribution policies (\text{-}01$ through \text{-}05$).
- [ ] Monte Carlo uncertainty quantification showing statistical significance bounds for all critical ranking boundaries.
- [ ] Final Epistemic Classification table assigning exactly one of [`VERIFIED`, `CONDITIONALLY SUPPORTED`, `SCREENING-ONLY`, `STATISTICALLY INCONCLUSIVE`, `UNSUPPORTED`, `CONTRADICTED`, `INVALID`] to each architecture and policy outcome.

### Deliverable & Provenance
- [ ] Comprehensive validation report generated at `audit_artifacts/reports/STAGE_2_ADVERSARIAL_VALIDATION.md` containing all 17 required sections.
- [ ] `RESEARCH_STATE.yaml` updated with audit state, commit hash, dataset hashes, and auditor provenance without changing canonical economic parameters.
- [ ] Explicit final gate decision: `PROCEED TO STAGE 3` or `HOLD STAGE 3`.
