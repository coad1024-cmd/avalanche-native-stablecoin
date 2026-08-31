# Comparative Architecture Analysis & Down-Selection Report

> **Document Identifier:** `BCRG-REPORT-2026-ARCHITECTURE-COMPARISON-01`  
> **Governing Plan:** `BCRG-DESIGN-DISCOVERY-LADDER-01` (Stage 2 / 7)  
> **Research Snapshot:** `SNAP-2026-08-31-02`  
> **Source Execution Parquet:** `audit_artifacts/execution/STAGE_2_RESULTS.parquet` ($N = 1,600$)  
> **Date:** August 31, 2026  

---

## 1. Structural Comparison of the 8 Evaluated Architectures

Stage 2 evaluated eight distinct token structural topologies under standardized Common Random Numbers (CRN) jump-diffusion trajectories ($N=500\text{ paths}$, $\sigma = 89.15\%, \lambda = 15.00$).

```
========================================================================================================================
                                     ARCHITECTURE PERFORMANCE COMPARISON MATRIX
========================================================================================================================
```

| Topology Code | Architecture Name | Structural Deleveraging Mechanism | Senior Haircut Prob | 99% Tail CVaR | Reset Frequency ($f_{\text{reset}}/\text{yr}$) | Solvency Survival Rate | Screening Classification |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **`A2`** | **Solvency Buffer Vault** | Hybrid reset + yield-funded reserve buffer vault ($B_{\text{res}}$) | **0.14%** | **0.67%** | **3.04** | **99.86%** | **RETAIN (Rank 1)** |
| **`A5.3`** | **Multi-LST Basket Vault** | 3-Asset LST basket diversification + discrete reset | **2.02%** | **5.57%** | **1.77** | **97.98%** | **RETAIN (Rank 2)** |
| **`A5.2`** | **Protocol-Owned AMM** | Protocol liquidity injection ($+30\%$ depth) + discrete reset | **9.16%** | **31.54%** | **2.89** | **90.84%** | **RETAIN (Rank 3)** |
| **`A0`** | **Dual Reset (*Legacy*)** | Unbuffered discrete NAV threshold resets ($H_d, H_u$) | **13.68%** | **33.83%** | **7.37** | **86.32%** | **DOMINATED** |
| **`A5.1`** | **Convertible Debt** | Dynamic Junior debt-to-equity conversion during stress | **77.88%** | **22.04%** | **0.00** | **22.12%** | **DOMINATED** |
| **`A1`** | **Continuous Streaming** | Continuous streaming share amortization ($\dot{\mathcal{M}}(t)$) | **74.20%** | **97.90%** | **0.00** | **25.80%** | **DOMINATED** |
| **`A3`** | **Floating Junior Equity** | Perpetual floating equity tranche without reset barriers | **74.20%** | **97.90%** | **0.00** | **25.80%** | **DOMINATED** |
| **`A4`** | **Zero-Controller CDP** | Pure market-arbitrage parity redemption CDP | **74.20%** | **97.90%** | **0.00** | **25.80%** | **DOMINATED** |

---

## 2. In-Depth Analysis of Individual Architectures

### 2.1 Architecture A2: Dedicated Solvency Buffer Vault (RETAIN - Top Rank)
* **Mechanics:** Channels an endogenous yield share ($\omega_{\text{res}}$) into an unallocated cash reserve vault ($B_{\text{res}}$). Upon downward reset ($V_B \le H_d$), the protocol absorbs collateral deficits directly from $B_{\text{res}}$ before any senior haircut is applied.
* **Empirical Screening Result:** Senior principal default risk is virtually eliminated ($\text{Mean Haircut} = 0.14\%$, with $> 80\%$ of configurations exhibiting strictly $0.000\%$ haircut). Reset churn is moderate ($3.04/\text{yr}$), well within the $5.0/\text{yr}$ gate.
* **Decision:** **RETAIN** as the primary structural topology for Stage 3 Global Sensitivity Analysis.

### 2.2 Architecture A5.3: Algorithmic Multi-LST Collateral Basket (RETAIN - Rank 2)
* **Mechanics:** Diversifies collateral across an algorithmic basket of Liquid Staked AVAX assets (`sAVAX`, `ggAVAX`, `yyAVAX`). Non-synchronous validator slashing and idiosyncratic de-pegs reduce aggregate volatility.
* **Empirical Screening Result:** Delivers the lowest reset churn of any reset-capable architecture ($1.77\text{ resets/year}$) and strong solvency ($\text{CVaR}_{99} = 5.57\%$).
* **Decision:** **RETAIN** for Stage 3 parameter interaction and basket-weight optimization.

### 2.3 Architecture A5.2: Protocol-Owned AMM (POL-AMM) (RETAIN - Rank 3)
* **Mechanics:** Reinvests protocol equity directly into secondary AMM liquidity pools, expanding orderbook depth $L_{\text{amm}}$ and reducing the secondary market DC plant gain $K_{\text{dc}}$.
* **Empirical Screening Result:** Reduces depeg recovery times and moderates reset churn ($2.89/\text{yr}$), though unbuffered collateral tail jumps still yield $9.16\%$ haircut risk.
* **Decision:** **RETAIN** as a modular liquidity extension to be evaluated in combination with $A_2$.

### 2.4 Architecture A0: Dual-Class Discrete Resets (*Legacy Baseline*) (DOMINATED)
* **Mechanics:** Subordinated scalar rebasing with discrete split/reverse-split resets ($H_d = \$0.25, H_u = \$2.00$).
* **Failure Mode:** Under empirical jump-diffusion ($\lambda = 15.0$), $A_0$ triggers **$7.37\text{ resets/year}$**, violating the screening gate ($f_{\text{reset}} \le 5.0/\text{yr}$). Furthermore, without an external solvency buffer, large negative jumps breach $V_B = 0$, leading to a $13.68\%$ senior haircut probability and $33.83\%$ tail loss.
* **Decision:** **DOMINATED** by $A_2$ and $A_{5.3}$.

### 2.5 Architectures A1, A3, A4: Continuous Streaming, Floating Junior & Zero Controller (DOMINATED)
* **Mechanics:** Attempt to operate without discrete resets through continuous streaming amortization ($A_1$), perpetual equity claims ($A_3$), or passive market arbitrage ($A_4$).
* **Failure Mode:** Without discrete deleveraging resets, severe downward Poisson jumps inevitably exhaust the junior equity tranche ($\mathcal{E}_B \to 0$). Once junior equity is wiped out, senior claims absorb $100\%$ of subsequent collateral drops, resulting in a **$74.20\%$ default probability** and **$97.90\%$ tail CVaR**.
* **Decision:** **DOMINATED** and eliminated from downstream research.

### 2.6 Architecture A5.1: Dynamic Debt-Equity Convertible Swaps (DOMINATED)
* **Mechanics:** Automatically converts junior debt claims into equity claims when collateral ratios breach safety thresholds.
* **Failure Mode:** While equity conversion absorbs $80\%$ of deficit amplitude (reducing $\text{CVaR}_{99}$ to $22.04\%$), the frequent dilution events trigger loss classifications on $77.88\%$ of paths.
* **Decision:** **DOMINATED**.

---

## 3. Pairwise Dominance Matrix

| Compared Topologies | Dominance Relationship | Mathematical & Empirical Rationale |
| :--- | :---: | :--- |
| **$A_2$ vs. $A_0$** | **$A_2 \succ A_0$** | $A_2$ strictly dominates $A_0$ across solvency ($\text{CVaR}_{99}: 0.67\% \ll 33.83\%$) and reset churn ($3.04 < 7.37$). |
| **$A_{5.3}$ vs. $A_0$** | **$A_{5.3} \succ A_0$** | Basket diversification cuts reset churn by $76\%$ and tail loss by $84\%$. |
| **$A_2$ vs. $A_1, A_3, A_4$** | **$A_2 \succ \{A_1, A_3, A_4\}$** | Eliminates catastrophic $74.2\%$ insolvency frequency. |
| **$A_2$ vs. $A_{5.3}$** | **Inconclusive (Pareto Trade-off)** | $A_2$ has superior solvency ($0.14\%$ vs $2.02\%$), while $A_{5.3}$ has lower reset churn ($1.77$ vs $3.04$). Both retained. |

---

## 4. Final Architecture Down-Selection

Stage 2 down-selection successfully reduces the architecture search space from **8 candidates to 3 active topologies**:
1. **Primary Structural Lead:** **`A2` (Dedicated Solvency Buffer Vault)**
2. **Diversified Collateral Lead:** **`A5.3` (Multi-LST Basket Vault)**
3. **Liquidity Modular Extension:** **`A5.2` (Protocol-Owned AMM)**
