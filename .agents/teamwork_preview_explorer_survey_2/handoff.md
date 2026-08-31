# Handoff Report — Survey Explorer 2: Codebase, Simulation Engine, KPI & Statistical Routines

> **Document Identifier:** `BCRG-HANDOFF-2026-CODEBASE-SURVEY-02`  
> **Agent:** Survey Explorer 2  
> **Working Directory:** `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_explorer_survey_2`  
> **Target Recipient:** Parent Orchestrator (`eeb3e555-14df-40a8-8fe7-f84199bcfa38`)  
> **Timestamp:** 2026-08-31T07:23:00Z  
> **Handoff Type:** Hard Handoff (Task Complete)  

---

## 1. Observation

Direct programmatic and textual observations across the codebase and runtime environment:

1. **Root Configuration & Dependencies:**
   - Linux environment running Python 3.13.12 (packaged by conda-forge) at `/home/hash/Miniforge3/bin/python3`.
   - Core libraries: `numpy` (2.4.4), `scipy` (1.17.1), `pandas` (3.0.2), `fastparquet` (2026.3.0), `matplotlib` (3.10.8), `pyyaml` (6.0.3), `jsonschema` (4.26.0).
   - Smart contract engine: `forge` 1.6.0-v1.7.0 (commit `f83bad91...`), `solc` 0.8.24, optimizer enabled with 200 runs (`contracts/foundry.toml`).
   - Git Commit: `cc1064897c16be16c0bbe2817a37a3911c322247` on branch `research/first-principles-adversarial-audit`.

2. **Stage 2 Screening Script Implementation (`simulations/design_discovery/stage2_architecture_screening.py`):**
   - **Kou Jump-Diffusion Path Generator (Lines 41–87):** Generates $(500 \times 366)$ standardized daily price paths using parameters $\sigma = 0.8915, \lambda_j = 15.0, p_{\text{up}} = 0.5955, \eta_1 = 7.671, \eta_2 = 7.801, \mu = -0.3402, \text{seed} = 2026$.
   - **Stratified Batch Selection (Lines 349–362):** Samples exactly 40 candidates per cell across 8 architectures ($A_0$–$A_{5.3}$) and 5 policies ($\text{POL-01}$–$\text{POL-05}$), totaling $N = 1,600$ configurations from `audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet` ($N_0 = 64,052$).
   - **Architecture Valuation Logic (Lines 171–237):**
     * A0: Resets on $V_B \ge H_u$ and $V_B \le H_d$. Haircut recorded if $2S_t < V_A$.
     * A1: No resets. Haircut recorded if $2S_t < 1.0$.
     * A2: Reserve buffer $B_{\text{res}}$ initialized. Downward reset on $V_B \le H_d$ absorbs deficits from $B_{\text{res}}$ before assigning haircuts. No upward reset check.
     * A3 & A4: Fixed claim $V_A = 1.0$, floating equity $V_B = \max(0, 2S_t - 1.0)$, no resets. A4 has $u(t) = 0.0$.
     * A5.1: Convertible debt absorbs $80\%$ of deficit amplitude.
     * A5.2: Protocol-owned AMM increases liquidity depth $L_{\text{amm}}$ by $+30\%$ ($\$19.5\text{M}$ vs $\$15.0\text{M}$).
     * A5.3: Multi-LST basket compresses path deviation: $P_{\text{basket}} = 1.0 + (P - 1.0) \times 0.80$.
   - **PI Controller Secondary AMM Dynamics (Lines 240–256):**
     * $u(t) = \text{clamp}(-K_p e(t) - K_i I(t), -0.05, 0.05)$, with anti-windup clamping $I(t) \in [-0.10, 0.10]$.
     * AMM flow: $dP_{\text{dex}} = \left(\frac{1.0 - P_{\text{dex}}}{\tau_{\text{arb}}} + \frac{u(t) \alpha_{\text{flow}}}{L_{\text{amm}}}\right) dt$.
   - **Redistribution Policies (Lines 267–288):**
     * POL-01: Static simplex split.
     * POL-02: Countercyclical validator boost $\omega_{\text{val}} = \text{clamp}(\omega_{\text{val}} + \kappa_{\text{dd}} \cdot \text{drawdown}, 0.15, 0.50)$.
     * POL-03: Reserve priority $\omega_{\text{res}} = \text{clamp}(0.30 \max(0, 1.25 - 2S_t), 0.0, 0.35)$.
     * POL-04: Burn maximizer $\omega_{\text{burn}} \ge 0.75, \omega_{\text{val}} = 0.10, \omega_{\text{res}} = 0.0$.
     * POL-05: State softmax routing $\omega_{\text{val}} = \text{clamp}(0.20 + 0.30 \cdot \text{drawdown}, 0.10, 0.50), \omega_{\text{res}} = \text{clamp}(0.15 \max(0, 1.10 - S_t), 0.0, 0.25)$.

3. **KPI Formulations & Aggregation (Lines 306–331):**
   - 11 metrics computed: `peg_rmse`, `max_depeg`, `haircut_prob`, `tail_cvar_99`, `recovery_time_days`, `validator_cr_min`, `validator_insolvency_prob`, `avax_burned_total`, `reset_churn_annual`, `rate_volatility`, `reserve_depletion_prob`.
   - Stored in `audit_artifacts/execution/STAGE_2_RESULTS.parquet` ($N = 1,600$, 25 columns, 0 nulls).

---

## 2. Logic Chain

1. **From Observation 1 (Dependencies & Environment):**
   - The environment provides modern scientific Python (3.13.12, NumPy 2.4.4, SciPy 1.17.1, Pandas 3.0.2) and fastparquet for zero-copy column reading, along with Foundry/Forge for contract testing.
2. **From Observation 2 (Stage 2 Screening Code Structure):**
   - The simulation engine executes an exact 2D grid allocation: $8 \times 5 \times 40 = 1,600$ configurations.
   - The random seed `2026` ensures Common Random Numbers across all candidate evaluations.
   - The architectural down-selection observed in `audit_artifacts/reports/STAGE_2_ARCHITECTURE_SCREENING.md` directly traces to the mathematical equations implemented in `stage2_architecture_screening.py`:
     * A0 experiences high reset churn ($7.37/\text{yr}$) because Kou jump frequency $\lambda = 15.0$ repeatedly breaches $H_d = 0.25$ and $H_u = 2.00$.
     * A1, A3, A4 experience high haircut probability ($74.20\%$) because without resets or buffer vaults, junior equity is wiped out during large negative jumps, forcing senior claims to absorb subsequent losses.
     * A2 achieves $0.14\%$ haircut probability because $B_{\text{res}}$ acts as a dedicated first-loss capital buffer absorbing deficits before senior claims take haircuts.
     * A5.3 achieves low churn ($1.77/\text{yr}$) and low tail loss ($5.57\%$) due to the $20\%$ volatility reduction from basket diversification.
3. **From Observation 3 (KPI Aggregations & Objectives):**
   - All 11 KPIs are well-defined and aggregated across 500 Monte Carlo paths.
   - Objective directions match `audit_artifacts/design_discovery/OBJECTIVES_AND_CONSTRAINTS.md` (minimize peg RMSE, churn, haircut, CVaR; maximize burn and validator coverage).

---

## 3. Caveats

1. **Validator OpEx Vault Scale:**
   - In `stage2_architecture_screening.py`, the validator coverage ratio is computed against a $1\text{M sAVAX}$ test pool ($\sim \$1.6\text{M}$ gross annual staking yield) vs the entire 1,450-node network annual OpEx ($\$6.09\text{M}$), resulting in sub-scale coverage numbers ($0.02\times - 0.03\times$). This is a documented test vault scale assumption.
2. **Multi-LST Basket Modeling:**
   - Architecture A5.3 models diversification via a scalar $20\%$ volatility damping rather than simulating 3 individual correlated jump processes.
3. **Architecture A2 Upward Reset Implementation:**
   - A2 only checks downward barrier resets in code; upward split profits remain in vault reserves.
4. **No Code Modification Performed:**
   - In accordance with read-only explorer constraints, no source code or historical outputs were modified.

---

## 4. Conclusion

The codebase, simulation hierarchy, and runner scripts have been fully mapped, categorized, and documented in `survey_codebase.md`. The Stage 2 Monte Carlo engine in `simulations/design_discovery/stage2_architecture_screening.py` is cleanly implemented, fully vectorized, implements genuine Common Random Numbers (CRN), and exactly produced the $1,600$-row `STAGE_2_RESULTS.parquet` dataset. The downstream audit team now has a complete inventory of every file, mechanism equation, KPI formula, and smart contract in the project.

---

## 5. Verification Method

To independently verify the inventory and codebase execution:

1. **Verify Python Environment & Dependencies:**
   ```bash
   python3 -c "import numpy, scipy, pandas, fastparquet; print('Environment Validated!')"
   ```
2. **Verify Stage 2 Parquet Dataset Structure:**
   ```bash
   python3 -c "import pandas as pd; df = pd.read_parquet('audit_artifacts/execution/STAGE_2_RESULTS.parquet'); assert df.shape == (1600, 25); assert df.isnull().sum().sum() == 0; print('Parquet Verified: 1,600 configs, 25 columns, 0 nulls')"
   ```
3. **Verify Stage 1 Survivor Parquet Dataset:**
   ```bash
   python3 -c "import pandas as pd; df = pd.read_parquet('audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet'); assert df.shape == (64052, 14); print('Stage 1 Survivors Verified: 64,052 configs')"
   ```
4. **Verify Smart Contract Compilation and Tests:**
   ```bash
   cd contracts && forge test
   ```
5. **Inspect Full Inventory Deliverable:**
   ```bash
   cat .agents/teamwork_preview_explorer_survey_2/survey_codebase.md
   ```
