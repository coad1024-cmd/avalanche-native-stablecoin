# Stage 2 Adversarial Validation Audit: Comprehensive Data & Provenance Inventory

> **Document Identifier:** `BCRG-AUDIT-DATA-INVENTORY-STAGE-2-01`  
> **Auditor Role:** Survey Explorer 3 (Data, Metadata, Schema & Provenance)  
> **Target System:** Avalanche-Native Stablecoin (`coad1024-cmd/avalanche-native-stablecoin`)  
> **Target Branch:** `research/first-principles-adversarial-audit`  
> **Snapshot ID:** `SNAP-2026-08-31-02`  
> **Audit Date:** August 31, 2026  
> **Integrity Mode:** Development (Read-Only Independent Verification)

---

## 1. Executive Summary & Inventory Overview

This report provides an exhaustive, independent first-principles survey of all datasets, parquet schemas, row counts, cell counts, column types, parquet metadata, cryptographic hashes, execution environments, and lineage registries associated with the **Stage 2 Architecture & Redistribution Policy Screening**.

### Key Inventory Highlights
1. **Primary Stage 2 Dataset (`STAGE_2_RESULTS.parquet`):**
   * **Dimensions:** Exactly **$1,600\text{ rows} \times 25\text{ columns}$** ($40,000$ total data cells).
   * **Integrity:** Exactly **0 nulls**, **0 NaNs**, **0 infinite values** across all $40,000$ cells.
   * **Stratification Balance:** Perfectly balanced $8 \times 5$ grid (8 discrete architectures $A_0 \dots A_{5.3}$, 5 redistribution policies $\text{POL-01} \dots \text{POL-05}$), with exactly $40$ configurations per $[arch, policy]$ cell ($200$ per architecture, $320$ per policy).
   * **Cryptographic Hash:** `653890da46dc822e87fda27b7a5e750b68bb54a027dd4864c1addf757211d24f` ($201,292\text{ bytes}$).
2. **Primary Stage 1 Input Baseline (`STAGE_1_CORRECTED_SURVIVORS.parquet`):**
   * **Dimensions:** Exactly **$64,052\text{ rows} \times 14\text{ columns}$** ($896,728$ total data cells).
   * **Integrity:** Exactly **0 nulls**, **0 NaNs**, **0 infinite values**.
   * **Cryptographic Hash:** `3d9ebe70ef522223edf0d115e9c0505b78ef9ceea57e5c40e22892a22bd13319` ($6,385,411\text{ bytes}$).
3. **Cryptographic Provenance Consistency:**
   * All dataset SHA-256 hashes match verbatim across `RESEARCH_STATE.yaml`, `STAGE_2_EXPERIMENT_MANIFEST.json`, `STAGE_1_ANALYTICAL_PRUNING_MANIFEST.json`, `calibrated_market_parameters.json`, and `_lineage.jsonl`.
4. **Deterministic Reproducibility:**
   * Stratified sampling from Stage 1 to Stage 2 is **$100.00\%$ deterministically reproducible** ($0$ difference across all 1,600 parameter tuples).
   * Monte Carlo SDE simulation outputs are **$100.00\%$ bit-for-bit reproducible** (maximum absolute metric difference across tested candidates = $0.0$).
5. **Critical Data Anomalies Identified for Downstream Auditors:**
   * `peg_rmse` is **identically 0.000000** across all 1,600 configurations because the secondary AMM price in `simulate_single_candidate` was initialized at $1.0000$ with zero exogenous noise or secondary DEX trade flow shocks.
   * `max_depeg` and `rate_volatility` are similarly **identically 0.000000**.
   * `validator_insolvency_prob` is **identically 1.000000** across all 1,600 rows because minimum validator coverage was evaluated on a $1\text{M sAVAX}$ test pool against the full $1,450$-node network annual OpEx ($\$6.09\text{M}$), making coverage $< 1.20\times$ on $100\%$ of paths.
   * Architectures $A_1$, $A_3$, and $A_4$ exhibit identical empirical haircut probabilities ($74.200\%$) and identical $\text{CVaR}_{99}$ ($97.8984\%$) because they share the identical subordinated junior equity default condition ($2.0 \cdot S_t < 1.0$) with zero buffer or reset mechanisms.

---

## 2. Primary Dataset Audit: `STAGE_2_RESULTS.parquet`

### 2.1 File Characteristics & Parquet Container Metadata
* **File Path:** `audit_artifacts/execution/STAGE_2_RESULTS.parquet`
* **File Size:** `201,292` bytes ($196.57\text{ KiB}$)
* **SHA-256 Hash:** `653890da46dc822e87fda27b7a5e750b68bb54a027dd4864c1addf757211d24f`
* **Format Version:** `1.0`
* **Created By:** `fastparquet-python version 2026.3.0 (build 0)`
* **Number of Row Groups:** `1`
* **Serialized Footer Size:** `5,900` bytes
* **Row Count:** `1,600`
* **Column Count:** `25`
* **Total Cell Count:** `40,000`
* **Compression Codec:** `SNAPPY` (applied uniformly across all 25 column chunks)
* **Encodings:** `PLAIN`
* **Custom Key-Value Metadata:** Includes Pandas schema JSON (`pandas_version: 3.0.2`, `creator: fastparquet 2026.3.0`).

### 2.2 Schema & Column Definitions

| Col # | Column Name | PyArrow Physical Type | Pandas dtype | Null Count | NaN Count | Inf Count | Physical Role |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **0** | `arch_id` | `INT64` | `int64` | 0 | 0 | 0 | Mechanism Architecture ID ($0 \dots 7$) |
| **1** | `policy_id` | `INT64` | `int64` | 0 | 0 | 0 | Redistribution Policy ID ($0 \dots 4$) |
| **2** | `R` | `DOUBLE` | `float64` | 0 | 0 | 0 | Senior Target Coupon / Staking APR ($R \in [0.01, 0.20]$) |
| **3** | `R_prime` | `DOUBLE` | `float64` | 0 | 0 | 0 | Junior Fixed Staking Surcharge ($R' \in [0.005, 0.10]$) |
| **4** | `H_d` | `DOUBLE` | `float64` | 0 | 0 | 0 | Downward Reset Barrier ($H_d \in [0.05, 0.60]$) |
| **5** | `H_u` | `DOUBLE` | `float64` | 0 | 0 | 0 | Upward Reset Barrier ($H_u \in [1.10, 3.50]$) |
| **6** | `omega_burn` | `DOUBLE` | `float64` | 0 | 0 | 0 | ACP-67 Deflationary Burn Weight |
| **7** | `omega_val` | `DOUBLE` | `float64` | 0 | 0 | 0 | Dynamic Validator Subsidy Weight |
| **8** | `omega_res` | `DOUBLE` | `float64` | 0 | 0 | 0 | Solvency Reserve Buffer Weight |
| **9** | `omega_l1` | `DOUBLE` | `float64` | 0 | 0 | 0 | Avalanche L1 Treasury Share |
| **10** | `K_p` | `DOUBLE` | `float64` | 0 | 0 | 0 | Proportional Feedback Control Gain ($K_p \in [0.01, 0.60]$) |
| **11** | `K_i` | `DOUBLE` | `float64` | 0 | 0 | 0 | Integral Feedback Control Gain ($K_i \in [0.001, 0.10]$) |
| **12** | `B_target` | `DOUBLE` | `float64` | 0 | 0 | 0 | Reserve Target Ratio ($B^* \in [0.00, 0.30]$) |
| **13** | `kappa_dd` | `DOUBLE` | `float64` | 0 | 0 | 0 | Countercyclical Drawdown Sensitivity ($\kappa_{dd} \in [0.05, 0.80]$) |
| **14** | `peg_rmse` | `DOUBLE` | `float64` | 0 | 0 | 0 | Secondary Peg Root Mean Squared Error |
| **15** | `max_depeg` | `DOUBLE` | `float64` | 0 | 0 | 0 | Maximum Secondary Depeg Magnitude ($|P_{\text{dex}} - 1|$) |
| **16** | `haircut_prob` | `DOUBLE` | `float64` | 0 | 0 | 0 | Senior Principal Haircut Probability ($\mathbb{P}(\text{Loss} > 0.01\%)$) |
| **17** | `tail_cvar_99` | `DOUBLE` | `float64` | 0 | 0 | 0 | Conditional Value at Risk ($99\%$ Tail Loss) |
| **18** | `recovery_time_days` | `DOUBLE` | `float64` | 0 | 0 | 0 | Peg Recovery Time in Days ($|P - 1| > 0.50\%$) |
| **19** | `validator_cr_min` | `DOUBLE` | `float64` | 0 | 0 | 0 | Minimum Validator OpEx Coverage Ratio ($\text{CR}_{\text{OpEx}}$) |
| **20** | `validator_insolvency_prob` | `DOUBLE` | `float64` | 0 | 0 | 0 | Validator Insolvency Probability ($\mathbb{P}(\text{CR} < 1.20)$) |
| **21** | `avax_burned_total` | `DOUBLE` | `float64` | 0 | 0 | 0 | Cumulative AVAX Burn Volume ($T = 365\text{ days}$) |
| **22** | `reset_churn_annual` | `DOUBLE` | `float64` | 0 | 0 | 0 | Annual Reset Frequency ($f_{\text{reset}}/\text{yr}$) |
| **23** | `rate_volatility` | `DOUBLE` | `float64` | 0 | 0 | 0 | Dynamic Rate Controller Volatility ($\sigma(u_t)$) |
| **24** | `reserve_depletion_prob` | `DOUBLE` | `float64` | 0 | 0 | 0 | Reserve Buffer Full Depletion Probability |

### 2.3 2D Stratification Balance Matrix ($8 \times 5 = 40$ Cells)

| Architecture | POL-01 (Static) | POL-02 (Countercyclical) | POL-03 (Reserve Priority) | POL-04 (Burn Max) | POL-05 (State Softmax) | Total Candidates |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`0` (A0: Dual-Class Discrete Reset)** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`1` (A1: Continuous Amortization)** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`2` (A2: Solvency Buffer Vault)** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`3` (A3: Floating Junior Equity)** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`4` (A4: Zero-Controller CDP)** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`5` (A5.1: Convertible Debt)** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`6` (A5.2: Protocol-Owned AMM)** | 40 | 40 | 40 | 40 | 40 | **200** |
| **`7` (A5.3: Multi-LST Basket)** | 40 | 40 | 40 | 40 | 40 | **200** |
| **Total Candidates** | **320** | **320** | **320** | **320** | **320** | **1,600** |

### 2.4 Complete Column Descriptive Statistics ($N = 1,600$)

| Column Name | Mean | Std Dev | Min | 25% | Median | 75% | Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `arch_id` | 3.500000 | 2.292004 | 0.000000 | 1.750000 | 3.500000 | 5.250000 | 7.000000 |
| `policy_id` | 2.000000 | 1.414656 | 0.000000 | 1.000000 | 2.000000 | 3.000000 | 4.000000 |
| `R` | 0.122192 | 0.047319 | 0.010396 | 0.084752 | 0.126487 | 0.161044 | 0.199838 |
| `R_prime` | 0.047060 | 0.026760 | 0.005001 | 0.023405 | 0.045866 | 0.069411 | 0.099931 |
| `H_d` | 0.324048 | 0.157919 | 0.050034 | 0.188210 | 0.322867 | 0.457814 | 0.598877 |
| `H_u` | 2.297715 | 0.701345 | 1.102321 | 1.674900 | 2.285888 | 2.923485 | 3.499446 |
| `omega_burn` | 0.243133 | 0.189587 | 0.000418 | 0.090623 | 0.199173 | 0.354170 | 0.920262 |
| `omega_val` | 0.254578 | 0.193982 | 0.000182 | 0.098485 | 0.210408 | 0.370005 | 0.960428 |
| `omega_res` | 0.250004 | 0.190399 | 0.000022 | 0.096309 | 0.207908 | 0.366472 | 0.916151 |
| `omega_l1` | 0.252285 | 0.187708 | 0.000074 | 0.103004 | 0.211475 | 0.364408 | 0.890152 |
| `K_p` | 0.312039 | 0.170589 | 0.010000 | 0.165278 | 0.317587 | 0.459960 | 0.599500 |
| `K_i` | 0.050011 | 0.028345 | 0.001027 | 0.025345 | 0.049479 | 0.073573 | 0.099987 |
| `B_target` | 0.149024 | 0.087301 | 0.000127 | 0.072551 | 0.150868 | 0.224855 | 0.299938 |
| `kappa_dd` | 0.428818 | 0.216394 | 0.050928 | 0.239335 | 0.435777 | 0.612196 | 0.799779 |
| `peg_rmse` | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `max_depeg` | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `haircut_prob` | 0.406855 | 0.349757 | 0.000000 | 0.000000 | 0.392000 | 0.742000 | 0.798000 |
| `tail_cvar_99` | 0.484174 | 0.400188 | 0.000000 | 0.000000 | 0.354181 | 0.978984 | 0.978984 |
| `recovery_time_days` | 0.500000 | 0.000000 | 0.500000 | 0.500000 | 0.500000 | 0.500000 | 0.500000 |
| `validator_cr_min` | 0.022927 | 0.014464 | 0.000128 | 0.012351 | 0.021021 | 0.030800 | 0.086148 |
| `validator_insolvency_prob` | 1.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 |
| `avax_burned_total` | 669,968.57 | 395,386.96 | 0.000000 | 338,813.06 | 667,238.16 | 988,963.29 | 1,419,592.39 |
| `reset_churn_annual` | 1.882531 | 2.990588 | 0.000000 | 0.000000 | 0.000000 | 2.978000 | 25.934000 |
| `rate_volatility` | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `reserve_depletion_prob` | 0.000176 | 0.002445 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.078000 |

### 2.5 Grouped Metric Breakdown by Architecture ($N = 200\text{ each}$)

| Architecture Code & Topology | Haircut Prob (%) | Tail $\text{CVaR}_{99}$ (%) | Reset Churn ($f_{\text{res}}/\text{yr}$) | Min Validator CR | Mean AVAX Burn | Res Depletion Prob |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`0` (A0: Dual-Class Reset)** | $13.675\%$ | $33.827\%$ | $7.368$ | $0.019623$ | $681,167$ | $0.000000$ |
| **`1` (A1: Cont. Amortization)** | $74.200\%$ | $97.898\%$ | $0.000$ | $0.025011$ | $632,829$ | $0.000000$ |
| **`2` (A2: Solvency Buffer)** | **$0.141\%$** | **$0.666\%$** | $3.041$ | $0.021147$ | $651,861$ | $0.001410$ |
| **`3` (A3: Floating Junior)** | $74.200\%$ | $97.898\%$ | $0.000$ | $0.023160$ | $645,168$ | $0.000000$ |
| **`4` (A4: Zero Controller)** | $74.200\%$ | $97.898\%$ | $0.000$ | $0.022937$ | $688,904$ | $0.000000$ |
| **`5` (A5.1: Convertible Debt)** | $77.880\%$ | $22.041\%$ | $0.000$ | $0.023024$ | $673,545$ | $0.000000$ |
| **`6` (A5.2: Protocol AMM)** | $9.164\%$ | $31.537\%$ | $2.885$ | $0.020318$ | $675,531$ | $0.000000$ |
| **`7` (A5.3: Multi-LST Basket)** | $2.024\%$ | $5.574\%$ | **$1.767$** | **$0.028198$** | **$710,744$** | $0.000000$ |

### 2.6 Grouped Metric Breakdown by Redistribution Policy ($N = 320\text{ each}$)

| Policy Code & Strategy | Haircut Prob (%) | Tail $\text{CVaR}_{99}$ (%) | Reset Churn ($f_{\text{res}}/\text{yr}$) | Min Validator CR | Mean AVAX Burn | Res Depletion Prob |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`0` (POL-01: Static Split)** | $40.650\%$ | $48.463\%$ | $1.988$ | $0.025169$ | $357,902$ | $0.000075$ |
| **`1` (POL-02: Countercyclical)** | $40.448\%$ | $48.622\%$ | $1.774$ | **$0.030886$** | $340,379$ | $0.000219$ |
| **`2` (POL-03: Reserve Priority)** | $40.359\%$ | $48.205\%$ | $1.815$ | $0.022259$ | $731,144$ | $0.000194$ |
| **`3` (POL-04: Burn Maximizer)** | $41.018\%$ | $48.498\%$ | $1.807$ | **$0.009323$** | **$1,155,426$** | $0.000281$ |
| **`4` (POL-05: State Softmax)** | $40.953\%$ | $48.299\%$ | $2.029$ | $0.026999$ | $764,992$ | $0.000113$ |

---

## 3. Input Population Dataset Audit: `STAGE_1_CORRECTED_SURVIVORS.parquet`

### 3.1 Container Characteristics
* **File Path:** `audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet`
* **File Size:** `6,385,411` bytes ($6.09\text{ MiB}$)
* **SHA-256 Hash:** `3d9ebe70ef522223edf0d115e9c0505b78ef9ceea57e5c40e22892a22bd13319`
* **Format Version:** `1.0`
* **Created By:** `fastparquet-python version 2026.3.0 (build 0)`
* **Number of Row Groups:** `1`
* **Serialized Footer Size:** `3,306` bytes
* **Total Rows:** `64,052`
* **Total Columns:** `14`
* **Total Data Cells:** `896,728`
* **Total Nulls / NaNs / Infs:** `0`
* **Compression Codec:** `SNAPPY` across all 14 columns

### 3.2 Schema & Survivor Bounds

| Col # | Field Name | PyArrow Physical Type | Min Value | Max Value | Mean | Std Dev |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **0** | `arch_id` | `INT64` | 0 | 7 | 3.495956 | 2.289946 |
| **1** | `policy_id` | `INT64` | 0 | 4 | 1.996175 | 1.414998 |
| **2** | `R` | `DOUBLE` | $0.010029$ | $0.199997$ | $0.123585$ | $0.046578$ |
| **3** | `R_prime` | `DOUBLE` | $0.005000$ | $0.099998$ | $0.047305$ | $0.026920$ |
| **4** | `H_d` | `DOUBLE` | $0.050014$ | $0.599973$ | $0.324575$ | $0.158615$ |
| **5** | `H_u` | `DOUBLE` | $1.100045$ | $3.499986$ | $2.301019$ | $0.694289$ |
| **6** | `omega_burn` | `DOUBLE` | $0.000003$ | $0.971993$ | $0.250093$ | $0.193103$ |
| **7** | `omega_val` | `DOUBLE` | $0.000001$ | $0.985299$ | $0.249700$ | $0.193153$ |
| **8** | `omega_res` | `DOUBLE` | $0.000008$ | $0.977791$ | $0.249802$ | $0.193362$ |
| **9** | `omega_l1` | `DOUBLE` | $0.000002$ | $0.975927$ | $0.250405$ | $0.194223$ |
| **10** | `K_p` | `DOUBLE` | $0.010000$ | $0.599986$ | $0.306087$ | $0.170620$ |
| **11** | `K_i` | `DOUBLE` | $0.001001$ | $0.099999$ | $0.050527$ | $0.028500$ |
| **12** | `B_target` | `DOUBLE` | $0.000013$ | $0.299993$ | $0.149785$ | $0.086658$ |
| **13** | `kappa_dd` | `DOUBLE` | $0.050012$ | $0.799974$ | $0.426402$ | $0.216337$ |

### 3.3 Stage 1 Architecture Survivor Counts ($N_0 = 64,052$)

| Architecture ID | Topology Name | Survivor Count | Percentage of Survivors |
| :---: | :--- | :---: | :---: |
| **`0`** | `A0_Dual_Tranche_Reset` | 8,096 | $12.64\%$ |
| **`1`** | `A1_Continuous_Amortization` | 7,959 | $12.43\%$ |
| **`2`** | `A2_Solvency_Buffer` | 7,903 | $12.34\%$ |
| **`3`** | `A3_Floating_Junior` | 8,023 | $12.53\%$ |
| **`4`** | `A4_Zero_Controller` | 8,094 | $12.64\%$ |
| **`5`** | `A5_1_Convertible_Debt` | 8,091 | $12.63\%$ |
| **`6`** | `A5_2_Protocol_Owned_AMM` | 7,944 | $12.40\%$ |
| **`7`** | `A5_3_Multi_LST_Basket` | 7,942 | $12.40\%$ |
| **Total** | **8 Topologies** | **64,052** | **100.00%** |

---

## 4. Master Cryptographic Provenance & Hash Reconciliation Table

| Artifact Logical Name | Target File Path | Actual On-Disk File Size (Bytes) | Computed SHA-256 Checksum | Registered Reference SHA-256 | State Record Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Stage 2 Results** | `audit_artifacts/execution/STAGE_2_RESULTS.parquet` | 201,292 | `653890da46dc822e87fda27b7a5e750b68bb54a027dd4864c1addf757211d24f` | `653890da46dc822e87fda27b7a5e750b68bb54a027dd4864c1addf757211d24f` (`RESEARCH_STATE.yaml`) | **VERIFIED (Exact Match)** |
| **Stage 2 Manifest** | `audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json` | 3,573 | `6b3e409b1dd72c73996c9c7f9737d20f6ceccfc92576b4d465960b6a642aec91` | *Referenced by path* | **VERIFIED** |
| **Stage 1 Survivors** | `audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet` | 6,385,411 | `3d9ebe70ef522223edf0d115e9c0505b78ef9ceea57e5c40e22892a22bd13319` | `3d9ebe70ef522223edf0d115e9c0505b78ef9ceea57e5c40e22892a22bd13319` (`RESEARCH_STATE.yaml`) | **VERIFIED (Exact Match)** |
| **Stage 1 Manifest** | `audit_artifacts/execution/STAGE_1_ANALYTICAL_PRUNING_MANIFEST.json` | 3,481 | `b0215f418f7d8a8fdf51b02521f9c2da3f2494fdae0927abf40074b6f99674b9` | `b0215f418f7d8a8fdf51b02521f9c2da3f2494fdae0927abf40074b6f99674b9` (`RESEARCH_STATE.yaml`) | **VERIFIED (Exact Match)** |
| **Research State** | `audit_artifacts/state/RESEARCH_STATE.yaml` | 7,145 | `f361c70679f67a62a09ef3ef249eec516e1a055848b94380eff33cec1326b15a` | *Canonical Snapshot 02* | **VERIFIED** |
| **Market Params** | `audit_artifacts/provenance/calibrated_market_parameters.json` | 2,832 | `f43c4fd6532d581c6fde51d99689ffacfa69a5faaa577365d52c69d7bb7e9ef6` | *Canonical Empirical Baseline* | **VERIFIED** |
| **Provenance Lineage** | `audit_artifacts/provenance/_lineage.jsonl` | 9,549 | `8e4b155ff6171c0592ffc4e46f83762c58da132a33fda201619e6a2be684590e` | `8e4b155ff6171c0592ffc4e46f83762c58da132a33fda201619e6a2be684590e` (`data/_lineage.jsonl`) | **VERIFIED (Identical)** |
| **Telemetry DAT-01** | `data/raw/DAT-01_avax_usd_5yr_daily.csv` | 443,216 | `83abd83158c6a9a9f13b12e359bd97afc6acf827849f9d0c6f1be6918a6e54e7` | `83abd83158c6a9a9f13b12e359bd97afc6acf827849f9d0c6f1be6918a6e54e7` (`calibrated_params.json`) | **VERIFIED (Exact Match)** |
| **Telemetry DAT-02** | `data/raw/DAT-02_savax_staking_apr_history.csv` | 179,174 | `47727cc6e7a6bc48fbaedbcb19d0eb09414c9d0276c52892997a0148fff307c7` | `47727cc6e7a6bc48fbaedbcb19d0eb09414c9d0276c52892997a0148fff307c7` (`calibrated_params.json`) | **VERIFIED (Exact Match)** |
| **Telemetry DAT-03** | `data/raw/DAT-03_traderjoe_liquidity_depth_profiles.csv` | 522 | `e88712a32d8e8e1c30a9a35b9d8c9d5dcb7c114b3943f367ab4e71449f5cfdd8` | `e88712a32d8e8e1c30a9a35b9d8c9d5dcb7c114b3943f367ab4e71449f5cfdd8` (`calibrated_params.json`) | **VERIFIED (Exact Match)** |
| **Telemetry DAT-07** | `data/raw/DAT-07_black_swan_ticks.csv` | 404 | `3ee1e8a991e5e6689376f0cb440b219a2f63407f5f8a2768faf2958431f4328d` | `3ee1e8a991e5e6689376f0cb440b219a2f63407f5f8a2768faf2958431f4328d` (`calibrated_params.json`) | **VERIFIED (Exact Match)** |

---

## 5. Complete Repository Data File Catalog

| File Path | Type | Size (Bytes) | Rows | Cols | Total Cells | Null Count | Primary Description |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `audit_artifacts/execution/STAGE_2_RESULTS.parquet` | Parquet | 201,292 | 1,600 | 25 | 40,000 | 0 | Stage 2 1,600-configuration Monte Carlo screening results |
| `audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet` | Parquet | 6,385,411 | 64,052 | 14 | 896,728 | 0 | Stage 1 analytical pruning survivor population |
| `data/raw/DAT-01_avax_usd_5yr_daily.csv` | CSV | 443,216 | 2,140 | 16 | 34,240 | 0 | 5-year aggregated AVAX/USD daily Binance OHLCV telemetry |
| `data/raw/DAT-02_savax_staking_apr_history.csv` | CSV | 179,174 | 2,140 | 4 | 8,560 | 0 | Historical sAVAX staking APR & exchange rate telemetry |
| `data/raw/DAT-03_traderjoe_liquidity_depth_profiles.csv` | CSV | 522 | 13 | 5 | 65 | 0 | TraderJoe DEX liquidity depth and slippage profiles |
| `data/raw/DAT-07_black_swan_ticks.csv` | CSV | 404 | 4 | 8 | 32 | 0 | Historical crypto black swan shock calibration events |
| `simulations/comprehensive_psuu_results.csv` | CSV | 84,988 | 729 | 11 | 8,019 | 0 | Historical PSUU 729-parameter grid optimization sweep |
| `simulations/monte_carlo_10k_results.csv` | CSV | 20,477 | 500 | 7 | 3,500 | 0 | Legacy 500-path Monte Carlo validation run |
| `simulations/robustness_study/adversarial_jump_stress_results.csv` | CSV | 697 | 6 | 9 | 54 | 0 | Single-step discrete crash stress responses |
| `simulations/robustness_study/controller_ablation_results.csv` | CSV | 748 | 12 | 6 | 72 | 0 | PI secondary peg controller ablation study metrics |
| `simulations/robustness_study/out_of_sample_regime_results.csv` | CSV | 20,578 | 165 | 9 | 1,485 | 0 | Multi-regime out-of-sample stress test outputs |
| `simulations/robustness_study/sobol_peg_volatility_indices.csv` | CSV | 365 | 8 | 4 | 32 | 0 | First-order and total-order Sobol sensitivity indices |
| `simulations/archive/psuu_sweep_results.csv` | CSV | 14,599 | 180 | 8 | 1,440 | 0 | Archive PSUU 180-parameter sweep results |

---

## 6. Execution Environment & Reproducibility Audit

### 6.1 Hardware, OS, and Runtime Specifications

| Attribute | Audited Environment Value | Baseline Lineage Record Value (`_lineage.jsonl`) | Reconciliation Status |
| :--- | :--- | :--- | :---: |
| **Operating System** | `Linux 6.19.13-400.asahi.fc43.aarch64+16k` | `Linux 6.19.13-400.asahi.fc43.aarch64+16k` | **MATCH** |
| **CPU Architecture** | `aarch64` (8 physical cores) | `aarch64` | **MATCH** |
| **Python Runtime** | `3.14.4` (`/home/hash/.cache/uv/...`) | `3.13.12` | **COMPATIBLE** |
| **NumPy Version** | `2.5.2` | `2.4.4` | **COMPATIBLE** |
| **Pandas Version** | `3.0.5` | `3.0.2` | **COMPATIBLE** |
| **PyArrow Version** | `25.0.1` | `25.0.1` | **MATCH** |
| **Parquet Writer** | `fastparquet 2026.3.0 (build 0)` | `fastparquet 2026.3.0` | **MATCH** |
| **Active Git Branch** | `research/first-principles-adversarial-audit` | `research/first-principles-adversarial-audit` | **MATCH** |
| **Head Git Commit** | `cc1064897c16be16c0bbe2817a37a3911c322247` | `b85c5f0756cbad1a500a53bdbbd394f81503bf3f` (Baseline Snapshot) | **VERIFIED LINEAGE** |

### 6.2 Common Random Numbers (CRN) & Determinism Audit
1. **Sampling Determinism:**
   * Method: Option A 2D Stratified Cell Allocation ($40$ configurations per cell from `STAGE_1_CORRECTED_SURVIVORS.parquet`).
   * Seed Equation: $\text{seed}_{\text{cell}} = 2026 + 10 \cdot \text{arch\_id} + \text{policy\_id}$.
   * Audit Result: Re-evaluating the sampling logic against the 64,052 survivor dataset reproduced the exact 1,600 candidate parameter sets with **zero variance** ($\Delta = 0$).
2. **Simulation SDE Determinism:**
   * Method: Kou SDE price paths ($N_{\text{mc}} = 500$, $T = 365$, $dt = 1/365$, seed = $2026$).
   * Audit Result: Re-running `simulate_single_candidate` against sampled candidates yielded identical metric values to machine precision ($\text{Max Abs Error} = 0.0000000000$).

---

## 7. Key Findings for Validation & Downstream Auditors

### Finding 1: Degenerate Secondary Peg SDE Actuation
* **Observation:** `peg_rmse`, `max_depeg`, and `rate_volatility` are **$0.000000$** across all 1,600 configurations.
* **Mechanism:** In `simulations/design_discovery/stage2_architecture_screening.py` (lines 153, 243-255), $P_{\text{dex}}$ is initialized at $1.0000$. Because there are no stochastic order book shocks or noisy liquidity trade flows, $P_{\text{dex}} - 1.0 = 0.0$, which implies $u_t = 0.0$ and $dP_{\text{dex}} = 0.0$.
* **Audit Implication:** While the code executed without error, the secondary peg stability gate was passed trivially due to the absence of secondary market noise excitation. Downstream Stage 3 and Stage 4 models must reintroduce secondary flow volatility.

### Finding 2: Validator OpEx Coverage Scaling
* **Observation:** `validator_insolvency_prob` is **$1.000000$** ($100\%$) and `validator_cr_min` averages **$0.022927$** ($2.29\%$).
* **Mechanism:** The Stage 2 test harness modeled a base pool of $1\text{M sAVAX}$ ($\sim \$25\text{M}$ collateral, generating $\approx \$1.6\text{M}$ annual gross staking yield) against the network-wide OpEx of 1,450 Avalanche validator nodes ($\$6.09\text{M}/\text{year}$).
* **Audit Implication:** The reported $< 1.20\times$ insolvency does not reflect architectural failure, but rather the sub-scale nature of the $1\text{M sAVAX}$ screening unit. Production scaling requires $\ge 100\text{M sAVAX}$ pool size.

### Finding 3: Structural Equivalence of Unhedged Subordinated Architectures ($A_1, A_3, A_4$)
* **Observation:** Architectures $A_1$, $A_3$, and $A_4$ have identical haircut probability ($74.200\%$) and identical tail CVaR ($97.8984\%$) across all policy variations.
* **Mechanism:** In `simulate_single_candidate`, $A_1$, $A_3$, and $A_4$ lack reserve buffers and discrete resets. Under any Kou jump trajectory where collateral drops such that $2.0 \cdot S_t < 1.0$, the senior tranche immediately incurs a loss of $1.0 - 2.0 \cdot S_t$. Because they share the identical CRN price trajectories and identical senior liability formulas, their tail default statistics are mathematically and computationally identical.

---

## 8. Summary Inventory Deliverables Sign-Off

* **Survey Report Path:** `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_explorer_survey_3/survey_data.md`
* **Audit Artifacts Surveyed:**
  - `audit_artifacts/execution/STAGE_2_RESULTS.parquet`
  - `audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet`
  - `audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json`
  - `audit_artifacts/execution/STAGE_1_ANALYTICAL_PRUNING_MANIFEST.json`
  - `audit_artifacts/state/RESEARCH_STATE.yaml`
  - `audit_artifacts/provenance/calibrated_market_parameters.json`
  - `audit_artifacts/provenance/_lineage.jsonl`
  - `data/raw/DAT-01_avax_usd_5yr_daily.csv`
  - `data/raw/DAT-02_savax_staking_apr_history.csv`
  - `data/raw/DAT-03_traderjoe_liquidity_depth_profiles.csv`
  - `data/raw/DAT-07_black_swan_ticks.csv`
  - Historical simulation results in `simulations/`
* **Status:** Complete, Verified, and Published.
