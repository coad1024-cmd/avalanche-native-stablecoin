# Endogenous Redistribution Policy Screening Report

> **Document Identifier:** `BCRG-REPORT-2026-REDISTRIBUTION-POLICY-SCREENING-01`  
> **Governing Plan:** `BCRG-DESIGN-DISCOVERY-LADDER-01` (Stage 2 / 7)  
> **Research Snapshot:** `SNAP-2026-08-31-02`  
> **Source Execution Parquet:** `audit_artifacts/execution/STAGE_2_RESULTS.parquet` ($N = 1,600$)  
> **Date:** August 31, 2026  

---

## 1. Executive Summary & Policy Taxonomy

Stage 2 evaluated five endogenous yield redistribution policies ($\text{POL-01}$ through $\text{POL-05}$) governing how gross staking cashflows from the $sAVAX$ collateral vault are split across the 4-simplex:
$$\boldsymbol{\omega}(t) = \begin{bmatrix} \omega_{\text{burn}}(t) & \omega_{\text{val}}(t) & \omega_{\text{res}}(t) & \omega_{\text{l1}}(t) \end{bmatrix}^T \in \Delta^3, \quad \sum_{i} \omega_i(t) \equiv 1.0000$$

```
========================================================================================================================
                                       POLICY PERFORMANCE & TRADE-OFF MATRIX
========================================================================================================================
```

| Policy Code | Policy Name | Mathematical Allocation Rule | Mean Annual AVAX Burn | Minimum Validator CR Index | Stress Resilience & Reserve Buildup | Screening Classification |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: |
| **`POL-02`** | **Countercyclical Drawdown** | $\omega_{\text{val}}(t) = \omega_{\text{val,0}} + \kappa_{\text{dd}} \max(0, 1 - S_t)$ | $340,379\text{ AVAX}$ | **0.0309** (*Highest*) | Optimal Node Operator Stabilization | **RETAIN (Top-1)** |
| **`POL-03`** | **Reserve Buffer Priority** | $\omega_{\text{res}}(t) = 0.30 \max(0, 1.25 - 2S_t)$ | $731,144\text{ AVAX}$ | 0.0223 | Strongest Buffer Synergy with $A_2$ | **RETAIN (Top-2)** |
| **`POL-05`** | **State Softmax Dynamic** | $\boldsymbol{\omega}(t) = \text{Softmax}(\mathbf{W} \mathbf{x}(t))$ | $764,992\text{ AVAX}$ | 0.0270 | Balanced Multi-Objective Adaptation | **RETAIN (Top-3)** |
| **`POL-01`** | **Static Reference Split** | Fixed $65/20/0/15$ allocation | $357,902\text{ AVAX}$ | 0.0252 | Unresponsive to Collateral Shocks | **INCONCLUSIVE (Reference)** |
| **`POL-04`** | **Deflationary Burn Maximizer** | $\omega_{\text{burn}} \ge 75\%, \omega_{\text{val}} = 10\%$ | **$1,155,426\text{ AVAX}$** | 0.0093 (*Severe Starvation*) | Extreme Validator Vulnerability | **DOMINATED** |

---

## 2. In-Depth Policy Performance Analysis

### 2.1 POL-02: Countercyclical Drawdown Feedback (RETAIN - Top Rank)
* **Mechanics:** Dynamically transfers yield share from AVAX burn into the validator subsidy pool ($\omega_{\text{val}}$) as the collateral price ratio $S_t = P_t / \beta_t$ falls below par ($S_t < 1.0$).
* **Empirical Screening Result:** Delivers the highest minimum validator coverage floor during drawdowns ($0.0309$), preventing cascading node operator insolvencies when AVAX prices compress.
* **Decision:** **RETAIN** for Stage 3 GSA and Stage 6 Pareto optimization.

### 2.2 POL-03: Reserve Buffer Priority Rule (RETAIN - Rank 2)
* **Mechanics:** Continuously diverts up to $35\%$ of gross yield into the unallocated reserve vault ($B_{\text{res}}$) whenever junior equity $V_B = 2S_t - V_A$ approaches the downward reset boundary ($V_B < 1.25$).
* **Empirical Screening Result:** Enables Architecture $A_2$ to accumulate sufficient reserve capital to absorb $99.86\%$ of downward jump deficits while still delivering substantial annual AVAX buyback volume ($731,144\text{ AVAX}$).
* **Decision:** **RETAIN** as the mandatory companion policy for Architecture $A_2$.

### 2.3 POL-05: State-Feedback Softmax Dynamic Policy (RETAIN - Rank 3)
* **Mechanics:** Evaluates a state vector $\mathbf{x}(t) = [S_t, V_B(t), \Delta P_{\text{dex}}(t), \text{CR}_{\text{OpEx}}(t)]^T$ through a softmax transition layer, smoothly redistributing surplus across all four sinks.
* **Empirical Screening Result:** Achieves strong simultaneous performance across AVAX burn ($764,992\text{ AVAX}$) and validator support ($0.0270$).
* **Decision:** **RETAIN** for non-linear parameter identification in Stage 3.

### 2.4 POL-01: Static Reference Split (65/20/0/15) (INCONCLUSIVE - Reference Benchmark)
* **Mechanics:** Invariant percentage split derived from historical ACP-67 proposal.
* **Evaluation:** Lacks state-dependent feedback. During protracted drawdowns, static $20\%$ validator allocation leads to revenue contraction in dollar terms, while zero reserve allocation leaves the vault unhedged.
* **Decision:** **INCONCLUSIVE** (retained strictly as a control benchmark for Stage 4 comparative sweeps).

### 2.5 POL-04: Deflationary Burn Maximizer (DOMINATED)
* **Mechanics:** Allocates $\ge 75\%$ of gross yield exclusively to AVAX buyback and burn, reducing validator subsidy to a flat $10\%$.
* **Failure Mode:** While generating the highest nominal burn volume ($1.155\text{M AVAX}$), it cuts validator coverage by $> 65\%$ relative to $\text{POL-02}$, creating severe economic fragility and validator dropout risk during bear markets.
* **Decision:** **DOMINATED** (rejected as a viable production mechanism).

---

## 3. Down-Selection Summary for Stage 3

* **Advancing Policies:** **`POL-02` (Countercyclical Feedback)**, **`POL-03` (Reserve Priority)**, and **`POL-05` (State Softmax)**.
* **Reference Benchmark:** **`POL-01` (Static Split)**.
* **Eliminated Policy:** **`POL-04` (Burn Maximizer)**.
