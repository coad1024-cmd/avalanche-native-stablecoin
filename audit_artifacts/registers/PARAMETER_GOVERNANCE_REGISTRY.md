# Parameter Governance Registry & Robust Operating Corridors

> **Document Identifier:** `BCRG-REGISTRY-2026-PARAMETER-GOVERNANCE-01`  
> **Governing Plan:** `BCRG-PLAN-2026-REVISED-MECHANISM-RESEARCH-02` (Phase 13)  
> **Classification Framework:** 8-Class Epistemic Parameter Taxonomy  
> **Baseline Snapshot ID:** `SNAP-2026-08-30-01` (Git Commit: `d57b3e601ca87733ec4343dbb70c7514ab264939`)  
> **Date:** August 30, 2026  

> [!NOTE]
> **Epistemic Status of Baseline Values:**  
> - **Structural Invariants (`P01`–`P02`):** Mathematically fixed system constants.  
> - **Empirical Calibrations (`P03`–`P08`):** Point estimates and 95% CIs calibrated directly from Avalanche C-Chain telemetry.  
> - **Governance & Control Parameters (`P09`–`P20`):** Designated strictly as **"Current Candidate Baseline (Unvalidated Initial Proposal)"** for snapshot baseline tracking. They are **NOT** validated optima. The upcoming Research Design Discovery and Multi-Objective Search phase will rigorously evaluate whether these candidate values deserve to survive or must be superseded on the Pareto frontier.

---

## 1. The 8-Class Epistemic Parameter Catalog

```
====================================================================================================
                        UNIFIED 8-CLASS PARAMETER GOVERNANCE REGISTRY
====================================================================================================
```

| ID | Parameter Name | Symbol | Epistemic Class | Baseline Value (Candidate / Calibrated) | Robust Governance Operating Corridor | Governance Authority & Timelock Rule |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **`P01`** | **Tranche Issuance Ratio** | $\chi$ | **STRUCTURAL** | $1.000$ | Fixed $1.000$ (Exact 1:1 Parity) | **Hardcoded Invariant (Cannot be modified)** |
| **`P02`** | **Par Normalization Index** | $V_0$ | **STRUCTURAL** | $\$1.000$ | Fixed $\$1.000$ | **Hardcoded Invariant (Cannot be modified)** |
| **`P03`** | **Diffusion Volatility** | $\sigma$ | **EMPIRICAL** | $89.13\%$ | $95\%$ CI: $[86.13\%, 92.00\%]$ | Calibrated via MLE (`DAT-01`) |
| **`P04`** | **Jump Intensity** | $\lambda$ | **EMPIRICAL** | $3.00\text{ / yr}$ | $95\%$ CI: $[2.20, 3.80]$ | Calibrated via Poisson MLE (`DAT-01`) |
| **`P05`** | **Up-Jump Probability** | $p$ | **EMPIRICAL** | $0.418$ | $95\%$ CI: $[0.320, 0.510]$ | Calibrated via Kou MLE (`DAT-01`) |
| **`P06`** | **Upward Tail Decay** | $\eta_1$ | **EMPIRICAL** | $3.181$ | $95\%$ CI: $[2.650, 3.820]$ | Calibrated via Kou MLE (`DAT-01`) |
| **`P07`** | **Downward Tail Decay** | $\eta_2$ | **EMPIRICAL** | $2.331$ | $95\%$ CI: $[1.920, 2.850]$ | Calibrated via Kou MLE (`DAT-01`) |
| **`P08`** | **sAVAX Staking APR** | $\bar{q}$ | **EMPIRICAL** | $5.85\%$ | $95\%$ CI: $[4.71\%, 6.98\%]$ | Calibrated via Consensus APR (`DAT-02`) |
| **`P09`** | **Senior Class A Coupon** | $R$ | **GOVERNANCE** | $7.30\%$ | Robust Corridor: $[5.00\%, 9.00\%]$ | 7-Day Timelocked Governance |
| **`P10`** | **anUSD Benchmark Rate** | $R'$ | **GOVERNANCE** | $3.00\%$ | Robust Corridor: $[1.50\%, 4.50\%]$ | 7-Day Timelocked Governance |
| **`P11`** | **Downward Reset Barrier** | $H_d$ | **GOVERNANCE** | $\$0.250$ | Robust Corridor: $[\$0.200, \$0.350]$ | 14-Day Timelocked Governance |
| **`P12`** | **Upward Reset Barrier** | $H_u$ | **GOVERNANCE** | $\$2.000$ | Robust Corridor: $[\$1.800, \$2.500]$ | 14-Day Timelocked Governance |
| **`P13`** | **AVAX Burn Allocation** | $\omega_{\text{burn}}$ | **GOVERNANCE** | $65.00\%$ | Robust Corridor: $[40.00\%, 75.00\%]$ | 7-Day Timelocked Governance |
| **`P14`** | **Validator Subsidy Base** | $\omega_{\text{val,0}}$ | **GOVERNANCE** | $20.00\%$ | Robust Corridor: $[15.00\%, 35.00\%]$ | 7-Day Timelocked Governance |
| **`P15`** | **L1 Treasury Allocation** | $\omega_{\text{l1}}$ | **GOVERNANCE** | $15.00\%$ | Robust Corridor: $[5.00\%, 25.00\%]$ | 7-Day Timelocked Governance |
| **`P16`** | **Reserve Buffer Allocation** | $\omega_{\text{res}}$ | **GOVERNANCE** | $0.00\%$ | Robust Corridor: $[0.00\%, 15.00\%]$ | 7-Day Timelocked Governance |
| **`P17`** | **Proportional Gain** | $K_p$ | **CONTROL** | $0.150$ | Robust Corridor: $[0.100, 0.250]$ | Autonomous On-Chain PI Controller |
| **`P18`** | **Integral Gain** | $K_i$ | **CONTROL** | $0.020$ | Robust Corridor: $[0.010, 0.040]$ | Autonomous On-Chain PI Controller |
| **`P19`** | **Rate Adjustment Clamp** | $\Delta R'_{\max}$ | **CONTROL** | $\pm 5.00\%$ | Robust Corridor: $[\pm 3.00\%, \pm 7.00\%]$ | Autonomous Anti-Windup Safety Guard |
| **`P20`** | **Drawdown Subsidy Slope** | $\kappa_{\text{dd}}$ | **CONTROL** | $0.350$ | Robust Corridor: $[0.200, 0.500]$ | Autonomous Countercyclical Function |
| **`P21`** | **Oracle Heartbeat Delay** | $\tau_{\text{heart}}$ | **SECURITY** | $300\text{ s}$ | Max Staleness: $300\text{ s}$ ($5\text{ min}$) | Security Circuit Breaker Guard |
| **`P22`** | **MEV Proximity Band** | $\delta_{\text{lock}}$ | **SECURITY** | $\pm 1.50\%$ | Fixed Band: $\pm 1.50\%$ | 1-Block Commit-Delay Lock |
| **`P23`** | **Derivative Gain** | $K_d$ | **ELIMINATED** | $0.000$ | Formally $0.000$ (Eliminated) | **Permanently Removed from Bytecode** |

---

## 2. Dynamic State-Feedback Governance Policy

$$\boldsymbol{\omega}(t) = \begin{bmatrix} \omega_{\text{burn}}(t) \\ \omega_{\text{val}}(t) \\ \omega_{\text{res}}(t) \\ \omega_{\text{l1}}(t) \end{bmatrix} = \begin{bmatrix} 1.0 - \omega_{\text{val}}(t) - \omega_{\text{res}}(t) - \omega_{\text{l1}} \\ \text{clamp}\left(0.20 + 0.35 \cdot \text{Drawdown}_t, 0.20, 0.45\right) \\ \text{clamp}\left(0.00 + 0.20 \cdot \max(0, 1.30 - \text{CR}_{\text{phys}}(t)), 0.00, 0.15\right) \\ 0.15 \end{bmatrix}$$

---

## 3. Governance Directives & Timelock Enforcement

1. **Structural Invariants (`P01`, `P02`):** Baked into smart contract arithmetic; zero governance modify hooks.
2. **Empirical Calibration Updates (`P03`–`P08`):** Recalibrated biannually from rolling 2-year on-chain tick data.
3. **Governance Levers (`P09`–`P16`):** Parameter changes constrained strictly within the **Robust Operating Corridors** by contract require statements (`require(val >= MIN && val <= MAX)`).
