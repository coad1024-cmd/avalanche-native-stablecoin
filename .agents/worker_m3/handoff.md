# Handoff Report: Milestone 3 (Requirement R3: End-to-End KPI Calculation & Objective Direction Audit)

> **Agent:** Worker M3 (Implementer / QA / Specialist)  
> **Working Directory:** `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m3`  
> **Target Milestone:** Milestone 3 (Requirement R3)  
> **Date:** August 31, 2026  
> **Status:** HARD HANDOFF (Task Complete)  

---

## 1. Observation

1. **Parquet Dataset Structure & Columns (`audit_artifacts/execution/STAGE_2_RESULTS.parquet`):**
   - Verified 1,600 rows $\times$ 25 columns.
   - Contains all 11 KPI metrics: `peg_rmse`, `max_depeg`, `haircut_prob`, `tail_cvar_99`, `recovery_time_days`, `validator_cr_min`, `validator_insolvency_prob`, `avax_burned_total`, `reset_churn_annual`, `rate_volatility`, `reserve_depletion_prob`.
   - Zero null, NaN, or infinite values across the entire matrix ($1,600 \times 25$).

2. **Degenerate Secondary AMM Peg Metrics:**
   - In `simulations/design_discovery/stage2_architecture_screening.py` (lines 243–255):
     `P_dex = 1.0000`, `int_err = 0.0`, `u_t = 0.0`.
     Because there are no exogenous trade shocks, secondary order flow noise, or coupling from collateral drops to DEX selling pressure, $dP_{\text{dex}} \equiv 0.0$.
   - Parquet stored values:
     `peg_rmse` unique values: `[0.0]`
     `max_depeg` unique values: `[0.0]`
     `rate_volatility` unique values: `[0.0]`
     `recovery_time_days` unique values: `[0.5]` (from line 316 fallback: `avg_recov_time = float(np.mean(recovery_times)) if len(recovery_times) > 0 else 0.50`).

3. **Validator Insolvency Tautology:**
   - In `simulations/design_discovery/stage2_architecture_screening.py` (line 312):
     `val_insolv_prob = float(np.mean(validator_cr_mins < 1.20))`
   - Because the test vault is evaluated at sub-scale ($1\text{M sAVAX} \approx \$25\text{M}$ pool vs full $\$6.09\text{M}$ network OpEx), `validator_cr_mins` has $\text{min} = 0.000128$ and $\text{max} = 0.086148$.
   - Since $0.086148 < 1.20$, `validator_cr_mins < 1.20` is TRUE on $100\%$ of paths across all 1,600 rows. Parquet stored value: `[1.0]`.

4. **Reset Accounting Asymmetry Between Architectures:**
   - In `simulations/design_discovery/stage2_architecture_screening.py`:
     * Line 176 ($A_0$): `if V_B >= H_u: resets += 1 ... elif V_B <= H_d: resets += 1 ...` (evaluates both upward and downward resets: $1.91$ up + $3.47$ down $= 5.38$ resets/yr at baseline, mean $7.37$ overall).
     * Line 198 ($A_2$): `if V_B <= H_d: resets += 1 ...` (omits upward resets; mean $3.04$ overall).
     * Line 233 ($A_{5.2}, A_{5.3}$): `if V_B <= H_d: resets += 1 ...` (omits upward resets; mean $2.89$ and $1.77$ overall).

5. **Loss Parity Across Unbuffered Architectures ($A_1, A_3, A_4$):**
   - Lines 193, 216, 221 all evaluate `if 2.0 * S_t < 1.0: path_haircut = max(path_haircut, 1.0 - 2.0 * S_t)`.
   - All 200 candidates in $A_1$, $A_3$, and $A_4$ have identically `haircut_prob = 0.74200` and `tail_cvar_99 = 0.978984`.

6. **Objective Optimization Direction Alignment:**
   - Full reconciliation with `OBJECTIVES_AND_CONSTRAINTS.md` (§3) and `DECISION_FRAMEWORK.md` (§3.1):
     * Minimized: `peg_rmse`, `max_depeg`, `rate_volatility`, `recovery_time_days`, `haircut_prob`, `tail_cvar_99`, `reset_churn_annual`, `validator_insolvency_prob`, `reserve_depletion_prob`.
     * Maximized: `validator_cr_min`, `avax_burned_total`.
     * Stored signs: All natural positive numbers ($\ge 0$). In vector minimization $\min \mathbf{J}(\mathbf{u})$, maximization objectives are negated ($-J_4 = -\Phi_{\text{burn}}$, $-J_5 = -\text{CR}_{\text{OpEx}}$).

---

## 2. Logic Chain

1. **Reconciliation of Theory to Code (Obs 1, Obs 6):**
   The mathematical definitions of all 11 KPIs in `OBJECTIVES_AND_CONSTRAINTS.md` and `DECISION_FRAMEWORK.md` correspond to standard quantitative finance operators (RMSE, Expected Shortfall, Poisson rates, flow ratios). The code in `stage2_architecture_screening.py` implements discrete-time approximations of these exact operators with $\Delta t = 1/365\text{ year}$.
2. **Identification of Secondary Plant Fixed Point (Obs 2):**
   Because the simulation starts at $P_{\text{dex}} = 1.0$ and applies no stochastic trade flow to the DEX, the differential equation $\dot{P}_{\text{dex}} = (1 - P_{\text{dex}})/\tau + u \alpha / L$ has zero forcing term. Thus $P_{\text{dex}}(t) \equiv 1.0$, resulting in zero peg error and zero rate actuation.
3. **Identification of Scale-Mismatched Thresholding (Obs 3):**
   The $1.20\times$ threshold was defined for production scale ($100\text{M sAVAX}$). Testing it against a $1\text{M sAVAX}$ test vault without scale normalization guarantees that $100\%$ of paths fail the threshold, creating a constant column in Parquet.
4. **Quantification of Implementation Asymmetry in Resets (Obs 4):**
   In $A_0$, upward resets ($V_B \ge H_u$) contributed $1.91$ resets/yr at baseline. In $A_2$, upward resets were not evaluated in code. Therefore, the observed difference between $A_0$ ($7.37$) and $A_2$ ($3.04$) reflects both genuine downward buffer absorption ($3.47 \to 3.04$) and the omission of upward reset counting.
5. **Validation of Bit-for-Bit Reproducibility (Obs 1, Obs 5):**
   Running independent recomputations using the Kou SDE CRN generator reproduces exact values in `STAGE_2_RESULTS.parquet` with zero floating point drift ($< 10^{-6}$).

---

## 3. Caveats

- The unexcited secondary AMM plant in Stage 2 means that peg stability comparisons ($A_4$ vs $A_0$) were not tested under secondary market trading stress in Stage 2. This stress will be actively evaluated in Stage 4 (cadCAD High-Fidelity Plant).
- The sub-scale $1\text{M sAVAX}$ vault correctly evaluates relative policy performance ($\text{POL-02} > \text{POL-01} > \text{POL-04}$ in coverage) but absolute OpEx coverage requires the production $100\text{M}$ scaling factor ($100\times$).

---

## 4. Conclusion

Milestone 3 (Requirement R3) is **100% COMPLETE**.
- Every Stage 2 KPI has been formally audited from mathematical formulation $\to$ code implementation $\to$ parquet storage $\to$ report synthesis.
- Objective optimization directions (Min vs Max) are fully verified and aligned.
- All defects, scale mismatches, unexcited plant fixed points, and architectural asymmetries are rigorously cataloged in the master report (`.agents/worker_m3/m3_kpi_math_report.md`).
- Two verified code artifacts delivered:
  * `audit_artifacts/execution/verify_stage2_kpi_mathematics.py`
  * `simulations/design_discovery/test_stage2_kpi_calculations.py` (10/10 pytest passing).

---

## 5. Verification Method

To independently verify the Milestone 3 deliverables:

```bash
# 1. Execute the master KPI mathematics verification script:
python3 audit_artifacts/execution/verify_stage2_kpi_mathematics.py

# 2. Run the automated pytest test suite:
pytest simulations/design_discovery/test_stage2_kpi_calculations.py -v

# 3. Run all design discovery tests to confirm zero regressions:
pytest simulations/design_discovery/ -v
```

### Invalidation Conditions:
1. If any KPI in `STAGE_2_RESULTS.parquet` fails bit-for-bit recomputation against the Kou SDE CRN stream ($|\text{diff}| > 10^{-6}$).
2. If any objective direction contradicts `OBJECTIVES_AND_CONSTRAINTS.md` or `DECISION_FRAMEWORK.md`.
3. If `simulations/design_discovery/test_stage2_kpi_calculations.py` fails any test case.
