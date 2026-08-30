# Handoff Report: Code Implementation Audit (Phase 0 Source & Derivation Audit)
**Agent**: Code Implementation Auditor (`explorer_survey_3`)  
**Working Directory**: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_3`  
**Timestamp**: 2026-08-30T11:50:00Z  
**Handoff Type**: Hard (Task Complete)  

---

## 1. Observation

Direct observations across smart contracts, simulations, test harnesses, and mathematical specifications:

### 1.1. $\beta \cdot P_0$ Double-Counting Bug in Reset State Machine
- **File**: `contracts/src/controller/ResetController.sol`, Lines 85–86 & 109–119:
  ```solidity
  85: uint256 P_0 = vault.referencePrice();
  86: uint256 poolValue = (2 * livePrice * SCALE) / ((vault.beta() * P_0) / SCALE);
  ...
  109: uint256 newBeta = (livePrice * SCALE) / P_0;
  ...
  119: vault.updateResetState(livePrice, newBeta);
  ```
- **File**: `contracts/src/core/CustodianVault.sol`, Lines 144–149:
  ```solidity
  144: function updateResetState(uint256 newPrice, uint256 newBeta) external onlyControllerOrOwner {
  145:     require(newPrice > 0 && newBeta > 0, "Invalid reset parameters");
  146:     referencePrice = newPrice;
  147:     beta = newBeta;
  148:     emit StateReset(newPrice, newBeta);
  149: }
  ```
- **File**: `simulations/cadcad_core/experiments/run_monte_carlo.py`, Lines 46–64:
  ```python
  46: if p_out4["reset_type"] != "NONE":
  47:     state["beta_rebase"] = p_out4["new_beta"]
  48:     state["P_0"] = p_out4["new_P_0"]
  ...
  56:     state["S_index"] = 1.0
  57:     state["V_A"] = 1.0
  58:     state["V_B"] = 1.0
  ```
- **File**: `simulations/cadcad_core/psubs.py`, Lines 72–73:
  ```python
  72: S_new = compute_normalized_pool_index(P_spot, beta, P_0)
  73: V_A, V_B = evaluate_primary_navs(S_new, v_new, params["coupon_R"])
  ```

### 1.2. Secondary Tranche ($A'/B'$) Rebase Disconnect
- **File**: `contracts/src/core/TrancheSplitter.sol`, Lines 24–43:
  ```solidity
  24: function split(uint256 amountA) external {
  ...
  28:     tokenAPrime.mint(msg.sender, amountA);
  29:     tokenBPrime.mint(msg.sender, amountA);
  30: }
  34: function merge(uint256 amountAPrime, uint256 amountBPrime) external {
  ...
  40:     tokenA.mint(msg.sender, amountAPrime);
  41: }
  ```
- **File**: `contracts/src/controller/ResetController.sol`, Lines 111–117:
  ```solidity
  111: if (rType == ResetType.UPWARD) {
  112:     tokenA.applyScalarSplit((tokenA.scalarMultiplier() * 150) / 100);
  113:     tokenB.applyScalarSplit((tokenB.scalarMultiplier() * 150) / 100);
  114: } else if (rType == ResetType.DOWNWARD) {
  115:     tokenA.applyScalarSplit((tokenA.scalarMultiplier() * 75) / 100);
  116:     tokenB.applyScalarSplit((tokenB.scalarMultiplier() * 75) / 100);
  117: }
  ```
  `tokenAPrime` and `tokenBPrime` are never passed to or updated by `ResetController`.

### 1.3. Rounding Dust & Truncation in `TrancheToken.sol`
- **File**: `contracts/src/core/TrancheToken.sol`, Lines 110–117:
  ```solidity
  110: function _transfer(address from, address to, uint256 amount) internal {
  111:     require(from != address(0) && to != address(0), "Zero address");
  112:     uint256 rawAmount = (amount * SCALE) / scalarMultiplier;
  113:     require(_rawBalances[from] >= rawAmount, "Insufficient balance");
  114:     _rawBalances[from] -= rawAmount;
  115:     _rawBalances[to] += rawAmount;
  116:     emit Transfer(from, to, amount);
  117: }
  ```

### 1.4. Test Suite Execution & Coverage
- Command: `forge test -vvv` in `contracts/`
- Output: 8 tests passed across 3 suites in 26.53 ms.
- Observation: Directory `contracts/test/fuzz/` contains 0 files. `SolvencyInvariantTest.testUpwardResetExecution` stops execution immediately after `controller.executeReset()` without calling `controller.checkReset()` to test post-reset stability.

---

## 2. Logic Chain

1. **State Machine Flapping Proof**:
   - In `ResetController.sol:86`, pool value is computed as $\text{poolValue} = 2 \cdot P_t / (\beta \cdot P_0)$.
   - When price moves from $P_0 = \$25$ to $P_t = \$40$, $\text{poolValue} = 2 \cdot 40 / 25 = 3.20$, so $V_B = 3.20 - 1.00 = 2.20 \ge H_u (2.00)$, triggering an upward reset (Obs 1.1).
   - In `executeReset()`, `newBeta = 40/25 = 1.6`, and `vault.updateResetState(40, 1.6)` sets `referencePrice = 40` and `beta = 1.6`.
   - On the very next check at the same price $P_t = \$40$, the denominator evaluates to $(\beta \cdot P_0) = 1.6 \times 40 = 64$.
   - Thus, $\text{poolValue} = 2 \times 40 / 64 = 1.25$.
   - $V_B = 1.25 - 1.00 = 0.25 \le H_d (0.25)$.
   - Therefore, `checkReset()` immediately returns `(ResetType.DOWNWARD, 0.25e18)`, proving that every upward reset immediately triggers a spurious downward reset at constant price.

2. **Secondary Tranche Free Profit Extraction Proof**:
   - `tokenA` rebase multiplier scales by $1.5\text{x}$ on upward reset (Obs 1.2).
   - `tokenAPrime` (anUSD) and `tokenBPrime` (Yield) scalar multipliers remain $1.0\text{x}$.
   - Splitting 100 Class A before reset creates 100 $A'$ and 100 $B'$.
   - Merging 100 $A'$ and 100 $B'$ post-reset calls `tokenA.mint(msg.sender, 100)`, crediting 100 raw units of `tokenA`.
   - With `tokenA.scalarMultiplier() = 1.5e18`, 100 raw units of `tokenA` equals 150 nominal `tokenA`, creating 50 Class A tokens without backing collateral.

3. **Truncation and Zero Transfer Proof**:
   - In `TrancheToken._transfer`, `rawAmount = (amount * SCALE) / scalarMultiplier` (Obs 1.3).
   - When `amount < scalarMultiplier / SCALE` (e.g. `amount = 1` wei with `scalarMultiplier = 1.5e18`), integer division yields `rawAmount = 0`.
   - The contract emits `Transfer(from, to, 1)` but modifies neither account's raw balance.

---

## 3. Caveats

- **No Live Mainnet Deployment**: The Solidity contracts were evaluated on local Foundry and Fuji deployment scripts (`DeployFuji.s.sol`); no mainnet contracts are deployed.
- **Off-Chain Keepers**: The smart contracts require external keepers to invoke `syncPriceWithOracle()`, `updateEmaPrice()`, and `executeReset()`. Off-chain bot automation was not present in the repository.
- **Alternative Interpretation of $P_0$**: If $P_0$ was meant to be fixed forever at $t=0$, then `vault.referencePrice` should never be overwritten in `updateResetState`. If $P_0$ was meant to be the moving anchor price of each epoch, then $\beta$ should not appear in the denominator of $S(t)$. Combining both was an unintended implementation error.

---

## 4. Conclusion

1. The anUSD codebase exhibits deep mathematical, architectural, and security divergences between its formal specifications and its code implementations.
2. The core reset state machine suffers from a critical $\beta \cdot P_0$ double-counting defect causing infinite reset flapping across both Solidity contracts and Python simulations.
3. The secondary tranche system ($A'/B'$) has a fatal rebase disconnect allowing free token extraction upon share merger post-reset.
4. Key claimed mechanisms (Reflexer PID feedback controller, 1-block MEV proximity lock, spot vs TWAP circuit breakers, and vault fees) are completely absent in the Solidity contracts.
5. All 23 protocol parameters have been fully audited, indexed, and cataloged in `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_3/survey_code_implementation.md`.

---

## 5. Verification Method

To independently reproduce and verify this audit:

```bash
# 1. Inspect the comprehensive Code Implementation Audit Report
view_file /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_3/survey_code_implementation.md

# 2. Run Foundry Smart Contract Test Suite
cd /home/hash/Hub/Projects/avalanche-native-stablecoin/contracts
forge test -vvv

# 3. Run Automated Contractual Quality Gates & Invariant Audit
cd /home/hash/Hub/Projects/avalanche-native-stablecoin
python3 simulations/verify_contractual_gates.py

# 4. Run Adversarial Empirical Challenge Test Harness (Float vs EVM Precision & Lineage)
python3 workflows/validation/adversarial_challenge_harness.py

# 5. Run Parameter Registry Verification
python3 simulations/robustness_study/parameter_registry.py
```
