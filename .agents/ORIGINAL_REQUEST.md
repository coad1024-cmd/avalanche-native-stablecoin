# Original User Request

## 2026-08-31T04:12:10Z

# Teamwork Project Prompt — Draft

> Status: Launched  
> Goal: Craft prompt → get user approval → delegate to `teamwork_preview`  
> Requested team: Multi-Disciplinary Quantitative Mechanism Design & Stablecoin Economics Research Team (9 Specialist Roles)  

Execute a rigorous, first-principles research design discovery campaign to formalize the complete quantitative mechanism-design problem, architecture search space, parameter bounds, dynamic redistribution policies, controller search space, multi-regime environmental uncertainty, formal robustness criteria, experimental ladder, and Pareto decision framework for an Avalanche-native stablecoin, determining what architecture and parameter corridors should actually be built under realistic uncertainty.

Working directory: `/home/hash/Hub/Projects/avalanche-native-stablecoin`  
Integrity mode: `development`  

---

## Core Problem Statement & Epistemic Charter

1. **Architecture A0 is a Candidate Design, Not Ground Truth:** The legacy dual-class securitization with periodic resets ($\text{A0}$) is one candidate among a discrete structural search space $\mathbb{A} = \{\text{A0}, \text{A1}, \text{A2}, \text{A3}, \text{A4}, \text{A5.1}, \text{A5.2}, \text{A5.3}\}$.
2. **SSRN-3856569 is a Source of Ideas, Not a Mandate:** Academic prototypes and preliminary derivations provide conceptual inspiration but require independent mathematical verification and double-entry accounting closure.
3. **ACP-67 / Stakeholder Inputs are Policy Objectives:** Avalanche governance proposals (such as static 65/20/15 yield splits) represent stakeholder preferences and policy inputs, not immutable physical invariants.
4. **Candidate Parameters are Hypotheses:** Legacy parameters ($R = 7.30\%, R' = 3.00\%, H_d = \$0.25, H_u = \$2.00$) are unvalidated candidate baselines subject to multi-objective Pareto optimization.
5. **Strict Stop Rule Enforced:** No large-scale simulations, full GSA sweeps, or NSGA-II optimization runs are executed during this formulation phase; exactly ONE minimum next execution block must be identified.

---

## Reference Materials & Baseline Registry

- **Frozen Research Baseline Snapshot:** `audit_artifacts/state/RESEARCH_STATE.yaml` (`SNAP-2026-08-30-01`, Commit `d57b3e601ca87733ec4343dbb70c7514ab264939`)
- **Empirical Calibration Report:** `audit_artifacts/reports/EMPIRICAL_CALIBRATION_REPORT.md` (2,140 days of Avalanche C-Chain telemetry: `DAT-01` to `DAT-07`)
- **Global Sensitivity Analysis Report:** `audit_artifacts/reports/GLOBAL_SENSITIVITY_ANALYSIS.md` (Saltelli-Sobol $N=2,048$)
- **Controller Ablation Study:** `audit_artifacts/reports/CONTROLLER_ABLATION_STUDY.md` ($K_d \equiv 0$ derivative noise elimination)
- **Out-of-Sample Stress Report:** `audit_artifacts/reports/OUT_OF_SAMPLE_STRESS_REPORT.md` (Flash crash, bear, yield compression)
- **Parameter Governance Registry:** `audit_artifacts/registers/PARAMETER_GOVERNANCE_REGISTRY.md` (8-Class Epistemic Taxonomy)
- **Source & Derivation Audit:** `audit_artifacts/reports/SOURCE_AND_DERIVATION_AUDIT.md` (Line-by-line delta audit vs SSRN-3856569)

---

## Multi-Agent Specialist Panel (9 Roles)

1. **Mechanism Design Specialist:** Mathematical game theory, incentive compatibility, double-entry stock-flow balance sheet conservation, and structural invariants.
2. **Quantitative Finance Specialist:** Continuous-time jump-diffusion modeling (Kou SDE), PIDE valuation, option pricing boundaries, and stochastic volatility.
3. **Stablecoin Economics Specialist:** Macroeconomic peg stability, senior-junior capital structure, collateral velocity, and redemption run dynamics.
4. **Optimization Specialist:** Multi-objective evolutionary algorithms (NSGA-II / MOEA/D), Pareto frontier topology, and hypervolume indicators.
5. **Redistribution & Network Economics Specialist:** 3-simplex yield routing ($\Delta^3$), validator operating margin solvency ($\text{CR}_{\text{OpEx}} \ge 1.20\times$), and AVAX burn dynamics.
6. **Control Systems Specialist:** Frequency-domain transfer functions, Routh-Hurwitz stability criteria, Lyapunov asymptotic stability, anti-windup clamping, and phase margin decay.
7. **Security Specialist:** MEV sandwiching protection, oracle staleness circuit breakers, flash loan arbitrage limits, and re-entrancy invariants.
8. **Empirical Modeling Specialist:** Maximum Likelihood Estimation (MLE), non-parametric bootstrap credible intervals, Kolmogorov-Smirnov goodness-of-fit, and empirical regime classification.
9. **Skeptical Peer Reviewer:** Adversarial auditor tasked with challenging objective function formulation, detecting circular calibrations, surfacing unstated assumptions, and probing failure boundaries.

---

## Requirements

### R1. Universal Problem Formulation & Mathematical Tensor Decomposition
Formulate the infinite-horizon stochastic mechanism design problem over the complete universal variable tensor $\mathcal{T}(t) = (\mathbf{X}(t), \mathbf{U}(t), \mathbf{W}(t), \boldsymbol{\theta}) \in \mathcal{X} \times \mathcal{U} \times \mathcal{W} \times \Theta$, decomposing state space $\mathcal{X} \subset \mathbb{R}^{28}$ into physical stocks, valuation multipliers, secondary AMM microstructure, controller states, and network telemetry.

### R2. Axiomatic Four-Tier Taxonomy of Objectives and Constraints
Establish the formal boundary separating:
- **Tier 1 (True Hard Constraints):** Physical stock non-negativity ($C \ge 0, B \ge 0, N_i \ge 0$), double-entry stock-flow balance sheet closure ($\mathcal{A}(t) \equiv \mathcal{D}_{\text{senior}} + \mathcal{E}_B + \mathcal{B}_{\text{res}} - \mathcal{D}_{\text{insolv}}$), realizable redemption solvency ($M_{\text{redemp}} \ge 0$), 3-simplex conservation ($\sum \omega_i = 1, \omega_i \ge 0$), and token mass conservation.
- **Tier 2 (Optimization Objectives):** Vector objective $\mathbf{J}(\boldsymbol{\theta}) = [J_{\text{peg}}, -J_{\text{burn}}, J_{\text{tail}}, -J_{\text{val}}, J_{\text{churn}}, J_{\text{frag}}]^T$ defining the Pareto search manifold.
- **Tier 3 (Stakeholder Preferences):** Multi-attribute utility functions ($U_{\text{usd}}, U_{\text{spec}}, U_{\text{val}}, U_{\text{avax}}, U_{\text{eco}}$).
- **Tier 4 (Diagnostic Metrics):** Real-time tracking error, damping ratio $\zeta$, phase margin $\text{PM}$, reserve buffer fill time $\tau_{\text{fill}}$, and Sobol total indices $S_{Ti}$.

### R3. Discrete Structural Architecture Search Space ($\mathbb{A} = \{\text{A0} \dots \text{A5+}\}$)
Formalize 8 distinct structural topologies:
- **A0:** Dual-Class Subordinated Scalar Rebasing with Discrete Barrier Resets ($H_d = \$0.25, H_u = \$2.00$).
- **A1:** Continuous Streaming Amortization (Infinitesimal dynamic rate $\dot{\mathcal{M}}(t)$, zero reset churn).
- **A2:** Dedicated Protocol Solvency Reserve Buffer Vault ($B_{\text{res}}(t)$ loss-absorption cushion).
- **A3:** Floating Junior Equity Tranche (Perpetual leveraged yield token, floating mark-to-market NAV).
- **A4:** Zero-Controller Primary CDP Arbitrage ($K_p = K_i = K_d \equiv 0$, pure mint/redeem arbitrage band).
- **A5.1–A5.3:** Advanced Hybrids (Dynamic Debt-Equity Convertibles, Protocol-Owned AMM, Algorithmic Multi-LST Basket).

### R4. Complete Parameter Search Space & Epistemic Taxonomy
Construct the comprehensive parameter inventory across all architectures, detailing Symbol, Meaning, Physical Units, Architecture Dependence, Current Baseline, Plausible Bounds $[\theta_{\min}, \theta_{\max}]$, Epistemic Classification (Structural Invariant, Calibrated Empirical, Governance Candidate, Dynamic Control, Security Guard), Uncertainty Source, Identification Status, and Sobol Sensitivity.

### R5. Endogenous Dynamic Redistribution Policy Space ($\boldsymbol{\omega}(t) \in \Delta^3$)
Formulate the gross protocol surplus generation function $\Phi_{\text{gross}}(t)$ and evaluate 5 candidate policy families:
- **POL-01:** Static Fixed Waterfall (Legacy 65/20/0/15).
- **POL-02:** Countercyclical Drawdown Feedback ($\omega_{\text{val}}(t) = \text{clamp}(0.20 + 0.35 \cdot \text{Drawdown}_t, 0.20, 0.45)$).
- **POL-03:** Reserve-Priority Tail-First Allocation ($\omega_{\text{res}}(t) = \text{clamp}(0.20 \cdot \max(0, 1.30 - \text{CR}), 0, 0.15)$).
- **POL-04:** Aggressive Deflationary Burn Maximization ($\omega_{\text{burn}} \ge 0.75$).
- **POL-05:** Adaptive Multi-Objective Dynamic State Softmax Law.

### R6. Closed-Loop Dynamic Control Policy Search Space & Stability Proofs
Evaluate the controller existence decision across $\{ \text{No Controller}, \text{P}, \text{PI}, \text{PID}, \text{MPC} \}$. Derive the secondary AMM plant transfer function $G_{\text{plant}}(s) = \frac{K_{\text{amm}}}{\tau_{\text{arb}} s + 1}$, prove closed-loop asymptotic stability via Routh-Hurwitz and Lyapunov criteria ($\dot{V} \le 0$), establish formal proof of derivative noise amplification ($K_d \equiv 0$), and specify anti-windup clamping ($|\Delta R'| \le 5.0\%$).

### R7. Multi-Regime Environmental & Structural Model Uncertainty
Ground environmental uncertainty in 2,140 days of empirical telemetry (`DAT-01` to `DAT-07`). Formalize the master uncertainty tensor $\Omega_{\text{total}} = \mathcal{U}_{\text{emp}} \times \mathcal{U}_{\text{stress}} \times \mathcal{U}_{\text{gov}}$ across 11 discrete stochastic market regimes, establishing Kou double-exponential jump-diffusion parameters ($\sigma = 89.15\%, \lambda = 15.00, p = 59.55\%, \eta_1 = 7.671, \eta_2 = 7.801, \bar{q} = 6.40\%$) and model comparison against Merton log-normal ($\Delta\text{AIC} = -5.51$).

### R8. Multi-Dimensional Formal Definition of Economic Robustness
Establish four axiomatic robustness criteria: Max-Min Worst-Case (Wald), Expected Bayesian Utility, $\text{CVaR}_{99\%}$ Tail Loss, and Distributionally Robust Optimization (DRO) with Wasserstein metric $W_1(\mathbb{P}, \hat{\mathbb{P}}_N) \le \epsilon$. Formulate the 5 analytical failure manifolds $\partial \Omega_{\text{fail}}$ and the parameter fragility index $\bar{S}_T$.

### R9. 7-Stage Adaptive Computational Hierarchy (The Experimental Ladder)
Define the computational ladder:
$$\text{Stage 1: Analytical Screening} \longrightarrow \text{Stage 2: Architecture Screening} \longrightarrow \text{Stage 3: GSA Sobol} \longrightarrow \text{Stage 4: Digital Twin Sweeps} \longrightarrow \text{Stage 5: Uncertainty Propagation} \longrightarrow \text{Stage 6: NSGA-II Pareto Search} \longrightarrow \text{Stage 7: Out-of-Sample / Adversarial Replay}$$

### R10. Multi-Objective Pareto Decision Framework & MCDA Selection
Define strict Pareto dominance ($\succ$), non-dominated frontier discovery ($\mathcal{P}^*$), hypervolume indicator $\mathcal{S}(\mathcal{P})$, Marginal Rates of Transformation (MRT), and preference aggregation via TOPSIS and Augmented Weighted Tchebycheff scalarization to evaluate whether legacy $\text{A0}$ is Dominant, Pareto-Efficient, Competitive, Conditionally Useful, or Structurally Dominated.

### R11. Canonical Master Diagram, Research State Update & Minimum Next Execution Block
Produce the master visual flow diagram, maintain `audit_artifacts/state/RESEARCH_STATE.yaml`, and specify exactly ONE next execution block (**Phase 1: Analytical Screening & Invariant Pruning**) with exact inputs, tools, success criteria, and stopping gates.

---

## Acceptance Criteria

### Deliverables & Verification Rubric
- [ ] Deliverable 1: `RESEARCH_PROBLEM_FORMULATION.md` published with universal variable tensor $(\mathbf{X}, \mathbf{U}, \mathbf{W}, \boldsymbol{\theta})$ and continuous-time state space.
- [ ] Deliverable 2: `OBJECTIVES_AND_CONSTRAINTS.md` published with axiomatic Four-Tier taxonomy and double-entry stock-flow closure proof.
- [ ] Deliverable 3: `ARCHITECTURE_SEARCH_SPACE.md` published covering 8 topologies ($\text{A0}$–$\text{A5+}$) with full continuous-time valuation and crash bound derivations.
- [ ] Deliverable 4: `PARAMETER_SEARCH_SPACE.md` published containing the unified parameter inventory across all architectures with 8-class epistemic taxonomy.
- [ ] Deliverable 5: `REDISTRIBUTION_SEARCH_SPACE.md` published formalizing gross surplus $\Phi_{\text{gross}}$ and 5 policy families on 3-simplex $\Delta^3$.
- [ ] Deliverable 6: `CONTROLLER_SEARCH_SPACE.md` published with AMM plant transfer functions, Routh-Hurwitz/Lyapunov stability proofs, and PID derivative elimination ($K_d \equiv 0$).
- [ ] Deliverable 7: `ENVIRONMENTAL_UNCERTAINTY_SPEC.md` published with 2,140-day empirical telemetry grounding, Kou MLE parameters, and 11-regime stochastic matrix.
- [ ] Deliverable 8: `ROBUSTNESS_DEFINITION.md` published with 4 formal robustness criteria, failure boundary geometry $\partial \Omega_{\text{fail}}$, and parameter fragility index $\bar{S}_T$.
- [ ] Deliverable 9: `EXPERIMENTAL_HIERARCHY.md` published formalizing the 7-Stage Adaptive Computational Sequence.
- [ ] Deliverable 10: `DECISION_FRAMEWORK.md` published formalizing multi-objective Pareto optimization, MCDA selection, and explicit criteria for evaluating $\text{A0}$.
- [ ] Deliverable 11: `RESEARCH_STATE.yaml` updated and verified against frozen baseline `SNAP-2026-08-30-01`.
- [ ] Concise Master Diagram embedded showing end-to-end lineage from Objectives $\to$ Constraints $\to$ Architectures $\to$ Parameters $\to$ Redistribution $\to$ Control $\to$ Uncertainty $\to$ Experiments $\to$ Robust Design.
- [ ] Strict Stop Rule Enforced: Zero large-scale simulations or optimization algorithms executed; exactly ONE minimum next execution block (Phase 1 Analytical Screening) specified.
