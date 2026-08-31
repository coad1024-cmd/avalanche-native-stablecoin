# Project: Avalanche-Native Stablecoin Design Discovery & Quantitative Mechanism Design

## Architecture & Epistemic Foundations
- **Core Paradigm**: Open Discovery Mandate. The legacy dual-tranche reset model (A0) is one candidate architecture among A0–A5+; ACP-67 represents stakeholder inputs, not immutable truths.
- **Physical Invariants**: Strict non-negativity ($C \ge 0, B \ge 0, N_i \ge 0$), double-entry stock-flow closure ($\mathcal{A}(t) \equiv \mathcal{D}_{\text{senior}}(t) + \mathcal{E}_B(t) + \mathcal{B}(t) + \mathcal{D}_{\text{insolvency}}(t)$), non-negative realizable solvency ($M_{\text{redemp}} \ge 0$), simplex weight conservation ($\sum \omega_i = 1$).
- **Multi-Regime Stochastic Foundations**: Kou (2002) asymmetric double-exponential jump-diffusion calibrated on 2,140 daily observations (DAT-01 to DAT-07).

## Feature Inventory
| # | Feature / Deliverable | Description | Milestone | Source |
|---|-----------------------|-------------|-----------|--------|
| 1 | `RESEARCH_PROBLEM_FORMULATION.md` | Master mathematical problem formulation, system vector, state space, open discovery charter | M1 | Survey Explorer 1, 2, 3 |
| 2 | `OBJECTIVES_AND_CONSTRAINTS.md` | 4-tier objective taxonomy (Hard, Optimization, Preferences, Diagnostic) & physical hard constraints | M1 | Survey Explorer 2, 3 |
| 3 | `ARCHITECTURE_SEARCH_SPACE.md` | Discrete structural architecture search space (A0 to A5+), comparison matrix, mathematical specs | M2 | Survey Explorer 3 |
| 4 | `REDISTRIBUTION_SEARCH_SPACE.md` | Endogenous redistribution policy simplex $\boldsymbol{\omega}(t) \in \Delta^3$, 5 policy families, stakeholder matrix | M2 | Survey Explorer 1, 3 |
| 5 | `CONTROLLER_SEARCH_SPACE.md` | Closed-loop controller existence decision, CPMM plant gain $K_{\text{amm}}(L)$, error dynamics, stability bounds | M2 | Survey Explorer 2 |
| 6 | `ENVIRONMENTAL_UNCERTAINTY_SPEC.md` | 11-regime parameter matrix, Kou SDE posteriors, empirical ($\mathcal{U}_{\text{emp}}$), stress ($\mathcal{U}_{\text{stress}}$), governance ($\mathcal{U}_{\text{gov}}$) | M3 | Survey Explorer 1 |
| 7 | `ROBUSTNESS_DEFINITION.md` | Formal multi-regime economic definition of robustness, Pareto viability, worst-case drawdown survival | M1 | Survey Explorer 1, 3 |
| 8 | `EXPERIMENTAL_LADDER.md` | Minimum 7-stage adaptive computational sequence from cheap screening to robust Pareto optimization | M3 | Survey Explorer 3 |
| 9 | `DECISION_FRAMEWORK.md` | Multi-objective Pareto decision framework, stakeholder weighting, master flow diagram, next execution phase | M3 | Survey Explorer 1, 2, 3 |

## Milestones
| # | Name | Scope & Deliverables | Dependencies | Status |
|---|------|----------------------|-------------|--------|
| M1 | Foundations, Objectives & Robustness | `RESEARCH_PROBLEM_FORMULATION.md`, `OBJECTIVES_AND_CONSTRAINTS.md`, `ROBUSTNESS_DEFINITION.md` | Survey | PLANNED |
| M2 | Structural & Policy Search Spaces | `ARCHITECTURE_SEARCH_SPACE.md`, `REDISTRIBUTION_SEARCH_SPACE.md`, `CONTROLLER_SEARCH_SPACE.md` | Survey | PLANNED |
| M3 | Uncertainty, Ladder & Decision Framework | `ENVIRONMENTAL_UNCERTAINTY_SPEC.md`, `EXPERIMENTAL_LADDER.md`, `DECISION_FRAMEWORK.md` | Survey | PLANNED |
| M4 | Verification & Audit Gate | 2x Reviewers, 2x Challengers, 1x Forensic Auditor across all 9 deliverables | M1, M2, M3 | PLANNED |

## Code & Artifact Layout
- Master Deliverables Directory: `/home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/design_discovery/`
  - `RESEARCH_PROBLEM_FORMULATION.md`
  - `OBJECTIVES_AND_CONSTRAINTS.md`
  - `ARCHITECTURE_SEARCH_SPACE.md`
  - `REDISTRIBUTION_SEARCH_SPACE.md`
  - `CONTROLLER_SEARCH_SPACE.md`
  - `ENVIRONMENTAL_UNCERTAINTY_SPEC.md`
  - `ROBUSTNESS_DEFINITION.md`
  - `EXPERIMENTAL_LADDER.md`
  - `DECISION_FRAMEWORK.md`
- Survey Metadata: `.agents/teamwork_preview_explorer_survey_{1,2,3}/handoff.md`
- Orchestrator Metadata: `.agents/orchestrator_discovery_1/`

## Interface Contracts
- **Deliverable Formatting**: Full LaTeX mathematical precision, comprehensive equations, complete proofs and citations, structured comparison tables, integrated Mermaid flow diagrams.
- **Cross-Referencing**: Consistent notation across all 9 documents ($\mathbf{x}(t)$, $\mathbf{u}(t)$, $\boldsymbol{\omega}(t) \in \Delta^3$, $S(t)$, $V_A(t)$, $V_B(t)$, $V_{A'}(t)$, $V_{B'}(t)$, $K_{\text{amm}}(L)$, $\mathcal{U}_{\text{emp}}$, $\mathcal{U}_{\text{stress}}$, $\mathcal{U}_{\text{gov}}$, $\mathbb{A} = \{\text{A0}, \dots, \text{A5.3}\}$).
- **Stopping Criteria for Phase 1 Execution**: Explicit numerical gates (analytical screening runtime $< 100\text{ms}$, failure margin tolerance $< 10^{-6}$, Pareto convergence metric $\Delta \mathcal{S} < 0.01$).
