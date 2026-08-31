# Dispatch for Worker M4

## Assigned Milestone
Milestone 4 (Requirement R4): Audit Architecture (A0–A5.3) and Policy (POL-01–POL-05) Classifications.

## Mandatory Integrity Warning
> DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective
Formally audit the down-selection, classification, and Pareto dominance claims across all 8 architectures and 5 redistribution policies:
1. Strict Separation of Concepts:
   - Disentangle **FAILED SCREENING GATE** from **MATHEMATICALLY PARETO-DOMINATED**.
   - For every architecture classified as DOMINATED (A0, A1, A3, A4, A5.1) vs RETENTION (A2, A5.2, A5.3), formally prove mathematical dominance or gate failure.
   - For A0: prove that every candidate is strictly dominated on the 5D objective space.
   - For A1, A3, A4, A5.1: prove that they sit on the unconstrained churn boundary ($0.00/\text{yr}$) but are rejected via Gate 4 failure ($\mathbb{P}(\text{Solvent}) \ge 99\%$).
2. Redistribution Policy Audit (POL-01 to POL-05):
   - Formally evaluate POL-04: prove whether POL-04 represents a legitimate non-dominated Pareto frontier extreme point (maximizing burn volume to $1.155\text{M AVAX}$) or unmitigated failure.
   - Clarify the stakeholder trade-off: POL-04 achieves maximum burn at the cost of node operator OpEx starvation ($\text{CR}_{\text{OpEx}} < 1.20\times$), making it non-dominated in pure mathematics but inadmissible under stakeholder acceptance criteria.
   - Validate survivor policies (POL-02, POL-03, POL-05) for robustness across architectures.
3. Compute exact multi-objective hypervolume, Pareto non-dominated frontiers (unconstrained and gate-constrained), and dominance matrices.

## Key Inputs & References
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md`
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md`
- `audit_artifacts/reports/STAGE_2_ARCHITECTURE_SCREENING.md`
- `audit_artifacts/reports/ARCHITECTURE_COMPARISON.md`
- `audit_artifacts/reports/REDISTRIBUTION_POLICY_SCREENING.md`
- `audit_artifacts/execution/STAGE_2_RESULTS.parquet`

## Deliverables
- Working directory: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m4`
- Independent verification script: `/home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/execution/verify_stage2_dominance_and_policies.py`
- Automated test suite: `simulations/design_discovery/test_stage2_dominance_classifications.py`
- Comprehensive report: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m4/m4_dominance_policy_report.md`
- `handoff.md` and `progress.md`.

## 2026-08-31T07:34:21Z
User Request received:
You are Worker M4 for Milestone 4 (Requirement R4: Audit Architecture and Policy Classifications).
Your working directory is: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m4
Read instructions in: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m4/DISPATCH.md
Read the authoritative user request: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md
Read PROJECT.md: /home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md

MANDATORY INTEGRITY WARNING:
> DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your mission:
1. Disentangle FAILED SCREENING GATE from MATHEMATICALLY PARETO-DOMINATED for all 8 architectures (A0-A5.3).
2. Formally audit POL-01 to POL-05: prove whether POL-04 reflects a legitimate Pareto trade-off (burn vs OpEx) or unmitigated failure, and validate survivor policies (POL-02, POL-03, POL-05).
3. Compute exact multi-objective hypervolume, Pareto non-dominated frontiers, and dominance matrices.
4. Deliver:
   - Verification script: `audit_artifacts/execution/verify_stage2_dominance_and_policies.py`
   - Test suite: `simulations/design_discovery/test_stage2_dominance_classifications.py`
   - Master report: `.agents/worker_m4/m4_dominance_policy_report.md`
   - `handoff.md` and `progress.md`. Send message to parent when finished.
