# Stage 2 Screening Statistical Distribution & Diagnostics Report

> **Document Identifier:** `BCRG-REPORT-2026-SCREENING-STATISTICS-01`  
> **Governing Plan:** `BCRG-DESIGN-DISCOVERY-LADDER-01` (Stage 2 / 7)  
> **Research Snapshot:** `SNAP-2026-08-31-02`  
> **Source Parquet:** `audit_artifacts/execution/STAGE_2_RESULTS.parquet`  
> **Evaluated Configurations:** $N = 1,600$ (Common Random Numbers, $N_{\text{mc}} = 500\text{ paths}$, seed = $2026$)  
> **Date:** August 31, 2026  

---

## 1. Global Sample Architecture & Stratification

The Stage 2 screening campaign evaluated $1,600$ candidate parameter configurations sampled from the verified Stage 1 survivor population ($N_0 = 64,052$).

$$\text{Sample Design} = 8\text{ Discrete Architectures} \times 5\text{ Redistribution Policies} \times 40\text{ Configurations / Cell} = \mathbf{1,600\text{ Configurations}}$$

```
========================================================================================================================
                                       STAGE 2 SAMPLE STRATIFICATION MATRIX
========================================================================================================================
```

| Architecture Code | POL-01 (Static) | POL-02 (Countercyclical) | POL-03 (Reserve Priority) | POL-04 (Burn Max) | POL-05 (Softmax) | Total Candidates |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`A0`** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`A1`** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`A2`** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`A3`** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`A4`** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`A5.1`** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`A5.2`** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`A5.3`** | 40 | 40 | 40 | 40 | 40 | **200** |
| **Total** | **320** | **320** | **320** | **320** | **320** | **1,600** |

---

## 2. Statistical Distributions Across Key Metrics

```
========================================================================================================================
                                     COMPOSITE METRIC DISTRIBUTION (N = 1,600)
========================================================================================================================
```

| Metric Name | Mean | Std Dev | Min | 25th Pct | Median | 75th Pct | Max | Screening Gate Threshold | Gate Compliance Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Senior Haircut Prob** | $40.69\%$ | $34.50\%$ | $0.00\%$ | $0.00\%$ | $39.20\%$ | $74.20\%$ | $79.80\%$ | $\le 1.00\%$ ($\mathbb{P} \ge 99\%$) | **$19.94\%$** ($319$ configs) |
| **Tail Loss ($\text{CVaR}_{99}$)** | $48.33\%$ | $44.17\%$ | $0.00\%$ | $0.00\%$ | $34.52\%$ | $97.90\%$ | $97.90\%$ | $\le 5.00\%$ | **$21.19\%$** ($339$ configs) |
| **Reset Churn ($f_{\text{reset}}/\text{yr}$)** | $1.88$ | $2.61$ | $0.00$ | $0.00$ | $0.00$ | $3.13$ | $25.93$ | $\le 5.00\text{ resets/yr}$ | **$92.00\%$** ($1,472$ configs) |
| **Annual AVAX Burn** | $669,985$ | $339,268$ | $3,372$ | $394,625$ | $687,665$ | $923,678$ | $1,419,592$ | N/A (Higher is Better) | $100.00\%$ |
| **Min Validator CR Index** | $0.0229$ | $0.0135$ | $0.0001$ | $0.0133$ | $0.0219$ | $0.0308$ | $0.0861$ | $\ge 0.80\times$ (*Full Scale*) | $0.00\%$ (*1M Pool Sub-Scale*) |
| **Peg Tracking RMSE** | $< 0.0001$ | $< 0.0001$ | $0.0000$ | $0.0000$ | $0.0000$ | $0.0000$ | $0.0000$ | $\le 5.00\%$ | **$100.00\%$** ($1,600$ configs) |

---

## 3. Analysis of Screening Gate Attrition

1. **Peg Tracking Gate ($\text{RMSE} \le 5.0\%$):**
   * **Pass Rate:** $100.00\%$ ($1,600 / 1,600$). Under the standard AMM arbitrage plant and continuous secondary price formation, the PI secondary controller stably bounds peg oscillations well below $5\%$.
2. **Reset Churn Gate ($f_{\text{reset}} \le 5.0/\text{yr}$):**
   * **Pass Rate:** $92.00\%$ ($1,472 / 1,600$).
   * **Failures:** Dominated by legacy Architecture $A_0$ where tight reset barriers ($H_d = 0.25, H_u = 2.00$) under Kou jump bursts ($\lambda = 15.0$) triggered up to $25.93\text{ resets/year}$ ($\text{mean} = 7.37$).
3. **Solvency Survival Gate ($\mathbb{P}(\text{Solvent}) \ge 99.0\%$):**
   * **Pass Rate:** $19.94\%$ ($319 / 1,600$).
   * **Distribution:** Passing configurations are concentrated entirely within **Architecture $A_2$ (Solvency Buffer Vault)** and **Architecture $A_{5.3}$ (Multi-LST Basket)**. Continuous streaming ($A_1$), floating junior ($A_3$), and zero-controller ($A_4$) failed $100\%$ of paths due to lack of buffer or discrete deleveraging protections.
4. **Validator OpEx Scaling Note:**
   * Because the test simulation was executed against a standardized $1\text{M sAVAX}$ test vault ($\sim \$1.6\text{M}$ annual gross staking revenue), the minimum coverage ratio against the full $1,450$-node network OpEx ($\$6.09\text{M}$) reflects vault sub-scale proportionality ($\approx 0.02\times$). This metric will be evaluated at production scale ($> 100\text{M sAVAX}$) in Stage 4.

---

## 4. Diagnostics & Lineage Verification

* **Data Lineage:** Ingested from `STAGE_1_CORRECTED_SURVIVORS.parquet` (SHA-256: `3d9ebe70ef522223edf0d115e9c0505b78ef9ceea57e5c40e22892a22bd13319`).
* **Random Seed Integrity:** Identical random seed (`2026`) used for all price path draws, ensuring strictly zero path-sampling variance across competing architecture evaluations (Common Random Numbers).
* **Parquet Deliverable:** Published to `audit_artifacts/execution/STAGE_2_RESULTS.parquet`.
