# Comprehensive Codebase, Simulation Engine, KPI & Statistical Routines Inventory Report

> **Document Identifier:** `BCRG-AUDIT-2026-CODEBASE-SURVEY-02`  
> **Author:** Survey Explorer 2 (Codebase & Simulation Engine Specialist)  
> **Working Directory:** `.agents/teamwork_preview_explorer_survey_2`  
> **Git Commit Target:** `cc1064897c16be16c0bbe2817a37a3911c322247` (Branch: `research/first-principles-adversarial-audit`)  
> **Timestamp:** 2026-08-31T07:22:00Z  
> **Epistemic Classification:** Rigorous Descriptive Codebase & Engine Inventory  

---

## 1. Executive Summary & Inventory Scope

This report delivers a complete, structured mapping of all simulation engines, model equations, discrete architectures, endogenous redistribution policies, KPI calculation routines, statistical evaluation methods, runner scripts, smart contracts, validation test harnesses, and execution datasets across the `coad1024-cmd/avalanche-native-stablecoin` repository.

### Key Highlights of the Codebase Architecture:
1. **Multi-Tier Simulation Hierarchy:**
   - **Stage 1 Analytical Screening Engine:** `simulations/design_discovery/stage1_analytical_screening.py` (Vectorized NumPy filtering over $N_0 = 100,000$ Dirichlet candidates across 8 architectures and 5 policies).
   - **Stage 2 Monte Carlo Screening Engine:** `simulations/design_discovery/stage2_architecture_screening.py` (Parallelized Monte Carlo evaluation over $N = 1,600$ stratified configurations with Common Random Numbers on 500 Kou jump-diffusion paths).
   - **cadCAD Core Multi-Agent Digital Twin:** `simulations/cadcad_core/` (5 Partial State Update Blocks, 3 behavioral agent classes, 6 analytical/numerical mechanism solvers, 6 experiment runners).
   - **Robustness & Adversarial Testing Suite:** `simulations/robustness_study/` (Sobol Global Sensitivity Analysis, controller ablation, 11-regime out-of-sample stress testing, parameter registry).
   - **Canonical Physical Accounting Ledger:** `simulations/canonical_accounting.py` (Double-entry balance sheet conservation, $O(1)$ scalar rebasing, stock-flow verification).
2. **Smart Contract Verification & Remediation Suite:**
   - `contracts/src/` (Foundry / Solidity 0.8.24 suite covering Vault, ResetController, TrancheSplitter, Tokenomics, Oracles, and Inter-Chain Messaging).
   - `contracts/src/remediation/` & `contracts/test/unit/` (Side-by-side comparative verification of buggy vs corrected smart contracts resolving VULN-01 price-squaring flapping and VULN-02/03 tranche disconnect).
3. **Execution Datasets & Parquet Lineage:**
   - `audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet` ($N = 64,052$ rows, 14 feature columns, SHA-256: `3d9ebe70...`).
   - `audit_artifacts/execution/STAGE_2_RESULTS.parquet` ($N = 1,600$ rows, 25 feature & KPI columns, SHA-256: `653890da...`).
   - `audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json` ($1,600$ configs, 500 MC paths, seed 2026, 8 worker processes, runtime 1303.11s).

---

## 2. Global Repository & Directory Topology

The repository is structured into functional sub-trees separating simulations, smart contracts, audit artifacts, workflows, data feeds, documentation, and tools:

```
avalanche-native-stablecoin/
├── .agents/                               # Multi-agent coordination metadata & reports
├── audit_artifacts/                       # Formal audit deliverables, manifests, reports & discovery specs
│   ├── cross_validation/                 # Dual implementation verification reports
│   ├── design_discovery/                 # 10 canonical search spaces, decision framework & ladder specs
│   ├── execution/                        # Stage 1 & Stage 2 Parquet datasets and JSON manifests
│   ├── figures/                          # Publication diagrams & charts
│   ├── provenance/                       # Lineage records, claims.yaml, gates.yaml, calibrated market params
│   ├── registers/                        # Assumptions, claims, contradictions, parameter governance
│   ├── remediation/                      # Reference buggy vs candidate corrected Solidity sources
│   ├── reports/                          # 13 formal markdown research & audit reports
│   └── state/                            # RESEARCH_STATE.yaml snapshot baseline registry
├── contracts/                             # Foundry Solidity Smart Contract Project
│   ├── foundry.toml                      # Foundry configuration (Solc 0.8.24, 200 optimizer runs)
│   ├── script/                           # Deployment and test scripts
│   ├── src/                              # Production Solidity source contracts
│   │   ├── controller/                   # ResetController.sol
│   │   ├── core/                         # CustodianVault.sol, TrancheSplitter.sol, TrancheToken.sol
│   │   ├── icm/                          # TeleporterUSDAdapter.sol (Avalanche Warp Messaging)
│   │   ├── interfaces/                   # Interface definitions
│   │   ├── oracles/                      # ChainlinkOracleAdapter.sol
│   │   ├── remediation/                  # Isolated Buggy vs Corrected reference contracts
│   │   └── tokenomics/                   # DynamicValidatorSubsidy.sol, YieldRecycler.sol
│   └── test/                             # Unit, invariant, and fuzz tests
│       ├── invariant/                    # SolvencyInvariant.t.sol
│       └── unit/                         # CustodianVault, DualImplementation, Reset/Splitter, YieldRecycler
├── data/                                  # Telemetry data feeds and raw CSV datasets
│   ├── raw/                              # DAT-01 (AVAX 5yr), DAT-02 (Staking APR), DAT-03 (DEX), DAT-07 (Ticks)
│   ├── fetch_real_telemetry.py           # Ingestion script from public APIs
│   └── _lineage.jsonl                    # Cryptographic dataset SHA-256 lineage
├── docs/                                  # Academic LaTeX whitepaper, engineering principles, figures
│   ├── WHITEPAPER.tex / .pdf / .md       # Formally compiled manuscript with Theorems 1 & 2
│   ├── build_docs.py                     # Document build automation
│   ├── incident-log.md                   # Chronological remediation log
│   └── notation.md / assumptions.md      # Mathematical symbols and epistemic assumptions
├── research/                              # Primary reference PDFs and literature summaries (SSRN-3856569)
├── simulations/                           # Python simulation engines, PSUU, GSA & screening runners
│   ├── archive/                          # 8 historical / legacy prototype simulation scripts
│   ├── cadcad_core/                      # Core cadCAD multi-agent simulation framework
│   │   ├── agents/                       # Arbitrageur, Speculator, Validator Pool agent models
│   │   ├── experiments/                  # 6 Experiment runners (Monte Carlo, PSUU, Controller, Subsidy, PIDE, BlackSwan)
│   │   ├── mechanisms/                   # Tranche math, Dynamic resets, PI controller, ACP-67, PIDE solver
│   │   ├── params.py                     # 20 governance levers & 7 stochastic environment parameters
│   │   ├── psubs.py                      # 5 Partial State Update Blocks pipeline
│   │   └── state.py                      # 25-state variable registry & initialization
│   ├── design_discovery/                 # Stage 1 & Stage 2 screening engines & boundary tests
│   │   ├── stage1_analytical_screening.py# Vectorized analytical candidate pruning (N=100k -> 64,052)
│   │   ├── stage2_architecture_screening.py# Stratified Monte Carlo screening (N=1,600 configs, 500 MC paths)
│   │   └── test_boundary_survivors.py    # Epsilon boundary perturbation tests
│   ├── robustness_study/                 # Parameter audit, Sobol GSA & stress engines
│   │   ├── adversarial_edge_cases_harness.py
│   │   ├── adversarial_stress_testing.py
│   │   ├── controller_isolation.py       # Core vs P vs PI vs PID ablation study
│   │   ├── empirical_challenger_harness.py
│   │   ├── market_regimes.py             # 11 stochastic market regimes generator
│   │   ├── master_robustness_engine.py   # Master robustness and out-of-sample engine
│   │   ├── parameter_registry.py         # 28-parameter canonical inventory & identification audit
│   │   └── sobol_sensitivity.py          # Saltelli QMC sampling & Sobol indices
│   ├── canonical_accounting.py           # Physical double-entry ledger & balance sheet invariants
│   ├── empirical_calibration.py          # Kou (2002) MLE, Merton (1976) MLE & Bootstrap CI calibration
│   └── verify_contractual_gates.py       # Automated validation of 20 BCRG gates and claims
├── tools/                                 # Interactive diagnostic tools
│   └── anusd_calculator.html             # Standalone JavaScript mathematical calculator
└── workflows/                             # Runtime data contracts and validation harnesses
    ├── contracts.py                      # Pydantic schema validation contracts
    └── validation/                       # Conservation and adversarial test harnesses
        ├── adversarial_challenge_harness.py
        ├── challenger2_empirical_proofs.py
        └── conservation.py
```

---

## 3. Simulation Engine & Architectural Modeling Framework

### 3.1 Stage 2 Architecture & Policy Screening Engine (`simulations/design_discovery/stage2_architecture_screening.py`)

This script is the core subject of the Stage 2 audit. It performs parallelized Monte Carlo screening over candidate configurations.

#### Key Functions and Algorithms:
1. **`generate_standardized_price_paths(n_paths, n_steps, dt, seed, sigma, lambda_j, p_up, eta1, eta2, mu)` (Lines 41–87):**
   - Simulates Kou (2002) Asymmetric Double-Exponential Jump-Diffusion SDE:
     $$\frac{dP_t}{P_{t^-}} = \mu dt + \sigma dW_t + (e^Y - 1) dN_t$$
   - Calculates exact Kou compensator $\zeta_j = \mathbb{E}[e^Y - 1] = p_{\text{up}}\frac{\eta_1}{\eta_1 - 1} + (1 - p_{\text{up}})\frac{\eta_2}{\eta_2 + 1} - 1$.
   - Drift adjustment: $\left(\mu - \frac{1}{2}\sigma^2 - \lambda_j \zeta_j\right) dt$.
   - Diffusion: $dW = \mathcal{N}(0, \sigma \sqrt{dt})$.
   - Jump Counts: $dN = \text{Poisson}(\lambda_j dt)$.
   - Jump Magnitudes: $Y \sim \begin{cases} +\text{Exp}(\eta_1) & \text{with prob } p_{\text{up}} \\ -\text{Exp}(\eta_2) & \text{with prob } 1 - p_{\text{up}} \end{cases}$.
   - Continuous price paths: $P(t) = \exp\left(\sum d\ln P\right)$ starting from $P_0 = 1.0$.
   - **CRN Isolation:** Uses single `np.random.default_rng(seed)` (seed = 2026) to generate a standardized $(500 \times 366)$ matrix passed identically to all candidate configurations.

2. **`simulate_single_candidate(row, price_paths)` (Lines 93–331):**
   - Simulates 365 daily steps for each of the 500 price paths ($182,500$ steps per candidate configuration).
   - **8 Discrete Architecture Topologies Evaluated:**
     * **`arch_id == 0` (A0 - Dual-Class Discrete Resets):**
       $$V_A = 1 + R v, \quad V_B = \max(0, 2S_t - V_A)$$
       Triggers resets when $V_B \ge H_u$ (upward split) or $V_B \le H_d$ (downward reverse split). On downward reset, if $2S_t < V_A$, senior deficit $\frac{V_A - 2S_t}{V_A}$ is recorded as haircut. Denominator resets to $\beta \leftarrow \beta \cdot S_t, v \leftarrow 0$.
     * **`arch_id == 1` (A1 - Continuous Streaming Amortization):**
       $$V_A = 1 + R v$$
       Operates with continuous yield de-leveraging and no discrete resets ($f_{\text{reset}} \equiv 0$). In code: `if 2.0 * S_t < 1.0: path_haircut = max(path_haircut, 1.0 - 2.0 * S_t)`.
     * **`arch_id == 2` (A2 - Dedicated Solvency Buffer Vault):**
       $$V_A = 1 + R v, \quad V_B = \max(0, 2S_t - V_A)$$
       Initializes reserve buffer $B_{\text{res}} = B_{\text{target}} \cdot C_{\text{sAVAX}} \cdot \$25.0 \cdot 0.5$. Accumulates yield surplus $B_{\text{res}} \mathrel{+}= \Phi_{\text{gross}} \cdot \omega_{\text{res}}$. Upon downward reset ($V_B \le H_d$), collateral deficit is covered from $B_{\text{res}}$. If $B_{\text{res}}$ is exhausted, `res_depleted = 1` and residual unbacked deficit is recorded as haircut. No upward reset is triggered in code.
     * **`arch_id == 3` (A3 - Floating Junior Equity Tranche):**
       $$V_A = 1.0000, \quad V_B = \max(0, 2S_t - 1.0)$$
       Zero coupon on senior tranche, perpetual floating junior equity, no discrete resets. Haircut when $2S_t < 1.0$.
     * **`arch_id == 4` (A4 - Zero-Controller Primary CDP):**
       $$V_A = 1.0000, \quad u(t) \equiv 0.0$$
       No secondary PI controller actuation. Haircut when $2S_t < 1.0$.
     * **`arch_id == 5` (A5.1 - Dynamic Debt-Equity Convertibles):**
       $$V_A = 1 + R v$$
       Upon collateral stress ($2S_t < V_A$), Junior debt claims convert to equity, absorbing $80\%$ of deficit amplitude: `path_haircut = max(path_haircut, (V_A - 2.0 * S_t) * 0.20)`. No discrete resets.
     * **`arch_id == 6` (A5.2 - Protocol-Owned AMM):**
       Expands secondary AMM liquidity depth by $+30\%$ ($L_{\text{amm}} = \$19.5\text{M}$ vs base $\$15.0\text{M}$), reducing secondary market plant gain $K_{\text{dc}}$. Evaluates reset on $V_B \le H_d$.
     * **`arch_id == 7` (A5.3 - Multi-LST Collateral Basket):**
       Models 3-asset LST basket diversification by damping price path deviations by $20\%$:
       $$P_{\text{basket}}(t) = 1.0 + (P_{\text{single}}(t) - 1.0) \times 0.80$$
       Evaluates reset on $V_B \le H_d$.
   - **5 Endogenous Redistribution Policy Families Evaluated:**
     * Gross staking surplus: $\Phi_{\text{gross}}(t) = q_{\text{sAVAX}} \cdot C_{\text{sAVAX}} \cdot P_t \cdot \$25.0 \cdot dt$.
     * Drawdown variable: $\text{drawdown}(t) = \max(0, 1.0 - S_t)$.
     * **`policy_id == 0` (POL-01 - Static Split):** $\omega_{\text{burn}}, \omega_{\text{val}}, \omega_{\text{res}}$ fixed at sampled simplex weights.
     * **`policy_id == 1` (POL-02 - Countercyclical Drawdown Feedback):**
       $$\omega_{\text{val}}(t) = \text{clamp}(\omega_{\text{val,0}} + \kappa_{\text{dd}} \cdot \text{drawdown}(t), 0.15, 0.50), \quad \omega_{\text{burn}} = \max(0, 1 - \omega_{\text{val}} - \omega_{\text{res}} - \omega_{\text{l1}})$$
     * **`policy_id == 2` (POL-03 - Reserve Priority):**
       $$\omega_{\text{res}}(t) = \text{clamp}(0.30 \max(0, 1.25 - 2S_t), 0.0, 0.35), \quad \omega_{\text{burn}} = \max(0, 1 - \omega_{\text{val}} - \omega_{\text{res}} - \omega_{\text{l1}})$$
     * **`policy_id == 3` (POL-04 - Deflationary Burn Maximizer):**
       $$\omega_{\text{val}} = 0.10, \quad \omega_{\text{res}} = 0.0, \quad \omega_{\text{burn}} = \max(0.75, 1.0 - \omega_{\text{val}} - \omega_{\text{l1}})$$
     * **`policy_id == 4` (POL-05 - State Softmax Dynamic):**
       $$\omega_{\text{val}}(t) = \text{clamp}(0.20 + 0.30 \cdot \text{drawdown}(t), 0.10, 0.50), \quad \omega_{\text{res}}(t) = \text{clamp}(0.15 \max(0, 1.10 - S_t), 0.0, 0.25)$$
   - **Secondary Market Microstructure & PI Controller Actuation:**
     * Error signal: $e(t) = P_{\text{dex}}(t) - 1.0000$.
     * Integral error with anti-windup clamping: $I(t) = \text{clamp}(I(t-1) + e(t)dt, -0.10, 0.10)$.
     * Control signal (rate modulation):
       $$u(t) = \text{clamp}(-K_p e(t) - K_i I(t), -0.05, 0.05)$$
       (Set to $u(t) = 0.0$ for A4).
     * Secondary DEX Price Evolution:
       $$dP_{\text{dex}} = \left( \frac{1.0000 - P_{\text{dex}}}{\tau_{\text{arb}}} + \frac{u(t) \cdot \alpha_{\text{flow}}}{L_{\text{amm}}} \right) dt$$
       with $\tau_{\text{arb}} = 5.55 / 365.25\text{ yrs}$, $\alpha_{\text{flow}} = 1.0 \times 10^7$, $P_{\text{dex}} = \text{clamp}(P_{\text{dex}} + dP_{\text{dex}}, 0.50, 1.50)$.
     * Peg error: $\text{err}_{\text{peg}}(p, s) = P_{\text{dex}} - 1.0000$.
   - **Validator OpEx Coverage Tracking:**
     * Node count: $N_{\text{nodes}} = 1450$, Monthly cost: $\$350.0$, Annual OpEx: $\$6.09\text{M}$.
     * Daily OpEx cost: $\text{OpEx}_{\text{daily}} = \$6,090,000 \cdot dt$.
     * Validator income flow: $\Phi_{\text{val}}(t) = \Phi_{\text{gross}}(t) \cdot \omega_{\text{val}}(t)$.
     * Coverage ratio: $\text{CR}_{\text{val}}(t) = \frac{\Phi_{\text{val}}(t)}{\text{OpEx}_{\text{daily}}}$.

3. **`execute_stage2_screening_campaign(n_sample_candidates, n_mc_paths, seed)` (Lines 337–420):**
   - Ingests `audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet` ($N_0 = 64,052$).
   - Performs 2D stratified sampling: selects 40 configurations per cell across $(8 \times 5 = 40\text{ cells}) = 1,600$ candidate configurations.
   - Stratified random seed assignment: `seed + a_id * 10 + p_id`.
   - Dispatches parallel execution via `ProcessPoolExecutor(max_workers=8)`.
   - Outputs resulting metrics to `audit_artifacts/execution/STAGE_2_RESULTS.parquet` and manifest to `audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json`.

---

### 3.2 Stage 1 Analytical Screening Engine (`simulations/design_discovery/stage1_analytical_screening.py`)

- **Candidate Tensor Generation:** Generates $N_0 = 100,000$ points uniformly distributed across continuous parameter bounds and uniformly across the 3-simplex $\Delta^3$ using normalized i.i.d. exponential draws (exact $\text{Dirichlet}(1,1,1,1)$).
- **Four Analytical Filters Applied:**
  * **`F1` (Simplex Conservation):** $\left|\sum_{i=1}^4 \omega_i - 1.0\right| < 10^{-7}$ and $\omega_i \ge 0$. Pass rate: $100.00\%$.
  * **`F2` (Tranche Yield Feasibility):** $R > R'$ and $R' \le q_{\max} = 10.0\%$. Pass rate: $64.05\%$.
  * **`F4` (Hurwitz Overdamping):** $\zeta(K_p, K_i; L, \tau) = \frac{1 + K_{\text{dc}} K_p}{2 \sqrt{\tau_{\text{arb}} K_{\text{dc}} K_i}} \ge 1.0$. Pass rate: $100.00\%$ (all sampled gain configurations are strongly overdamped).
  * **`F5` (Reset Barrier Ordering):** For barrier architectures (A0, A2): $0 < H_d < 1.0 < H_u$. Pass rate: $100.00\%$.
- **Output:** Prunes $35.948\%$ of invalid space, retaining $N_{\text{survivors}} = 64,052$ feasible configurations published in `STAGE_1_CORRECTED_SURVIVORS.parquet`.

---

### 3.3 cadCAD Core Multi-Agent Simulation Engine (`simulations/cadcad_core/`)

The cadCAD framework provides the high-fidelity behavioral simulation sub-layer:
- **`state.py`:** Defines 25 system state variables across temporal tracking, spot index, tranche NAVs, secondary AMM pools, physical token stocks, ACP-67 sinks, and discrete reset counters.
- **`params.py`:** Defines canonical default values for all 20 governance levers ($\Theta \subset \mathbb{R}^{20}$) and 7 environmental uncertainty parameters ($W \subset \mathbb{R}^7$).
- **`psubs.py`:** 5-step sequential Partial State Update Blocks pipeline:
  1. *PSUB 1:* Exogenous Kou / Merton stochastic price innovation.
  2. *PSUB 2:* Primary ($V_A, V_B$) and secondary ($V_{A'}, V_{B'}$) tranche NAV accrual & solvency check.
  3. *PSUB 3:* Behavioral agent policies (Arbitrageur mint/redeem trades, Speculator leverage demand).
  4. *PSUB 4:* Dynamic reset state transitions (Upward profit payout, Downward debt restructuring).
  5. *PSUB 5:* ACP-67 gross staking yield distribution waterfall.
- **Mechanisms:**
  * `tranche_math.py`: Primary NAVs $V_A = 1+Rv, V_B = 2S - V_A$, secondary NAVs $V_{A'} = 1+R'v, V_{B'} = 2V_A - V_{A'}$, effective leverage $\Lambda_B(S) = 2S / V_B$ (capped at 50x singularity guard).
  * `dynamic_resets.py`: Upward and downward reset executions; single-step crash bound evaluation function `evaluate_single_step_crash_tolerance`.
  * `feedback_controller.py`: `ReflexerPIDController` class with anti-windup clamping and damping ratio calculation $\zeta = \frac{1 + K K_p}{2 \sqrt{K K_i \tau}}$.
  * `dynamic_subsidy.py`: Countercyclical validator allocation $\omega_{\text{val}}(t) = \min(\omega_{\max}, \omega_{\text{base}} + \kappa_{\text{dd}} \cdot \text{drawdown} + \psi \cdot \text{yield\_gap})$.
  * `pide_solver.py`: `TranchePIDESolver` implementing IMEX Crank-Nicolson finite difference scheme with Thomas tridiagonal matrix inversion on a $(60 \times 60)$ grid for continuous jump-diffusion pricing.
  * `acp67_waterfall.py`: Gross yield routing across burn, validator boost, and L1 sovereign grants.
- **Agents:**
  * `arbitrageur.py`: Profit-maximizing secondary AMM arbitrageur calculating optimal arbitrage volume $\Delta x^*$ to restore $P_{\text{dex}} = V_{A'}$.
  * `speculator.py`: Leveraged bullish speculation on Class B equity.
  * `validator_pool.py`: Node operator staking dynamics and OpEx solvency.

---

### 3.4 Robustness & Adversarial Testing Suite (`simulations/robustness_study/`)

- **`parameter_registry.py`:** Comprehensive 28-parameter registry categorizing every variable by symbol, name, subsystem, baseline, bounds, classification (Governance, Environmental, Structural, Behavioral), and empirical identifiability.
- **`master_robustness_engine.py`:** Orchestrator executing full-factorial parameter sweeps, Saltelli Sobol GSA, controller ablation, and 11-regime stress testing.
- **`controller_isolation.py`:** Controlled experiment isolating the impact of Core Balance Sheet Arbitrage alone vs Core + P vs Core + PI vs Core + PID across liquidity depths ($\$1.5\text{M}, \$10\text{M}, \$30\text{M}$).
- **`market_regimes.py`:** Formulates 11 discrete stochastic market regimes:
  1. `CALM_BULL` ($\sigma = 45\%, \mu = +35\%$)
  2. `NORMAL` ($\sigma = 89.86\%, \mu = +10\%$)
  3. `HIGH_VOLATILITY` ($\sigma = 135\%, \mu = -5\%$)
  4. `SEVERE_BEAR` ($\sigma = 110\%, \mu = -55\%$)
  5. `FLASH_CRASH` (Deterministic $-60\%$ drop at day 100)
  6. `MULTI_JUMP_CASCADE` (3 consecutive $-30\%$ drops at days 100, 102, 104)
  7. `V_SHAPED_RECOVERY` ($-50\%$ crash followed by $+100\%$ rebound)
  8. `PROLONGED_STAGNANT_BEAR` (2-year continuous grind at $-30\%$ annual drift)
  9. `HIGH_YIELD` ($q_{\text{sAVAX}} = 10\%$)
  10. `LOW_YIELD_COMPRESSION` ($q_{\text{sAVAX}} = 3.5\%$)
  11. `ILLIQUID_AMM` ($L_{\text{amm}} = \$1.5\text{M}$)
- **`sobol_sensitivity.py`:** Implements Saltelli low-discrepancy sampling and computes first-order ($S_i$) and total-order ($S_{Ti}$) Sobol indices using Jansen variance estimators.

---

### 3.5 Canonical Accounting & Empirical Calibration

- **`simulations/canonical_accounting.py`:** Implements `PhysicalBalanceSheet` tracking physical collateral $C_{\text{sAVAX}}$, spot price, surplus reserve buffer $B_{\text{res}}$, and nominal circulating supplies. Proves stock-flow closure:
  $$\mathcal{A}_{\text{total}} \equiv \mathcal{D}_{\text{senior}} + \mathcal{E}_B + \mathcal{B}_{\text{unallocated}} - \mathcal{D}_{\text{insolvency}}$$
  Provides automated invariant checkers: `INV_MODEL_PRIMARY`, `INV_MODEL_SECONDARY`, `INV_PHYSICAL_BALANCE`, and `INV_REDEMPTION_SOLVENCY`.
- **`simulations/empirical_calibration.py`:** Maximum Likelihood Estimation (MLE) fitting of Kou (2002) double-exponential and Merton (1976) log-normal models against 2,140 real daily AVAX/USD returns (`DAT-01`), computing 500-sample bootstrap credible intervals and Kolmogorov-Smirnov test statistics.

---

## 4. Smart Contracts & Dual Implementation Verification

Located in `contracts/src/` and compiled via Foundry (`solc 0.8.24`):

```
contracts/src/
├── controller/
│   └── ResetController.sol              # On-chain dynamic reset state machine
├── core/
│   ├── CustodianVault.sol               # Physical collateral vault & share accounting
│   ├── TrancheSplitter.sol              # 2:1 Class A splitting into anUSD (A') and Yield (B')
│   └── TrancheToken.sol                 # Rebase-compliant ERC-20 tranche share token
├── icm/
│   └── TeleporterUSDAdapter.sol         # Cross-subnet Avalanche Interchain Messaging adapter
├── interfaces/                          # ICustodianVault, IResetController, ITrancheToken, IPriceOracle
├── oracles/
│   └── ChainlinkOracleAdapter.sol       # AggregatorV3 price feed adapter with staleness checks
├── remediation/                         # Forensic vulnerability remediation pairs
│   ├── candidate_corrected/
│   │   ├── ResetControllerCorrected.sol # Fixes VULN-01 (price squaring flapping)
│   │   └── TrancheSplitterCorrected.sol # Fixes VULN-02/03 (2:1 value backing)
│   └── reference_buggy/
│       ├── ResetControllerBuggy.sol     # Flapping bug reference
│       └── TrancheSplitterBuggy.sol     # 1:1 tranche disconnect reference
└── tokenomics/
    ├── DynamicValidatorSubsidy.sol      # Dynamic countercyclical yield allocator
    └── YieldRecycler.sol                # ACP-67 automated buyback and burn router
```

### Smart Contract Test Suite (`contracts/test/`):
- `CustodianVault.t.sol`: Unit tests for deposit, mint, redeem, and withdrawal workflows.
- `DualImplementationComparison.t.sol`: Differential tests running buggy vs corrected implementations side-by-side.
- `ResetAndSplitterVulnerabilities.t.sol`: Exploit proofs reproducing VULN-01 and VULN-02/03.
- `SolvencyInvariant.t.sol`: Invariant tests asserting physical asset backing across randomized rebase sequences.
- `YieldRecycler.t.sol`: Unit tests for yield splitting and burn execution.

---

## 5. Workflows & Evidence Validation Suites

- **`workflows/contracts.py`:** Pydantic runtime data contracts:
  * `GovernanceParametersContract`: Enforces parameter bounds, non-negativity, and exact simplex sum ($\sum \omega_i \equiv 1.000$).
  * `SystemStateContract`: Enforces dimension invariants, stock non-negativity, and balance sheet bounds.
- **`workflows/validation/conservation.py`:** Core mathematical invariant verifiers:
  * `verify_primary_solvency_invariant(V_A, V_B, S_index)`: Asserts $|V_A + V_B - 2S| \le 10^{-12}$.
  * `verify_sub_tranche_parity_invariant(V_A_prime, V_B_prime, V_A)`: Asserts $|V_{A'} + V_{B'} - 2V_A| \le 10^{-12}$.
- **`workflows/validation/challenger2_empirical_proofs.py`:** Empirical verification suite proving:
  1. ResetController $\beta \cdot P_0$ double-counting flapping defect (where a $+60\%$ bull market erroneously triggered an immediate downward reset).
  2. TrancheSplitter secondary tranche rebase disconnect bug.
  3. $1.37\%$ peg volatility simulation artifact proof.
- **`workflows/validation/adversarial_challenge_harness.py`:** Stress-tests schemas and edge cases (extreme crashes, negative NAVs, zero reserves).

---

## 6. Execution Datasets, Manifests & Lineage

### Summary of Authoritative Execution Artifacts:

| Artifact Path | Format | Rows | Cols | Size (Bytes) | SHA-256 Checksum | Purpose / Description |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| `audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet` | Parquet | 64,052 | 14 | 6,385,411 | `3d9ebe70ef522223edf0d115e9c0505b78ef9ceea57e5c40e22892a22bd13319` | Feasible parameter configurations surviving Stage 1 analytical filters F1, F2, F4, F5. |
| `audit_artifacts/execution/STAGE_1_ANALYTICAL_PRUNING_MANIFEST.json` | JSON | 136 lines | — | 3,481 | `b0215f418f7d8a8fdf51b02521f9c2da3f2494fdae0927abf40074b6f99674b9` | Stage 1 execution manifest recording sample size ($100\text{k}$), filter attrition, and bounding box. |
| `audit_artifacts/execution/STAGE_2_RESULTS.parquet` | Parquet | 1,600 | 25 | 201,292 | `653890da46dc822e87fda27b7a5e750b68bb54a027dd4864c1addf757211d24f` | Full Stage 2 screening outputs across all 1,600 configurations and 11 KPI metrics. |
| `audit_artifacts/execution/STAGE_2_EXPERIMENT_MANIFEST.json` | JSON | 110 lines | — | 3,573 | `95faeb49e29a39ecdafb97b47b4d1b82772714249a4f6cf70e4e7e6ae8f5fbc5` | Stage 2 execution manifest recording parameters, gates, runtime ($1303.11\text{s}$), and classifications. |
| `audit_artifacts/provenance/calibrated_market_parameters.json` | JSON | 85 lines | — | 3,115 | `fa2cbb105ec7636e09e13b4ea4e857418d1a153229b47e5b53ebbfbc1d520ae1` | Ingested Kou & Merton MLE parameters, 95% bootstrap CIs, and KS goodness-of-fit stats. |
| `audit_artifacts/state/RESEARCH_STATE.yaml` | YAML | 132 lines | — | 7,145 | `2709aa8e3aa7da9d873d6ebddbbd8ae7b3ebecfe8fbe6b5a3fa1e9e0f63b2df7` | Research snapshot baseline registry (`SNAP-2026-08-31-02`). |

### Cryptographic Lineage Tracking:
Dataset generation and validation events are recorded in append-only JSON Lines files at `data/_lineage.jsonl` and `audit_artifacts/provenance/_lineage.jsonl`.

---

## 7. Line-by-Line KPI Formulation, Objectives & Aggregation Logic

The Stage 2 screening engine (`simulations/design_discovery/stage2_architecture_screening.py`, lines 306–331) calculates 11 distinct performance and risk KPIs across the 500 Monte Carlo paths ($p \in \{1, \dots, 500\}$) and 365 daily steps ($s \in \{1, \dots, 365\}$):

```
========================================================================================================================
                                      STAGE 2 KPI AUDIT & FORMULATION MATRIX
========================================================================================================================
```

| KPI Name in Parquet | Mathematical Definition & Theoretical Formulation | Code Implementation Formula | Objective Direction | Potential Auditor Attention Items |
| :--- | :--- | :--- | :---: | :--- |
| **`peg_rmse`** | $\text{RMSE} = \sqrt{\frac{1}{N_{\text{paths}} N_{\text{steps}}} \sum_{p=1}^{N_p} \sum_{s=1}^{N_s} (P_{\text{dex}}(p, s) - 1.0)^2}$ | `np.sqrt(np.mean(peg_errors**2))` (Line 307) | **Minimize** | Measures global root-mean-square deviation of secondary AMM price from par. |
| **`max_depeg`** | $\Delta_{\max} = \max_{p, s} |P_{\text{dex}}(p, s) - 1.0|$ | `np.max(np.abs(peg_errors))` (Line 308) | **Minimize** | Worst-case single-step absolute depeg amplitude observed across all paths. |
| **`haircut_prob`** | $\mathbb{P}(\text{Loss}) = \frac{1}{N_p} \sum_{p=1}^{N_p} \mathbf{1}_{\{\text{haircut}_p > 10^{-4}\}}$ | `np.mean(haircuts > 0.0001)` (Line 309) | **Minimize** | Fraction of simulation paths where senior principal experienced $> 0.01\%$ loss. |
| **`tail_cvar_99`** | $\text{CVaR}_{99} = \mathbb{E}\left[\text{haircut} \;\middle|\; \text{haircut} \ge \text{VaR}_{99}(\text{haircut})\right]$ | `np.mean(haircuts[haircuts >= np.percentile(haircuts, 99.0)]) if np.sum(haircuts > 0) > 0 else 0.0` (Line 310) | **Minimize** | Conditional expectation of senior loss in the worst $1\%$ of paths. |
| **`recovery_time_days`** | $\bar{\tau}_{\text{rec}} = \frac{1}{K} \sum_{k=1}^K (\tau_{\text{end}, k} - \tau_{\text{start}, k})$ | `np.mean(recovery_times) if len(recovery_times) > 0 else 0.50` (Line 316) | **Minimize** | Average duration (in days) to re-enter the $\pm 0.5\%$ peg band following a depeg. |
| **`validator_cr_min`** | $\overline{\text{CR}}_{\min} = \frac{1}{N_p} \sum_{p=1}^{N_p} \min_{s} \text{CR}_{\text{val}}(p, s)$ | `np.mean(validator_cr_mins)` (Line 311) | **Maximize** | Average path-minimum validator OpEx coverage ratio during market contractions. |
| **`validator_insolvency_prob`** | $\mathbb{P}(\text{Insolvent}) = \frac{1}{N_p} \sum_{p=1}^{N_p} \mathbf{1}_{\{\min_s \text{CR}_{\text{val}}(p, s) < 1.20\}}$ | `np.mean(validator_cr_mins < 1.20)` (Line 312) | **Minimize** | Fraction of paths where validator income fell below $120\%$ of operating expenses. |
| **`avax_burned_total`** | $\bar{B}_{\text{cum}} = \frac{1}{N_p} \sum_{p=1}^{N_p} \sum_{s=1}^{N_s} \Phi_{\text{gross}}(p, s) \cdot \omega_{\text{burn}}(p, s)$ | `np.mean(burn_totals)` (Line 313) | **Maximize** | Expected cumulative native AVAX buyback and burn volume over the 1-year horizon. |
| **`reset_churn_annual`** | $\bar{f}_{\text{reset}} = \frac{1}{N_p} \sum_{p=1}^{N_p} N_{\text{resets}}(p)$ | `np.mean(reset_counts)` (Line 314) | **Minimize** | Expected annual reset frequency (discrete split / reverse-split events per year). |
| **`rate_volatility`** | $\sigma_u = \sqrt{\frac{1}{N_p N_s} \sum_{p, s} (u(p, s) - \bar{u})^2}$ | `np.std(rate_mods)` (Line 315) | **Minimize** | Standard deviation of the PI controller rate modulation signal $u(t) = \Delta R'(t)$. |
| **`reserve_depletion_prob`** | $\mathbb{P}(\text{Depleted}) = \frac{1}{N_p} \sum_{p=1}^{N_p} \mathbf{1}_{\{B_{\text{res}} \le 0\}}$ | `np.mean(res_depletions)` (Line 317) | **Minimize** | Fraction of paths where Architecture A2 reserve buffer was completely exhausted. |

---

## 8. Statistical Evaluation & Stochastic Environment Methods

### 8.1 Common Random Numbers (CRN) Methodology
The screening engine employs Common Random Numbers (CRN) to minimize variance when comparing competing architectures and policies:
1. **RNG Initialization:** `rng = np.random.default_rng(seed=2026)`.
2. **Price Path Matrix:** A single 2D array of shape $(500, 366)$ is generated once in memory.
3. **Identical Innovation Sequences:** Every candidate configuration (across all 8 architectures and 5 policies) is subjected to the exact same sequence of 500 Brownian increments $dW$ and Poisson jumps $dN$.
4. **Variance Reduction Impact:** For any pairwise difference $\Delta = J(\mathbf{u}_A) - J(\mathbf{u}_B)$, the variance is:
   $$\text{Var}(\Delta) = \text{Var}(J_A) + \text{Var}(J_B) - 2\text{Cov}(J_A, J_B)$$
   Because $\text{Cov}(J_A, J_B) > 0$ under CRN, the estimation error on pairwise comparisons is drastically reduced.

### 8.2 Kou (2002) Jump-Diffusion Calibration Grounding
The stochastic environment parameters in `stage2_architecture_screening.py` (lines 43–45) match the empirical MLE calibration reported in `audit_artifacts/provenance/calibrated_market_parameters.json`:
- Annualized diffusion volatility: $\sigma = 0.8915$ ($89.15\%$).
- Jump intensity: $\lambda = 15.00\text{ yr}^{-1}$ (Reached upper optimization bound; retained as conservative stress bound).
- Upward jump probability: $p_{\text{up}} = 0.5955$ ($59.55\%$).
- Upward tail decay: $\eta_1 = 7.671$ ($\text{Mean up-jump} = +13.04\%$).
- Downward tail decay: $\eta_2 = 7.801$ ($\text{Mean down-jump} = -12.82\%$).
- Annualized drift: $\mu = -0.3402$.
- Mean staking APR: $\bar{q} = 0.0640$ ($6.40\%$).

---

## 9. Environment, Dependencies & Root Configuration

### 9.1 Execution Environment & Tooling Versions:
- **Operating System:** Linux (Kernel 6.17)
- **Python Runtime:** Python 3.13.12 (packaged by conda-forge, GCC 14.3.0) at `/home/hash/Miniforge3/bin/python3`
- **Package Manager:** `uv` at `/home/hash/.local/bin/uv`
- **Core Scientific Python Libraries:**
  * `NumPy`: 2.4.4
  * `SciPy`: 1.17.1
  * `Pandas`: 3.0.2
  * `Fastparquet`: 2026.3.0
  * `Matplotlib`: 3.10.8
  * `PyYAML`: 6.0.3
  * `JSONSchema`: 4.26.0
- **Smart Contract Tooling:**
  * `Foundry / Forge`: 1.6.0-v1.7.0 (Commit `f83bad91...`, Build 2026-04-28)
  * `Solc Version`: 0.8.24
  * `Optimizer`: Enabled, 200 runs
  * `Configuration`: `contracts/foundry.toml`

---

## 10. Identified Code Observations & Audit Nuances for Downstream Agents

During the detailed mapping of `simulations/design_discovery/stage2_architecture_screening.py`, several specific code-level implementations were identified that downstream validation auditors and challengers should explicitly examine:

1. **Architecture A1, A3, A4 Haircut Condition Logic (Lines 192, 216, 220):**
   * In `stage2_architecture_screening.py`, the deficit check for A1, A3, and A4 is written as:
     `if 2.0 * S_t < 1.0: path_haircut = max(path_haircut, 1.0 - 2.0 * S_t)`
   * *Observation:* For A1, $V_A = 1.0 + R v > 1.0$. If $2S_t$ falls below $V_A$ but is above $1.0$, coupon loss occurs, but code checks against $1.0$ par principal. For A3 and A4, $V_A \equiv 1.0$, so $2S_t < 1.0$ matches principal default.
2. **Architecture A2 Upward Reset Omission (Lines 198–210):**
   * Architecture A0 has both upward (`V_B >= H_u`) and downward (`V_B <= H_d`) resets.
   * Architecture A2 in `stage2_architecture_screening.py` only implements downward resets (`if V_B <= H_d:`). Upward split profits in A2 remain embedded in collateral or are not explicitly reset in the screening loop. This explains why A2 reset churn ($3.04/\text{yr}$) is lower than A0 ($7.37/\text{yr}$).
3. **Architecture A5.3 Basket Diversification Scaling (Lines 145–148):**
   * A5.3 models 3-asset basket return as: `P_path = 1.0 + (P_path - 1.0) * 0.80`.
   * *Observation:* This represents a constant $20\%$ volatility reduction rather than simulating 3 individual correlated stochastic jump diffusion series. Downstream auditors should note this heuristic modeling assumption.
4. **Validator Coverage Ratio Scaling Proportionality (Lines 290–293):**
   * The gross surplus is generated on a base test vault size of $1\text{M sAVAX}$ ($\sim \$25\text{M}$ TVL, $\sim \$1.6\text{M}$ gross annual staking revenue), whereas validator OpEx is modeled against the full 1,450-node network ($\$6.09\text{M}$).
   * *Observation:* As noted in `SCREENING_STATISTICS.md`, this results in sub-scale coverage ratios ($\sim 0.02\times - 0.03\times$), which must be evaluated at full production scale ($> 100\text{M sAVAX}$) in Stage 4.
5. **Redistribution Policy POL-04 Hardcoded Constraints (Lines 280–283):**
   * POL-04 hardcodes $\omega_{\text{val}} = 0.10, \omega_{\text{res}} = 0.0, \omega_{\text{burn}} = \max(0.75, 1.0 - \omega_{\text{val}} - \omega_{\text{l1}})$. This directly starves the validator pool by design, explaining its low minimum CR ($0.0093$).
