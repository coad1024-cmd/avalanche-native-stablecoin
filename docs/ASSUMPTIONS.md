# Ledger of Modeling Assumptions & Empirical Validity Regimes

**Governing Standard:** BCRG Mathematical & Economic Modeling Canon  
**Owner:** Bonding Curve Research Group (BCRG)  
**Project:** Avalanche Native Stablecoin (`anUSD`)  
**Status:** Canonical Ledger (Calibrated against 5-Year Avalanche Telemetry) · August 2026  

---

## 1. Market Environment & Empirical Stochasticity Assumptions

### A01: Collateral Price Follows a Merton-Kou Double-Exponential Jump-Diffusion Process
* **Formal Mathematical Statement:** The spot price of $AVAX$ collateral $P(t)$ evolves on filtered probability space $(\Omega, \mathcal{F}, (\mathcal{F}_t)_{t \ge 0}, \mathbb{Q})$ as:
  $$\frac{dP(t)}{P(t^-)} = (r - q - \lambda \zeta) dt + \sigma dW(t) + (e^Y - 1) dN(t)$$
  where $Y$ has asymmetric double-exponential density $f_Y(y) = p \eta_1 e^{-\eta_1 y} \mathbf{1}_{\{y \ge 0\}} + (1-p) \eta_2 e^{\eta_2 y} \mathbf{1}_{\{y < 0\}}$.
* **Empirical Calibration:** Calibrated against 1,826 daily price observations of AVAX/USD (2021--2026):
  * Continuous annualized volatility: $\sigma = 89.86\%$
  * Poisson jump intensity: $\lambda = 2.40\text{ jumps/year}$
  * Upward jump probability: $p = 0.40$, rate $\eta_1 = 3.50$ (mean upward jump $+28.57\%$)
  * Downward jump rate: $\eta_2 = 2.00$ (mean downward jump $-50.00\%$)
* **Breakdown Regime:** Prolonged network-wide halt (> 24 hours) or total off-chain centralized exchange liquidity evaporation.
* **Contingency Action:** Circuit breaker pause activated on oracle staleness $\tau_{\text{heart}} > 300\text{s}$.

### A02: Liquid Staking Cash Flow Continuity & Consensus Integrity
* **Formal Mathematical Statement:** Staked collateral token ($sAVAX$) continuously generates a strictly positive, non-negative staking dividend $q \in [4.5\%, 8.0\%]$ derived from Avalanche Primary Network consensus rewards.
* **Empirical Grounding:** Calibrated against Benqi ($sAVAX$) and GoGoPool ($ggAVAX$) on-chain staking data. Avalanche Snowman consensus does not employ slashing for offline nodes, eliminating validator slashing risk.
* **Breakdown Regime:** Hard-fork consensus modification altering Avalanche Primary Network staking reward curves ($ARR$).
* **Contingency Action:** Dynamic recalculation of gross yield waterfall in `YieldRecycler.sol`.

### A03: Concentrated AMM Liquidity Depth on Avalanche C-Chain
* **Formal Mathematical Statement:** Secondary market trading liquidity on DEXs (Trader Joe v2.1 / Uniswap v3) maintains at least $\$20\text{M}$ effective liquidity within a $\pm 0.50\%$ price band around $\$1.00$.
* **Empirical Grounding:** Initial liquidity bootstrapped via ACP-67 Sovereign L1 & Ecosystem Grants pool ($\omega_{\text{l1}} = 15.0\%$).
* **Breakdown Regime:** Severe DEX liquidity drain due to extreme market-wide deleveraging.
* **Contingency Action:** Reflexer-style PI controller automatically elevates benchmark coupon $R'(t)$ up to $+5.00\%$, creating strong economic incentives for market buyers to purchase discounted `anUSD`.

---

## 2. Mechanism & Structural Dynamics Assumptions

### A04: Zero-Friction Instantaneous Share Restructuring ($O(1)$ Complexity)
* **Formal Mathematical Statement:** Dynamic resets at $H_u = \$2.00$ and $H_d = \$0.25$ execute in $O(1)$ computational complexity without state loops across individual user accounts.
* **Implementation:** Verified in `TrancheToken.sol` using virtual share accounting ($\text{RealBalance} = \text{VirtualShares} \times \beta(t)$). Total gas cost per reset is strictly bounded below $85,000\text{ gas}$.

### A05: Model-Free Catastrophic Crash Invariance (Theorem 1)
* **Formal Mathematical Statement:** For any instantaneous single-step price decline $\Delta P / P \ge -60.00\%$ from the lower barrier $H_d = 0.25$ (and $\ge -75.00\%$ from par), Class A$'$ (`anUSD`) experiences exactly **zero principal haircut**:
  $$V_{A'}(t^+) = V_{A'}(t^-) = \$1.0000$$
* **Analytical Proof:** Formally proven in Whitepaper Section 4 via residual pool conservation and boundary substitutions.

### A06: Bear-Market Coupon Subsidy ($\tilde{R} = 10.00\%$) Equity Retention
* **Formal Mathematical Statement:** Transferring an annual coupon subsidy $\tilde{R} = 10.00\%$ from Class A to Class B during downward reverse splits establishes an economic floor that retains speculative equity demand during prolonged bear regimes.

---

## 3. Cryptographic, Oracle & MEV Security Assumptions

### A07: Sub-Second Consensus Finality & Reorg Immunity
* **Formal Mathematical Statement:** Avalanche Snowman consensus achieves deterministic transaction finality in $< 1.5$ seconds without probabilistic reorg risk.
* **Security Implication:** Prevents multi-block chain reorganizations and long-range MEV reset manipulation attacks.

### A08: 1-Block Commit-Settlement Delay Lock Resistance
* **Formal Mathematical Statement:** When spot oracle price enters a $\pm 1.50\%$ proximity band around $H_u$ or $H_d$, user mints and redemptions enter a mandatory 1-block delay lock.
* **Security Result:** Maximum Profitable Manipulation Cost (MPMC) exceeds $\$45\text{M}$, rendering atomic flash-loan reset front-running attacks unprofitable ($\mathbb{E}[\Pi_{\text{attack}}] < -\$3.2\text{M}$).

### A09: Multi-Oracle Cross-Verification & TWAP Breaker
* **Formal Mathematical Statement:** Dual-oracle pipeline consuming primary Chainlink data feeds cross-verified against a 30-minute DEX TWAP. Deviations $> \pm 8.00\%$ pause primary vault operations automatically.

### A10: Teleporter (ICM) Cross-L1 Consensus Integrity
* **Formal Mathematical Statement:** Cross-chain state transfers between C-Chain and sovereign Avalanche L1s utilize Avalanche Warp Messaging (AWM) signed by active validator BLS threshold signatures at the consensus layer, with zero wrapped bridge counterparty risk.

---

## 4. Macroeconomic & Ecosystem Value Capture Assumptions

### A11: ACP-67 Deflationary Buyback Efficacy
* **Formal Mathematical Statement:** Routing 65.00% of collateral staking yield to open-market $AVAX$ buybacks and burns contracts circulating supply, generating $\$4.06\text{M}$ to $\$203.12\text{M}$ in annual burn volume across TVL milestones ($\$100\text{M}$ to $\$5.0\text{B}$).

### A12: Active Validator Economic Alignment
* **Formal Mathematical Statement:** Routing 20.00% of staking yield to active validators enhances baseline validator staking APR by $+0.21$ to $+10.40$ percentage points, strengthening network consensus security.
