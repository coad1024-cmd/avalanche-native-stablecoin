# Ledger of Modeling Assumptions — Avalanche Native Stablecoin (`anUSD`)

**Governing Standard:** BCRG Mathematical & Economic Modeling Canon  
**Owner:** Bonding Curve Research Group (BCRG)  
**Status:** Canonical Ledger · August 2026  

---

## 1. Market Environment Assumptions

### A01: Collateral Price Follows a Merton-Kou Jump-Diffusion Process
* **Statement:** The spot price of $AVAX$ collateral $P(t)$ evolves according to a geometric Brownian motion superposed with compound Poisson log-normal jumps:
  $$\frac{dP(t)}{P(t^-)} = (\mu - \lambda \kappa) dt + \sigma dW(t) + dJ(t)$$
* **Justification:** Captures both continuous volatility ($\sigma = 89.86\%$) and sudden structural jump discontinuities ($\lambda = 2.4\text{ jumps/yr}$, $\mu_J = -12.0\%$) observed in crypto assets.
* **Breakdown Regime:** Extreme prolonged oracle outage (> 24 hours) where no price updates reach the blockchain.

### A02: Liquid Staking Cash Flow Continuity
* **Statement:** The underlying collateral token ($sAVAX$) continuously generates a non-negative staking yield $r_{\text{savax}} \in [4.0\%, 8.0\%]$ derived from Avalanche Primary Network validator validation rewards.
* **Justification:** Avalanche network staking emissions are governed by protocol consensus rules without slashing risk for offline downtime.
* **Breakdown Regime:** Fundamental Avalanche consensus hard-fork altering staking emission rules.

### A03: Secondary AMM Liquidity Depth
* **Statement:** Secondary market exchange liquidity for `anUSD` is provided via concentrated liquidity AMMs (e.g. Trader Joe v2.1) with depth sufficient to absorb standard retail flow without exceeding $\pm 0.50\%$ slippage.
* **Justification:** Initial protocol bootstrapping seeds liquidity pools using ACP-67 ecosystem grants.

---

## 2. Mechanism & Structural Assumptions

### A04: Zero-Friction Instantaneous Share Restructuring
* **Statement:** Dynamic resets (upward share splits at $H_u = \$2.00$ and downward reverse splits at $H_d = \$0.25$) execute deterministically in $O(1)$ computational complexity via a global conversion multiplier $\beta(t)$.
* **Justification:** Implemented in `TrancheToken.sol` using virtual share accounting (`RealBalance = VirtualShares × β`), eliminating iteration loops across user balances.

### A05: Model-Free Catastrophic Crash Bound (Theorem 1)
* **Statement:** For any single-step collateral price drop up to $\Delta P \ge -60.00\%$, the senior stablecoin tranche `anUSD` ($V_{A'}$) experiences exactly **zero principal loss**.
* **Justification:** Analytically proven in Section 4 of the Whitepaper by substituting the boundary condition $V_B(t^-) \ge H_d = 0.25$ into the residual pool conservation equation.

### A06: Bear-Market Coupon Subsidy ($\tilde{R}$) Demand Floor
* **Statement:** Transferring a coupon subsidy $\tilde{R} = 10.00\%$ from Class $A$ to Class $B$ during downward resets creates an economic floor that sustains Class $B$ leveraged equity demand during bear markets.
* **Justification:** Derived from SSRN-3856569 Section 2.5; provides positive cash returns to equity holders upon downward restructuring.

---

## 3. Cryptographic, Oracle & Security Assumptions

### A07: Sub-Second Finality & MEV Resistance
* **Statement:** Avalanche Snowman consensus finalizes transactions in $< 1.5$ seconds, preventing multi-block mempool front-running games.
* **Justification:** Primary C-Chain network architecture and Coreth execution engine.

### A08: Multi-Oracle Redundancy & Sanity TWAP Filter
* **Statement:** Collateral pricing uses Chainlink decentralized data feeds filtered against a 30-minute DEX Time-Weighted Average Price (TWAP). Deviations $> \pm 8.00\%$ pause vault operations automatically.
* **Justification:** Prevents single-block flash loan price manipulation attacks on reset barriers.

### A09: Teleporter Cross-L1 Consensus Integrity
* **Statement:** Cross-L1 transfers executed via Avalanche Inter-Chain Messaging (ICM / Teleporter) rely on BLS multi-signature threshold signing by active Avalanche validators, with zero wrapped bridge counterparty risk.
* **Justification:** Avalanche Warp Messaging (AWM) cryptographic protocol specification.

---

## 4. Macroeconomic & Value Capture Assumptions

### A10: ACP-67 Deflationary Buyback Efficacy
* **Statement:** Routing 65.00% of collateral staking yield to programmatic open-market $AVAX$ buyback-and-burn creates permanent supply contraction that supports network-wide capital capitalization.
* **Justification:** Avalanche Community Proposal ACP-67 (GitHub Discussion #293).

### A11: Validator Staking Yield Complementarity
* **Statement:** Routing 20.00% of yield to active Avalanche validators enhances baseline validator staking APR by $+0.21$ to $+10.40$ percentage points across scaling tiers ($100\text{M}$ to $5.0\text{B}$ TVL).

### A12: Rational Arbitrageur Efficiency
* **Statement:** Market arbitrageurs capture $\ge 85.00\%$ of secondary DEX peg discrepancies within 1 hour whenever spread $|P_{\text{DEX}} - V_{A'}| > 0.05\%$.
* **Justification:** Competitive automated searcher infrastructure operating on Avalanche C-Chain.
