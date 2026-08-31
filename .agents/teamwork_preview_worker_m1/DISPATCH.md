## 2026-08-31T02:45:04Z

<USER_REQUEST>
You are Worker 1 (Foundations, Objectives & Robustness).
Your working directory is: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_worker_m1/

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

You MUST read:
- /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md
- /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/orchestrator_discovery_1/PROJECT.md
- /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_explorer_survey_1/handoff.md
- /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_explorer_survey_2/handoff.md
- /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_explorer_survey_3/handoff.md

Your Exclusive Write Ownership (You own and must create these 3 files in audit_artifacts/design_discovery/):
1. /home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/design_discovery/RESEARCH_PROBLEM_FORMULATION.md
2. /home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/design_discovery/OBJECTIVES_AND_CONSTRAINTS.md
3. /home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/design_discovery/ROBUSTNESS_DEFINITION.md

Detailed Requirements for your Deliverables:
1. `RESEARCH_PROBLEM_FORMULATION.md`:
   - Full mathematical specification of the quantitative mechanism design problem: state space X, action/control space U, environmental disturbance space W, variable tensor decomposition.
   - Formal Open Discovery charter: A0 is one candidate architecture, ACP-67 is stakeholder input, no inherited assumptions without proof.
   - Comprehensive system state equations in continuous and discrete time.
   - Integrated Mermaid architecture & state transition flow diagrams.
2. `OBJECTIVES_AND_CONSTRAINTS.md`:
   - Complete 4-tier taxonomy:
     * Tier 1: True Physical & Mathematical Hard Constraints (Strict non-negativity C >= 0, B >= 0, N_i >= 0; double-entry stock-flow balance sheet closure A(t) = D_senior(t) + E_B(t) + B(t) + D_insolvency(t); non-negative realizable redemption solvency M_redemp >= 0; simplex weight conservation sum omega_i = 1; 2:1 token pair mass conservation).
     * Tier 2: Optimization Objectives (Peg RMSE, Flash crash survival, Validator OpEx margin, Cumulative AVAX burns, Recovery time, Capital efficiency, Secondary liquidity resilience).
     * Tier 3: Stakeholder Preferences & Multi-Attribute Utilities.
     * Tier 4: Diagnostic Metrics & Invariant Health Trackers.
   - Explicit debunking of aspirational targets as hard constraints (explaining why -60% survival, 1.37% volatility, 65/20/15 splits are objectives/preferences on the Pareto frontier, not physical constraints).
3. `ROBUSTNESS_DEFINITION.md`:
   - Rigorous multi-regime mathematical definition of economic robustness.
   - Max-min worst-case, expected utility, Conditional Value at Risk (CVaR_alpha), and distributional robustness across Kou jump-diffusion uncertainty spaces.
   - Formal definitions of parameter fragility, phase margin decay, and failure boundary distances dist(theta, d Omega_fail).

Deliverables must be written with publication-grade mathematical rigor, complete LaTeX equations, tables, citations, and clear Mermaid diagrams.
When complete, write a detailed handoff to `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_worker_m1/handoff.md` and message the parent.
</USER_REQUEST>
