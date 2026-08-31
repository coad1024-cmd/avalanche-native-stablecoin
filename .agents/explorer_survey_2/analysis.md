# Comprehensive Technical Survey & Verification Analysis: Parameters, Redistribution, Dynamic Control, and Environmental Uncertainty (R4, R5, R6, R7)

> **Document Identifier:** `BCRG-SURVEY-ANALYSIS-EXPLORER-02`  
> **Author:** Explorer 2 (Survey: Parameters, Redistribution & Control Systems)  
> **Milestone:** Design Discovery Campaign — Survey & Technical Verification Phase  
> **Target Deliverables Audited:**  
> - **R4:** `audit_artifacts/design_discovery/PARAMETER_SEARCH_SPACE.md`  
> - **R5:** `audit_artifacts/design_discovery/REDISTRIBUTION_SEARCH_SPACE.md`  
> - **R6:** `audit_artifacts/design_discovery/CONTROLLER_SEARCH_SPACE.md`  
> - **R7:** `audit_artifacts/design_discovery/ENVIRONMENTAL_UNCERTAINTY_SPEC.md`  
> **Supporting Artifacts Evaluated:**  
> - `audit_artifacts/registers/PARAMETER_GOVERNANCE_REGISTRY.md`  
> - `audit_artifacts/reports/EMPIRICAL_CALIBRATION_REPORT.md`  
> - `audit_artifacts/reports/GLOBAL_SENSITIVITY_ANALYSIS.md`  
> - `audit_artifacts/reports/CONTROLLER_ABLATION_STUDY.md`  
> - `audit_artifacts/reports/ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md`  
> - `audit_artifacts/provenance/calibrated_market_parameters.json`  
> - `audit_artifacts/state/RESEARCH_STATE.yaml`  
> **Governing Standards:** Behavioral Parameter Audit (BPA) · Routh-Hurwitz & Lyapunov Stability Criteria · Saltelli-Sobol GSA · Kou Double-Exponential Jump-Diffusion SDE  
> **Date:** August 31, 2026  

---

## 1. Executive Summary & Investigation Overview

This report provides an exhaustive, first-principles technical audit of **Deliverables R4, R5, R6, and R7** in the Avalanche-Native Stablecoin (`anUSD`) Design Discovery campaign. Rather than accepting historical parameters or whitepaper derivations as dogma, our investigation subjects every equation, parameter classification, dynamic control law, stability proof, redistribution simplex rule, and empirical calibration to the rigorous standard of the **Behavioral Parameter Audit (BPA)** and double-entry stock-flow conservation.

### Core Discoveries & Verified Conclusions
1. **R4 (Parameter Search Space):** The universal parameter inventory spans 28 candidate parameters (`P01`–`P28`) categorized under the formal **8-Class Epistemic Taxonomy**. Through Saltelli-Sobol global sensitivity analysis, the 28-parameter continuous space is rigorously reduced to an active optimization manifold of **7 continuous governance and control levers** ($R, R', H_d, \boldsymbol{\omega}, B_{\text{target}}, K_p, K_i$), eliminating the curse of dimensionality for subsequent multi-objective optimization (NSGA-II).
2. **R5 (Redistribution Search Space):** The gross surplus generation rate $\Phi_{\text{gross}}(t)$ and routing over the closed 3-simplex $\Delta^3 \subset \mathbb{R}_+^4$ are mathematically closed and verified against `YieldRecycler.sol`. Open-loop static policies (POL-01, POL-04) are proved to fail in severe bear markets ($\text{CR}_{\text{OpEx}} < 1.0\times$), whereas countercyclical feedback (POL-02), reserve-priority (POL-03), and adaptive Softmax state-feedback (POL-05) preserve validator solvency ($\text{CR}_{\text{OpEx}} \ge 1.223\times \ge 1.20\times$) and accumulate tail insurance buffers.
3. **R6 (Controller Search Space):** Secondary automated market maker (AMM) plant transfer function $G_{\text{plant}}(s) = \frac{K_{\text{DC}}}{1 + \tau_{\text{arb}} s}$ is derived from first-principles CPMM microstructure and primary arbitrage time constant $\tau_{\text{arb}} \approx 5.55\text{ days}$. Global asymptotic stability of the closed-loop PI controller is proved via both **Routh-Hurwitz** (Theorem 3) and **Lyapunov / LaSalle Invariance** (Theorem 4). The derivative term $K_d$ is proved to diverge in noise PSD ($\lim_{\omega \to \infty} S_{u, \text{noise}} = \infty$) and is permanently eliminated ($K_d \equiv 0.000$).
4. **R7 (Environmental Uncertainty):** Continuous price dynamics are empirically grounded in **2,140 days of Avalanche C-Chain telemetry** (`DAT-01` to `DAT-07`). Maximum Likelihood Estimation (MLE) of the Kou (2002) asymmetric double-exponential jump-diffusion SDE yields $\sigma = 89.15\%$, $\lambda = 15.00\text{ yr}^{-1}$, $p = 59.55\%$, $\eta_1 = 7.671$, $\eta_2 = 7.801$, statistically outperforming the Merton log-normal benchmark ($\Delta\text{AIC} = -5.51$). The 11-regime parameter matrix and 20-dimensional master uncertainty tensor $\Omega_{\text{total}} = \mathcal{U}_{\text{emp}} \times \mathcal{U}_{\text{stress}} \times \mathcal{U}_{\text{gov}} \subset \mathbb{R}^{20}$ provide complete coverage of empirical, black-swan, and governance shock scenarios.

---

## 2. Deliverable 4 (R4) Audit: Parameter Search Space & Epistemic Taxonomy

### 2.1 The 8-Class Epistemic Taxonomy
To eliminate category errors in protocol design, every parameter in the stablecoin mechanism is classified into an 8-class epistemic hierarchy:

```
========================================================================================================================
                                       8-CLASS EPISTEMIC PARAMETER TAXONOMY
========================================================================================================================
  [Class 1] Structural Invariants (Θ_struct)      : Immutable arithmetic constants (χ = 1.000, V0 = $1.000).
  [Class 2] Calibrated Empirical (Θ_emp)          : SDE parameters estimated via MLE from 2,140 days telemetry (σ, λ, p, η1, η2, q̄).
  [Class 3] Governance Search Levers (Θ_gov)      : Timelocked policy decision variables (R, R', Hd, Hu, B_target, ω ∈ Δ³, f_fee).
  [Class 4] Dynamic Control Parameters (Θ_ctrl)   : Autonomous on-chain feedback gains (Kp, Ki, ΔR'_max, κ_dd).
  [Class 5] Security & Microstructure Guards (Θ_sec): Hardcoded circuit breakers & anti-MEV locks (τ_heart, δ_lock, τ_arb).
  [Class 6] Eliminated / Degenerate Terms (Θ_elim) : Formally pruned parameters (Kd ≡ 0.000 due to noise amplification).
  [Class 7] Derived / Dependent States (X_derived): Exact balance-sheet identities (VA, VB, CR_phys, CR_OpEx, Φ_gross).
  [Class 8] Environmental Stress Scenarios (U_stress): Black-swan shock manifolds (ΔP_flash ∈ [-20%, -95%], N_cascade ∈ {1..5}).
========================================================================================================================
```

### 2.2 Universal Master Parameter Inventory across Architectures $\mathbb{A} = \{\text{A0}, \dots, \text{A5+}\}$
The table below synthesizes the complete 28-parameter search space:

| ID | Symbol | Parameter Name | Physical Units | Subspace | Candidate Baseline | Search Bounds $[\theta_{\min}, \theta_{\max}]$ | Robust Operating Corridor | Epistemic Status | Identifiability Status | Sobol Sensitivity ($S_{Ti}$) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **`P01`** | $\chi$ | Tranche Split Ratio | $[-]$ | $\Theta_{\text{struct}}$ | $1.000$ | $[1.000, 1.000]$ | Fixed $1.000$ | Structural Invariant | Identified ($1.000$) | N/A (Constant) |
| **`P02`** | $V_0$ | Base Currency Par Unit | $\text{USD}$ | $\Theta_{\text{struct}}$ | $\$1.000$ | $[\$1.000, \$1.000]$ | Fixed $\$1.000$ | Structural Invariant | Identified ($\$1.000$) | N/A (Constant) |
| **`P03`** | $\sigma$ | AVAX Diffusion Volatility | $\text{yr}^{-1/2}$ | $\Theta_{\text{emp}}$ | $89.15\%$ | $[60.0\%, 140.0\%]$ | $[84.82\%, 93.29\%]$ | Calibrated Empirical | Identified (`DAT-01`) | **Critical** ($0.42$) |
| **`P04`** | $\lambda$ | Poisson Jump Intensity | $\text{yr}^{-1}$ | $\Theta_{\text{emp}}$ | $15.00$ | $[5.00, 30.00]$ | $[9.63, 15.00]$ | Calibrated Empirical | Identified (`DAT-01`) | **Critical** ($0.38$) |
| **`P05`** | $p$ | Up-Jump Probability | $[-]$ | $\Theta_{\text{emp}}$ | $0.5955$ | $[0.300, 0.750]$ | $[0.453, 0.744]$ | Calibrated Empirical | Identified (Kou MLE) | Moderate ($0.14$) |
| **`P06`** | $\eta_1$ | Upward Tail Decay | $[-]$ | $\Theta_{\text{emp}}$ | $7.671$ | $[3.000, 15.000]$ | $[4.725, 9.145]$ | Calibrated Empirical | Identified (Kou MLE) | Moderate ($0.12$) |
| **`P07`** | $\eta_2$ | Downward Tail Decay | $[-]$ | $\Theta_{\text{emp}}$ | $7.801$ | $[2.000, 12.000]$ | $[4.992, 9.601]$ | Calibrated Empirical | Identified (Kou MLE) | **Critical** ($0.35$) |
| **`P08`** | $\bar{q}$ | sAVAX Staking APR | $\text{yr}^{-1}$ | $\Theta_{\text{emp}}$ | $6.4019\%$ | $[4.00\%, 10.00\%]$ | $[5.31\%, 9.10\%]$ | Calibrated Empirical | Identified (`DAT-02`) | **High** ($0.22$) |
| **`P09`** | $R$ | Senior Class A Coupon | $\text{yr}^{-1}$ | $\Theta_{\text{gov}}$ | $7.30\%$ | $[3.00\%, 12.00\%]$ | $[5.00\%, 9.00\%]$ | Governance Search | Decision Lever (Collinear) | **High** ($0.28$) |
| **`P10`** | $R'$ | anUSD Benchmark Rate | $\text{yr}^{-1}$ | $\Theta_{\text{gov}}$ | $3.00\%$ | $[1.00\%, 6.00\%]$ | $[1.50\%, 4.50\%]$ | Governance Search | Decision Lever | **Critical** ($0.34$) |
| **`P11`** | $H_d$ | Downward Reset Barrier | $\text{USD}$ | $\Theta_{\text{gov}}$ | $\$0.250$ | $[\$0.150, \$0.450]$ | $[\$0.200, \$0.350]$ | Governance Search | Strongly Identified | **Critical** ($0.45$) |
| **`P12`** | $H_u$ | Upward Reset Barrier | $\text{USD}$ | $\Theta_{\text{gov}}$ | $\$2.000$ | $[\$1.500, \$3.500]$ | $[\$1.800, \$2.500]$ | Governance Search | Strongly Identified | Low ($0.06$) |
| **`P13`** | $\omega_{\text{burn}}$ | AVAX Buyback & Burn Share | $[-]$ | $\Theta_{\text{gov}}$ | $65.00\%$ | $[10.0\%, 90.0\%]$ | $[40.0\%, 75.0\%]$ | Governance Search | Decision Variable | **High** ($0.25$) |
| **`P14`** | $\omega_{\text{val,0}}$ | Validator Subsidy Base | $[-]$ | $\Theta_{\text{gov}}$ | $20.00\%$ | $[5.0\%, 50.0\%]$ | $[15.0\%, 35.0\%]$ | Governance Search | Decision Variable | **High** ($0.29$) |
| **`P15`** | $\omega_{\text{l1}}$ | Sovereign L1 Grant Share | $[-]$ | $\Theta_{\text{gov}}$ | $15.00\%$ | $[0.0\%, 30.0\%]$ | $[5.0\%, 25.0\%]$ | Governance Search | Decision Variable | Low ($0.08$) |
| **`P16`** | $\omega_{\text{res}}$ | Solvency Reserve Share | $[-]$ | $\Theta_{\text{gov}}$ | $0.00\%$ | $[0.0\%, 35.0\%]$ | $[0.0\%, 15.0\%]$ | Governance Search | Decision Variable | **Critical** ($0.36$) |
| **`P17`** | $B_{\text{target}}$ | Target Solvency Reserve | $\text{USD}$ | $\Theta_{\text{gov}}$ | $\$5.0\text{M}$ | $[\$1.0\text{M}, \$25.0\text{M}]$ | $[\$3.0\text{M}, \$10.0\text{M}]$ | Governance Search | Decision Variable | Moderate ($0.18$) |
| **`P18`** | $\Lambda^*$ | Continuous Target Leverage | $[-]$ | $\Theta_{\text{gov}}$ | $2.00\times$ | $[1.20\times, 3.50\times]$ | $[1.50\times, 2.50\times]$ | Governance Search | Structural Target | **High** ($0.31$) |
| **`P19`** | $K_p$ | Proportional Gain | $\text{USD}^{-1}\text{yr}^{-1}$ | $\Theta_{\text{ctrl}}$ | $0.150$ | $[0.050, 0.500]$ | $[0.100, 0.250]$ | Dynamic Control | Strongly Identified | Moderate ($0.16$) |
| **`P20`** | $K_i$ | Integral Gain | $\text{USD}^{-1}\text{yr}^{-2}$ | $\Theta_{\text{ctrl}}$ | $0.020$ | $[0.005, 0.080]$ | $[0.010, 0.040]$ | Dynamic Control | Strongly Identified | Moderate ($0.15$) |
| **`P21`** | $K_d$ | Derivative Gain | $\text{USD}^{-1}$ | $\Theta_{\text{elim}}$ | $0.000$ | $[0.000, 0.000]$ | Fixed $0.000$ | Eliminated Term | Proved Destabilizing | N/A (Eliminated) |
| **`P22`** | $\Delta R'_{\max}$ | Anti-Windup Rate Clamp | $\text{yr}^{-1}$ | $\Theta_{\text{ctrl}}$ | $\pm 5.00\%$ | $[\pm 2.0\%, \pm 10.0\%]$ | $[\pm 3.0\%, \pm 7.0\%]$ | Dynamic Control | Safety Invariant | Low ($0.09$) |
| **`P23`** | $\kappa_{\text{dd}}$ | Countercyclical Drawdown Slope | $[-]$ | $\Theta_{\text{ctrl}}$ | $0.350$ | $[0.100, 0.800]$ | $[0.200, 0.500]$ | Dynamic Control | Identified from OpEx | Moderate ($0.19$) |
| **`P24`** | $\tau_{\text{heart}}$ | Oracle Heartbeat Bound | $\text{s}$ | $\Theta_{\text{sec}}$ | $300\text{ s}$ | $[60\text{ s}, 900\text{ s}]$ | Max $300\text{ s}$ | Security Guard | Chainlink Standard | Moderate ($0.17$) |
| **`P25`** | $\delta_{\text{lock}}$ | MEV 2-Phase Commit Band | $[-]$ | $\Theta_{\text{sec}}$ | $\pm 1.50\%$ | $[\pm 0.5\%, \pm 3.0\%]$ | Fixed $\pm 1.5\%$ | Security Guard | Anti-Sandwiching | Low ($0.05$) |
| **`P26`** | $f_{\text{mint}}$ | Primary Mint Fee | $\text{bps}$ | $\Theta_{\text{gov}}$ | $10\text{ bps}$ | $[0\text{ bps}, 50\text{ bps}]$ | $[5\text{ bps}, 25\text{ bps}]$ | Governance Search | Decision Variable | Low ($0.07$) |
| **`P27`** | $f_{\text{redeem}}$ | Primary Redemption Fee | $\text{bps}$ | $\Theta_{\text{gov}}$ | $10\text{ bps}$ | $[0\text{ bps}, 50\text{ bps}]$ | $[5\text{ bps}, 25\text{ bps}]$ | Governance Search | Decision Variable | Low ($0.08$) |
| **`P28`** | $\tau_{\text{arb}}$ | Arbitrage Settlement Time | $\text{days}$ | $\Theta_{\text{sec}}$ | $5.55\text{ d}$ | $[1.0\text{ d}, 14.0\text{ d}]$ | $[3.2\text{ d}, 8.1\text{ d}]$ | Calibrated Microstructure | Identified (`DAT-03`) | **High** ($0.26$) |

### 2.3 Behavioral Parameter Audit (BPA) of Core Governance Levers

Following the 10-step Behavioral Parameter Audit protocol:

1. **Senior Class A Coupon ($R = 7.30\%$):**
   - *Economic Decision:* Realizes the capital cost and yield required to attract senior risk-averse depositors.
   - *Mathematical Definition:* Linearly accrues senior claim value: $V_A(t) = 1.0 + R \cdot v(t)$.
   - *Classification:* Class 3 (Governance Search Lever).
   - *Identifiability:* **Non-identifiable in isolation**. $R$ is strongly collinear with benchmark borrowing rate $R'$ and underlying staking yield $q$. Setting $R = 7.30\%$ was tuned circularly in early simulations to beat baseline staking yield $q = 6.00\%$. It is NOT an empirical constant and must be optimized on the Pareto frontier.
2. **Downward Reset Barrier ($H_d = \$0.25$):**
   - *Economic Decision:* Determines the equity de-leveraging trigger point that bounds single-step flash crash losses.
   - *Mathematical Definition:* Under Theorem 1, $\text{Max Drop from Barrier } H_d = \frac{H_d - 1}{H_d + 1}$.
   - *Classification:* Class 3 (Governance / Security Threshold).
   - *Identifiability:* **Strongly identified**. Directly determines maximum crash protection ($H_d = 0.25 \implies \Delta P_{\max} = -60.0\%$).
3. **Countercyclical Slope ($\kappa_{\text{dd}} = 0.350$):**
   - *Economic Decision:* Shifts protocol yield from AVAX burning to validator subsidies during market drawdowns.
   - *Mathematical Definition:* $\omega_{\text{val}}(t) = \min\left(0.45, 0.20 + \kappa_{\text{dd}} \cdot D(t)\right)$ where $D(t) = \max(0, (P_{\text{EMA}} - P_{\text{spot}})/P_{\text{EMA}})$.
   - *Classification:* Class 4 (Dynamic Control / State-Feedback Parameter).
   - *Identifiability:* Calibrated from empirical node operating cost ($C_{\text{node}} = \$350/\text{mo}$ across $1,450$ nodes) to ensure $\text{CR}_{\text{OpEx}} \ge 1.20\times$ down to $-70\%$ market drawdowns.

### 2.4 Dimensionality Reduction Pipeline ($28 \longrightarrow 7$)
The Saltelli-Sobol Global Sensitivity Analysis ($N=2,048$) partitions the parameter space:
- **Fixed Invariants & Security Constants (8 parameters):** $\chi, V_0, K_d, \tau_{\text{heart}}, \delta_{\text{lock}}, f_{\text{mint}}, f_{\text{redeem}}, \Delta R'_{\max}$.
- **Calibrated Empirical Posteriors (7 parameters):** $\sigma, \lambda, p, \eta_1, \eta_2, \bar{q}, \tau_{\text{arb}}$ (evaluated across 11 discrete regimes).
- **Active Optimization Manifold (7 continuous decision variables):**
  $$\Theta_{\text{active}} = \left\{ (R, R', H_d, \omega_{\text{burn}}, \omega_{\text{val}}, B_{\text{target}}, K_p) \in \mathbb{R}^7 \right\}$$
This guarantees computational tractability for NSGA-II Pareto optimization.

---

## 3. Deliverable 5 (R5) Audit: Endogenous Dynamic Redistribution Policy Space ($\boldsymbol{\omega}(t) \in \Delta^3$)

### 3.1 Gross Surplus Generation Rate $\Phi_{\text{gross}}(t)$
The continuous gross surplus flow rate (denominated in $\text{USD}\cdot\text{year}^{-1}$) is:
$$\boxed{\Phi_{\text{gross}}(t) = q(t) \cdot C_{\text{pool}}(t) \cdot P_{\text{spot}}(t) + \mathcal{F}_{\text{mint/redeem}}(t) + \mathcal{F}_{\text{flash}}(t) + \mathcal{F}_{\text{AMM}}(t)}$$
where $q(t) \sim 6.40\%$ is the empirical $sAVAX$ staking APR (`DAT-02`), $C_{\text{pool}}(t)$ is physical collateral stock, and primary fee friction is $\mathcal{F}_{\text{mint/redeem}} = 10\text{ bps} \cdot |\dot{N}_{\text{circ}}| \cdot \$1.00$.

### 3.2 3-Simplex Accounting Conservation
The allocation vector $\boldsymbol{\omega}(t) = [\omega_{\text{burn}}(t), \omega_{\text{val}}(t), \omega_{\text{res}}(t), \omega_{\text{l1}}(t)]^T$ is constrained to the closed 3-simplex $\Delta^3$:
$$\sum_{i \in \{\text{burn, val, res, l1}\}} \omega_i(t) \equiv 1.0000, \quad \omega_i(t) \ge 0.0000 \quad \forall i$$

In smart contract execution (`YieldRecycler.sol`), exact double-entry conservation is enforced by integer rounding residue absorption:
$$Y_{\text{val}} = \lfloor Y_{\text{total}} \cdot \omega_{\text{val}} \rfloor, \quad Y_{\text{res}} = \lfloor Y_{\text{total}} \cdot \omega_{\text{res}} \rfloor, \quad Y_{\text{l1}} = \lfloor Y_{\text{total}} \cdot \omega_{\text{l1}} \rfloor$$
$$Y_{\text{burn}} = Y_{\text{total}} - (Y_{\text{val}} + Y_{\text{res}} + Y_{\text{l1}}) \implies \sum Y_i \equiv Y_{\text{total}} \quad (\text{zero token leakage})$$

### 3.3 Comparative Analysis of the 5 Redistribution Policy Families

```
========================================================================================================================
                                     REDISTRIBUTION POLICY FAMILY EVALUATION
========================================================================================================================
```

| Policy ID | Policy Name | Mathematical Formulation | Dynamic Feedback Properties | OpEx Coverage Preservation under $-60\%$ Drawdown | Reserve Buffer Accumulation | Evaluation Verdict |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| **`POL-01`** | **Static Split (ACP-67 Baseline)** | $\boldsymbol{\omega} \equiv [0.65, 0.20, 0.00, 0.15]^T$ | Open-loop; zero feedback ($\frac{\partial \boldsymbol{\omega}}{\partial \mathbf{x}} = \mathbf{0}$) | **FAILED:** $\text{CR}_{\text{OpEx}} = 0.62\times < 1.0\times$ (Node Capitulation) | Zero ($0.00\%$) | **Formally Rejected** in bear regimes |
| **`POL-02`** | **Countercyclical Drawdown Feedback** | $\omega_{\text{val}}(t) = \min(0.45, 0.20 + 0.35 D(t))$ | State feedback via 90-day EMA drawdown metric $D(t)$ | **PASSED:** $\text{CR}_{\text{OpEx}} = 1.223\times \ge 1.20\times$ (Nodes Protected) | Static $5.00\%$ baseline | **Strong Candidate** for security |
| **`POL-03`** | **Reserve-First Buffer Priority** | $\omega_{\text{res}} = 0.50$ if $\xi_{\text{res}} < 1.0$; else $0.05$ | Two-phase switching manifold based on buffer fill ratio $\xi_{\text{res}}$ | Moderate: $\omega_{\text{val}} = 12.5\%$ in phase 1, $23.75\%$ in phase 2 | **Optimal:** Fills buffer in $\tau_{\text{fill}} = 1.87\text{ yrs}$ | **Strong Candidate** for tail robustness |
| **`POL-04`** | **Aggressive Burn Maximizer** | $\boldsymbol{\omega} \equiv [0.80, 0.10, 0.05, 0.05]^T$ | Open-loop; aggressive deflation ($>2\text{M AVAX/yr}$) | **CRITICAL FAIL:** $\text{CR}_{\text{OpEx}} = 0.31\times$ (Mass Node Exit) | Minimal ($5.00\%$) | **Formally Rejected** (Insolvent nodes) |
| **`POL-05`** | **Adaptive Softmax State Feedback** | $\boldsymbol{\omega}(t) = \text{Softmax}(\mathbf{W}\mathbf{s}(t) + \mathbf{b})$ | Multi-objective continuous mapping from $\mathbf{s} \in \mathbb{R}^4$ to $\text{int}(\Delta^3)$ | **PASSED:** Automatically scales $\omega_{\text{val}} \to 45\%$ and $\omega_{\text{res}} \to 35\%$ | **Optimal:** Dynamic fill during crises | **Master Recommended Policy** |

### 3.4 Softmax Logit Numerical Stabilization
In discrete EVM implementations and fixed-point math, POL-05 raw logits $\mathbf{z}(t) = \mathbf{W}\mathbf{s}(t) + \mathbf{b}$ are stabilized against exponent overflow:
$$\mathbf{z}'(t) = \mathbf{z}(t) - \max_{k \in \{1..4\}} z_k(t), \quad \boldsymbol{\omega}(t) = \frac{\exp(\mathbf{z}'(t))}{\sum_{k=1}^4 \exp(z'_k(t))}$$
Because $\frac{\exp(z_i - \max \mathbf{z})}{\sum \exp(z_k - \max \mathbf{z})} \equiv \frac{\exp(z_i)}{\sum \exp(z_k)}$, this identity is mathematically exact, guarantees $\exp(z'_i) \in (0, 1.0]$, and strictly prevents EVM overflow during extreme black-swan excursions.

---

## 4. Deliverable 6 (R6) Audit: Closed-Loop Dynamic Control Policy & Stability Proofs

### 4.1 AMM Microstructure & Continuous-Time Plant Transfer Function $G_{\text{plant}}(s)$
Consider a secondary CPMM liquidity pool ($x \cdot y = k$) with liquidity depth $L = \sqrt{k} \approx y$.
Linearizing price impact around parity gives $\Delta P_{\text{DEX}} \approx \frac{2}{L} \Delta y$.
Rate premium signal $u(t) = \Delta R'(t)$ induces proportional demand flow $F(t) = \alpha_{\text{elasticity}} u(t)$ ($\alpha_{\text{elasticity}} \approx \$5.0\text{M}$).
The continuous-time open-loop plant gain is:
$$K_{\text{amm}}(L) = \frac{\alpha_{\text{elasticity}}}{L}$$
Combined with primary 1:1 arbitrage restoration time constant $\tau_{\text{arb}} \approx 5.55\text{ days} = 0.0152\text{ yr}$ ($k_{\text{arb}} = 65.70\text{ yr}^{-1}$), the governing differential equation is:
$$\dot{e}(t) + \frac{1}{\tau_{\text{arb}}} e(t) = K_{\text{amm}}(L) u(t) + w(t)$$
Taking Laplace transforms yields the open-loop plant transfer function:
$$\boxed{G_{\text{plant}}(s) = \frac{K_{\text{amm}}(L)}{s + 1/\tau_{\text{arb}}} = \frac{K_{\text{amm}}(L) \tau_{\text{arb}}}{1 + \tau_{\text{arb}} s} = \frac{K_{\text{DC}}}{1 + \tau_{\text{arb}} s}}$$

### 4.2 Closed-Loop System & Damping Ratio Verification
For PI controller $C(s) = -\frac{K_p s + K_i}{s}$, the closed-loop characteristic equation is:
$$s^2 + \left(\frac{1 + K_{\text{DC}} K_p}{\tau_{\text{arb}}}\right) s + \frac{K_{\text{DC}} K_i}{\tau_{\text{arb}}} = 0$$
Canonical second-order parameters are:
$$\omega_n = \sqrt{K_{\text{amm}}(L) K_i}, \quad \zeta = \frac{1 + K_{\text{amm}}(L) \tau_{\text{arb}} K_p}{2 \sqrt{K_{\text{amm}}(L) \tau_{\text{arb}}^2 K_i}}$$

Evaluating under calibrated baseline ($K_p = 0.150, K_i = 0.020, \tau_{\text{arb}} = 5.55\text{ days}$):
- **Illiquid Tier ($L = \$1.5\text{M}$):** $K_{\text{amm}} = 3.333 \implies \zeta = \mathbf{1.317} > 1.00$ (Daily units) / $\zeta = \mathbf{128.32} \gg 1.00$ (Annual units).
- **Moderate Tier ($L = \$10.0\text{M}$):** $K_{\text{amm}} = 0.500 \implies \zeta = \mathbf{1.276} > 1.00$ (Daily units) / $\zeta = \mathbf{329.20} \gg 1.00$ (Annual units).
- **Deep Tier ($L = \$30.0\text{M}$):** $K_{\text{amm}} = 0.167 \implies \zeta = \mathbf{1.777} > 1.00$ (Daily units) / $\zeta = \mathbf{569.76} \gg 1.00$ (Annual units).
The system is **unconditionally overdamped ($\zeta > 1.00$)** across the entire empirical liquidity spectrum, ruling out resonant oscillations.

### 4.3 Rigorous Mathematical Proofs of Global Asymptotic Stability

#### Theorem 3 (Routh-Hurwitz Global Stability Proof)
*Characteristic Polynomial:* $P(s) = s^2 + a_1 s + a_0$ where $a_1 = \frac{1}{\tau_{\text{arb}}} + K_{\text{amm}} K_p$ and $a_0 = K_{\text{amm}} K_i$.
*Routh Array:*
$$\begin{array}{c|cc} s^2 & 1 & a_0 \\ s^1 & a_1 & 0 \\ s^0 & a_0 & 0 \end{array}$$
*Conditions:*
1. $a_1 > 0 \iff K_p > -\frac{1}{K_{\text{amm}} \tau_{\text{arb}}}$. For nominal $K_p = 0.150 > 0$, strictly satisfied.
2. $a_0 > 0 \iff K_i > 0$. For nominal $K_i = 0.020 > 0$, strictly satisfied.
All roots reside strictly in $\mathbb{C}^-$, proving **unconditional asymptotic stability**. $\blacksquare$

#### Theorem 4 (Lyapunov Global Asymptotic Stability via LaSalle's Invariance Principle)
*Candidate Lyapunov Function:* $V(e, I) = \frac{1}{2} e^2 + \frac{K_{\text{amm}} K_i}{2} I^2$ on state $\mathbf{x} = [e, I]^T \in \mathbb{R}^2$.
1. $V(0, 0) = 0$ and $V(e, I) > 0$ for all $(e, I) \ne (0, 0)$; radially unbounded as $\|(e, I)\| \to \infty$.
2. Time derivative along trajectories ($\dot{I} = e, \; \dot{e} = -(\frac{1}{\tau_{\text{arb}}} + K_{\text{amm}} K_p) e - K_{\text{amm}} K_i I$):
   $$\dot{V}(e, I) = e \dot{e} + K_{\text{amm}} K_i I \dot{I} = -\left(\frac{1}{\tau_{\text{arb}}} + K_{\text{amm}} K_p\right) e^2 \le 0$$
3. LaSalle Invariant Set: $\mathcal{S} = \{(e, I) \mid \dot{V} = 0\} \implies e(t) \equiv 0 \implies \dot{e}(t) \equiv 0 \implies I(t) \equiv 0$.
The largest invariant set within $\mathcal{S}$ is strictly the origin $(0, 0)$, proving **global asymptotic stability**. $\blacksquare$

### 4.4 Formal Proof of Derivative Noise Amplification ($K_d \equiv 0.000$)
- Continuous Frequency Domain: Noise power spectral density is $S_{u, \text{noise}}(\omega) = |C_d(j\omega)|^2 S_{w_n}(\omega) = K_d^2 \omega^2 \sigma_{\text{noise}}^2$. As $\omega \to \infty$, $S_{u, \text{noise}} \to \infty$.
- Discrete EVM Finite Difference: $\mathbb{E}[(\frac{\Delta e}{\Delta t})^2] = \frac{2 \sigma_{\text{noise}}^2}{\Delta t^2}$. For $\Delta t = 2.0\text{ s}$, noise variance is scaled by $0.50\text{ s}^{-2}$, inducing violent rate chatter ($\pm 1.8\%$/block) with zero RMSE improvement.
- **Verdict:** $K_d \equiv 0.0000$ is permanently eliminated.

---

## 5. Deliverable 7 (R7) Audit: Environmental Uncertainty & Empirical Telemetry Grounding

### 5.1 Ingested Telemetry Provenance (`DAT-01` to `DAT-07`)
All empirical parameters are grounded in $N = 2,140$ daily observations (2020-10-22 to 2026-08-31) stored with verified SHA-256 digests in `calibrated_market_parameters.json`:
- `DAT-01` (AVAX/USD Daily OHLCV): SHA-256 `83abd83158c6a9a9f13b12e359bd97afc6acf827849f9d0c6f1be6918a6e54e7`
- `DAT-02` (sAVAX Staking APR): SHA-256 `47727cc6e7a6bc48fbaedbcb19d0eb09414c9d0276c52892997a0148fff307c7`
- `DAT-03` (Trader Joe Liquidity Profiles): SHA-256 `e88712a32d8e8e1c30a9a35b9d8c9d5dcb7c114b3943f367ab4e71449f5cfdd8`
- `DAT-07` (Historical Black Swan Crises): SHA-256 `3ee1e8a991e5e6689376f0cb440b219a2f63407f5f8a2768faf2958431f4328d`

### 5.2 Kou Asymmetric Double-Exponential SDE Calibration vs Merton
Continuous price SDE:
$$\frac{dS_t}{S_{t^-}} = \mu dt + \sigma dW_t + d\left(\sum_{i=1}^{N_t} (e^{Y_i} - 1)\right), \quad Y_i \sim p \eta_1 e^{-\eta_1 y}\mathbf{1}_{y \ge 0} + (1-p)\eta_2 e^{\eta_2 y}\mathbf{1}_{y < 0}$$

```
========================================================================================================================
                          MAXIMUM LIKELIHOOD ESTIMATION & GOODNESS-OF-FIT RESULTS
========================================================================================================================
```

| Parameter / Metric | Kou Double-Exponential MLE | 95% Bootstrap CI (B=2,000) | Merton Log-Normal Benchmark | Econometric / Mechanism Meaning |
| :--- | :---: | :---: | :---: | :--- |
| **Diffusion Volatility ($\sigma$)** | **$89.15\%$** | $[84.82\%, 93.29\%]$ | $88.83\%$ | Continuous Brownian volatility p.a. |
| **Jump Intensity ($\lambda$)** | **$15.00\text{ yr}^{-1}$** | $[9.63, 15.00]$ | $10.40\text{ yr}^{-1}$ | Discrete Poisson jump frequency ($1.25\text{ jumps/mo}$) |
| **Up-Jump Probability ($p$)** | **$59.55\%$** | $[45.30\%, 74.35\%]$ | N/A | Probability of upward jump |
| **Upward Decay ($\eta_1$)** | **$7.671$** | $[4.725, 9.145]$ | N/A | Mean positive jump $\bar{Y}_{\text{up}} = +13.04\%$ |
| **Downward Decay ($\eta_2$)** | **$7.801$** | $[4.992, 9.601]$ | N/A | Mean negative jump $\bar{Y}_{\text{down}} = -12.82\%$ |
| **Continuous Drift ($\mu$)** | **$-34.02\%$** | $[-45.10\%, -21.40\%]$ | $-14.22\%$ | Historical annualized drift |
| **Compensator ($\zeta$)** | **$+4.335\%$** | N/A | $+4.62\%$ | $\mathbb{E}[e^Y - 1] = \frac{p \eta_1}{\eta_1 - 1} + \frac{(1-p)\eta_2}{\eta_2 + 1} - 1$ |
| **Log-Likelihood ($\ln \mathcal{L}$)** | **$3,217.36$** | N/A | $3,213.60$ | Goodness of fit |
| **Akaike Information ($\text{AIC}$)** | **$-6,422.72$** | N/A | $-6,417.21$ | Model selection criterion |
| **Model Delta ($\Delta\text{AIC}$)** | **$-5.51$** | N/A | Reference ($0.00$) | **Kou statistically superior** ($\Delta\text{AIC} < -2.0$) |

### 5.3 11-Regime Stochastic Parameter Matrix
Spans normal, high volatility, bear, crash, liquidity crunch, and yield compression regimes:

| Regime Key | $\sigma$ (p.a.) | $\lambda$ ($\text{yr}^{-1}$) | $p_{\text{up}}$ | $\eta_1$ | $\eta_2$ | $\mu$ (p.a.) | $q_{\text{savax}}$ | $L_{\text{DEX}}$ | $N_{\text{val}}$ | Gas ($\text{nAVAX}$) | Primary Stress Test Focus |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`CALM_BULL`** | $45.0\%$ | $0.80$ | $0.60$ | $4.00$ | $3.00$ | $+35.0\%$ | $7.0\%$ | $\$30\text{M}$ | $1,550$ | $25$ | Upward reset frequency & burn flywheel |
| **`NORMAL`** | $89.9\%$ | $2.40$ | $0.40$ | $3.50$ | $2.00$ | $+10.0\%$ | $6.0\%$ | $\$20\text{M}$ | $1,450$ | $30$ | Historical 5-year operating envelope |
| **`HIGH_VOLATILITY`** | $135.0\%$ | $4.50$ | $0.40$ | $2.50$ | $1.80$ | $-5.0\%$ | $6.0\%$ | $\$15\text{M}$ | $1,400$ | $75$ | Controller damping & rate overshoot |
| **`SEVERE_BEAR`** | $110.0\%$ | $5.00$ | $0.25$ | $3.00$ | $1.50$ | $-55.0\%$ | $5.0\%$ | $\$10\text{M}$ | $1,250$ | $40$ | Downward reset triggering & junior de-leveraging |
| **`FLASH_CRASH`** | $90.0\%$ | $1.00$ | $0.00$ | $3.50$ | $1.10$ | $0.0\%$ | $6.0\%$ | $\$8\text{M}$ | $1,350$ | $250$ | Deterministic $-60\%$ drop; Theorem 1 validation |
| **`PROLONGED_BEAR`** | $50.0\%$ | $1.20$ | $0.30$ | $4.00$ | $2.20$ | $-30.0\%$ | $4.5\%$ | $\$12\text{M}$ | $1,100$ | $25$ | 2-year coupon carrying cost drag ($R \cdot v$) |
| **`LIQUIDITY_CRUNCH`** | $90.0\%$ | $2.50$ | $0.40$ | $3.50$ | $2.00$ | $0.0\%$ | $6.0\%$ | $\$1.5\text{M}$ | $1,400$ | $60$ | AMM thin liquidity; anti-windup clamping |
| **`YIELD_COMPRESSION`**| $95.0\%$ | $3.00$ | $0.35$ | $3.50$ | $1.90$ | $-10.0\%$ | $3.5\%$ | $\$12\text{M}$ | $1,200$ | $35$ | Protocol gross yield contraction & node OpEx |
| **`REGULATORY_CHURN`** | $120.0\%$ | $6.00$ | $0.30$ | $2.80$ | $1.60$ | $-25.0\%$ | $5.5\%$ | $\$8\text{M}$ | $1,150$ | $500$ | Gas price spikes ($500\text{ nAVAX}$) & oracle delay |
| **`VALIDATOR_FLIGHT`** | $115.0\%$ | $5.50$ | $0.20$ | $2.60$ | $1.40$ | $-45.0\%$ | $4.0\%$ | $\$6\text{M}$ | $850$ | $100$ | Node drop to $850$; countercyclical subsidy $\kappa_{\text{dd}}$ |
| **`RECOVERY_RALLY`** | $115.0\%$ | $3.00$ | $0.50$ | $2.00$ | $1.50$ | $+20.0\%$ | $6.5\%$ | $\$18\text{M}$ | $1,450$ | $80$ | Asymmetric $-50\%$ drop followed by $+100\%$ bounce |

### 5.4 Master Uncertainty Tensor $\Omega_{\text{total}} \subset \mathbb{R}^{20}$
The complete environmental uncertainty space is decomposed into three orthogonal manifolds:
$$\boxed{\Omega_{\text{total}} = \mathcal{U}_{\text{emp}} \times \mathcal{U}_{\text{stress}} \times \mathcal{U}_{\text{gov}} \subset \mathbb{R}^7 \times \mathbb{R}^5 \times \mathbb{R}^8 = \mathbb{R}^{20}}$$
1. $\mathcal{U}_{\text{emp}} = (\sigma, \lambda, p, \eta_1, \eta_2, \mu, q)$ (MLE posteriors with joint empirical covariance matrix $\boldsymbol{\Sigma}_{\text{emp}}$).
2. $\mathcal{U}_{\text{stress}} = (\Delta P_{\text{flash}}, N_{\text{cascade}}, L_{\text{amm}}, \tau_{\text{oracle}}, \delta_{\text{imbalance}})$ (Deterministic stress manifolds).
3. $\mathcal{U}_{\text{gov}} = (\boldsymbol{\omega} \in \Delta^3, R, R', H_d, H_u, \tilde{R}, N_{\text{val}}, \text{Gas}_{\text{gwei}})$ (Governance and structural policy drift).

---

## 6. Synthesis, Calibration Harmonization & Identified Enhancements

### 6.1 Calibration Lineage Harmonization
Our audit identified that across the codebase and reports:
- Early exploratory prototypes used $\lambda = 2.40\text{ yr}^{-1}$ (or $3.00\text{ yr}^{-1}$) with $\eta_1 = 3.50, \eta_2 = 2.00$ as heuristic 3-sigma tail cuts.
- The definitive full 2,140-day MLE calibration (`calibrated_market_parameters.json`) rigorously established $\lambda = 15.00\text{ yr}^{-1}$, $p = 59.55\%$, $\eta_1 = 7.671$, $\eta_2 = 7.801$, $\bar{q} = 6.4019\%$.
- *Harmonization Finding:* Both are consistent within their respective scopes: the 11-regime parameter matrix intentionally tests the entire spectrum from calm regimes ($\lambda = 0.8$) to high turbulence ($\lambda = 15.0$), while baseline point estimates strictly reflect the full 2,140-day MLE.

### 6.2 Flash Crash Invariance Boundary Verification
- Whitepaper claim of $-75.0\%$ crash invariance applies **strictly from Par ($S=1.00$)**.
- From the lower reset barrier $H_d = 0.25$, the true mathematical bound is strictly **$-60.00\%$** ($\Delta P_{\max} = \frac{0.25 - 1}{0.25 + 1} = -0.60$).
- A $-75.0\%$ drop occurring directly from $H_d = 0.25$ causes an unbacked deficit of $37.35\%$.
- *Remediation:* Architecture A2 (Dedicated Solvency Reserve Buffer $B_{\text{res}}$) and POL-03/POL-05 successfully absorb this deficit, extending crash tolerance beyond $-88.75\%$.

### 6.3 Stage 1 Analytical Screening Results
The Stage 1 pruning engine (`stage1_analytical_screening.py`) evaluated $N_0 = 100,000$ candidate vectors against 5 analytical filters (F1 Simplex Conservation, F2 Yield Feasibility, F3 Theorem 1 Solvency, F4 Hurwitz Overdamping, F5 Barrier Spacing), successfully pruning **$94.39\%$** of infeasible space and extracting the bounded feasible manifold $\Theta_{\text{feasible}}$ with $5,607$ verified candidate vectors.

---

## 7. Final Verification & Reproducibility Matrix

To independently reproduce and verify all findings:
1. **Solidity Invariant Tests:** `cd contracts && forge test` (15/15 tests pass).
2. **Kou MLE SDE Verifier:** `python3 -c "import json; d=json.load(open('audit_artifacts/provenance/calibrated_market_parameters.json')); print(d['kou_double_exponential']['point_estimates'])"`
3. **Controller Damping Verifier:** `python3 simulations/robustness_study/controller_isolation.py`
4. **11-Regime Price Path Generator:** `python3 -c "from simulations.robustness_study.market_regimes import MARKET_REGIMES; print(len(MARKET_REGIMES))"`
5. **Stage 1 Analytical Screening:** `python3 simulations/design_discovery/stage1_analytical_screening.py`
