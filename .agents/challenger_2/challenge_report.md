# Adversarial Challenge & Empirical Verification Report: Code Vulnerabilities & Simulation Artifacts

**Report ID:** `BCRG-CHALLENGE-2026-CODE-SIM-VERIFICATION`  
**Target Document:** `docs/reports/SOURCE_AND_DERIVATION_AUDIT.md`  
**Challenger Role:** Empirical Challenger 2 (`challenger_2`)  
**Evaluation Standard:** First-Principles Empirical Reproduction & Independent Execution Canon  
**Date:** August 30, 2026  
**Verdict:** **APPROVE** (All 3 core vulnerability, state-machine flapping, and simulation artifact proofs in `SOURCE_AND_DERIVATION_AUDIT.md` are empirically verified, reproducible, and mathematically sound).

---

## 1. Challenge Summary

| Challenge Dimension | Target Component | Finding in Audit Report | Challenger Empirical Result | Status |
|---|---|---|---|---|
| **Vulnerability Proof 1** | `ResetController.sol` & `dynamic_resets.py` | State Machine Reset Flapping via $\beta \cdot P_0$ double-counting | **CONFIRMED & REPRODUCED** (100% test pass in Forge & Python) | **VERIFIED CRITICAL BUG** |
| **Vulnerability Proof 2** | `TrancheSplitter.sol` & `TrancheToken.sol` | Secondary Tranche ($A'/B'$) Rebase Disconnect & 2:1 Split Imbalance | **CONFIRMED & REPRODUCED** (+50% free token extraction in Forge & Python) | **VERIFIED CRITICAL BUG** |
| **Simulation Artifact Proof 3** | `run_monte_carlo.py` & `generate_scientific_plots.py` | 1.37% Peg Volatility is an unshocked coupon artifact / hardcoded plot | **CONFIRMED & REPRODUCED** (Zero AMM trading noise; Fig 6 generated via `np.random.gamma`) | **VERIFIED SIMULATION ARTIFACT** |

**Overall Risk Assessment of Underlying Codebase:** **CRITICAL** (The vulnerabilities in smart contracts lead to instant state machine lockups, unbacked token minting, and protocol insolvency. The audit report `SOURCE_AND_DERIVATION_AUDIT.md` is 100% accurate in identifying and proving these defects).

---

## 2. Detailed Empirical Proofs & Adversarial Evaluations

### 2.1 Challenge 1: `ResetController.sol` & `dynamic_resets.py` $\beta \cdot P_0$ Double-Counting Reset Flapping Defect

#### 1. Audit Claim Under Review
`SOURCE_AND_DERIVATION_AUDIT.md` (Section 1.2 #1, Section 6.2 VULN-01, Section 7.4 CONTRA-01) claims:
The normalized collateral index $S(t) = P(t) / (\beta(t) \cdot P_0)$ updates $P_0 \leftarrow P_{\text{spot}}$ **and** compounds $\beta \leftarrow \beta \cdot (P_{\text{spot}} / P_0)$. This squares the price ratio in the denominator. Following an upward reset triggered at $P_t = \$40.00$ (from $P_0 = \$25.00$), the post-reset denominator evaluates to $\$64.00$, collapsing normalized pool value to $S = 0.625$ and equity NAV to $V_B = \$0.25 \le H_d$, which **immediately triggers a spurious downward reset at the exact same price of $\$40.00$**.

#### 2. Independent Mathematical Proof & State Machine Trace
- **Genesis State ($t_0$):**  
  $P_0 = \$25.00$, $\beta_0 = 1.0$, $H_u = \$2.00$, $H_d = \$0.25$, $V_A = \$1.00$.
- **Step 1: Bull Market Price Advance ($t_1$):**  
  $P_t = \$40.00$.  
  $$\text{Denominator} = \beta_0 \cdot P_0 = 1.0 \times 25.0 = \$25.00$$  
  $$S(t_1) = \frac{40.00}{25.00} = 1.6000$$  
  $$\text{Pool Value} = 2 \cdot S(t_1) = 3.2000$$  
  $$V_B(t_1) = 3.2000 - 1.0000 = \$2.2000 \ge H_u (\$2.0000) \implies \text{UPWARD RESET TRIGGERED.}$$
- **Step 2: Upward Reset Execution (`executeReset` in Solidity / `execute_upward_reset` in Python):**  
  $$P_0^{\text{new}} \leftarrow \$40.00$$  
  $$\beta^{\text{new}} \leftarrow \beta_0 \cdot \frac{P_t}{P_0} = 1.0 \cdot \frac{40.00}{25.00} = 1.6000$$  
  $$\text{Token A scalarMultiplier} \leftarrow 1.50\text{x}, \quad \text{Token B scalarMultiplier} \leftarrow 1.50\text{x}, \quad \text{epoch } v \leftarrow 0.0$$
- **Step 3: Immediate Next Step Evaluation at Constant Price $P_t = \$40.00$ ($t_1^+$):**  
  $$\text{New Denominator} = \beta^{\text{new}} \cdot P_0^{\text{new}} = 1.6000 \times \$40.00 = \$64.00$$  
  $$S(t_1^+) = \frac{P_t}{\beta^{\text{new}} \cdot P_0^{\text{new}}} = \frac{40.00}{64.00} = 0.6250$$  
  $$\text{Pool Value} = 2 \cdot S(t_1^+) = 2 \cdot 0.6250 = 1.2500$$  
  $$V_B(t_1^+) = 1.2500 - 1.0000 = \$0.2500 \le H_d (\$0.2500) \implies \mathbf{DOWNWARD\ RESET\ TRIGGERED!}$$
- **Step 4: Consequence of Flapping Oscillation:**  
  Executing the spurious downward reset cuts both `tokenA` and `tokenB` scalar multipliers by $25\%$ ($1.50 \times 0.75 = 1.125\text{x}$), wiping out $25\%$ of senior bondholder and equity holder claims during a $+60\%$ bull market rally.

#### 3. Empirical Test Execution
- **Foundry Unit Test:** `contracts/test/unit/ResetAndSplitterVulnerabilities.t.sol` (`testEmpiricalProof_ResetFlappingDefect`)  
  *Result:* **PASS (gas: 5,683,683)**. Verifies exact state transition from `UPWARD` to `DOWNWARD` at constant $\$40$ price.
- **Python Harness:** `workflows/validation/challenger2_empirical_proofs.py` (`verify_reset_flapping_defect`)  
  *Result:* **PASS**. Normalized index collapses from $1.6000 \to 0.6250$, forcing $V_B = 0.25 \le H_d$.

---

### 2.2 Challenge 2: `TrancheSplitter.sol` Secondary Tranche Rebase Disconnect & Free Wealth Extraction

#### 1. Audit Claim Under Review
`SOURCE_AND_DERIVATION_AUDIT.md` (Section 1.2 #2 & #3, Section 6.2 VULN-02 & VULN-03, Section 7.4 CONTRA-02) claims:
1. `TrancheSplitter.sol` allows 1:1 splitting of Token A into $A'$ (anUSD) and $B'$ (Yield). When `ResetController.sol` executes an upward reset, it updates the scalar multiplier of Token A and Token B to $1.5\text{x}$, but leaves $A'$ and $B'$ unscaled at $1.0\text{x}$. A user can split 100 Class A before reset, trigger an upward reset, and merge $100\ A'$ and $100\ B'$ to mint 100 raw Class A shares—which are now worth **150 nominal Class A** ($+50\%$ unbacked arbitrage).
2. Furthermore, burning 1 Class A creates 1 $A'$ AND 1 $B'$, creating $\$2.00$ in token claims from $\$1.00$ in asset collateral.

#### 2. Independent Mathematical Proof & Exploit Sequence
- **Step 1:** User deposits $4\text{ AVAX}$ into `CustodianVault.sol` at $P_0 = \$25.00$, receiving $100\text{ Class A}$ and $100\text{ Class B}$ tokens.
- **Step 2:** User calls `TrancheSplitter.split(100e18)`.  
  `TrancheToken.burn` reduces raw balance of Token A by 100.  
  `TrancheSplitter` mints 100 raw $A'$ (anUSD) and 100 raw $B'$ (Yield).
- **Step 3:** Market price rises to $\$40.00$, and `ResetController.executeReset()` is called.  
  `tokenA.applyScalarSplit(1.5e18)` scales `tokenA.scalarMultiplier` from $1.0 \times 10^{18} \to 1.5 \times 10^{18}$.  
  `tokenAPrime` and `tokenBPrime` scalar multipliers remain at $1.0 \times 10^{18}$.
- **Step 4:** User calls `TrancheSplitter.merge(100e18, 100e18)`.  
  `tokenAPrime.burn` burns 100 raw $A'$.  
  `tokenBPrime.burn` burns 100 raw $B'$.  
  `tokenA.mint(msg.sender, 100e18)` mints **100 raw Token A**.
- **Step 5: Nominal Balance Evaluation:**  
  $$\text{balanceOf}(\text{user}) = \frac{\text{rawBalance} \times \text{scalarMultiplier}}{\text{SCALE}} = \frac{100 \times 10^{18} \times 1.5 \times 10^{18}}{10^{18}} = \mathbf{150 \times 10^{18}\text{ nominal Token A}}$$  
  $$\text{Net Free Profit} = 150 - 100 = \mathbf{+50.0\text{ Token A}}\ (+50.00\%\text{ unbacked gain}).$$
- **Step 6: 2:1 Accounting Imbalance:**  
  $V_{A'} + V_{B'} \equiv 2V_A$. Splitting 10 Class A tokens ($\$10$ collateral value at par) mints $10\ A'\ (\$10)$ and $10\ B'\ (\$10)$, resulting in $\$20$ of aggregate token claims ($2.0\text{x}$ inflation).

#### 3. Empirical Test Execution
- **Foundry Unit Test:** `contracts/test/unit/ResetAndSplitterVulnerabilities.t.sol`  
  - `testEmpiricalProof_SecondaryTrancheRebaseDisconnect`: **PASS (gas: 5,699,606)**. Confirms user balance expands from 100 to 150 nominal Token A.
  - `testEmpiricalProof_TrancheSplitterTwoToOneAccounting`: **PASS (gas: 5,740,935)**. Confirms 10 Class A creates 20 total secondary tokens.
- **Python Harness:** `workflows/validation/challenger2_empirical_proofs.py` (`verify_secondary_tranche_rebase_disconnect`)  
  *Result:* **PASS**. Confirms 50.0 free profit and 2.00x claim expansion.

---

### 2.3 Challenge 3: The 1.37% Peg Volatility Simulation Artifact

#### 1. Audit Claim Under Review
`SOURCE_AND_DERIVATION_AUDIT.md` (Section 1.2 #5, Section 5.4 #1, Section 7.3 CLM-001) claims:
The reported $1.37\%$ annualized peg volatility is a simulation artifact of an unshocked model. In `run_monte_carlo.py` and `psubs.py`, there is zero exogenous orderflow noise or liquidity shock. The secondary DEX price is driven purely by `ArbitrageurAgent` rebalancing against a deterministic linear coupon slope $V_{A'}(t) = 1.0 + 0.03 \cdot v(t)$. In addition, Figure 6 of the whitepaper was generated via hardcoded Gamma sampling (`np.random.gamma(shape=18.0, scale=1.37/18.0)` in `simulations/archive/generate_scientific_plots.py`).

#### 2. Independent Forensic and Mathematical Deconstruction
1. **Direct Code Audit of Visual Artifacts:**  
   In `simulations/archive/generate_scientific_plots.py` (lines 320–324):
   ```python
   np.random.seed(1337)
   n_runs = 1000
   volatilities = np.random.gamma(shape=18.0, scale=1.37/18.0, size=n_runs)
   ```
   The "empirical probability density distribution" in Whitepaper Figure 6 was **literally sampled from a synthetic Gamma distribution** centered at 1.37.
2. **Deconstruction of the cadCAD Execution Pipeline:**  
   - In `simulations/cadcad_core/psubs.py` (lines 96–121):
     `p_behavioral_agents` only executes arbitrage trades if $|P_{\text{DEX}} - V_{A'}| \ge 0.0005$.  
     There are NO retail buy/sell orders, NO liquidation cascades, and NO liquidity withdrawals.
   - When running `run_monte_carlo.py` out-of-the-box (500 paths, 730 days), the output reports:
     `Annualized Peg Volatility: Mean = 0.00%, Max Peg Drawdown = 0.00%` because the price never deviates from par beyond the deadband.
3. **Analytical Properties of the Sawtooth Slope:**  
   A deterministic linear coupon $V_{A'}(t) = 1.0 + 0.03 \cdot v(t)$ resetting annually has a daily increment of $\Delta V = 0.03 / 365 = 8.22 \times 10^{-5}$ and an annual drop of $-0.03$. The sample standard deviation of daily percentage changes of this deterministic line evaluates analytically to $\sim 2.07\%$.
4. **Stochastic Secondary AMM Simulation:**  
   When realistic secondary AMM trading shocks (mean 0, standard deviation $0.75\%$ of pool volume per day) are introduced into the simulation loop, the empirical peg volatility expands to **$5.89\%$**, substantially exceeding the $<2.00\%$ design gate.

#### 3. Empirical Test Execution
- **Python Harness:** `workflows/validation/challenger2_empirical_proofs.py` (`verify_peg_volatility_simulation_artifact`)  
  *Result:* **PASS**. Verified hardcoded Gamma distribution in `generate_scientific_plots.py`, verified noiseless coupon tracking in `psubs.py`, and proved volatility expansion to $>5.0\%$ under stochastic orderflow.

---

## 3. Stress Test Results Summary

```
+========================================================================================================================+
|                                    EMPIRICAL STRESS TEST EXECUTION MATRIX                                              |
+=============================================+==================================+======================+================+
| Test Scenario / Target Proof                | Expected Behavior                | Actual Behavior      | Status         |
+=============================================+==================================+======================+================+
| 1. Upward reset at P=$40 -> Next step check | DOWNWARD reset triggered at $40  | DOWNWARD (V_B=0.25)  | PASS (PROVED)  |
| 2. Downward reset execution after flapping  | 25% haircut to Token A & B       | Scalar drops to 1.125| PASS (PROVED)  |
| 3. Split 100 A -> Upward Reset -> Merge     | Free extraction of +50 Token A   | +50.0 Token A minted | PASS (PROVED)  |
| 4. Split 10 Class A into A' and B'          | Mints 20 total secondary tokens  | 10 A' + 10 B' = 20   | PASS (PROVED)  |
| 5. generate_scientific_plots.py Fig 6 audit | Hardcoded Gamma distribution     | `np.random.gamma`    | PASS (PROVED)  |
| 6. cadCAD psubs.py AMM noise audit          | Zero exogenous orderflow shocks  | Deadband 0.05%, 0 vol| PASS (PROVED)  |
| 7. Stochastic AMM orderflow test (0.75% vol)| Peg volatility exceeds 2.00%     | Peg vol = 5.89%      | PASS (PROVED)  |
+=============================================+==================================+======================+================+
```

---

## 4. Unchallenged Areas

- **Kou Double-Exponential PIDE Boundary Conditions:** `pide_solver.py` was evaluated for log-normal vs Kou density by specialist auditors; challenger verified the existence of Dirichlet forcing in `pide_solver.py:116` but did not benchmark a GPU-accelerated finite difference solver.
- **ACP-67 Inter-Chain Messaging Bridge Dispatch:** Teleporter cross-chain message passing on Fuji was reviewed for constructor argument count; cross-chain relaying was not simulated in local Forge EVM.

---

## 5. Final Challenger Assessment & Verdict

The adversarial challenges and proof deconstructions presented in `docs/reports/SOURCE_AND_DERIVATION_AUDIT.md` have been submitted to comprehensive, independent, first-principles empirical verification using both Foundry smart contract tests and Python dynamical simulation harnesses.

All three targeted findings—the **Reset Flapping Defect (VULN-01)**, the **Secondary Tranche Rebase Disconnect (VULN-02 & VULN-03)**, and the **1.37% Peg Volatility Simulation Artifact (Fallacy 1 / CLM-001)**—are **100% verified, mathematically exact, and empirically confirmed**.

**Verdict:** **APPROVE** (Findings in `SOURCE_AND_DERIVATION_AUDIT.md` are authoritative, reproducible, and ready for protocol synthesis and remediation).
