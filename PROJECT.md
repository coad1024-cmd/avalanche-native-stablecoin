# Project: Avalanche-Native Stablecoin First-Principles Research Design Discovery Campaign

## Architecture
This project formalizes the complete quantitative mechanism-design problem, architecture search space, parameter bounds, dynamic redistribution policies, controller search space, multi-regime environmental uncertainty, formal robustness criteria, experimental ladder, and Pareto decision framework for an Avalanche-native stablecoin (anUSD).

The architecture establishes:
1. **Universal Variable Tensor & Continuous-Time State Space**: $\mathcal{T}(t) = (\mathbf{X}(t), \mathbf{U}(t), \mathbf{W}(t), \boldsymbol{\theta}) \in \mathcal{X} \times \mathcal{U} \times \mathcal{W} \times \Theta$ with 28 orthogonal state variables ($\mathbf{x}_{\text{phys}} \in \mathbb{R}_+^6, \mathbf{x}_{\text{val}} \in \mathbb{R}^{11}, \mathbf{x}_{\text{amm}} \in \mathbb{R}_+^4, \mathbf{x}_{\text{ctrl}} \in \mathbb{R}^3, \mathbf{x}_{\text{net}} \in \mathbb{R}_+^4$).
2. **Axiomatic Four-Tier Taxonomy**: Clear separation of Tier 1 (Hard Constraints / Double-Entry Stock-Flow Closure), Tier 2 (Pareto Optimization Objectives), Tier 3 (Stakeholder Utility Preferences), and Tier 4 (Diagnostic KPIs).
3. **Discrete Architectural Search Space ($\mathbb{A} = \{\text{A0} \dots \text{A5+}\}$)**: Formal valuation, state transitions, and crash bounds for 8 distinct structural topologies.
4. **Unified Parameter Inventory & 8-Class Epistemic Taxonomy**: 28 candidate parameters classified with active dimensionality reduction from 28 to 7 continuous levers via Sobol GSA.
5. **3-Simplex Redistribution Dynamics ($\boldsymbol{\omega}(t) \in \Delta^3$)**: Gross surplus generation $\Phi_{\text{gross}}(t)$ routed across 4 sinks with 5 candidate policy families (POL-01 to POL-05).
6. **Closed-Loop Dynamic Control & Stability Proofs**: Secondary AMM plant transfer functions $G_{\text{plant}}(s)$, Routh-Hurwitz and Lyapunov stability proofs ($\dot{V} \le 0$), over-damping guarantees ($\zeta > 1.0$), derivative elimination ($K_d \equiv 0$), and anti-windup clamping.
7. **2,140-Day Empirical Grounding & Kou Jump-Diffusion**: Kou double-exponential SDE MLE calibration ($\sigma = 89.15\%, \lambda = 15.00, p = 59.55\%, \eta_1 = 7.671, \eta_2 = 7.801, \bar{q} = 6.40\%$, $\Delta\text{AIC} = -5.51$ vs Merton) across 11 market regimes.
8. **Multi-Dimensional Robustness**: 4 formal criteria (Max-Min Wald, Bayesian Utility, $\text{CVaR}_{99\%}$, Wasserstein DRO), 5 analytical failure boundaries $\partial \Omega_{\text{fail}}$, and parameter fragility index $\bar{S}_T$.
9. **7-Stage Adaptive Computational Sequence**: Stage 1 Analytical Screening $\to$ Stage 2 Architecture Screening $\to$ Stage 3 GSA Sobol $\to$ Stage 4 Twin Sweeps $\to$ Stage 5 Uncertainty Propagation $\to$ Stage 6 NSGA-II $\to$ Stage 7 Adversarial Replay.
10. **Pareto Decision Framework & MCDA**: 6D vector optimization $\mathbf{J}(\mathbf{u})$, hypervolume indicator, Marginal Rates of Transformation, and TOPSIS / PROMETHEE II MCDA evaluating legacy A0 as an unvalidated hypothesis.
11. **State Lineage & Strict Stop Rule**: Verified reconciliation against `SNAP-2026-08-30-01` and execution of Phase 1 Analytical Screening ($N_0 = 100,000$, $90.101\%$ pruned, $N_{\text{survivors}} = 9,899$) as the ONE minimum next execution block.

## Feature Inventory
| # | Feature | Description | Milestone | Status |
|---|---------|-------------|-----------|--------|
| 1 | R1 Mathematical Tensor Decomposition | Universal variable tensor $\mathcal{T}(t)$ and 28-D continuous-time state space | M1 | DONE |
| 2 | R2 Axiomatic 4-Tier Taxonomy | True hard constraints, stock-flow closure proof, objectives, preferences, KPIs | M1 | DONE |
| 3 | R3 Discrete Architecture Search Space | 8 topologies (A0-A5+), continuous-time valuation ODEs, Theorem 1 & 2 crash bounds | M1 | DONE |
| 4 | R4 Parameter Search Space & Taxonomy | 28-parameter inventory, 8-class epistemic classification, GSA dimension reduction | M2 | DONE |
| 5 | R5 Redistribution Policy Space | Gross surplus $\Phi_{\text{gross}}(t)$, 3-simplex $\Delta^3$ conservation, POL-01 to POL-05 | M2 | DONE |
| 6 | R6 Closed-Loop Dynamic Control | AMM plant transfer function, Routh-Hurwitz / Lyapunov proofs, $K_d \equiv 0$, anti-windup | M2 | DONE |
| 7 | R7 Environmental Uncertainty Spec | 2,140-day telemetry grounding, Kou MLE parameters, 11-regime stochastic matrix | M3 | DONE |
| 8 | R8 Formal Robustness Definition | 4 criteria (Wald, Bayes, CVaR, DRO), 5 failure boundaries $\partial \Omega_{\text{fail}}$, fragility index $\bar{S}_T$ | M3 | DONE |
| 9 | R9 7-Stage Experimental Hierarchy | Adaptive computational ladder with hierarchical filtering and budget profiling | M3 | DONE |
| 10 | R10 Pareto Decision Framework | 6D Pareto vector, hypervolume, MRT, TOPSIS/PROMETHEE II MCDA, A0 evaluation | M4 | DONE |
| 11 | R11 Research State Update & Master Lineage | Reconciliation with SNAP-2026-08-30-01, master visual diagram, Phase 1 execution gate | M4 | DONE |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1: Core Mathematical & Architectural Space | Deliverables R1, R2, R3 (`RESEARCH_PROBLEM_FORMULATION.md`, `OBJECTIVES_AND_CONSTRAINTS.md`, `ARCHITECTURE_SEARCH_SPACE.md`) | none | DONE |
| 2 | M2: Parameters, Redistribution & Control | Deliverables R4, R5, R6 (`PARAMETER_SEARCH_SPACE.md`, `REDISTRIBUTION_SEARCH_SPACE.md`, `CONTROLLER_SEARCH_SPACE.md`) | M1 | DONE |
| 3 | M3: Uncertainty, Robustness & Experimental Ladder | Deliverables R7, R8, R9 (`ENVIRONMENTAL_UNCERTAINTY_SPEC.md`, `ROBUSTNESS_DEFINITION.md`, `EXPERIMENTAL_HIERARCHY.md`) | M2 | DONE |
| 4 | M4: Decision Framework, Lineage & Verification | Deliverables R10, R11 (`DECISION_FRAMEWORK.md`, `RESEARCH_STATE.yaml`, Master Flow Diagram, Phase 1 Screening) | M3 | DONE |
| 5 | M5: Multi-Disciplinary Adversarial Gate & Audit | Multi-reviewer, challenger stress testing, and forensic integrity audit verification | M1, M2, M3, M4 | DONE |

## Interface Contracts
### Continuous Dynamics ↔ Accounting Balance Sheet
- State vectors $\mathbf{X}(t) \in \mathcal{X} \subset \mathbb{R}^{28}$ strictly preserve double-entry closure:
  $\mathcal{A}(t) \equiv \mathcal{D}_{\text{senior}}(t) + \mathcal{E}_B(t) + \mathcal{B}_{\text{res}}(t) - \mathcal{D}_{\text{insolv}}(t)$.
- All state transitions preserve stock non-negativity $C_{\text{sAVAX}}(t) \ge 0, B_{\text{res}}(t) \ge 0, N_i(t) \ge 0$.

### Secondary AMM Microstructure ↔ PI Controller
- Plant Transfer Function: $G_{\text{plant}}(s) = \frac{K_{\text{amm}}(L)}{s + 1/\tau_{\text{arb}}} = \frac{K_{\text{DC}}}{1 + \tau_{\text{arb}} s}$.
- Control Law: $u(t) = \text{clamp}(K_p e(t) + K_i I(t), -0.05, 0.05)$ with $K_d \equiv 0.0000$.

### Redistribution Routing ↔ 3-Simplex Conservation
- Surplus routing vector $\boldsymbol{\omega}(t) = [\omega_{\text{burn}}, \omega_{\text{val}}, \omega_{\text{res}}, \omega_{\text{l1}}]^T \in \Delta^3$ satisfies $\sum \omega_i(t) \equiv 1.0000$ and $\omega_i(t) \ge 0$.

## Code Layout & Deliverables
- `audit_artifacts/design_discovery/RESEARCH_PROBLEM_FORMULATION.md`: Universal variable tensor & 28-D continuous-time state space.
- `audit_artifacts/design_discovery/OBJECTIVES_AND_CONSTRAINTS.md`: Four-tier taxonomy & stock-flow closure proof.
- `audit_artifacts/design_discovery/ARCHITECTURE_SEARCH_SPACE.md`: 8 structural topologies, continuous valuation ODEs, crash bounds.
- `audit_artifacts/design_discovery/PARAMETER_SEARCH_SPACE.md`: Parameter inventory across 8-class epistemic taxonomy.
- `audit_artifacts/design_discovery/REDISTRIBUTION_SEARCH_SPACE.md`: Gross surplus $\Phi_{\text{gross}}$ & 5 policy families on $\Delta^3$.
- `audit_artifacts/design_discovery/CONTROLLER_SEARCH_SPACE.md`: AMM transfer functions, stability proofs, $K_d \equiv 0$.
- `audit_artifacts/design_discovery/ENVIRONMENTAL_UNCERTAINTY_SPEC.md`: 2,140-day empirical grounding & Kou jump SDE.
- `audit_artifacts/design_discovery/ROBUSTNESS_DEFINITION.md`: 4 formal robustness criteria & failure boundaries.
- `audit_artifacts/design_discovery/EXPERIMENTAL_HIERARCHY.md`: 7-Stage Adaptive Computational Sequence.
- `audit_artifacts/design_discovery/DECISION_FRAMEWORK.md`: Pareto optimization, MCDA selection, A0 evaluation.
- `audit_artifacts/state/RESEARCH_STATE.yaml`: Reconciled research state against `SNAP-2026-08-30-01`.
- `audit_artifacts/execution/STAGE_1_ANALYTICAL_PRUNING_MANIFEST.json`: Phase 1 screening execution record ($N_{\text{survivors}} = 9,899$).
