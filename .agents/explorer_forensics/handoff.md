# Forensic Investigation & Discrepancy Reconciliation Report

> **Document Identifier:** `BCRG-AUDIT-FORENSICS-RECONCILIATION-01`  
> **Agent:** Explorer Forensics  
> **Working Directory:** `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_forensics/`  
> **Status:** COMPLETE — Hard Handoff  
> **Date:** August 30, 2026  
> **Governing Standards:** No Trust Transfer, First-Principles Code & Mathematical Tracing, 5-Component Handoff  

---

## 1. Observation

Direct forensic examination of the codebase, simulation engines, reports, registers, and provenance manifests yielded the following verbatim observations:

### Issue 1: GSA Sobol First-Order Index Implementation & Mathematical Flaw
- **File:** `simulations/robustness_study/sobol_sensitivity.py`, lines 81–88:
  ```python
  81:         # First-order index formula: S_i = ( (1/N) sum(y_A * y_AB_i) - (E[y])^2 ) / Var(y)
  82:         f_0_sq = np.mean(y_A) * np.mean(y_B)
  83:         v_i = np.mean(y_B * (y_AB_i - y_A))
  84:         S_i[i] = max(0.0, min(1.0, (np.mean(y_A * y_AB_i) - f_0_sq) / var_total))
  85:         
  86:         # Total-order index formula: S_Ti = ( (1/(2N)) sum( (y_A - y_AB_i)^2 ) ) / Var(y)
  87:         S_Ti[i] = max(S_i[i], min(1.5, np.mean((y_A - y_AB_i)**2) / (2.0 * var_total)))
  ```
- **File:** `simulations/robustness_study/master_robustness_engine.py`, lines 146, 211–248:
  - Line 146: `P_dex += np.random.normal(0.0, 0.001)` injects unseeded Gaussian microstructure noise during every epoch evaluation.
  - Lines 216–245: Runs 1,152 evaluations ($N_{\text{base}} = 64, D = 8$). Peg volatility ensemble has $\text{mean}(Y) \approx 42.1723$, sample variance $\text{Var}(Y) \approx 0.025515$.
  - Evaluation of the raw numerator on line 84:
    $$\text{Num}_i = \frac{1}{N}\sum y_A y_{AB_i} - \bar{y}_A \bar{y}_B \in [0.9206, 2.9353]$$
    Raw ratio $\frac{\text{Num}_i}{\text{Var}(Y)} \in [36.08, 115.04] \gg 1.00$.
- **File:** `simulations/robustness_study/sobol_peg_volatility_indices.csv`, lines 1–10:
  ```csv
  parameter,first_order_Si,total_order_STi,interaction_effect
  H_u,1.0,1.076330500848303,0.07633050084830306
  omega_burn,1.0,1.0654581105704934,0.06545811057049344
  coupon_R,1.0,1.0,0.0
  coupon_R_prime,1.0,1.0,0.0
  H_d,1.0,1.0,0.0
  omega_val,1.0,1.0,0.0
  Kp,1.0,1.0,0.0
  Ki,1.0,1.0,0.0
  ```
- **File:** `audit_artifacts/reports/GLOBAL_SENSITIVITY_ANALYSIS.md`, lines 23–32 verbatim publishes this table with $S_i = 1.0000$ for all 8 parameters, claiming $\sum S_i = 8.0000$ and identifying all parameters as fully identifiable.

---

### Issue 2: Data Ingestion Reality vs Synthetic SDE Generator
- **Directory:** `data/` contains exclusively `_lineage.jsonl` (5,604 bytes). Zero raw tick files, zero API clients, zero order-book dumps, zero on-chain transaction data.
- **File:** `simulations/empirical_calibration.py`, lines 129–179, 215–251:
  - Lines 140–147: Hardcodes synthetic ground-truth parameters:
    ```python
    true_mu = 0.18
    true_sigma = 0.885
    true_lambda = 2.50
    true_p = 0.42
    true_eta1 = 3.20  # Mean up-jump = +31.25%
    true_eta2 = 2.10  # Mean down-jump = -47.62%
    ```
  - Lines 176–177: Synthesizes staking yield via $q_t = 0.0585 + 0.008 \sin(2\pi t / 365) + \mathcal{N}(0, 0.003)$.
  - Line 217: `run_full_calibration_pipeline()` calls `generate_synthetic_historical_avax_series()`.
  - Lines 219–221: Fits MLE and bootstrap intervals on this synthetic series, recovering $\sigma = 89.13\%$, $\lambda = 3.00$, $\eta_1 = 3.181$, $\eta_2 = 2.331$, $\bar{q} = 5.85\%$.
  - Line 248: Writes output to `audit_artifacts/provenance/calibrated_market_parameters.json`.
- **File:** `audit_artifacts/registers/DATA_REQUIREMENTS.md`, line 5: `> **Status:** Phase 0 — No datasets ingested yet`.
- **File:** `audit_artifacts/reports/EMPIRICAL_CALIBRATION_REPORT.md`, lines 5, 23–32: Claims ingestion of `DAT-01` and `DAT-02`.

---

### Issue 3: Crash Safety Scoping ($-60.00\%$ from $H_d = 0.25$ vs $-75.00\%$ from Par $S = 1.00$)
- **File:** `docs/WHITEPAPER.tex`, lines 210–238 (Theorem 1 Proof and Corollary):
  - Theorem 1 establishes the single-step par redemption condition:
    $$\frac{\Delta P}{P} \ge \frac{1}{2}\left(\frac{R' v_t + 1}{R v_t + 1 + H_d}\right) - 1$$
  - Line 232: $\left(\frac{\Delta P}{P}\right)_{\text{barrier}} = \frac{1}{2}\left(\frac{1.00}{1.25}\right) - 1 = \mathbf{-60.0\%}$.
  - Line 236: $\left(\frac{\Delta P}{P}\right)_{\text{par}} = \frac{1}{2}\left(\frac{1.00}{2.00}\right) - 1 = \mathbf{-75.0\%}$.
- **File:** `audit_artifacts/reports/SOURCE_AND_DERIVATION_AUDIT.md`, lines 346–362:
  - If a $-75.00\%$ drop occurs at $H_d = 0.25$: post-jump pool index is $S^+ = 0.625 \times 0.25 = 0.15625$, secondary pool payout is $\$0.6250$, resulting in an immediate **$37.35\%$ haircut** on `anUSD`.
- **File:** `audit_artifacts/provenance/claims.yaml`, lines 16–25 (`CLM-002`): States "-60.00%" threshold, but earlier whitepaper text claimed unconditional "-75.00% flash crash tolerance".

---

### Issue 4: Controller Damping ($\zeta = 1.42$ vs $\zeta = 17.03$ vs Discrete Settling Time)
- **File:** `simulations/cadcad_core/mechanisms/feedback_controller.py`, lines 57–69:
  ```python
  zeta = (1.0 + plant_gain_K * self.K_p) / (2.0 * (plant_gain_K * self.K_i * plant_time_constant_tau) ** 0.5)
  ```
  - For $K_{\text{amm}} = 1.20, \tau_{\text{arb}} = 0.05, K_p = 0.150, K_i = 0.020$:
    $$\zeta = \frac{1.18}{2 \sqrt{1.20 \times 0.020 \times 0.05}} = \frac{1.18}{0.069282} = \mathbf{17.0312 \approx 17.03}$$
- **File:** `audit_artifacts/provenance/claims.yaml`, line 60: `empirical_value: 1.42`.
- **File:** `docs/validation/gates.yaml`, line 82: `damping ratio zeta = 1.42`.
- **File:** `audit_artifacts/reports/CONTROLLER_ABLATION_STUDY.md`, lines 22–36:
  - Thin liquidity ($L = \$1.5\text{M}$): Settling time drops from $28.1\text{ days}$ (Core alone) to $4.6\text{ days}$ (PI controller).
  - Base liquidity ($L = \$10.0\text{M}$): Settling time drops from $25.5\text{ days}$ to $12.1\text{ days}$.
  - PID with $K_d = 0.005$ produces $4.7\text{ days}$ and $12.2\text{ days}$ (no gain, amplifies noise).

---

### Issue 5: Redistribution Optimization Status (ACP-67 $\omega_{\text{burn}} = 0.65$)
- **File:** `simulations/cadcad_core/experiments/run_comprehensive_psuu_suite.py`, lines 78–108 (Track 2):
  - Evaluates static grid: `t2_burn = [0.50, 0.65, 0.75]`, `t2_val = [0.15, 0.20, 0.25]`, `t2_tvl = [$100M, $500M, $1B, $5B]`.
  - Calls `execute_acp67_yield_distribution(...)` which performs direct static multiplication `burn_usd = gross_yield_usd * omega_burn`.
  - Zero behavioral validator response function, zero token price feedback, zero endogenous optimization.
- **File:** `audit_artifacts/reports/ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md`, line 75: Categorizes $\omega_{\text{burn}} = 65.00\%$ as `"Governance Selected"` under `"ACP-67 Deflation Mandate"`.

---

### Issue 6: Architecture Exploration Status (Architectures B1–B4)
- **File:** `audit_artifacts/RESEARCH_PLAN_OPTIMIZATION.md`, lines 184–190, 274–276:
  - Mentions B1 (Continuous Share Amortization), B2 (Dedicated Solvency Reserve), B3 (Floating Junior Tranche), B4 (Pure Balance Sheet Arbitrage).
- **Search across Entire Filesystem:** Zero implementation files, zero test scripts, zero simulation data for B1–B4 in `simulations/`, `contracts/`, `docs/`, or `audit_artifacts/`.

---

### Issue 7: Pareto Optimization Status (NSGA-II / MOEA/D Multi-Objective Frontiers)
- **File:** `simulations/cadcad_core/experiments/run_comprehensive_psuu_suite.py`, lines 56–64, 170–201:
  - Metric values in `fig7_psuu_pareto_frontier.png` and `comprehensive_psuu_results.csv` generated by closed-form mock proxy equations:
    ```python
    peg_vol = 1.20 * (sig / 0.8986) * (1.0 + 0.10 * (hu - 2.0) - 0.15 * (hd - 0.25))
    annual_resets = 1.15 * (sig / 0.8986) * (1.0 / (hu - hd))
    ```
  - Zero evolutionary optimization (NSGA-II / MOEA/D) executed; zero non-dominated sorting or hypervolume calculation.

---

## 2. Logic Chain

```
[Observation 1: sobol_sensitivity.py:84 evaluates uncentered covariance ratio]
  ├── Observation 1.1: y_A and y_AB_i share 7/8 parameters -> y_A * y_AB_i ≈ y_A^2
  ├── Observation 1.2: Mean output μ ≈ 42.17% with small N=64 -> μ(ȳ_A - ȳ_B) ≈ 2.10
  ├── Observation 1.3: Ensemble variance Var(Y) ≈ 0.0255 -> Ratio ≈ 2.10 / 0.0255 = 82.6 >> 1.0
  ├── Observation 1.4: Line 84 clamps max(0.0, min(1.0, ...)) -> S_i pinned to 1.0000 for all 8 parameters
  └── Logic 1.5: S_Ti = max(S_i, ...) on Line 87 forces S_Ti >= 1.0000; report claims sum(S_i) = 8.0000 (mathematical impossibility).

[Observation 2: data/ contains only _lineage.jsonl; empirical_calibration.py generates synthetic SDE]
  ├── Observation 2.1: true_mu, true_sigma, true_lambda hardcoded on lines 141-146
  ├── Observation 2.2: MLE fitted against synthetic data generated on line 217
  └── Logic 2.3: Zero empirical exchange or on-chain feeds (DAT-01..DAT-07) were ingested; calibration is closed-loop synthetic estimation.

[Observation 3: Theorem 1 pool solvency equation 1 + ΔP/P >= 0.5 * (1 + R'v)/(V_A + V_B)]
  ├── Observation 3.1: At Par (S=1.0), V_A + V_B = 2.00 -> ΔP/P >= -75.00%
  ├── Observation 3.2: At Reset Barrier H_d (S=0.625), V_A + V_B = 1.25 -> ΔP/P >= -60.00%
  └── Logic 3.3: -75.00% is strictly conditional on Par; at barrier H_d, a -75% drop incurs a 37.35% haircut. True model-free bound is -60.00%.

[Observation 4: Transfer function zeta = (1 + K*Kp)/(2*sqrt(K*Ki*tau)) = 17.0312]
  ├── Observation 4.1: Calibrated plant defaults K=1.20, tau=0.05, Kp=0.15, Ki=0.02 yield zeta = 17.03
  ├── Observation 4.2: claims.yaml CLM-006 records zeta = 1.42 from an unrecorded legacy trial (K=1.0, tau=1.0, Ki=0.16)
  └── Logic 4.3: zeta = 17.03 is the active continuous transfer function value; PI controller reduces discrete settling time from 28.1d to 4.6d; Kd is redundant.

[Observation 5: run_comprehensive_psuu_suite.py Track 2 multiplies gross yield by static omega_burn]
  ├── Observation 5.1: No endogenous behavioral response or dynamic optimization
  └── Logic 5.2: omega_burn = 0.65 is an inherited governance policy heuristic, not an optimized equilibrium parameter.

[Observation 6: Zero code or simulation files exist for Architectures B1-B4]
  └── Logic 6.1: Phase 6 (Mechanism-Space Exploration) was specified conceptually in RESEARCH_PLAN_OPTIMIZATION.md but never executed.

[Observation 7: run_comprehensive_psuu_suite.py uses closed-form linear proxy formulas for fig7]
  └── Logic 7.1: Multi-objective NSGA-II / MOEA/D Pareto optimization across M01-M10 (Phase 10) was never executed; Pareto claims are mock proxies.
```

---

## 3. Caveats

1. **No Production Execution of Missing Sweeps:** In compliance with the Hard Execution Stop Rule, no new NSGA-II runs, live telemetry ingestion pipelines, or large-scale Sobol sweeps were launched during this audit.
2. **Correctness of Core Single-Step Mathematics:** While the empirical calibration used synthetic data and the GSA implementation had an estimator bug, the underlying analytical proof of Theorem 1 ($-60.00\%$ single-step crash bound from barrier $H_d$) is mathematically sound under its stated balance sheet assumptions.
3. **Plant Parameter Uncertainty:** The controller damping ratio $\zeta = 17.03$ assumes fixed plant constants $K_{\text{amm}} = 1.20$ and $\tau_{\text{arb}} = 0.05$. Under severely depleted liquidity ($L \le \$1.5\text{M}$), effective plant gain increases, which could push the physical loop toward underdamped behavior if anti-windup clamping is saturated.

---

## 4. Conclusion

| Issue Area | Discrepancy & Forensic Root Cause | True Technical Status | Reconciled Ground Truth |
| :--- | :--- | :---: | :--- |
| **1. GSA Sobol Indices** | Uncentered Saltelli numerator + small $N_{base}=64$ on non-zero-mean output ($\mu \approx 42\%$) caused overflow ($\text{ratio} \approx 80$), which was hard-clamped by `min(1.0, ...)` on line 84 to $S_i = 1.0000$. Dead code `v_i` unreferenced; unseeded noise in simulation violates Sobol determinism. | **CODE / MATH BUG** | $\sum S_i = 8.0000$ is invalid. GSA must be rerun using centered Jansen/Saltelli estimators with fixed random seeds and $N_{\text{base}} \ge 512$. |
| **2. Data Ingestion** | `empirical_calibration.py` fitted MLE against a closed-loop synthetic Kou jump-diffusion generator (`true_sigma = 0.885`, `true_lambda = 2.50`) instead of live tick feeds. Zero raw files in `data/`. | **SYNTHETIC ONLY** | No empirical telemetry (DAT-01..DAT-07) was ingested. Calibrated parameters are synthetic estimates. |
| **3. Crash Safety Scoping** | Marketing claims cited $-75.00\%$ crash safety unconditionally. $-75.00\%$ applies strictly at Par ($S=1.0$); from barrier $H_d = 0.25$, tolerance is strictly $-60.00\%$ (a $-75\%$ drop at $H_d$ causes a $37.35\%$ haircut). | **UNCONSTRAINED CLAIM** | Guaranteed model-free single-step crash bound is strictly **$-60.00\%$ from $H_d = 0.25$**. |
| **4. Controller Damping** | Contradiction between `claims.yaml` ($\zeta = 1.42$) and Whitepaper ($\zeta = 17.03$). $\zeta = 1.42$ was an unupdated legacy draft; $\zeta = 17.03$ derives from continuous ODE with $K=1.20, \tau=0.05$. | **DOCUMENTATION TYPO** | True analytical damping ratio is **$\zeta = 17.03$** (overdamped). Discrete PI reduces thin-liquidity settling time from $28.1\text{d}$ to $4.6\text{d}$; $K_d \equiv 0$. |
| **5. ACP-67 Optimization** | $\omega_{\text{burn}} = 0.65$ was not derived from an endogenous objective function; Track 2 was a static multiplication tensor. | **POLICY HEURISTIC** | Inherited governance policy parameter, not an empirically optimized equilibrium. |
| **6. Alternative Architectures** | Architectures B1–B4 were described conceptually in the research plan but never coded or simulated. | **PLANNED ONLY** | Phase 6 unexecuted; no comparative empirical data exists. |
| **7. Pareto Optimization** | NSGA-II / MOEA/D multi-objective optimization across M01–M10 was never run; `fig7` was generated from linear proxy equations. | **PLANNED ONLY** | Phase 10 unexecuted; Pareto frontier claims are mock proxies. |

---

## 5. Verification Method

To independently verify all findings in this report, execute the following commands:

### 1. Verify GSA Sobol Clamping & Estimator Overflow:
```bash
python3 -c "
import numpy as np
import sys
sys.path.append('simulations/robustness_study')
import sobol_sensitivity, master_robustness_engine

param_bounds = {'R': (0.04, 0.12), 'Rp': (0.01, 0.05), 'Hu': (1.30, 2.50), 'Hd': (0.15, 0.40),
                'omega_burn': (0.30, 0.80), 'omega_val': (0.10, 0.40), 'Kp': (0.05, 0.35), 'Ki': (0.005, 0.05)}
samples, param_names = sobol_sensitivity.generate_saltelli_samples(param_bounds, N_base=64, seed=42)
baseline_path, _ = master_robustness_engine.generate_regime_price_path('NORMAL', days=365, seed=101)

peg_vols = [master_robustness_engine.simulate_protocol_epoch(baseline_path, *samples[i,:2], *samples[i,2:4], *samples[i,4:6], *samples[i,6:8], True)['annualized_peg_vol'] for i in range(len(samples))]
y_A, y_B = np.array(peg_vols[:64]), np.array(peg_vols[64:128])
var_tot = np.var(np.concatenate([y_A, y_B]))
for i, p in enumerate(param_names):
    y_AB = np.array(peg_vols[(2+i)*64:(3+i)*64])
    raw_ratio = (np.mean(y_A * y_AB) - np.mean(y_A)*np.mean(y_B)) / var_tot
    print(f'{p}: raw_ratio={raw_ratio:.2f}, clamped_Si={max(0.0, min(1.0, raw_ratio))}')
"
```
*Expected Output:* Confirms `raw_ratio` $\in [36.0, 115.0]$, clamping every parameter's $S_i$ to `1.0`.

### 2. Verify Synthetic Data Generation in Empirical Calibration:
```bash
python3 -c "
with open('simulations/empirical_calibration.py') as f:
    code = f.read()
assert 'def generate_synthetic_historical_avax_series' in code
assert 'true_sigma = 0.885' in code
print('CONFIRMED: empirical_calibration.py generates synthetic data with hardcoded ground-truth parameters.')
"
```

### 3. Verify Damping Ratio Calculation:
```bash
python3 -c "
import sys
sys.path.append('simulations/cadcad_core/mechanisms')
from feedback_controller import ReflexerPIDController
ctrl = ReflexerPIDController(K_p=0.150, K_i=0.020, K_d=0.005)
zeta = ctrl.compute_system_damping_ratio(plant_gain_K=1.20, plant_time_constant_tau=0.05)
print(f'Computed zeta: {zeta:.4f}')
assert abs(zeta - 17.0312) < 1e-3
"
```

### 4. Verify Theorem 1 Single-Step Crash Bounds:
```bash
python3 -c "
# Barrier Hd = 0.25 (v=0)
crash_barrier = 0.5 * (1.00 / (1.00 + 0.25)) - 1.0
# Par S = 1.00 (v=0)
crash_par = 0.5 * (1.00 / (1.00 + 1.00)) - 1.0
print(f'Crash from Barrier Hd: {crash_barrier*100:.2f}%')
print(f'Crash from Par S: {crash_par*100:.2f}%')
assert abs(crash_barrier - (-0.60)) < 1e-5
assert abs(crash_par - (-0.75)) < 1e-5
"
```

### Invalidation Conditions:
This forensic reconciliation would be invalidated if:
1. An unreferenced empirical data repository was proven to have ingested raw L2/exchange tick feeds into `data/`.
2. A true NSGA-II Pareto optimization log with Pareto frontier points CSV was proven to exist in the repository.
3. The Saltelli Sobol indices in `GLOBAL_SENSITIVITY_ANALYSIS.md` were proven to satisfy $\sum S_i \le 1.0000$ without line 84 clamping.

---
