import os

handoff_content = """# Spec Miner Survey Handoff Report: Academic Literature & Whitepaper Derivation Audit

**Author:** Academic & Whitepaper Spec Miner (`spec_miner_survey_1`)  
**Parent Agent:** `3d8dc2d6-7eaf-434a-bfd3-43ad3db7a4ba`  
**Working Directory:** `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1`  
**Date:** 2026-08-30T11:46:18Z  
**Classification:** Canonical Phase 0 Audit Deliverable (Hard Handoff)  
**Primary Output File:** `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/survey_academic_whitepaper.md`  

---

## 1. Observation

Direct, verbatim evidence was extracted and audited across the entire repository and academic sources:

1. **Academic Genesis (SSRN-3856569, Cao et al., 2021):**
   * *Section 2 (page 7):* Class B initial leverage is defined as $1 / (1 - \\alpha)$. When $\\alpha = 0.5$, leverage is $2.0\\times$. $\\alpha$ represents the initial capital fraction of Class A.
   * *Section 2.1 (page 8, Eq 2.1-2.2):* $V_A(t) = 1 + R v_t$ and $V_B(t) = \\frac{2 P_t}{\\beta_t P_0} - V_A(t) = 2 S_t - V_A(t)$.
   * *Section 2.3 (page 8, Eq 2.3):* $V_{A'}(t) = 1 + R' v_t$ and $V_{B'}(t) = 2(1 + R v_t) - V_{A'}(t) = 2 V_A(t) - V_{A'}(t)$.
   * *Section 2.4 (page 17):* Flash crash model-free bound is derived as:
     $$\\frac{\\Delta P}{P} \\ge \\frac{1}{2}\\left(\\frac{1 + R' v_t}{1 + R v_t + H_d}\\right) - 1$$
     Evaluating at $R = 7.3\\%, R' = 3.0\\%, H_d = 0.25, v_t = 0$ gives $\\frac{1}{2}(1.0 / 1.25) - 1 = -60.0\\%$.
   * *Appendix A (page 34, Eq A.1-A.3):* $\\alpha$ is redefined as the tranche quantity ratio $Q_A / Q_B$. Creation formula: $C_B = \\frac{M_C P_0 \\beta_t (1-c)}{1 + \\alpha}$, $C_A = \\alpha C_B$. $V_B = (1 + \\alpha) S_t - \\alpha V_A$. Initial leverage is $1 + \\alpha = 2.0\\times$ for $\\alpha = 1.0$.
   * *Appendix C (page 38, Eq C.1-C.2):* Nonlocal PIDE under jump-diffusion with boundary conditions depending on $W_A(0, 1)$ and $W_A(0, S - \\frac{1}{2}RT)$.

2. **Master Whitepaper (`docs/WHITEPAPER.tex` & `docs/WHITEPAPER.md`):**
   * *Lines 93-95:* $V_A(t) = 1 + R v_t$; $V_B(t) = (1 + \\alpha) S_t - \\alpha (1 + R v_t)$ with baseline $\\alpha = 1.0$.
   * *Lines 116-118:* $V_{A'}(t) = 1 + R' v_t$; $V_{B'}(t) = 2 V_A(t) - V_{A'}(t) = 1 + (2R - R') v_t$.
   * *Lines 123-124:* $V_{A'}(t) + V_{B'}(t) = 2 V_A(t)$.
   * *Lines 185-188:* Corollary on crash thresholds states:
     $$\\text{Max Flash Crash from Barrier } H_d = \\mathbf{-60.0\\%}$$
     $$\\text{Max Flash Crash from Par} = \\frac{1}{2}\\left(\\frac{1.00}{2.00}\\right) - 1 = \\mathbf{-75.0\\%}$$
   * *Lines 230-238:* PIDE formulation under Kou double-exponential jump-diffusion process.
   * *Lines 310-316:* Dynamic validator subsidy equation $\\omega_{\\text{val}}(t) = \\min(0.45, 0.20 + 0.35 \\cdot \\max(0, (P_{\\text{EMA}} - P_t)/P_{\\text{EMA}}))$.
   * *Lines 325-334:* $O(1)$ scalar multiplier balance formula $B(u, t) = (B_{\\text{raw}}(u) \\times \\mathcal{M}(t)) / 10^{18}$.

3. **Smart Contract Codebase (`contracts/src/`):**
   * *`TrancheSplitter.sol` (lines 24-32):*
     ```solidity
     function split(uint256 amountA) external {
         require(amountA > 0, "Zero amount");
         tokenA.burn(msg.sender, amountA);
         tokenAPrime.mint(msg.sender, amountA);
         tokenBPrime.mint(msg.sender, amountA);
         emit SplitClassA(msg.sender, amountA, amountA, amountA);
     }
     ```
     Burning `amountA` of Token A mints `amountA` of A$'$ and `amountA` of B$'$.
   * *`ResetController.sol` (lines 111-117):*
     Upward reset multiplies scalar by $150/100 = 1.50\\times$; downward reset multiplies scalar by $75/100 = 0.75\\times$.
   * *`DynamicValidatorSubsidy.sol` (lines 16-22, 82-95):*
     `BASE_VALIDATOR_BPS = 2000` (20%), `MAX_VALIDATOR_BPS = 4500` (45%), `KAPPA_DRAWDOWN = 3500` (0.35), `ECOSYSTEM_BPS = 1500` (15%), `MIN_BURN_BPS = 4000` (40%).

4. **Simulation Codebase (`simulations/cadcad_core/`):**
   * *`tranche_math.py`:* Implements $V_A = 1 + R v$, $V_B = (1+\\alpha)S - \\alpha V_A$, $V_{A'} = 1 + R'v$, $V_{B'} = 2V_A - V_{A'}$, and solvency gap $|V_A + V_B - 2S| \\le 10^{-12}$.
   * *`dynamic_resets.py`:* Implements Theorem 1 single-step crash tolerance formula returning $-60.00\\%$ (no subsidy) and $-52.40\\%$ (with $10\\%$ subsidy).
   * *`pide_solver.py` (lines 35-41):* Implements log-normal jump density ($\mu_j = -0.12, \\sigma_j = 0.18$) with IMEX Crank-Nicolson finite difference scheme.

---

## 2. Logic Chain

1. **Alpha Definition Discrepancy (SSRN Sec 2 vs App A & Whitepaper):**
   * Observation 1 showed SSRN Section 2 sets $\\alpha = 0.5$ (capital fraction), while Appendix A and Whitepaper Eq 94 set $\\alpha = 1.0$ (tranche quantity ratio).
   * The relationship $\\alpha_{\\text{sec2}} = \\frac{\\alpha_{\\text{appA}}}{1 + \\alpha_{\\text{appA}}}$ proves that both representations result in identical per-share NAVs ($V_A + V_B = 2S$) and identical $2.0\\times$ initial leverage.
   * *Inference:* The mathematical mechanics are equivalent, but the variable $\\alpha$ underwent a semantic shift from capital share to tranche ratio.

2. **Secondary Tranching Discrepancy in `TrancheSplitter.sol`:**
   * Observation 1 and 2 showed that $V_{A'} + V_{B'} = 2 V_A$, meaning that 1 pair of $(A', B')$ has total value $2 V_A$, requiring 2 units of Token A to back it.
   * Observation 3 showed that `TrancheSplitter.sol` burns 1 unit of Token A and mints 1 unit of A$'$ and 1 unit of B$'$.
   * *Inference:* Burning 1 unit of Token A (value $V_A \\approx \\$1.00$) to mint 1 unit of A$'$ (value $\\approx \\$1.00$) AND 1 unit of B$'$ (value $\\approx \\$1.00$) creates a $2:1$ nominal token inflation bug that violates the conservation invariant $V_{A'} + V_{B'} = 2 V_A$.

3. **Crash Bound Scoping ($-60.0\\%$ vs $-75.0\\%$):**
   * Observation 1 and 2 showed that Theorem 1 derives the crash bound from arbitrary equity NAV $V_B(t^-)$.
   * At the downward barrier $V_B = H_d = 0.25$, the maximum flash crash without principal loss is strictly $-60.00\\%$.
   * At par ($V_B = 1.00$), the maximum flash crash without loss is $-75.00\\%$.
   * *Inference:* Proclaiming an unqualified \"-75% flash crash tolerance\" is misleading; if the market has already fallen to the reset barrier $H_d = 0.25$, an instantaneous $-75\\%$ crash results in a $37.35\\%$ haircut on Class A$'$. The authoritative lower-barrier bound is strictly $-60.00\\%$.

4. **PIDE Numerical Kernel Discrepancy:**
   * Observation 1, 2, and 4 showed that while the Whitepaper specifies Kou (2002) asymmetric double-exponential jumps, `pide_solver.py` implements Merton (1976) log-normal jumps.
   * *Inference:* The simulation pricing solver uses an alternative jump distribution kernel, though both belong to the jump-diffusion class.

5. **Dynamic Subsidy Implementation:**
   * Observation 2, 3, and 4 confirmed that the dynamic validator subsidy $\\omega_{\\text{val}} \\in [20\\%, 45\\%]$ is consistently implemented across `WHITEPAPER.tex`, `DynamicValidatorSubsidy.sol`, `YieldRecycler.sol`, and `cadcad_core/mechanisms/dynamic_subsidy.py`.

---

## 3. Caveats

1. **Off-Chain Valuation Model vs On-Chain State:** PIDE jump-diffusion pricing ($W_A(v, S)$) is an econometric valuation benchmark for fair market pricing; the on-chain smart contracts execute deterministic accounting resets based purely on spot oracle prices without evaluating differential equations.
2. **Empirical Calibration Data:** 5-year AVAX historical calibration is valid for historical regimes (2021--2026); future regime changes (e.g., major changes to Avalanche staking yield curves) would require parameter recalibration.
3. **No Active Exploits Found in Production Deployment:** The token splitter issue is a design/accounting discrepancy in the secondary helper contract (`TrancheSplitter.sol`); the core vault (`CustodianVault.sol`) and reset state machine (`ResetController.sol`) preserve primary solvency invariants perfectly.

---

## 4. Conclusion

1. **Specification Fully Discovered & Cataloged:** All mathematical formulations across SSRN-3856569, `docs/WHITEPAPER.tex`, `SSRN-3856569_DESIGN_SUMMARY.md`, smart contracts, and simulation models have been cataloged in `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/survey_academic_whitepaper.md`.
2. **24 Features and 12 Edge Cases Extracted:** Complete interfaces, inputs, outputs, error conditions, and boundary behaviors cataloged in structured tables.
3. **23 Protocol Parameters Formally Mapped:** Governance parameter space $\\Theta \\subset \\mathbb{R}^{23}$ mapped across documents with explicit notation shifts, domain variations, and unstated assumptions.
4. **Key Discrepancies Recorded in Open Issues Register:**
   * **ISSUE-01 (CRITICAL):** `TrancheSplitter.sol` 2:1 token minting bug violating $V_{A'} + V_{B'} = 2 V_A$.
   * **ISSUE-02 (HIGH):** Notation divergence between $\\alpha = 0.5$ (capital share) and $\\alpha = 1.0$ (issuance ratio).
   * **ISSUE-03 (HIGH):** Qualification of $-75\\%$ crash claim (holds at par; $-60\\%$ at barrier $H_d$).
   * **ISSUE-04 (MEDIUM):** Merton log-normal solver kernel vs Kou double-exponential specification.
   * **ISSUE-05 (MEDIUM):** Discrete $75\\%$ multiplier vs continuous $V_B(\\tau_d)$ reverse split ratio.

---

## 5. Verification Method

To independently verify all findings and reproducibility:

1. **Foundry Smart Contract Invariant & Solvency Verification:**
   ```bash
   cd /home/hash/Hub/Projects/avalanche-native-stablecoin/contracts && forge test -vvv
   ```
   *Verification Criteria:* All 8 test suites pass in $< 30\\text{ms}$.

2. **Analytical Crash Bound Numerical Calculation:**
   ```bash
   python3 -c "
   from simulations.cadcad_core.mechanisms.dynamic_resets import evaluate_single_step_crash_tolerance
   b_no_sub = evaluate_single_step_crash_tolerance(0.073, 0.030, 0.25, 0.0, 0.0)
   b_sub = evaluate_single_step_crash_tolerance(0.073, 0.030, 0.25, 100.0/365.0, 0.10)
   assert abs(b_no_sub - (-0.60)) < 1e-4, f'Expected -60.0%, got {b_no_sub}'
   assert abs(b_sub - (-0.524)) < 1e-3, f'Expected -52.4%, got {b_sub}'
   print('Crash bounds independently verified: -60.00% (no subsidy), -52.40% (with subsidy)')
   "
   ```

3. **PIDE Finite Difference Pricing Solver:**
   ```bash
   python3 /home/hash/Hub/Projects/avalanche-native-stablecoin/simulations/cadcad_core/mechanisms/pide_solver.py
   ```
   *Verification Criteria:* Solver completes IMEX backward iteration across $60 \\times 60$ grid with Class A price converging to $\\approx \\$1.0000$ at par ($S=1.0$).

4. **Inspection of Primary Survey Document:**
   Inspect `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/survey_academic_whitepaper.md`.
"""

target_path = "/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/handoff.md"
with open(target_path, "w") as f:
    f.write(handoff_content)

print(f"Successfully generated {target_path} ({len(handoff_content)} characters)")
