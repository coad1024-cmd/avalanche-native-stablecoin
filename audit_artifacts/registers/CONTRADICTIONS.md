# Contradictions & Open Issues Register

> **Source:** Extracted from [`SOURCE_AND_DERIVATION_AUDIT.md`](../reports/SOURCE_AND_DERIVATION_AUDIT.md) Section 7.4  
> **Last Updated:** 2026-08-30  
> **Status:** Phase 0 — Unverified Research Artifact  
> **Rule:** Entries are immutable. New contradictions are appended; existing entries are never silently modified.  

---

| Issue ID | Severity | Subsystem | Verbatim Code Locations | Exact Discrepancy & Root Cause |
|:---:|:---:|:---:|:---|:---|
| **CONTRA-01** | **CRITICAL** | Smart Contracts | `ResetController.sol:85, 109`<br>`dynamic_resets.py:31` | **$\beta \cdot P_0$ Double-Counting Reset Flapping Bug:** Denominator $S = P_t / (\beta \cdot P_0)$ updates $P_0 \leftarrow P_t$ AND $\beta \leftarrow \beta \cdot (P_t / P_0)$. This squares the price ratio. An upward reset at $\$40$ immediately triggers a downward reset at $\$40$ in the next block. |
| **CONTRA-02** | **CRITICAL** | Smart Contracts | `TrancheSplitter.sol:26-29`<br>`ResetController.sol:112` | **Secondary Tranche Rebase Disconnect:** `TrancheSplitter` splits 1 A into 1 A$'$ and 1 B$'$. When A rebases to $1.5\text{x}$, A$'$ and B$'$ do not rebase. Merging 100 A$'$ and 100 B$'$ mints 100 raw A worth 150 nominal A (+50% free unbacked profit). |
| **CONTRA-03** | **HIGH** | Control / Gates | `claims.yaml:CLM-006` ($\zeta = 1.42$)<br>`WHITEPAPER.tex:573` ($\zeta = 17.03$) | **Damping Ratio Contradiction:** Machine-verifiable claims specify $\zeta = 1.42$, while Whitepaper, Tooling Audit, and Adversarial Study specify $\zeta = 17.03$. |
| **CONTRA-04** | **HIGH** | Simulation Math | `pide_solver.py:35-41`<br>`WHITEPAPER.tex:Sec 5.3` | **PIDE Jump Density Mismatch:** Whitepaper specifies Kou asymmetric double-exponential jump density ($p, \eta_1, \eta_2$), but `pide_solver.py` implements Merton log-normal jump density ($\mu_j, \sigma_j$). |
| **CONTRA-05** | **HIGH** | Marketing / Math | `WHITEPAPER.tex:Sec 4`<br>`claims.yaml:CLM-002` | **Crash Bound Scope Misrepresentation:** Claims cite "-75% flash crash tolerance" unconditionally. Theorem 1 proves tolerance from barrier $H_d = 0.25$ is strictly $-60.00\%$; $-75.00\%$ applies strictly from par ($S=1.0$). |
| **CONTRA-06** | **HIGH** | Simulation Code | `controller_isolation.py:53, 92` | **Liquidity Cancellation & Price Drop Clamping:** Code clamps $P_{\text{dex}}$ drop to $-15\%$ and cancels liquidity $L$ in `controller_flow = (L * 0.8 * delta_r / L) * dt`, forcing identical outputs across all pools. |
| **CONTRA-07** | **MEDIUM** | Smart Contracts | `ResetController.sol:112, 115` | **Hardcoded Symmetrical Reset Multipliers:** Solidity hardcodes 150/100 and 75/100 scalar multipliers applied symmetrically to both `tokenA` and `tokenB`, haircutting Class A on downward resets without principal payout. |
| **CONTRA-08** | **MEDIUM** | Smart Contracts | `ChainlinkOracleAdapter.sol:30`<br>`WHITEPAPER.tex:Sec 11.2` | **Oracle Staleness Heartbeat Divergence:** Solidity initializes `maxStalenessSeconds = 3600` (1 hour), divergent from the 300-second (5 minute) whitepaper standard. |
| **CONTRA-09** | **MEDIUM** | Tokenomics | `DynamicValidatorSubsidy.sol:19`<br>`dynamic_subsidy.py:48` | **Burn Allocation Floor Divergence:** `DynamicValidatorSubsidy.sol` enforces `MIN_BURN_BPS = 4000` (40.0% floor), while `dynamic_subsidy.py` enforces a 20.0% floor. |
| **CONTRA-10** | **MEDIUM** | Smart Contracts | `CustodianVault.sol:111, 130` | **Zero Mint/Redeem Fees in Bytecode:** `depositAndMint` and `redeemAndBurn` charge 0 bps fee, omitting the 10 bps fee revenue intended for ACP-67 yield recycling. |
| **CONTRA-11** | **MEDIUM** | Verification | `verify_contractual_gates.py:34-41` | **Circular Self-Referential Validation:** Verification script merely checks if `gates.yaml` contains the string `"status: PASSED"`. |
| **CONTRA-12** | **LOW** | Smart Contracts | `TrancheToken.sol:168-173` | **1-Wei Dust Loss & Zero-Transfer Exploit:** Truncation in `(amount * SCALE) / scalarMultiplier` permanently destroys 1 wei per transfer. |
