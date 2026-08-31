## 2026-08-31T02:45:04Z
You are Worker 3 (Uncertainty, Experimental Ladder & Decision Framework).
Your working directory is: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_worker_m3/

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

You MUST read:
- /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md
- /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/orchestrator_discovery_1/PROJECT.md
- /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_explorer_survey_1/handoff.md
- /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_explorer_survey_2/handoff.md
- /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_explorer_survey_3/handoff.md

Your Exclusive Write Ownership (You own and must create these 3 files in audit_artifacts/design_discovery/):
1. /home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/design_discovery/ENVIRONMENTAL_UNCERTAINTY_SPEC.md
2. /home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/design_discovery/EXPERIMENTAL_LADDER.md
3. /home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/design_discovery/DECISION_FRAMEWORK.md

Detailed Requirements for your Deliverables:
1. `ENVIRONMENTAL_UNCERTAINTY_SPEC.md`:
   - Empirical grounding from 2,140 days of market telemetry (DAT-01 to DAT-07) and Kou SDE MLE parameters.
   - Comprehensive 11-Regime Parameter Matrix: CALM_BULL, NORMAL, HIGH_VOLATILITY, SEVERE_BEAR, FLASH_CRASH, PROLONGED_STAGNATION, LIQUIDITY_CRUNCH, STAKING_YIELD_COMPRESSION, REGULATORY_CHURN, VALIDATOR_CAPITAL_FLIGHT, RECOVERY_RALLY.
   - Formal specification of the 3 uncertainty spaces:
     * U_emp: Calibrated empirical posterior parameter space with bootstrap 95% credible intervals.
     * U_stress: Deterministic and stochastic stress scenarios (e.g. Terra-style run, 3AC crash, flash jump events).
     * U_gov: Governance and structural parameter shocks (staking yield shocks, gas spikes, validator count drops).
2. `EXPERIMENTAL_LADDER.md`:
   - Complete 7-Stage Adaptive Computational Sequence:
     * Stage 1: Cheap Analytical Screening (closed-form Theorem 1 solvency bounds, Hurwitz stability, <100ms per candidate).
     * Stage 2: Structural Architecture & Policy Family Screening (coarse Monte Carlo, 500 paths).
     * Stage 3: Global Sensitivity Analysis (Sobol first-order & total-order indices via Saltelli sampling, uncorrupted variance decomposition).
     * Stage 4: High-Fidelity Simulation Sweeps (canonical accounting, Kou jump-diffusion, dynamic fee routing, 10,000 paths).
     * Stage 5: Multi-Regime Uncertainty Propagation & Robustness Scoring (stress testing across U_emp x U_stress x U_gov).
     * Stage 6: Evolutionary Pareto Optimization (NSGA-II / MOEA/D on Theta x Delta^3 to discover Pareto frontier P*).
     * Stage 7: Out-of-Sample & Adversarial Stress Validation (unseen historical replay, adversarial MEV/arbitrage stress).
   - Computational budget, runtime bounds, pruning filters, and convergence metrics for each stage.
3. `DECISION_FRAMEWORK.md`:
   - Formal Multi-Objective Pareto Decision Framework: Pareto dominance, hypervolume indicator, trade-off frontier analysis.
   - Stakeholder Utility Aggregation & Multi-Criteria Decision Analysis (TOPSIS / PROMETHEE / weighted Tchebycheff).
   - Concise Master Mermaid System Flow Diagram linking empirical data, architectures, redistribution policies, controllers, uncertainty propagation, experimental ladder, and final governance selection.
   - Specification of the SINGLE NEXT EXECUTION PHASE (Phase 1: Analytical Screening & Candidate Pruning) with concrete input parameters, mathematical formulas, and rigorous stopping criteria.

Deliverables must be written with publication-grade mathematical rigor, complete LaTeX equations, tables, citations, and clear Mermaid diagrams.
When complete, write a detailed handoff to `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_worker_m3/handoff.md` and message the parent.
