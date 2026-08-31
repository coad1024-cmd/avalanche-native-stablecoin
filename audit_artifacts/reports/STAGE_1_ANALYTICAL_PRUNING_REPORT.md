# Stage 1: Analytical Screening & Space Pruning Report (Validated & Corrected)

> **Document Identifier:** `BCRG-REPORT-2026-STAGE-1-ANALYTICAL-PRUNING-02`  
> **Governing Plan:** `BCRG-DESIGN-DISCOVERY-DECISION-FRAMEWORK-01` (Stage 1 / 7)  
> **Execution Date:** August 31, 2026  
> **Sample Size:** $N_0 = 100,000$ Configurations (Vectorized Uniform Random & Dirichlet Simplex Sampling)  
> **Runtime:** 229.98 ms (Vectorized NumPy Execution)  
> **Status:** Fully Validated · Zero Inherited Heuristics  

---

## 1. Executive Summary & Epistemic Corrections

Following the first-principles validation of Stage 1 screening:
1. **Replaced "Feasible Manifold" with "Survivor Bounding Box":** Explicitly terminology-corrected; full non-convex survivor geometry preserved in `STAGE_1_CORRECTED_SURVIVORS.parquet`.
2. **Reclassified Filter F3 (Crash Threshold):** Recognized that $-50\%$ crash survival is an aspirational risk preference (Tier 2 Optimization Objective), **not** a physical hard constraint. Filter F3 was removed as a mandatory pruning filter.
3. **Rigorously Derived Filter F4 (Damping Ratio):** Derived $\zeta = \frac{1 + K_{\text{DC}} K_p}{2\sqrt{\tau_{\text{arb}} K_{\text{DC}} K_i}}$ directly from the secondary AMM plant $G_{\text{plant}}(s) = \frac{K_{\text{DC}}}{\tau_{\text{arb}} s + 1}$, proving overdamping across all active gain ranges and liquidity tiers.
4. **Included All 8 Discrete Architectures ($	ext{A0}$–$	ext{A5.3}$):** Extended discrete search space to include advanced modular topologies ($	ext{A5.1}$ Convertible Debt, $	ext{A5.2}$ Protocol-Owned AMM, $	ext{A5.3}$ Multi-LST Basket).
5. **Exact Simplex Sampling Verified:** Proved that $\boldsymbol{\omega} \sim \text{Dirichlet}(1,1,1,1)$ guarantees uniform distribution over the 3-simplex $\Delta^3$.

### Headline Results
* **Initial Candidate Tensor:** $N_0 = 100,000$ (across 8 architectures and 5 redistribution policies)
* **Feasible Survivors:** $N_{\text{survivors}} = 64,052 \; (64.05\%)$
* **Pruning Rate:** **35.95\%** of mathematically invalid parameter space pruned.
* **Survivor Bounding Box:** Extracted and saved.

---

## 2. Filter-by-Filter Attrition Table

| Filter ID | Filter Name & Mathematical Condition | Individual Pass Count | Individual Pass Rate | Cumulative Survivors | Cumulative Survivor Rate |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **`F1`** | **Simplex Conservation:** $\sum \omega_i = 1.0, \; \omega_i \ge 0$ | 100,000 | 100.00% | 100,000 | 100.00% |
| **`F2`** | **Tranche Yield Feasibility:** $R > R', \; R' \le q_{\max} = 10.0\%$ | 64,052 | 64.05% | 64,052 | 64.05% |
| **`F4`** | **Hurwitz Overdamping:** $\zeta(K_p, K_i; L, \tau) \ge 1.0$ | 100,000 | 100.00% | 64,052 | 64.05% |
| **`F5`** | **Reset Barrier Ordering:** $0.0 < H_d < 1.0 < H_u$ (*A0, A2 only*) | 100,000 | 100.00% | **64,052** | **64.05%** |

---

## 3. Architecture Survival Breakdown (8 Topologies)

| Architecture Code | Architecture Topology Description | Initial Samples | Feasible Survivors | Survival Rate (%) | Dominant Attrition Mechanism |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **`A0`** | Dual-Tranche Securitized Reset (*Legacy*) | 12,632 | **8,096** | **64.09%** | Yield spread ($R \le R'$) |
| **`A1`** | Continuous Streaming Amortization | 12,477 | **7,959** | **63.79%** | Yield spread ($R \le R'$) |
| **`A2`** | Dedicated Solvency Buffer Vault | 12,483 | **7,903** | **63.31%** | Yield spread ($R \le R'$) |
| **`A3`** | Floating Junior Tranche Equity | 12,467 | **8,023** | **64.35%** | Yield spread ($R \le R'$) |
| **`A4`** | Zero-Controller Primary Arbitrage | 12,524 | **8,094** | **64.63%** | Yield spread ($R \le R'$) |
| **`A5.1`** | Dynamic Convertible Junior Debt | 12,647 | **8,091** | **63.98%** | Yield spread ($R \le R'$) |
| **`A5.2`** | Protocol-Owned Hybrid AMM | 12,317 | **7,944** | **64.50%** | Yield spread ($R \le R'$) |
| **`A5.3`** | Algorithmic Multi-LST Basket | 12,453 | **7,942** | **63.78%** | Yield spread ($R \le R'$) |

---

## 4. Extracted Survivor Bounding Box

```json
{
  "R": [
    0.0100287126638566,
    0.19999723350455675
  ],
  "R_prime": [
    0.005000283495863172,
    0.09999790204716957
  ],
  "H_d": [
    0.05001421190200737,
    0.5999733879323967
  ],
  "H_u": [
    1.100045154782417,
    3.4999856499602733
  ],
  "omega_burn": [
    3.399662014318779e-06,
    0.9719930617779509
  ],
  "omega_val": [
    5.26256229955052e-07,
    0.9852986039632984
  ],
  "omega_res": [
    8.190400606858328e-06,
    0.9777913374754502
  ],
  "omega_l1": [
    2.236813477174557e-06,
    0.9759270391021594
  ],
  "K_p": [
    0.010000082694093148,
    0.5999860804331149
  ],
  "K_i": [
    0.0010013235923495305,
    0.09999912612052997
  ],
  "B_target": [
    1.2523702293876227e-05,
    0.29999280788118154
  ],
  "kappa_dd": [
    0.05001222419760025,
    0.7999737428708164
  ]
}
```

---

## 5. Next Stage Unlocked

With Stage 1 analytical pruning verified against first principles and freed from inherited heuristic biases, the surviving dataset (64,052 configurations across 8 architectures) is ready for **Stage 2: Architecture & Policy Screening**.
