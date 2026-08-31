# Master Audit Report: Stage 2 KPI Mathematical Formulation, Code Implementation & Objective Direction Audit

> **Document Identifier:** `BCRG-AUDIT-2026-M3-KPI-MATHEMATICS-01`  
> **Auditor:** Worker M3 (Adversarial Validation Auditor — Implementer / QA / Specialist)  
> **Milestone:** Milestone 3 (Requirement R3): End-to-End KPI Calculation & Objective Direction Audit  
> **Target Path:** `.agents/worker_m3/m3_kpi_math_report.md`  
> **Governing Specifications:**  
> - `audit_artifacts/design_discovery/OBJECTIVES_AND_CONSTRAINTS.md` (`BCRG-DISCOVERY-2026-OBJECTIVES-CONSTRAINTS-01`)  
> - `audit_artifacts/design_discovery/DECISION_FRAMEWORK.md` (`BCRG-DESIGN-DISCOVERY-DECISION-FRAMEWORK-01`)  
> - `PROJECT.md` & `ORIGINAL_REQUEST.md`  
> **Execution Targets:**  
> - `simulations/design_discovery/stage2_architecture_screening.py`  
> - `audit_artifacts/execution/STAGE_2_RESULTS.parquet` ($N=1,600$ candidate configurations)  
> - `audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json`  
> - `audit_artifacts/reports/STAGE_2_ARCHITECTURE_SCREENING.md`, `ARCHITECTURE_COMPARISON.md`, `REDISTRIBUTION_POLICY_SCREENING.md`, `SCREENING_STATISTICS.md`  
> **Verification Scripts & Test Suites:**  
> - `audit_artifacts/execution/verify_stage2_kpi_mathematics.py`  
> - `simulations/design_discovery/test_stage2_kpi_calculations.py`  
> **Date:** August 31, 2026  
> **Epistemic Classification:** First-Principles Adversarial Audit Hard Deliverable  

---

## 1. Executive Summary & Epistemic Findings Matrix

This report delivers the comprehensive, line-by-line, first-principles mathematical and software execution audit of **all 11 Stage 2 Key Performance Indicators (KPIs)** evaluated during the Architecture & Redistribution Policy Screening phase of the Avalanche-Native Stablecoin research program.

The audit tracked every KPI across its full lifecycle:
$$\text{Mathematical Formulation} \;\longrightarrow\; \text{Python Simulation Engine} \;\longrightarrow\; \text{Parquet Storage Representation} \;\longrightarrow\; \text{Report Synthesis}$$

```
========================================================================================================================
                                      STAGE 2 KPI AUDIT CLASSIFICATION MATRIX
========================================================================================================================
```

| KPI Identifier | Parquet Column Name | Mathematical Status | Software Implementation Status | Objective Direction | Epistemic Audit Classification |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Peg RMSE** | `peg_rmse` | Valid Integral | Unexcited Plant ($P_{\text{dex}} \equiv 1.0$) | Minimize (Aligned) | **DEGENERATE ZERO (Fixed Point)** |
| **Max Depeg** | `max_depeg` | Valid Suprenum | Unexcited Plant ($P_{\text{dex}} \equiv 1.0$) | Minimize (Aligned) | **DEGENERATE ZERO (Fixed Point)** |
| **Rate Volatility** | `rate_volatility` | Valid Variance | Zero Error ($u_t \equiv 0.0$) | Minimize (Aligned) | **DEGENERATE ZERO (Fixed Point)** |
| **Depeg Recovery Time** | `recovery_time_days` | Valid Stopping Time | Hardcoded Fallback ($0.50\text{d}$) | Minimize (Aligned) | **HARDCODED FALLBACK ARTIFACT** |
| **Senior Haircut Prob** | `haircut_prob` | Valid Frequency | Genuine Vectorized Logic | Minimize (Aligned) | **VERIFIED (Active Discriminator)** |
| **Tail Loss (CVaR 99)** | `tail_cvar_99` | Valid Expected Shortfall | Genuine 99th Pct Tail Avg | Minimize (Aligned) | **VERIFIED (Active Discriminator)** |
| **Reset Churn Annual** | `reset_churn_annual` | Valid Rate Counter | Asymmetric Upward Reset Check | Minimize (Aligned) | **ASYMMETRIC IMPLEMENTATION** |
| **Min Validator CR** | `validator_cr_min` | Valid Flow Ratio | Sub-scale 1M Pool ($0.02\times$) | Maximize (Aligned) | **VERIFIED (Sub-Scale Proportional)** |
| **Validator Insolvency** | `validator_insolvency_prob` | Valid Indicator | Scale Mismatched Threshold ($1.20$) | Minimize (Aligned) | **SCALE-TAUTOLOGY SATURATION ($100\%$)** |
| **AVAX Burn Total** | `avax_burned_total` | Valid Cashflow Sum | USD Yield vs AVAX Tokens | Maximize (Aligned) | **VERIFIED (Unit Mislabeling in Reports)**|
| **Reserve Depletion** | `reserve_depletion_prob` | Valid Buffer Tracker | Genuine $A_2$-Specific Logic | Minimize (Aligned) | **VERIFIED ($A_2$ Architecture Specific)**|

### Core Audit Discoveries:
1. **Four Completely Unexcited Secondary Market Metrics:** Because the Stage 2 screening harness initialized secondary AMM spot price at $P_{\text{dex}}(0) = 1.0000$ without exogenous order flow noise or collateral-to-DEX price coupling, the secondary market remained at a static fixed point ($\dot{P}_{\text{dex}} = 0$). Consequently, `peg_rmse` ($0.0000$), `max_depeg` ($0.0000$), and `rate_volatility` ($0.0000$) were degenerate zeros across all 1,600 configurations, while `recovery_time_days` defaulted entirely to its literal hardcoded fallback of `0.50` days.
2. **Scale-Mismatched Validator Insolvency Tautology:** `validator_insolvency_prob` is identically $1.0000$ ($100.0\%$) across all 1,600 rows. This occurred because the evaluation compared a sub-scale $1\text{M sAVAX}$ test pool (maximum coverage $0.0861\times$) against the full-scale network production threshold of $1.20\times$, providing zero discriminative power in Stage 2.
3. **Reset Accounting Asymmetry ($A_0$ vs $A_2/A_{5.2}/A_{5.3}$):** In Architecture $A_0$, both upward resets ($V_B \ge H_u$) and downward resets ($V_B \le H_d$) were tracked ($7.37\text{ resets/year}$ total: $1.91$ upward, $3.47$ downward at baseline). In $A_2$, $A_{5.2}$, and $A_{5.3}$, the upward reset check (`if V_B >= H_u:`) was omitted in code lines 198 and 233, resulting in only downward resets being recorded ($3.04\text{ resets/year}$ in $A_2$). While $A_2$ remains superior in tail solvency, part of the reported reset churn reduction was an artifact of this implementation asymmetry.
4. **Loss Equivalence Among Unbuffered/Non-Reset Architectures ($A_1, A_3, A_4$):** Architectures $A_1$ (Streaming Amortization), $A_3$ (Floating Junior Equity), and $A_4$ (Zero Controller CDP) produced bit-for-bit identical haircut probabilities ($74.20\%$) and tail losses ($\text{CVaR}_{99} = 97.90\%$) across all candidate configurations because they lacked discrete reset deleveraging and shared the identical single-step collapse condition ($2 S_t < 1.0$).
5. **AVAX Burn Unit Mismatch:** The code accumulated USD gross yield diverted to burns ($\int \omega_{\text{burn}}(t) \Phi_{\text{gross}}(t) dt$ in USD), whereas historical reports labeled this output as "Mean AVAX Burn (AVAX)" while prefixing values with dollar signs (`$651,861`), conflating USD value with physical AVAX tokens.
6. **Strict Optimization Direction Alignment:** All 11 metrics exhibit $100.0\%$ alignment with the objective directions formalized in `OBJECTIVES_AND_CONSTRAINTS.md` (§3) and `DECISION_FRAMEWORK.md` (§3.1).

---

## 2. End-to-End Audit of All 11 Stage 2 KPIs

### 2.1 KPI 1: Secondary AMM Peg Volatility / RMSE (`peg_rmse`)

#### Mathematical Definition:
In continuous time over evaluation horizon $T = 1.0\text{ year}$, the secondary market peg tracking error root mean square is defined as:
$$J_{\text{peg}}(\mathbf{u}) = \sqrt{\frac{1}{T} \int_0^T \left( P_{\text{DEX}}(t) - 1.0000 \right)^2 dt}$$

In discrete simulation with timestep $\Delta t = 1/365\text{ year}$ and $N_{\text{steps}} = 365$ across $N_{\text{paths}} = 500$:
$$\text{RMSE}_p = \sqrt{\frac{1}{N_{\text{steps}}} \sum_{s=1}^{N_{\text{steps}}} \left( P_{\text{DEX}}(p, s) - 1.0000 \right)^2}, \quad \text{RMSE}_{\text{global}} = \sqrt{\frac{1}{N_{\text{paths}} N_{\text{steps}}} \sum_{p=1}^{N_{\text{paths}}} \sum_{s=1}^{N_{\text{steps}}} \left( P_{\text{DEX}}(p, s) - 1.0000 \right)^2}$$

#### Code Trace (`stage2_architecture_screening.py`):
```python
# Lines 243-255: Secondary DEX Price Evolution
err = P_dex - 1.0000
int_err = np.clip(int_err + err * dt, -0.10, 0.10)
u_t = np.clip(-K_p * err - K_i * int_err, -0.05, 0.05)
rate_mods[p, s] = u_t

arb_pull = (1.0000 - P_dex) / tau_arb
rate_demand_flow = u_t * alpha_flow / L_amm_base
dP_dex = (arb_pull + rate_demand_flow) * dt
P_dex = float(np.clip(P_dex + dP_dex, 0.50, 1.50))
peg_errors[p, s] = P_dex - 1.0000

# Line 307: Aggregation
peg_rmse = float(np.sqrt(np.mean(peg_errors**2)))
```

#### Parquet Storage & Empirical Distribution:
- **Parquet Column:** `peg_rmse` (`float64`)
- **Distribution ($N=1,600$):** $\text{Min} = 0.000000$, $\text{Mean} = 0.000000$, $\text{Max} = 0.000000$, $\text{Std} = 0.000000$.
- **Unique Values:** Exactly 1 (`0.0`).

#### Forensic Findings:
- **Integrity Status:** Mathematical formula is algebraically correct.
- **Root Cause of Degeneracy:** Initial condition $P_{\text{DEX}}(0) = 1.0000$ and initial integral error $\text{int\_err} = 0.0$ represent an exact unforced equilibrium point. In the absence of exogenous Poisson trade shocks or Brownian secondary order flow, $dP_{\text{DEX}} \equiv 0.0$.
- **Report Misstatement:** `SCREENING_STATISTICS.md` §3.1 states "Under the standard AMM arbitrage plant and continuous secondary price formation, the PI secondary controller stably bounds peg oscillations well below 5%." The metric did not prove controller stability; it merely recorded an unperturbed zero.

---

### 2.2 KPI 2: Maximum Peg Deviation (`max_depeg`)

#### Mathematical Definition:
$$\text{MaxDepeg}(\mathbf{u}) = \max_{p \in [1, N_{\text{paths}}]} \max_{s \in [1, N_{\text{steps}}]} |P_{\text{DEX}}(p, s) - 1.0000|$$

#### Code Trace (`stage2_architecture_screening.py`):
```python
# Line 308:
max_depeg = float(np.max(np.abs(peg_errors)))
```

#### Parquet Storage & Empirical Distribution:
- **Parquet Column:** `max_depeg` (`float64`)
- **Distribution ($N=1,600$):** $\text{Min} = 0.0000$, $\text{Mean} = 0.0000$, $\text{Max} = 0.0000$.
- **Unique Values:** Exactly 1 (`0.0`).

#### Forensic Findings:
- Identically zero due to unexcited secondary plant. Objective direction: **MINIMIZE** (Aligned).

---

### 2.3 KPI 3: Interest / Rebalancing Rate Volatility (`rate_volatility`)

#### Mathematical Definition:
$$\sigma_{\text{rate}}(\mathbf{u}) = \sqrt{\frac{1}{N_{\text{paths}} N_{\text{steps}}} \sum_{p=1}^{N_{\text{paths}}} \sum_{s=1}^{N_{\text{steps}}} \left( u(p, s) - \bar{u} \right)^2}$$

#### Code Trace (`stage2_architecture_screening.py`):
```python
# Line 315:
rate_vol = float(np.std(rate_mods))
```

#### Parquet Storage & Empirical Distribution:
- **Parquet Column:** `rate_volatility` (`float64`)
- **Distribution ($N=1,600$):** $\text{Min} = 0.0000$, $\text{Mean} = 0.0000$, $\text{Max} = 0.0000$.
- **Unique Values:** Exactly 1 (`0.0`).

#### Forensic Findings:
- Zero actuation signal variance because $P_{\text{dex}} \equiv 1.0 \implies u(t) \equiv 0.0$. Objective direction: **MINIMIZE** (Aligned).

---

### 2.4 KPI 4: Depeg Recovery Time (`recovery_time_days`)

#### Mathematical Definition:
$$\tau_{\text{settle}}(\mathbf{u}) = \mathbb{E}\left[ \inf \{ \Delta t > 0 \mid |P_{\text{DEX}}(t_{\text{depeg}} + \Delta t) - 1.0000| \le 0.0050 \} \right]$$

#### Code Trace (`stage2_architecture_screening.py`):
```python
# Lines 258-264:
if abs(P_dex - 1.0) > 0.005:
    if depeg_start_idx is None:
        depeg_start_idx = s
else:
    if depeg_start_idx is not None:
        recovery_times.append((s - depeg_start_idx) * dt * 365.0)
        depeg_start_idx = None

# Line 316:
avg_recov_time = float(np.mean(recovery_times)) if len(recovery_times) > 0 else 0.50
```

#### Parquet Storage & Empirical Distribution:
- **Parquet Column:** `recovery_time_days` (`float64`)
- **Distribution ($N=1,600$):** $\text{Min} = 0.500000$, $\text{Mean} = 0.500000$, $\text{Max} = 0.500000$.
- **Unique Values:** Exactly 1 (`0.5`).

#### Forensic Findings:
- **Hardcoded Fallback Artifact:** Because $|P_{\text{DEX}} - 1.0| > 0.005$ is never satisfied, `recovery_times` was empty for all 1,600 candidates, causing line 316 to return the hardcoded default `0.50`.
- **Right-Censoring Bias in Formula:** The logic only appends to `recovery_times` when the error returns below $0.005$. Any depeg occurring near $s=365$ that does not recover before the run ends is silently dropped rather than penalized as $\ge (365 - s)$, introducing survivorship/truncation bias.

---

### 2.5 KPI 5: Senior Principal Default Loss Frequency (`haircut_prob`)

#### Mathematical Definition:
Let $\mathcal{L}_p = \max_{s \in [1, N_{\text{steps}}]} h(p, s)$ be the maximum senior principal haircut fraction experienced on path $p \in [1, N_{\text{paths}}]$.
$$\mathbb{P}(\text{Haircut} > 0) = \frac{1}{N_{\text{paths}}} \sum_{p=1}^{N_{\text{paths}}} \mathbf{1}_{\{\mathcal{L}_p > 10^{-4}\}}$$

#### Code Trace (`stage2_architecture_screening.py`):
```python
# Architecture-specific deficit calculations (Lines 182-237):
# A0:
deficit = (V_A - 2.0 * S_t) / V_A
path_haircut = max(path_haircut, deficit)

# A2 (with reserve absorption):
deficit_usd = (V_A - 2.0 * S_t) * base_pool_savax
if B_res >= deficit_usd:
    B_res -= deficit_usd
else:
    uncovered = deficit_usd - B_res
    B_res = 0.0
    res_depleted = 1
    path_haircut = max(path_haircut, uncovered / (V_A * base_pool_savax))

# Line 309: Aggregation
haircut_prob = float(np.mean(haircuts > 0.0001))
```

#### Parquet Storage & Empirical Distribution:
- **Parquet Column:** `haircut_prob` (`float64`)
- **Distribution ($N=1,600$):**
  * Global: $\text{Min} = 0.0000$, $\text{Mean} = 0.4069$, $\text{Median} = 0.3920$, $\text{Max} = 0.7980$.
  * By Architecture:
    - $A_2$ (Solvency Buffer Vault): $\text{Mean} = 0.141\%$ ($319$ configurations $\le 1.0\%$).
    - $A_{5.3}$ (Multi-LST Basket): $\text{Mean} = 2.024\%$.
    - $A_{5.2}$ (Protocol AMM): $\text{Mean} = 9.164\%$.
    - $A_0$ (Dual Reset Legacy): $\text{Mean} = 13.675\%$.
    - $A_1, A_3, A_4$: $\text{Mean} = 74.200\%$ (constant across all 200 configs per arch).
    - $A_{5.1}$ (Convertible Debt): $\text{Mean} = 77.880\%$.

#### Forensic Findings:
- **Integrity Status:** **VERIFIED**. Genuinely discriminates across architectures.
- **Threshold Validation:** The $10^{-4}$ ($0.01\%$) threshold appropriately filters machine epsilon floating-point noise.
- **Objective Direction:** **MINIMIZE** (Aligned).

---

### 2.6 KPI 6: Conditional Value at Risk at 99% Confidence (`tail_cvar_99`)

#### Mathematical Definition:
For discrete losses $\mathcal{L}_p \ge 0$ across $N = 500$ paths:
$$\text{VaR}_{0.99}(\mathcal{L}) = \text{Quantile}_{0.99}(\mathcal{L})$$
$$\text{CVaR}_{0.99}(\mathcal{L}) = \mathbb{E}\left[ \mathcal{L}_p \;\middle|\; \mathcal{L}_p \ge \text{VaR}_{0.99}(\mathcal{L}) \right] = \frac{\sum_{p=1}^N \mathcal{L}_p \cdot \mathbf{1}_{\{\mathcal{L}_p \ge \text{VaR}_{0.99}\}}}{\sum_{p=1}^N \mathbf{1}_{\{\mathcal{L}_p \ge \text{VaR}_{0.99}\}}}$$

#### Code Trace (`stage2_architecture_screening.py`):
```python
# Line 310:
tail_cvar_99 = float(np.mean(haircuts[haircuts >= np.percentile(haircuts, 99.0)])) if np.sum(haircuts > 0) > 0 else 0.0
```

#### Parquet Storage & Empirical Distribution:
- **Parquet Column:** `tail_cvar_99` (`float64`)
- **Distribution ($N=1,600$):**
  * Global: $\text{Min} = 0.0000$, $\text{Mean} = 0.4842$, $\text{Median} = 0.3452$, $\text{Max} = 0.9790$.
  * By Architecture:
    - $A_2$: $\text{Mean} = 0.666\%$ (with $170$ configurations having strictly $0.000\%$).
    - $A_{5.3}$: $\text{Mean} = 5.574\%$.
    - $A_{5.2}$: $\text{Mean} = 31.537\%$.
    - $A_0$: $\text{Mean} = 33.827\%$.
    - $A_1, A_3, A_4$: $\text{Mean} = 97.898\%$ (constant).
    - $A_{5.1}$: $\text{Mean} = 22.041\%$.

#### Forensic Findings:
- **Integrity Status:** **VERIFIED**. Correct mathematical implementation of upper tail expectation.
- **Boundary Handling:** Correctly handles zero-haircut distributions via `if np.sum(haircuts > 0) > 0 else 0.0`.
- **Objective Direction:** **MINIMIZE** (Aligned).

---

### 2.7 KPI 7: Annual Reset / Rebalancing Churn Frequency (`reset_churn_annual`)

#### Mathematical Definition:
$$J_{\text{churn}}(\mathbf{u}) = \frac{365}{T} \cdot \frac{1}{N_{\text{paths}}} \sum_{p=1}^{N_{\text{paths}}} N_{\text{resets}}(p)$$

#### Code Trace (`stage2_architecture_screening.py`):
```python
# A0 (Lines 176-186):
if V_B >= H_u:
    resets += 1
    beta *= S_t
    epoch_v = 0.0
elif V_B <= H_d:
    resets += 1
    ...

# A2 (Lines 198-210):
if V_B <= H_d:
    resets += 1
    ...

# A5.2 & A5.3 (Lines 232-237):
if V_B <= H_d:
    resets += 1
    ...

# Line 314: Aggregation
avg_resets = float(np.mean(reset_counts))
```

#### Parquet Storage & Empirical Distribution:
- **Parquet Column:** `reset_churn_annual` (`float64`)
- **Distribution ($N=1,600$):**
  * Global: $\text{Min} = 0.0000$, $\text{Mean} = 1.8825$, $\text{Max} = 25.9340$.
  * By Architecture:
    - $A_0$: $\text{Mean} = 7.3675\text{ resets/yr}$ ($\text{Max} = 25.934$).
    - $A_2$: $\text{Mean} = 3.0406\text{ resets/yr}$ ($\text{Max} = 5.172$).
    - $A_{5.2}$: $\text{Mean} = 2.8854\text{ resets/yr}$.
    - $A_{5.3}$: $\text{Mean} = 1.7667\text{ resets/yr}$.
    - $A_1, A_3, A_4, A_{5.1}$: $\text{Mean} = 0.0000\text{ resets/yr}$ (continuous/no resets).

#### Forensic Findings:
- **Asymmetric Reset Counting Discrepancy:**
  * In $A_0$, resets are triggered on both upward ($V_B \ge H_u$) and downward ($V_B \le H_d$) breaches ($1.91$ upward + $3.47$ downward $= 5.38$ resets/yr at baseline).
  * In $A_2$, $A_{5.2}$, and $A_{5.3}$, the upward check `if V_B >= H_u:` was omitted.
  * Quantitative Impact: Comparing $A_0$ downward-only resets ($3.47$) to $A_2$ downward resets ($3.04$) reveals that the true structural churn reduction was $\approx 12.4\%$, not the reported $\approx 58.7\%$ reduction ($7.37 \to 3.04$).
- **Objective Direction:** **MINIMIZE** (Aligned).

---

### 2.8 KPI 8: Minimum Validator OpEx Coverage Ratio (`validator_cr_min`)

#### Mathematical Definition:
$$\text{CR}_{\text{OpEx}}(p, s) = \frac{\omega_{\text{val}}(p, s) \cdot \Phi_{\text{gross}}(p, s)}{\text{OpEx}_{\text{daily}}}$$
$$\text{CR}_{\text{OpEx, min}}(\mathbf{u}) = \frac{1}{N_{\text{paths}}} \sum_{p=1}^{N_{\text{paths}}} \min_{s \in [1, N_{\text{steps}}]} \text{CR}_{\text{OpEx}}(p, s)$$

#### Code Trace (`stage2_architecture_screening.py`):
```python
# Lines 129, 267, 290-293:
validator_annual_opex = 1450 * 350.0 * 12.0  # $6,090,000
gross_surplus_flow = base_staking_apr * base_pool_savax * P_t * 25.0 * dt
validator_income_flow = gross_surplus_flow * w_val
daily_opex_cost = validator_annual_opex * dt
cr_val = validator_income_flow / daily_opex_cost if daily_opex_cost > 0 else 2.0
min_cr_val = min(min_cr_val, cr_val)

# Line 311: Aggregation
val_cr_mean = float(np.mean(validator_cr_mins))
```

#### Parquet Storage & Empirical Distribution:
- **Parquet Column:** `validator_cr_min` (`float64`)
- **Distribution ($N=1,600$):**
  * Global: $\text{Min} = 0.000128$, $\text{Mean} = 0.022927$, $\text{Max} = 0.086148$.
  * By Policy:
    - $\text{POL-02}$ (Countercyclical): $\text{Mean} = 0.030886$ (Highest).
    - $\text{POL-05}$ (Softmax): $\text{Mean} = 0.027003$.
    - $\text{POL-01}$ (Static 65/20): $\text{Mean} = 0.025215$.
    - $\text{POL-03}$ (Reserve Priority): $\text{Mean} = 0.022340$.
    - $\text{POL-04}$ (Burn Maximizer): $\text{Mean} = 0.009323$ (Lowest).

#### Forensic Findings:
- **Integrity Status:** **VERIFIED** as sub-scale proportional metric.
- **Sub-Scale Context:** $1\text{M sAVAX}$ test pool ($\$25\text{M}$ TVL) earns $\sim \$1.6\text{M}$ annual gross staking yield. Against a $\$6.09\text{M}$ network OpEx, a $20\%$ allocation yields $\text{CR} \approx 0.0525$ at $P=1.0$, dipping to $\sim 0.02$ during drawdowns. Scaling to production ($100\text{M sAVAX}$) scales $\text{CR}$ by $100\times \to 2.29\times$.
- **Path Aggregation Order:** Correctly aggregates the arithmetic mean of path minimums.
- **Objective Direction:** **MAXIMIZE** (Aligned).

---

### 2.9 KPI 9: Validator Operational Insolvency Probability (`validator_insolvency_prob`)

#### Mathematical Definition:
$$\mathbb{P}(\text{Insolvency}) = \frac{1}{N_{\text{paths}}} \sum_{p=1}^{N_{\text{paths}}} \mathbf{1}_{\{\min_s \text{CR}_{\text{OpEx}}(p, s) < 1.2000\}}$$

#### Code Trace (`stage2_architecture_screening.py`):
```python
# Line 312:
val_insolv_prob = float(np.mean(validator_cr_mins < 1.20))
```

#### Parquet Storage & Empirical Distribution:
- **Parquet Column:** `validator_insolvency_prob` (`float64`)
- **Distribution ($N=1,600$):** $\text{Min} = 1.0000$, $\text{Mean} = 1.0000$, $\text{Max} = 1.0000$.
- **Unique Values:** Exactly 1 (`1.0`).

#### Forensic Findings:
- **Scale-Mismatched Threshold Tautology:** Because the full-scale threshold ($1.20\times$) was tested against a $1\text{M}$ test vault where $\max(\text{CR}) = 0.0861 < 1.20$, the condition `validator_cr_mins < 1.20` was trivially true for all $500$ paths across all $1,600$ configurations.
- **Objective Direction:** **MINIMIZE** (Aligned, but metric carries zero discriminative information in Stage 2).

---

### 2.10 KPI 10: Cumulative AVAX Token Burn Volume (`avax_burned_total`)

#### Mathematical Definition:
In continuous time:
$$J_{\text{burn}}(\mathbf{u}) = \int_0^T \omega_{\text{burn}}(t) \cdot \Phi_{\text{gross}}(t) \, dt$$
In discrete steps:
$$\text{Burn}_p = \sum_{s=1}^{N_{\text{steps}}} \omega_{\text{burn}}(p, s) \cdot \left[ q_{\text{sAVAX}} \cdot C_{\text{sAVAX}} \cdot P_t \cdot P_0 \cdot \Delta t \right]$$

#### Code Trace (`stage2_architecture_screening.py`):
```python
# Lines 267, 296, 313:
gross_surplus_flow = base_staking_apr * base_pool_savax * P_t * 25.0 * dt
cum_burn += gross_surplus_flow * w_burn
avg_burn = float(np.mean(burn_totals))
```

#### Parquet Storage & Empirical Distribution:
- **Parquet Column:** `avax_burned_total` (`float64`)
- **Distribution ($N=1,600$):**
  * Global: $\text{Min} = 0.00$, $\text{Mean} = 669,968.57$, $\text{Median} = 687,665.34$, $\text{Max} = 1,419,592.39$.
  * By Policy:
    - $\text{POL-04}$ (Burn Maximizer): $\text{Mean} = \$1,155,426.03$.
    - $\text{POL-05}$ (Softmax Dynamic): $\text{Mean} = \$764,992.34$.
    - $\text{POL-03}$ (Reserve Priority): $\text{Mean} = \$731,143.91$.
    - $\text{POL-01}$ (Static 65/20): $\text{Mean} = \$357,901.89$.
    - $\text{POL-02}$ (Countercyclical): $\text{Mean} = \$340,378.75$.

#### Forensic Findings:
- **Integrity Status:** **VERIFIED** as cumulative gross USD yield allocation.
- **Unit Mislabeling in Reports:** The code accumulates gross USD yield allocated to buybacks ($\$$). In reports, this was labeled as "Mean AVAX Burn (AVAX)" while displaying dollar signs (`$1,155,426`). If converting to physical AVAX tokens burned ($\text{USD} / P_{\text{AVAX}}(t)$), spot price $P_{\text{AVAX}}(t)$ cancels out:
  $$\Delta \text{AVAX}_{\text{burn}} = \omega_{\text{burn}}(t) \cdot q \cdot C_{\text{sAVAX}} \cdot \Delta t = \omega_{\text{burn}} \cdot (0.064 \times 1,000,000) \cdot \frac{1}{365} \approx 175.34 \cdot \omega_{\text{burn}}\text{ AVAX/day}$$
  Annual physical AVAX tokens burned for $\omega_{\text{burn}} = 0.65$ is $41,600\text{ AVAX/year}$ (equivalent to $\$1,040,000$ at $P=\$25$).
- **Objective Direction:** **MAXIMIZE** (Aligned).

---

### 2.11 KPI 11: Reserve Buffer Depletion Frequency (`reserve_depletion_prob`)

#### Mathematical Definition:
$$\mathbb{P}(\text{Depletion}) = \frac{1}{N_{\text{paths}}} \sum_{p=1}^{N_{\text{paths}}} \mathbf{1}_{\{\text{ReserveBufferDepleted}_p = 1\}}$$

#### Code Trace (`stage2_architecture_screening.py`):
```python
# Lines 206-208 (in A2):
if B_res < deficit_usd:
    uncovered = deficit_usd - B_res
    B_res = 0.0
    res_depleted = 1

# Line 317: Aggregation
res_depletion_prob = float(np.mean(res_depletions))
```

#### Parquet Storage & Empirical Distribution:
- **Parquet Column:** `reserve_depletion_prob` (`float64`)
- **Distribution ($N=1,600$):**
  * Architecture $A_2$: $\text{Min} = 0.0000$, $\text{Mean} = 0.001410$ ($0.141\%$), $\text{Max} = 0.0780$ ($7.8\%$). Active non-zero in 29 configurations.
  * Non-$A_2$ Architectures: Identically $0.0000$.

#### Forensic Findings:
- **Integrity Status:** **VERIFIED** as an architecture-specific health metric for $A_2$.
- **Objective Direction:** **MINIMIZE** (Aligned).

---

## 3. Objective Optimization Direction & Sign Convention Alignment

We reconciled every KPI against the canonical optimization formulations in `OBJECTIVES_AND_CONSTRAINTS.md` (§3 Tier 2 Objectives) and `DECISION_FRAMEWORK.md` (§3.1 Multi-Objective Vector Problem $\mathbf{J}(\mathbf{u})$):

$$\min_{\mathbf{u} \in \mathcal{U}_{\text{feasible}}} \mathbf{J}(\mathbf{u}) = \begin{bmatrix}
J_1(\mathbf{u}) = \sigma_{\text{peg}}(\mathbf{u}) & \text{(Annualized Secondary Peg Volatility)} \\
J_2(\mathbf{u}) = f_{\text{reset}}(\mathbf{u}) & \text{(Annual Reset / Rebalancing Churn)} \\
J_3(\mathbf{u}) = \mathcal{L}_{\max}(\mathbf{u}) & \text{(Maximum Flash Crash Haircut Loss)} \\
J_4(\mathbf{u}) = -\Phi_{\text{burn}}(\mathbf{u}) & \text{(Annual AVAX Buyback \& Burn Volume)} \\
J_5(\mathbf{u}) = -\text{CR}_{\text{OpEx, min}}(\mathbf{u}) & \text{(Minimum Validator OpEx Coverage Floor)} \\
J_6(\mathbf{u}) = \bar{S}_T(\mathbf{u}) & \text{(Parameter Fragility / Mean Sobol Total Sensitivity)}
\end{bmatrix}$$

```
========================================================================================================================
                                      OBJECTIVE DIRECTION RECONCILIATION TABLE
========================================================================================================================
```

| Metric Name | Parquet Column | Canonical Math ID | Specification Direction | Framework Direction | Storage Sign | Solver Transformation | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Peg RMSE** | `peg_rmse` | $J_1 / J_{\text{peg}}$ | **MINIMIZE** | **MINIMIZE** | Positive ($\ge 0$) | $\min J_1$ | **ALIGNED** |
| **Max Depeg** | `max_depeg` | $\text{MaxDepeg}$ | **MINIMIZE** | **MINIMIZE** | Positive ($\ge 0$) | $\min \text{MaxDepeg}$ | **ALIGNED** |
| **Rate Volatility** | `rate_volatility` | $\sigma_{\text{rate}}$ | **MINIMIZE** | **MINIMIZE** | Positive ($\ge 0$) | $\min \sigma_{\text{rate}}$ | **ALIGNED** |
| **Recovery Time** | `recovery_time_days` | $J_{\text{settle}}$ | **MINIMIZE** | **MINIMIZE** | Positive ($\ge 0$) | $\min J_{\text{settle}}$ | **ALIGNED** |
| **Haircut Prob** | `haircut_prob` | $\mathbb{P}(\text{Loss}) / J_3$| **MINIMIZE** | **MINIMIZE** | Positive ($\in [0, 1]$)| $\min \mathbb{P}(\text{Loss})$| **ALIGNED** |
| **Tail CVaR 99** | `tail_cvar_99` | $J_{\text{tail}}$ | **MINIMIZE** | **MINIMIZE** | Positive ($\in [0, 1]$)| $\min J_{\text{tail}}$ | **ALIGNED** |
| **Reset Churn** | `reset_churn_annual` | $J_2 / J_{\text{churn}}$ | **MINIMIZE** | **MINIMIZE** | Positive ($\ge 0$) | $\min J_2$ | **ALIGNED** |
| **Validator CR Min**| `validator_cr_min` | $J_5 / J_{\text{val}}$ | **MAXIMIZE** | **MAXIMIZE** | Positive ($\ge 0$) | $\min -J_5$ (Negation)| **ALIGNED** |
| **Val Insolvency** | `validator_insolvency_prob`| $U_{\text{val}}$ | **MINIMIZE** | **MINIMIZE** | Positive ($\in [0, 1]$)| $\min \mathbb{P}(\text{Insolv})$| **ALIGNED** |
| **AVAX Burned** | `avax_burned_total` | $J_4 / J_{\text{burn}}$ | **MAXIMIZE** | **MAXIMIZE** | Positive ($\ge 0$) | $\min -J_4$ (Negation)| **ALIGNED** |
| **Reserve Deplete** | `reserve_depletion_prob` | $D03$ | **MINIMIZE** | **MINIMIZE** | Positive ($\in [0, 1]$)| $\min \mathbb{P}(\text{Deplete})$| **ALIGNED** |

**Conclusion on Optimization Direction:** Zero sign inversion errors or conflicting optimization directions were identified between specifications, decision frameworks, and code implementation.

---

## 4. Methodological, Numerical & Structural Bias Audit

### 4.1 Time-Stepping Causal Invariance (Look-Ahead Bias Check)
We traced the execution order of the daily time-stepping loop in `simulate_single_candidate`:
1. **Price Observation:** $P_t = P_{\text{path}}[s+1]$ (observed realization at $t = (s+1)\Delta t$).
2. **Tranche NAV Evaluation:** $S_t = P_t / \beta_t$ evaluated using current price and current epoch base $\beta_t$.
3. **Barrier Evaluation & Deleveraging:** Reset state updates ($\beta_{t+1} = \beta_t \cdot S_t$) occur immediately upon threshold breach.
4. **Controller Actuation:** $u_t = \text{clip}(-K_p e_t - K_i \int e dt, -0.05, 0.05)$ uses beginning-of-step error.
5. **Surplus Cashflow Allocation:** $\Phi_{\text{gross}}(t)$ and $\boldsymbol{\omega}(t)$ use current spot drawdown $S_t$.
*Verdict:* **Zero Look-Ahead Bias**. All state updates and policy actions are strictly causal forward-Euler operations.

### 4.2 Denominator Singularities & Algebraic Tautologies
- **Guarded Denominators:**
  * $\beta_t$: Clamped to $\max(0.01, S_t)$, preventing $\beta \to 0$ and $S_t = P_t / \beta \to \infty$.
  * $V_A(t) = 1.0 + R \cdot \text{epoch\_v} \ge 1.0$, preventing zero division in $(V_A - 2S_t)/V_A$.
  * $\text{daily\_opex\_cost} = \$16,684.93 > 0$, preventing zero division in coverage ratio calculations.
- **Tautological Saturation:**
  * `validator_insolvency_prob`: $100\%$ saturation due to scale-mismatched $1.20\times$ threshold against $1\text{M}$ test vault.
  * `peg_rmse`, `max_depeg`, `rate_volatility`: $0.0000$ due to unexcited deterministic equilibrium.

### 4.3 Monte Carlo Aggregation & Quantile Estimation
- **Sample Size:** $N = 500$ paths per candidate configuration. Total evaluations: $1,600 \times 500 = 800,000$ paths ($292,000,000$ step transitions).
- **CVaR 99 Quantile Estimator:**
  * Uses `np.percentile(haircuts, 99.0)`. In a sample of $N=500$, the 99th percentile isolates the worst 5-6 paths ($1\%$ tail).
  * Arithmetic mean of upper tail is conditionally unbiased.
- **Zero Survivorship Bias:** 1,600 out of 1,600 configurations completed without dropped paths or unhandled exceptions.

---

## 5. Behavioral Parameter Audit (BPA) Summary Trace

Applying the 10-Step Behavioral Parameter Audit protocol to the Stage 2 control and policy parameters:

```
========================================================================================================================
                                      BEHAVIORAL PARAMETER AUDIT (BPA) TRACE
========================================================================================================================
```

| Parameter | Symbol | Step 1: Decision Margin | Step 2: Governing Equation | Step 3: Type | Step 5: Dyn/Stat | Step 6: Units | Step 8: Calibration Status |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **Proportional Gain** | $K_p$ | AMM Spread Arb Rate | $u_t = -K_p e_t - K_i \int e dt$ | Gain Coefficient | Dynamic | $\text{yr}^{-1} / (\$/\$)$ | Pinned ($0.150$) |
| **Integral Gain** | $K_i$ | Steady-State Error | $\dot{u}_t = -K_i (P_{\text{dex}} - 1)$ | Learning Rate | Dynamic | $\text{yr}^{-2} / (\$/\$)$ | Pinned ($0.020$) |
| **Rate Modulation Clamp**| $\Delta R'_{\max}$ | Anti-Windup Security | $|u_t| \le \Delta R'_{\max}$ | Upper Bound | Static | $\text{yr}^{-1}$ (APR) | Pinned ($\pm 5.0\%$) |
| **Drawdown Feedback** | $\kappa_{\text{dd}}$ | Node OpEx Subsidy | $\omega_{\text{val}} = \omega_0 + \kappa_{\text{dd}} (1 - S)$ | Sensitivity Coeff | Dynamic | Dimensionless | Pinned ($0.350$) |
| **Arbitrage Lag** | $\tau_{\text{arb}}$ | DEX Liquidity Pull | $\dot{P} = (1 - P)/\tau_{\text{arb}} + u \alpha / L$ | Time Constant | Dynamic | Years ($5.55\text{d}$) | Calibrated Empirical |
| **AMM Plant Gain** | $K_{\text{dc}}$ | Secondary Slippage | $K_{\text{dc}} = \alpha_{\text{flow}} \tau_{\text{arb}} / L_{\text{amm}}$ | Plant Gain | Static | $(\$/\$) / \text{yr}^{-1}$ | Calibrated ($0.667$) |

---

## 6. Discrepancy & Defect Register

| Defect ID | Severity | Category | Description | Root Cause | Impact on Stage 2 Findings | Recommended Stage 3/4 Fix |
| :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| **DEF-01** | **Moderate** | Secondary Plant | `peg_rmse`, `max_depeg`, `rate_volatility` degenerate to $0.0$. | No exogenous trade flow or collateral coupling in secondary AMM. | Peg stability gates passed trivially; did not test controller rejection. | Inject Kou Poisson DEX trade flow and Brownian arbitrage noise. |
| **DEF-02** | **Minor** | Metric Fallback | `recovery_time_days` equals hardcoded `0.50` days. | Recovery list empty because peg never depegged $> 0.5\%$. | Metric has zero variance across all 1,600 rows. | Calculate recovery times from active noise shocks in Stage 4. |
| **DEF-03** | **Moderate** | Scale Threshold | `validator_insolvency_prob` saturates at $1.0000$ ($100\%$). | Production threshold $1.20\times$ tested on $1\text{M}$ sub-scale vault. | Zero discriminative power across architectures/policies. | Scale pool to production ($100\text{M sAVAX}$) or normalize threshold ($0.02\times$). |
| **DEF-04** | **Major** | Implementation | Upward reset ($V_B \ge H_u$) omitted in $A_2, A_{5.2}, A_{5.3}$. | Code lines 198 & 233 check only `if V_B <= H_d:`. | Exaggerated reset churn reduction between $A_0$ and $A_2$. | Unify reset condition `if V_B >= H_u or V_B <= H_d:` across all topologies. |
| **DEF-05** | **Minor** | Documentation | AVAX Burn unit conflation (USD cashflow vs token count). | `avax_burned_total` accumulates USD yield; report labels as AVAX. | Cosmetic reporting ambiguity; relative rankings preserved. | Explicitly report both `USD_burned_annual` and `AVAX_tokens_burned`. |

---

## 7. Verification Artifacts & Independent Reproducibility

1. **Standalone Verification Script:** `audit_artifacts/execution/verify_stage2_kpi_mathematics.py`
   - Executes full programmatic verification across all 11 KPIs.
   - Recomputes candidate lifecycle simulations on raw Kou CRN price paths.
   - Confirms $100.00\%$ bit-for-bit mathematical reproducibility.
2. **Automated Pytest Test Suite:** `simulations/design_discovery/test_stage2_kpi_calculations.py`
   - Contains 10 automated test functions covering:
     * Dataset integrity and no-NaN checks.
     * Objective direction alignment.
     * KPI value domain boundaries.
     * Peg dynamics unexcited fixed-point analysis.
     * Validator scale-mismatched saturation analysis.
     * Architecture solvency separation ($A_2$ vs $A_{5.3}$ vs $A_0$ vs $A_1/3/4$).
     * Loss parity among unbuffered architectures ($A_1, A_3, A_4$).
     * Policy trade-off verification ($\text{POL-04}$ vs $\text{POL-02}$).
     * Reserve depletion $A_2$ isolation.
     * Bit-for-bit CRN recomputation.
   - Result: **10 passed in 10.84 seconds** (and 17/17 passed across `simulations/design_discovery/`).

---

## 8. Epistemic Verdict & Final Recommendation

| Requirement | Audit Scope | Verification Status | Final Epistemic Verdict |
| :---: | :--- | :---: | :---: |
| **R3.1** | Mathematical Formulation $\to$ Implementation Equivalence | $11/11$ KPIs Audited | **VERIFIED (With Documented Asymmetries)** |
| **R3.2** | Objective Optimization Direction Alignment | $11/11$ Directions Aligned | **VERIFIED (100% Consistent)** |
| **R3.3** | Numerical Bias, Look-Ahead & Tautology Checks | Exhaustive Check Complete | **DEFECTS FORMALLY REGISTERED (DEF 01–05)** |
| **R3.4** | Independent Recomputation & Bit-for-Bit Reproducibility | Confirmed on CRN Stream | **VERIFIED (Bit-for-Bit Exact)** |

**Final Recommendation:** **PROCEED TO DOWNSTREAM MILESTONES (M4, M5, M6)** with full incorporation of registered defects (DEF-01 through DEF-05) into the final Adversarial Validation Report.
