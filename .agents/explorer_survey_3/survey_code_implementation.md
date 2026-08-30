# Code Implementation Audit: anUSD Dual-Class Securitization Protocol
**Author**: Code Implementation Auditor (`explorer_survey_3`)  
**Repository**: `avalanche-native-stablecoin`  
**Date**: 2026-08-30  
**Status**: COMPLETE (Phase 0 First-Principles Source and Derivation Audit)  

---

## 1. Executive Summary

This report delivers a first-principles, line-by-line source code and implementation audit of the **Avalanche Native Stablecoin (anUSD)** repository. The audit evaluates all Solidity smart contracts in `contracts/`, cadCAD / Python simulation engines in `simulations/`, data validation contracts in `workflows/`, and test suites across Foundry and pytest.

### Key Audit Findings

1. **CRITICAL: The $\beta \cdot P_0$ Double-Counting Reset Flapping Defect**:
   - In both the Solidity smart contracts (`ResetController.sol`, `CustodianVault.sol`) and Python simulations (`dynamic_resets.py`, `master_robustness_engine.py`, `psubs.py`), the normalized pool index is defined as $S(t) = P(t) / (\beta(t) \cdot P_0)$.
   - Upon an upward or downward reset, the code **both** sets $P_0 \leftarrow P_{\text{spot}}$ **and** compounds $\beta \leftarrow \beta \cdot (P_{\text{spot}} / P_{0,\text{old}})$.
   - This squares the price ratio in the denominator. Immediately after an upward reset at $P_t = \$40$ (from $P_0 = \$25$), the post-reset pool value evaluates to $1.25$, yielding $V_B = 0.25 \le H_d$, which **immediately triggers a spurious downward reset at the exact same price of \$40**.
   - In Python cadCAD runs (`run_monte_carlo.py`), this defect was masked by hardcoding `state["S_index"] = 1.0`, `state["V_B"] = 1.0` immediately post-reset, but on the subsequent timestep $S_{\text{new}}$ collapsed.

2. **CRITICAL: Secondary Tranche ($A'/B'$) Rebase Disconnect & Free Wealth Extraction**:
   - `TrancheSplitter.sol` allows 1:1 splitting of `tokenA` into `tokenAPrime` (anUSD) and `tokenBPrime` (Yield).
   - However, `ResetController.sol` only rebases `tokenA` and `tokenB`. `tokenAPrime` and `tokenBPrime` are never registered with or updated by `ResetController`.
   - After an upward reset where `tokenA` rebase multiplier increases to $1.5$, calling `TrancheSplitter.merge(25, 25)` burns 25 $A'$ and 25 $B'$ and mints 25 raw units of `tokenA`, which instantly equals $37.5$ nominal `tokenA` (a 50% free instant arbitrage).

3. **CRITICAL: Rounding Dust Loss and Balance Manipulation in `TrancheToken.sol`**:
   - In `TrancheToken._transfer(from, to, amount)`, raw balance is computed as `rawAmount = (amount * SCALE) / scalarMultiplier`.
   - Because of integer division truncation, transferring tokens when `scalarMultiplier > 1e18` loses up to 1 wei per transfer. Furthermore, if `amount < scalarMultiplier / SCALE`, `rawAmount` truncates to `0`, transferring 0 raw balance while emitting a nominal transfer event.

4. **HIGH: Hardcoded Reset Multipliers Violating Senior Tranche Solvency**:
   - `ResetController.sol:112-116` hardcodes fixed scalar multipliers `150/100` (+50%) for upward resets and `75/100` (-25%) for downward resets, applied symmetrically to **both** `tokenA` and `tokenB`.
   - In the governing paper (SSRN-3856569), Class A receives accrued coupon, not a share split, and downward reset amortizes Class A principal $(1 - V_B)$. In Solidity, Class A is arbitrarily haircut by 25% without returned principal.

5. **HIGH: Multiple Unimplemented Mechanisms Claimed in Documentation**:
   - **Reflexer PID Feedback Controller**: Completely absent in Solidity (no contracts exist).
   - **1-Block MEV Delay Lock ($\delta_{\text{lock}} = \pm 1.5\%$)**: Completely absent in Solidity.
   - **Spot vs. TWAP Circuit Breaker ($\Delta P_{\max} = \pm 8.0\%$)**: Completely absent in Solidity.
   - **Primary Vault Mint/Redeem Fees ($f_{\text{mint}} = 10$ bps)**: Implemented as 0 fee in `CustodianVault.sol`.
   - **Epoch Horizon Maturity ($T = 365$ days)**: Not enforced on-chain.
   - **Dynamic Subsidy Yield Compression Term ($\psi_{\text{yield}} \cdot \Delta_{\text{yield}}$)**: Omitted in `DynamicValidatorSubsidy.sol`.

---

## 2. Codebase Inventory & Component Architecture

```
contracts/
├── foundry.toml                          # Foundry project configuration (Solc 0.8.24, via-ir: false)
├── script/
│   └── DeployFuji.s.sol                  # Fuji testnet deployment script (Chain ID 43113)
├── src/
│   ├── controller/
│   │   └── ResetController.sol           # State machine for upward/downward resets & NAV calculations
│   ├── core/
│   │   ├── CustodianVault.sol            # Collateral vault (sAVAX), deposit/mint, redeem/burn
│   │   ├── MocksAVAX.sol                 # Mock ERC-20 sAVAX for testing and faucet
│   │   ├── TrancheSplitter.sol           # Secondary tranching: Class A <-> anUSD (A') + Yield (B')
│   │   └── TrancheToken.sol              # O(1) rebasing ERC-20 token implementation
│   ├── icm/
│   │   └── TeleporterUSDAdapter.sol      # Cross-L1 Avalanche Warp Messaging (ICM) bridge stub
│   ├── interfaces/
│   │   ├── ICustodianVault.sol           # Vault interface
│   │   ├── IResetController.sol          # Controller interface & ResetType enum
│   │   └── ITrancheToken.sol             # TrancheToken interface & TrancheType enum
│   ├── oracles/
│   │   └── ChainlinkOracleAdapter.sol    # Chainlink AggregatorV3 price normalizer & staleness check
│   └── tokenomics/
│       ├── DynamicValidatorSubsidy.sol   # Countercyclical validator share computation (EMA drawdown)
│       └── YieldRecycler.sol             # ACP-67 3-sink native yield waterfall dispatcher
└── test/
    ├── fuzz/                             # EMPTY DIRECTORY (0 fuzz tests)
    ├── invariant/
    │   └── SolvencyInvariant.t.sol       # 2 unit/state tests (testUpwardResetExecution, testDownwardResetExecution)
    └── unit/
        ├── CustodianVault.t.sol          # 3 unit tests (testDepositAndMint, testSecondaryTrancheSplit, testSolvencyInvariant)
        └── YieldRecycler.t.sol           # 3 unit tests (test_InitialStaticDistribution, test_DynamicDrawdownSubsidyBoost, test_MaxDynamicValidatorCeiling)

simulations/
├── cadcad_core/                          # Discrete-event simulation digital twin
│   ├── agents/
│   │   ├── arbitrageur.py                # DEX AMM constant-product arbitrageur
│   │   ├── speculator.py                 # Leveraged Class B demand model
│   │   └── validator_pool.py             # Avalanche validator OpEx & APR model
│   ├── experiments/
│   │   ├── run_black_swan_replays.py     # Deterministic historical crash replays
│   │   ├── run_comprehensive_psuu_suite.py# 180-point PSUU parameter sweep
│   │   ├── run_dynamic_validator_subsidy_audit.py
│   │   ├── run_feedback_controller_audit.py
│   │   ├── run_monte_carlo.py            # 1,000 / 10,000 path Monte Carlo runner
│   │   └── run_pide_surface.py           # 2D IMEX PIDE Crank-Nicolson surface generator
│   ├── mechanisms/
│   │   ├── acp67_waterfall.py            # Static ACP-67 65/20/15 waterfall
│   │   ├── dynamic_resets.py             # Dynamic reset formulas & single-step crash bound
│   │   ├── dynamic_subsidy.py            # Dynamic countercyclical validator allocation
│   │   ├── feedback_controller.py        # Reflexer PID controller with anti-windup
│   │   ├── pide_solver.py                # IMEX Crank-Nicolson PIDE solver with Thomas algorithm
│   │   └── tranche_math.py               # Primary & secondary NAV formulas, leverage, solvency
│   ├── params.py                         # Master dictionary of 20 governance levers + 7 env params
│   ├── psubs.py                          # 5 Partial State Update Blocks (PSUBs)
│   └── state.py                          # 22-dimensional SystemState registry
├── robustness_study/                     # Parameter Identification & Sobol GSA Engine
│   ├── adversarial_stress_testing.py
│   ├── controller_isolation.py
│   ├── market_regimes.py
│   ├── master_robustness_engine.py
│   ├── parameter_registry.py             # 23-parameter canonical metadata registry
│   └── sobol_sensitivity.py
└── verify_contractual_gates.py           # Automated G01-G20 verification runner

workflows/
├── contracts.py                          # Pydantic data validation schemas
└── validation/
    ├── adversarial_challenge_harness.py  # Empirical test harness auditing schema & float vs EVM dust
    └── conservation.py                   # Machine-epsilon conservation invariant checker
```

---

## 3. 23 Protocol Parameters & Mechanism Traceability Matrix

The table below traces all 23 canonical protocol parameters across mathematical definitions, Solidity smart contracts, Python simulation models, and implementation fidelity verdicts.

| ID | Symbol | Parameter Name | Whitepaper Baseline | Solidity Contract & Variable | cadCAD / Python Variable | Implementation Fidelity | Key Semantic Divergence / Flaw |
|:---|:---|:---|:---|:---|:---|:---:|:---|
| **P01** | $R$ | Senior Class A Coupon Rate | 7.30% p.a. | `ResetController.sol:23` (`couponRateR`) | `params.py:18` (`coupon_R`), `tranche_math.py:24` | **PARTIAL** | Integer truncation in `(couponRateR * dt) / 365 days`; resets to 0 on every reset. |
| **P02** | $R'$ | anUSD Benchmark Coupon Rate | 3.00% p.a. | *NOT IMPLEMENTED* | `params.py:19` (`coupon_R_prime`), `tranche_math.py:34` | **MISSING** | Completely omitted in Solidity; `tokenAPrime` has zero yield accrual on-chain. |
| **P03** | $\tilde{R}$ | Bear Coupon Subsidy Rate | 10.00% p.a. | *NOT IMPLEMENTED* | `params.py:20` (`bear_subsidy_R`), `dynamic_resets.py:69` | **MISSING** | Completely omitted in Solidity; no wealth transfer from A to B during reset. |
| **P04** | $\alpha$ | Primary Tranche Split Ratio | 1.0000 | `CustodianVault.sol:111` (Hardcoded 1:1) | `params.py:21` (`tranche_ratio_chi`), `tranche_math.py:22` | **HARDCODED** | Hardcoded 1:1 pair minting; not configurable via state variable. |
| **P05** | $T$ | Epoch Maturity Horizon | 365 days (1.0 yr) | *NOT ENFORCED* | `params.py:22` (`epoch_maturity_T_days`) | **MISSING** | No rollover or maturity function exists in `ResetController.sol`. |
| **P06** | $H_u$ | Upward Reset Barrier | $2.00 NAV | `ResetController.sol:24` (`H_u = 2.0e18`) | `params.py:27` (`barrier_H_u`), `dynamic_resets.py:11` | **MATCH** | Triggers when $V_B \ge 2.00$. |
| **P07** | $H_d$ | Downward Reset Barrier | $0.25 NAV | `ResetController.sol:25` (`H_d = 0.25e18`) | `params.py:28` (`barrier_H_d`), `dynamic_resets.py:17` | **MATCH** | Triggers when $V_B \le 0.25$. |
| **P08** | $\mu_{\text{split}}$ | Upward Split Multiplier | $(V_B - 1.0)/1.0$ (Dynamic) | `ResetController.sol:112` (`* 150 / 100`) | `params.py:29` (`split_mult_up = 1.50`) | **BUGGY / HARDCODED** | Hardcodes 1.5x split to BOTH tokenA and tokenB regardless of actual $V_B$. |
| **P09** | $\mu_{\text{merge}}$ | Downward Merge Multiplier | $V_B$ (Dynamic) | `ResetController.sol:115` (`* 75 / 100`) | `params.py:30` (`merge_mult_down = 0.75`) | **BUGGY / HARDCODED** | Hardcodes 0.75x merge to BOTH tokenA and tokenB regardless of actual $V_B$. |
| **P10** | $K_p$ | Proportional Controller Gain | 0.150 | *NOT IMPLEMENTED* | `params.py:36` (`controller_Kp`), `feedback_controller.py:15` | **MISSING** | No on-chain PID feedback controller contract exists. |
| **P11** | $K_i$ | Integral Controller Gain | 0.020 | *NOT IMPLEMENTED* | `params.py:37` (`controller_Ki`), `feedback_controller.py:15` | **MISSING** | No on-chain PID feedback controller contract exists. |
| **P12** | $K_d$ | Derivative Controller Gain | 0.005 | *NOT IMPLEMENTED* | `params.py:38` (`controller_Kd`), `feedback_controller.py:15` | **MISSING** | No on-chain PID feedback controller contract exists. |
| **P13** | $\Delta R'_{\max}$ | Max Rate Modulation Clamp | $\pm 5.00\%$ p.a. | *NOT IMPLEMENTED* | `params.py:39` (`controller_max_adj`), `feedback_controller.py:53` | **MISSING** | No rate clamping on-chain. |
| **P14** | $\Delta t_{\text{sample}}$ | DEX TWAP Sampling Window | 1800 sec (30 min) | *NOT IMPLEMENTED* | `params.py:40` (`twap_window_sec = 1800`) | **MISSING** | `ChainlinkOracleAdapter.sol` has no TWAP logic. |
| **P15** | $\omega_{\text{burn}}$ | AVAX Buyback & Burn Share | 65.00% | `YieldRecycler.sol:21` (`STATIC_BUYBACK_BPS = 6500`) | `params.py:45` (`acp67_burn_pct = 0.650`), `acp67_waterfall.py:12` | **PARTIAL** | Floor is 40% in `DynamicValidatorSubsidy.sol:19`, but 20% in `dynamic_subsidy.py:48`. |
| **P16** | $\omega_{\text{val}}$ | Baseline Validator Share | 20.00% | `YieldRecycler.sol:22` (`STATIC_VALIDATOR_BPS = 2000`) | `params.py:46` (`acp67_val_pct = 0.200`), `dynamic_subsidy.py:12` | **MATCH** | Base 20.0%, max 45.0%. |
| **P17** | $\omega_{\text{l1}}$ | Sovereign L1 Grants Share | 15.00% | `YieldRecycler.sol:23` (`STATIC_ECOSYSTEM_BPS = 1500`) | `params.py:47` (`acp67_l1_pct = 0.150`), `dynamic_subsidy.py:17` | **MATCH** | Exactly 15.0% in both. |
| **P18** | $\kappa_{\text{drawdown}}$ | Validator Drawdown Responsiveness | 0.3500 | `DynamicValidatorSubsidy.sol:22` (`KAPPA_DRAWDOWN = 3500`) | `parameter_registry.py:319`, `dynamic_subsidy.py:14` | **MATCH** | Scaled by 10000 BPS scale. |
| **P19** | $\delta_{\text{lock}}$ | MEV Proximity State-Lock Band | $\pm 1.50\%$ | *NOT IMPLEMENTED* | `params.py:31` (`mev_band_delta = 0.0150`) | **MISSING** | No 1-block delay lock or barrier proximity check exists in Solidity. |
| **P20** | $\Delta P_{\max}$ | Oracle Circuit Breaker Divergence | $\pm 8.00\%$ | *NOT IMPLEMENTED* | `params.py:55` (`max_oracle_divergence = 0.080`) | **MISSING** | `isCircuitBreakerTripped()` only checks staleness and non-positive price. |
| **P21** | $\tau_{\text{heart}}$ | Max Oracle Staleness Heartbeat | 300 sec (5 min) | `ChainlinkOracleAdapter.sol:30` (`maxStalenessSeconds = 3600`) | `params.py:56` (`oracle_heartbeat_sec = 300`) | **DIVERGENT** | Solidity initializes to 3600s (1 hour), divergent from 300s standard. |
| **P22** | $f_{\text{mint}}$ | Primary Vault Issuance Fee | 10 bps (0.10%) | `CustodianVault.sol:111` (0 bps fee) | `params.py:48` (`fee_mint_bps = 10`) | **MISSING** | Zero fee collected in Solidity contracts. |
| **P23** | $f_{\text{redeem}}$ | Primary Vault Redemption Fee | 10 bps (0.10%) | `CustodianVault.sol:130` (0 bps fee) | `params.py:49` (`fee_redeem_bps = 10`) | **MISSING** | Zero fee collected in Solidity contracts. |

---

## 4. Comparative Execution Semantics: Discrete EVM vs Continuous Math

### 4.1. Precision Representation & Truncation

- **Solidity (EVM)**: All token and accounting values are modeled as unsigned 256-bit integers with 18 decimals of fixed precision (`SCALE = 1e18`), or basis points (`TOTAL_BPS = 10000`). EVM integer division `/` truncates towards zero (floor).
- **Python / cadCAD**: All numerical values are IEEE 754 double-precision floating-point numbers (`float64`, 53 bits of mantissa).
- **Precision Divergence at Scale ($100M TVL)**:
  - At $\$100\text{M}$ TVL, the Unit in the Last Place (ULP) for `float64` is $\approx 1.49 \times 10^{-8}$ USD.
  - In EVM `uint256`, 1 wei is $10^{-18}$ USD, giving 10 orders of magnitude finer precision than `float64`.
  - However, in `float64`, mathematical identities like $(A / B) \times B \approx A$ hold up to $\sim 10^{-16}$, whereas in EVM integer math, `(A * B) / C` loses the remainder $A \cdot B \pmod C$.

### 4.2. Critical Rounding Vulnerability in `TrancheToken.sol`

In `TrancheToken.sol`, transfer logic converts nominal transfer amounts to internal raw units:
```solidity
function _transfer(address from, address to, uint256 amount) internal {
    require(from != address(0) && to != address(0), "Zero address");
    uint256 rawAmount = (amount * SCALE) / scalarMultiplier;
    require(_rawBalances[from] >= rawAmount, "Insufficient balance");
    _rawBalances[from] -= rawAmount;
    _rawBalances[to] += rawAmount;
    emit Transfer(from, to, amount);
}
```

#### Vulnerability Analysis:
1. **Token Evaporation via Truncation**:
   - Suppose `scalarMultiplier = 1.5e18` (post-upward reset).
   - Alice sends 1.0 nominal token (`1e18` wei).
   - `rawAmount = (1e18 * 1e18) / 1.5e18 = 666,666,666,666,666,666` wei (truncated from $.666...$).
   - Alice's raw balance decreases by `666,666,666,666,666,666`.
   - Bob's raw balance increases by `666,666,666,666,666,666`.
   - When Bob calls `balanceOf(to)`, he gets `(666666666666666666 * 1.5e18) / 1e18 = 999,999,999,999,999,999` wei.
   - **1 wei is permanently destroyed** on every transfer.
2. **Zero-Raw-Amount Transfer Exploit**:
   - If a caller transfers `amount < scalarMultiplier / 1e18` (e.g. `amount = 1` when `scalarMultiplier = 1.5e18`), `rawAmount` evaluates to `0`.
   - `_rawBalances[from] -= 0`, `_rawBalances[to] += 0`.
   - The contract emits `Transfer(from, to, 1)` without transferring any balance, which desynchronizes off-chain indexers and event listeners.

---

## 5. Tranche Mechanics & Lifecycle Audit

### 5.1. Primary Tranching: `CustodianVault.sol`

```solidity
// Minting (depositAndMint)
uint256 pairAmount = (collateralAmount * referencePrice) / SCALE;
tokenA.mint(msg.sender, pairAmount);
tokenB.mint(msg.sender, pairAmount);

// Redeeming (redeemAndBurn)
tokenA.burn(msg.sender, rawAmountA);
tokenB.burn(msg.sender, rawAmountB);
collateralReturned = (rawAmountA * SCALE) / referencePrice;
```

#### Flaws Identified:
1. **Post-Reset Redemption Lock / Under-Redemption**:
   - `depositAndMint` adds `pairAmount` to `_rawBalances[msg.sender]`.
   - After an upward reset where `scalarMultiplier = 1.5e18`, the user's nominal balance is $1.5 \times \text{pairAmount}$.
   - However, `redeemAndBurn` accepts `rawAmountA` and calls `tokenA.burn(msg.sender, rawAmountA)`.
   - If a user passes their nominal balance $1.5 \times \text{pairAmount}$, the call reverts with `"Burn amount exceeds raw balance"`.
   - If the user passes their raw balance `pairAmount`, they receive `collateralReturned = (pairAmount * SCALE) / referencePrice`. Because `referencePrice` is now higher ($P_{\text{new}} = \$40$ instead of $\$25$), the returned collateral is $(250 \times 1e18) / 40e18 = 6.25$ sAVAX (worth $\$250$).
   - The user cannot redeem their accrued capital gain ($+50\%$) because `CustodianVault` has no mechanism to redeem surplus shares!

### 5.2. Secondary Tranching: `TrancheSplitter.sol`

```solidity
function split(uint256 amountA) external {
    tokenA.burn(msg.sender, amountA);
    tokenAPrime.mint(msg.sender, amountA);
    tokenBPrime.mint(msg.sender, amountA);
}

function merge(uint256 amountAPrime, uint256 amountBPrime) external {
    require(amountAPrime == amountBPrime && amountAPrime > 0, "Must merge equal pairs");
    tokenAPrime.burn(msg.sender, amountAPrime);
    tokenBPrime.burn(msg.sender, amountBPrime);
    tokenA.mint(msg.sender, amountAPrime);
}
```

#### Flaws Identified:
1. **Critical Secondary Tranche Rebase Disconnect**:
   - `TrancheToken` instances `tokenAPrime` and `tokenBPrime` are instantiated as independent contracts with their own `scalarMultiplier`.
   - `ResetController.sol` only sets `tokenA` and `tokenB` controllers.
   - When resets execute, `tokenAPrime.scalarMultiplier` and `tokenBPrime.scalarMultiplier` remain fixed at `1e18`.
   - When a user calls `merge(amount, amount)`, `tokenA.mint(msg.sender, amount)` adds `amount` to `tokenA._rawBalances[msg.sender]`.
   - If `tokenA.scalarMultiplier()` was scaled to $1.5 \times 1e18$, that `amount` of raw `tokenA` is instantly worth $1.5 \times \text{amount}$ nominal `tokenA`!
   - **Exploit**: An attacker splits 100 Class A before reset $\rightarrow$ holds 100 $A'$ and 100 $B'$. Reset occurs ($1.5\text{x}$). Attacker calls `merge(100, 100)` $\rightarrow$ receives 100 raw Class A, which is now worth 150 Class A. The attacker extracted 50 Class A tokens for free out of thin air.

---

## 6. Reset Controller & Oracle Mechanics Audit

### 6.1. The Critical $\beta \cdot P_0$ Double-Counting Bug

In `ResetController.sol`:
```solidity
function checkReset() public view override returns (ResetType, uint256 currentNAV_B) {
    uint256 livePrice = getLivePrice();
    uint256 dt = block.timestamp - lastResetTimestamp;
    uint256 accruedCoupon = (couponRateR * dt) / (365 days);
    uint256 V_A = SCALE + accruedCoupon;

    // Line 85-86:
    uint256 P_0 = vault.referencePrice();
    uint256 poolValue = (2 * livePrice * SCALE) / ((vault.beta() * P_0) / SCALE);
    
    if (poolValue <= V_A) {
        currentNAV_B = 0;
    } else {
        currentNAV_B = poolValue - V_A;
    }
    if (currentNAV_B >= H_u) return (ResetType.UPWARD, currentNAV_B);
    else if (currentNAV_B <= H_d) return (ResetType.DOWNWARD, currentNAV_B);
    else return (ResetType.NONE, currentNAV_B);
}

function executeReset() external override returns (ResetType) {
    (ResetType rType, ) = checkReset();
    require(rType != ResetType.NONE, "No reset condition met");

    uint256 livePrice = getLivePrice();
    uint256 P_0 = vault.referencePrice();
    // Line 109:
    uint256 newBeta = (livePrice * SCALE) / P_0;

    // Line 119:
    vault.updateResetState(livePrice, newBeta);
    lastResetTimestamp = block.timestamp;
    return rType;
}
```

#### Step-by-Step Mathematical Proof of State Machine Flapping:

1. **Initial State**:
   - Initial reference price $P_0 = \$25.00$ (`25e18`), `beta = 1.0` (`1e18`).
2. **Market Price Rises to $\$40.00$**:
   - In `checkReset()`:
     $$\text{poolValue} = \frac{2 \times 40 \times 10^{18}}{(1.0 \times 25)} = 3.20$$
     $$V_A = 1.00 \implies \text{NAV}_B = 3.20 - 1.00 = 2.20 \ge H_u (2.00)$$
   - Upward reset condition met.
3. **`executeReset()` Executes**:
   - `newBeta = (40e18 * 1e18) / 25e18 = 1.6e18` ($1.6$).
   - `vault.updateResetState(40e18, 1.6e18)` sets:
     - `vault.referencePrice() = 40e18` ($\$40.00$)
     - `vault.beta() = 1.6e18` ($1.60$)
4. **Immediate Subsequent Block (Price remains $\$40.00$)**:
   - In `checkReset()`:
     $$P_0 = \text{vault.referencePrice()} = 40e18$$
     $$\text{vault.beta()} = 1.6e18$$
     $$\text{Denominator} = \frac{\text{vault.beta()} \times P_0}{10^{18}} = \frac{1.6 \times 10^{18} \times 40 \times 10^{18}}{10^{18}} = 64 \times 10^{18} \quad (\$64.00)$$
     $$\text{Numerator} = 2 \times \text{livePrice} \times 10^{18} = 2 \times 40 \times 10^{18} = 80 \times 10^{18} \quad (\$80.00)$$
     $$\text{poolValue} = \frac{80 \times 10^{18}}{64 \times 10^{18}} = 1.25 \times 10^{18} \quad (\$1.25)$$
     $$\text{NAV}_B = 1.25 - 1.00 = 0.25 \times 10^{18} \quad (\$0.25)$$
   - Because $\text{NAV}_B = 0.25 \le H_d (0.25)$, `checkReset()` **immediately returns `(ResetType.DOWNWARD, 0.25e18)`**!
5. **Impact**:
   - An upward reset immediately induces a spurious downward reset in the very next block without any change in asset price.
   - The protocol enters an unrecoverable flapping oscillation where every upward reset triggers an immediate downward reset.

---

## 7. Tokenomics, Dynamic Subsidy & Waterfall Audit

### 7.1. `YieldRecycler.sol` & `DynamicValidatorSubsidy.sol`

```solidity
// YieldRecycler.sol
uint256 public constant STATIC_BUYBACK_BPS = 6500;   // 65.0%
uint256 public constant STATIC_VALIDATOR_BPS = 2000; // 20.0%
uint256 public constant STATIC_ECOSYSTEM_BPS = 1500; // 15.0%

// DynamicValidatorSubsidy.sol
function computeDynamicShares(uint256 spotPrice) public view returns (
    uint256 valBps, uint256 burnBps, uint256 ecoBps
) {
    ecoBps = ECOSYSTEM_BPS; // 1500
    if (spotPrice >= emaPrice || emaPrice == 0) {
        valBps = BASE_VALIDATOR_BPS; // 2000
        burnBps = TOTAL_BPS - valBps - ecoBps; // 6500
        return (valBps, burnBps, ecoBps);
    }
    uint256 drawdownBps = ((emaPrice - spotPrice) * TOTAL_BPS) / emaPrice;
    uint256 subsidyBoostBps = (drawdownBps * KAPPA_DRAWDOWN) / TOTAL_BPS;
    valBps = BASE_VALIDATOR_BPS + subsidyBoostBps;
    if (valBps > MAX_VALIDATOR_BPS) valBps = MAX_VALIDATOR_BPS; // 4500
    burnBps = TOTAL_BPS - valBps - ecoBps;
    require(burnBps >= MIN_BURN_BPS, "Burn share below floor"); // 4000
}
```

#### Divergences Identified:
1. **Omission of Yield Compression Term**:
   - In the Whitepaper and Python specification (`dynamic_subsidy.py:29`), the dynamic validator allocation includes a yield compression term:
     $$\omega_{\text{val}}(t) = \min\left(\omega_{\text{val}}^{\max}, \omega_{\text{val}}^{\text{base}} + \kappa \Delta_{\text{drawdown}} + \psi_{\text{yield}} \Delta_{\text{yield}}\right)$$
   - In `DynamicValidatorSubsidy.sol`, $\psi_{\text{yield}} \Delta_{\text{yield}}$ is **completely omitted**. The on-chain contract only responds to price drawdowns and cannot respond to staking yield compression.
2. **Floor Inconsistency for Buyback & Burn**:
   - In `DynamicValidatorSubsidy.sol:19`, `MIN_BURN_BPS = 4000` (40.0% floor).
   - In `simulations/cadcad_core/mechanisms/dynamic_subsidy.py:48`, `omega_burn = max(0.20, ...)` (20.0% floor).

---

## 8. Test Suite & Verification Audit

### 8.1. Foundry Suite Assessment

Executing `forge test -vvv` in `contracts/`:
- Ran **8 tests across 3 test files**:
  - `YieldRecyclerUnitTest`: 3 tests (`test_InitialStaticDistribution`, `test_DynamicDrawdownSubsidyBoost`, `test_MaxDynamicValidatorCeiling`)
  - `SolvencyInvariantTest`: 2 tests (`testUpwardResetExecution`, `testDownwardResetExecution`)
  - `CustodianVaultUnitTest`: 3 tests (`testDepositAndMint`, `testSecondaryTrancheSplit`, `testSolvencyInvariant`)
- All 8 tests passed in 26.53 ms.

#### Critical Test Gaps and Blind Spots:
1. **Zero Fuzz Testing**: The directory `contracts/test/fuzz/` is empty. No property-based or invariant fuzz tests exist.
2. **Single-Step Reset Truncation**:
   - `SolvencyInvariantTest.testUpwardResetExecution` stops execution immediately after `controller.executeReset()`.
   - It **never calls `controller.checkReset()` post-reset**. If it had asserted `checkReset() == ResetType.NONE`, the test would have immediately failed and exposed the $\beta \cdot P_0$ double-counting flapping bug.
3. **No Multi-Epoch / Rollover Testing**: Zero tests verify consecutive resets or redemption after a reset.
4. **No Secondary Tranche Reset Interaction Testing**: Zero tests verify what happens when `TrancheSplitter` is used before and after a reset.

---

## 9. Comprehensive Register of Implementation Vulnerabilities

| Finding ID | Severity | Component | Vulnerability Title | Root Cause | Impact | Recommended Fix |
|:---|:---:|:---|:---|:---|:---|:---|
| **VULN-01** | **CRITICAL** | `ResetController.sol`, `CustodianVault.sol`, `dynamic_resets.py` | State Machine Reset Flapping via $\beta \cdot P_0$ Double-Counting | Denominator $S(t) = P(t) / (\beta \cdot P_0)$ combines moving anchor $P_0 \leftarrow P_{\text{spot}}$ with cumulative ratio $\beta \leftarrow \beta \cdot (P_{\text{spot}}/P_{0,\text{old}})$. | Every upward reset immediately induces a spurious downward reset at the same price. | Fix $P_0$ permanently to initial issuance price $P(0)$, OR remove $\beta$ from the denominator of $S(t)$ and use $S(t) = P(t) / P_0$ with moving $P_0$. |
| **VULN-02** | **CRITICAL** | `TrancheSplitter.sol`, `ResetController.sol` | Secondary Tranche Rebase Disconnect Free Arbitrage | `TrancheToken` for $A'$ and $B'$ are not linked to `ResetController.executeReset()`. | Users can split $A$ into $A'/B'$ before upward reset and merge post-reset to extract unbacked Class A tokens (+50% free profit). | Register $A'$ and $B'$ with `ResetController` or adjust `TrancheSplitter.merge()` to account for `tokenA.scalarMultiplier()`. |
| **VULN-03** | **CRITICAL** | `TrancheToken.sol` | Token Evaporation & Zero-Transfer Exploit via Integer Truncation | `rawAmount = (amount * SCALE) / scalarMultiplier` truncates division without remainder tracking. | 1 wei destroyed per transfer; transfers of small amounts emit events without moving raw balances. | Implement virtual share balance model or round in favor of protocol balance preservation. |
| **VULN-04** | **HIGH** | `ResetController.sol` | Hardcoded Symmetrical Reset Multipliers | `applyScalarSplit` hardcodes 150/100 and 75/100 to both `tokenA` and `tokenB`. | Violates senior/equity tranching specification; arbitrarily haircuts Class A on downward resets without principal payout. | Calculate dynamic scalar splits $\mu_A, \mu_B$ based on actual $V_B$ and return principal to Class A. |
| **VULN-05** | **HIGH** | `CustodianVault.sol` | Post-Reset Redemption Lock | `redeemAndBurn` expects `rawAmount` and divides by updated `referencePrice`. | Users cannot redeem surplus split shares post-upward reset; capital gains cannot be realized in collateral. | Allow redeeming nominal rebased balances or implement dedicated profit payout / withdrawal queue. |
| **VULN-06** | **MEDIUM** | `DynamicValidatorSubsidy.sol` | Missing Yield Compression Sensitivity | On-chain contract lacks $\psi_{\text{yield}} \cdot \Delta_{\text{yield}}$ term. | Validator subsidy cannot respond to staking reward compression post ACP-77. | Add staking APR oracle input and dynamic yield compression term to `computeDynamicShares`. |
| **VULN-07** | **MEDIUM** | `ChainlinkOracleAdapter.sol` | Excessive Staleness Window & Missing Circuit Breaker | `maxStalenessSeconds = 3600` (1 hr) default; no spot vs TWAP divergence breaker. | Protocol vulnerable to stale or manipulated oracle prices during rapid market moves. | Enforce 300s heartbeat default and implement 30-min TWAP circuit breaker comparison. |
| **VULN-08** | **LOW** | `CustodianVault.sol` | Omission of Vault Mint/Redeem Fees | `depositAndMint` and `redeemAndBurn` charge 0 fee. | Protocol misses 10 bps fee revenue intended for ACP-67 recirculation waterfall. | Implement configurable `feeMintBps` and `feeRedeemBps` and route fees to `YieldRecycler`. |

---

## 10. Verification Commands & Independent Reproducibility

To independently verify all findings in this audit report, execute the following commands in the workspace:

```bash
# 1. Run Foundry Smart Contract Test Suite
cd /home/hash/Hub/Projects/avalanche-native-stablecoin/contracts
forge test -vvv

# 2. Run Automated Contractual Quality Gates & Invariant Audit
cd /home/hash/Hub/Projects/avalanche-native-stablecoin
python3 simulations/verify_contractual_gates.py

# 3. Run Adversarial Empirical Challenge Test Harness (Float vs EVM Precision & Lineage)
python3 workflows/validation/adversarial_challenge_harness.py

# 4. Verify PIDE Solver Convergence
python3 simulations/cadcad_core/mechanisms/pide_solver.py

# 5. Verify Parameter Registry Metadata
python3 simulations/robustness_study/parameter_registry.py
```
