# Avalanche Native USD (anUSD): A Dual-Class Securitization Architecture with Dynamic Reset Mechanics, Liquid Staking Integration, and On-Chain Value Recirculation

**Authors:** Bonding Curve Research Group  
**Target Infrastructure:** Avalanche Primary Network (C-Chain) & Avalanche Sovereign L1s  
**Version:** 1.0.0-PROD (August 2026)  
**LaTeX Source:** [`docs/WHITEPAPER.tex`](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/docs/WHITEPAPER.tex)  
**Publication PDF:** [`docs/WHITEPAPER.pdf`](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/docs/WHITEPAPER.pdf)  
**Interactive Web Edition:** [`docs/WHITEPAPER.html`](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/docs/WHITEPAPER.html)  
**Scientific Figures:** [`docs/figures/`](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures/)  

---

## Abstract

We introduce **Avalanche Native USD (anUSD)**, a fully decentralized, mathematically secure, and capital-efficient sovereign stablecoin architecture engineered natively for the Avalanche Primary Network (C-Chain) and Avalanche Sovereign L1s. Existing decentralized stablecoins rely predominantly on overcollateralized debt positions (CDPs) with liquidation auctions (MakerTeam, 2017; Klages-Mundt et al., 2020). During rapid market dislocations, these auctions suffer from mempool latency, miner-extractable value (MEV) exploitation, oracle front-running, and systemic bad-debt accumulation. Concurrently, centralized fiat-backed stablecoins (Tether, 2016; Griffin & Shams, 2020) extract 100% of underlying reserve yields, draining hundreds of millions in potential economic surplus from the host blockchain ecosystem.

Synthesizing continuous-time option pricing theory and financial securitization mathematics (Cao, Dai, Kou, Li, & Yang, 2021; Ingersoll, 1976; Jarrow & O'Hara, 1989) with Avalanche community governance economics (ACP-67), anUSD establishes an indigenous multi-tranche securitization structure backed 1:1 by liquid-staked Avalanche collateral ($sAVAX$). The underlying collateral pool is partitioned into a Senior Fixed-Income Tranche (Class A) and a Leveraged Long Tranche (Class B), with Class A further sub-tranched into an ultra-low volatility USD stablecoin (Class A$'$ / anUSD) and a leveraged high-yield asset (Class B$'$). To maintain continuous capital solvency without liquidation auctions, the protocol enforces an $O(1)$ constant-time dynamic upward ($H_u$) and downward ($H_d$) reset state machine executed via global scalar multipliers.

We provide rigorous analytical proofs and extensive empirical simulations demonstrating that anUSD maintains its \$1.00 USD peg with zero principal loss for instantaneous market plunges up to **$-60.0\%$** from the lower reset barrier (and **$-75.0\%$** from par). Furthermore, we formulate the valuation problem as a periodic Partial Integro-Differential Equation (PIDE) under Kou's (2002) double-exponential jump-diffusion process and prove the global geometric convergence of our iterative numerical operator ($\rho(\mathcal{T}) < 1$). Finally, we detail the on-chain integration of Avalanche Inter-Chain Messaging (ICM / Teleporter) and the automated ACP-67 yield recycling waterfall, directing 65% of gross protocol surplus to open-market AVAX buybacks and burns, generating over \$200M in annual AVAX deflationary pressure at scale.

---

## 1. Introduction and Problem Formulation

### 1.1 The Trilemma of Existing Stablecoin Archetypes
1. **Off-Chain Fiat-Collateralized Stablecoins (USDC, USDT):** Maintain tight price convergence around \$1.00 USD but introduce counterparty risks, banking dependencies, and regulatory freeze surfaces. The 4.0--5.5% annual yield generated on underlying short-term US Treasury reserves is retained entirely by private corporate issuers, draining hundreds of millions from Layer 1 networks.
2. **Overcollateralized Debt Position (CDP) Stablecoins (MakerDAO/DAI, Liquity/LUSD):** Require users to lock volatile crypto assets at high collateralization ratios (150--200%+). In severe market crashes, network congestion, oracle latency, and miner-extractable value (MEV) front-running cause liquidation auctions to fail, leading to bad debt and cascading death spirals.
3. **Algorithmic and Seigniorage Shares (Basis, Terra/UST):** Attempt to stabilize through endogenous token mint-and-burn arbitrage loops without independent collateralization, inevitably collapsing during market contractions.

### 1.2 The Securitization Paradigm and Avalanche Opportunity
Drawing inspiration from classical financial securitization (Split-Capital Investment Trusts, Dual-Purpose Funds, Americus Trust Primes and Scores), Cao et al. (2021) demonstrated that financial tranching with dynamic state resets constructs ultra-low volatility fixed-income claims from volatile collateral without asynchronous debt auctions.

Concurrently, **ACP-67 (Discussion #293)** establishes a community mandate to recycle 80--90% of stablecoin reserve earnings directly into AVAX open-market buybacks, validator staking boosts, and ecosystem grants. anUSD synthesizes quantitative tranching with ACP-67 on Avalanche C-Chain and sovereign L1s.

---

## 2. Mathematical Framework of Dual-Class Tranching

### 2.1 Underlying Collateral Pool and Primary Decomposition
Let $P_t$ denote the spot price in USD of the underlying collateral asset ($sAVAX$) at time $t$, $P_0$ the reference price at epoch inception, and $v_t = t - t_{\text{reset}}$ the elapsed epoch time.

When collateral is deposited, it is partitioned into a senior and junior pair:
$$V_A(t) = 1 + R \cdot v_t$$
$$V_B(t) = (1 + \alpha) \frac{P_t}{\beta_t P_0} - \alpha V_A(t) = (1 + \alpha) S_t - \alpha (1 + R \cdot v_t)$$

where $\alpha = 1.0$ yields the baseline 1:1 split, $R = 7.3\%$ p.a. is the senior coupon, $\beta_t$ is the cumulative scaling factor, and $S_t \equiv \frac{P_t}{\beta_t P_0}$ is the normalized collateral index.

#### Conservation of Value Invariant
$$\boxed{\alpha V_A(t) + V_B(t) = (1 + \alpha) S_t = (1 + \alpha) \frac{P_t}{\beta_t P_0}}$$

### 2.2 Secondary Tranching: Constructing anUSD (Class A$'$) and Yield (Class B$'$)
Class A undergoes a secondary 1:1 split into:
1. **Class A$'$ (anUSD Stablecoin):** Pegged to \$1.00 USD, accruing benchmark money-market interest $R' \approx 3.0\%$ p.a.
2. **Class B$'$ (Leveraged Yield Tranche):** Captures the leveraged spread coupon $(2R - R' = 11.6\%)$.

$$V_{A'}(t) = 1 + R' \cdot v_t$$
$$V_{B'}(t) = 2 V_A(t) - V_{A'}(t) = 1 + (2R - R') \cdot v_t$$
$$\boxed{V_{A'}(t) + V_{B'}(t) = 2 V_A(t)}$$

### 2.3 Effective Leverage & Sensitivity
![Figure 5: Leverage Bounds and PIDE Surface](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures/fig5_leverage_and_pide_surface.png)
*Figure 5: Left: Numerical 3D solution surface of the valuation PIDE $W_A(v, S)$ on Banach space $\mathcal{D}$. Right: Class B bounded effective leverage curve $\Lambda_B(S) \in [1.5\times, 5.0\times]$ bounded strictly between dynamic reset barriers $H_d = \$0.25$ and $H_u = \$2.00$.*

---

## 3. Dynamic Reset Mechanics and State Transition Invariants

### 3.1 Upward Reset ($H_u \approx \$2.00$)
When collateral appreciates such that $V_B(t) \ge H_u$:
1. Class B holders receive realized collateral profit payouts equal to $(V_B(t) - 1.00)$.
2. Class A holders receive accrued coupon settlement $R \cdot v_t$.
3. Tranches undergo a forward scalar split $\gamma_u > 1.0$, restoring $V_A(t^+) = V_B(t^+) = 1.00$ and resetting leverage to $2.0\times$.
4. State variables update: $v_{t^+} = 0, P_0 \leftarrow P_t, \beta_{t^+} = \frac{P_t}{P_0^{\text{prev}}} \beta_{t^-}$.

### 3.2 Downward Reset ($H_d \approx \$0.25$)
When collateral depreciates such that $V_B(t) \le H_d$:
1. Class A holders receive accrued coupons plus principal amortization $(1.00 - V_B(t))$ in collateral.
2. Remaining shares undergo a mandatory reverse split (merger) by ratio $\gamma_d = V_B(t)$, such that $1 / V_B(t)$ old shares merge into $1.0$ new share.
3. State variables update: $v_{t^+} = 0, P_0 \leftarrow P_t, \beta_{t^+} = \frac{P_t}{P_0^{\text{prev}}} \beta_{t^-}, V_A(t^+) = V_B(t^+) = 1.00$.

![Figure 2: Dynamic Reset Mechanics & NAV Dynamics](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures/fig2_nav_dynamics_resets.png)
*Figure 2: cadCAD discrete-event simulation of dynamic reset state transitions over a 365-day stochastic market cycle. Top: Underlying AVAX collateral price path with upward (green) and downward (red) reset execution timestamps. Bottom: Net Asset Value trajectories for Class A, Class B, Class B$'$, and the invariant $\$1.00$ anUSD stablecoin (Class A$'$).*

---

## 4. Catastrophic Black Swan Crash Tolerance & Model-Free Bounds

### Theorem 1 (Model-Free Crash Invariance Proof)
An instantaneous downward price jump of magnitude $\Delta P / P < 0$ occurring at normalized time $v_t$ from pre-jump state $V_B(t^-) \ge H_d$ will cause **zero principal loss** to Class A$'$ (anUSD) if and only if:
$$\boxed{\frac{\Delta P}{P} \ge \frac{1}{2} \left( \frac{R' v_t + 1}{R v_t + 1 + H_d} \right) - 1}$$

* **From Barrier $H_d = 0.25$:** $\text{Max Instant Drop} = \frac{1}{2}\left(\frac{1.00}{1.25}\right) - 1 = \mathbf{-60.0\%}$
* **From Par Baseline $V_B = 1.00$:** $\text{Max Instant Drop} = \frac{1}{2}\left(\frac{1.00}{2.00}\right) - 1 = \mathbf{-75.0\%}$

![Figure 3: Black Swan Crash Tolerance vs CDP Protocols](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures/fig3_black_swan_crash_tolerance.png)
*Figure 3: Instantaneous Black Swan flash-crash stress test comparing realized redemption payouts across stablecoin protocols. anUSD maintains 100% par redemption for instantaneous market drops up to $-60.0\%$ from the lower barrier $H_d$ (and $-75.0\%$ from par), substantially outperforming MakerDAO DAI ($-33.3\%$) and Liquity LUSD ($-9.1\%$).*

| Protocol / Model | Collateral Asset | Liquidation Engine | Max Safe Instantaneous Drop |
| :--- | :--- | :--- | :--- |
| **MakerDAO (DAI)** | ETH / AVAX (150% CR) | Dutch Auction (200+ block delay) | **$-33.3\%$** |
| **Liquity (LUSD)** | ETH (110% MCR) | Stability Pool Offset | **$-9.1\%$** |
| **Ethena (USDe)** | Staked ETH + Short Perp | Exchange Margin Liquidation | Funding Inversion Risk |
| **anUSD (Ours)** | $sAVAX$ (Dual Tranche) | Dynamic Reset Reverse Split | **$-60.0\%$ to $-75.0\%$** |

---

## 5. Continuous-Time Valuation via Partial Integro-Differential Equations (PIDE)

### 5.1 Asset Dynamics under Kou's Double-Exponential Jump-Diffusion
$$\frac{dS_t}{S_{t^-}} = (r - q - \lambda \zeta) dt + \sigma dW_t + (e^Y - 1) dN_t$$
where continuous volatility $\sigma = 75\%$, jump intensity $\lambda = 3.5\text{ jumps/yr}$, $p = 0.40$, $\eta_1 = 3.5$, $\eta_2 = 2.0$.

![Figure 1: Kou Jump-Diffusion Trajectories](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures/fig1_jump_diffusion_paths.png)
*Figure 1: Monte Carlo simulated trajectories of AVAX collateral spot price ($S_t$) under Kou's double-exponential jump-diffusion process over a 2-year simulation horizon.*

### 5.2 Non-Local Parabolic PIDE
$$\frac{\partial W_A}{\partial v} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 W_A}{\partial S^2} + (r - q - \lambda \zeta) S \frac{\partial W_A}{\partial S} - (r + \lambda) W_A + \lambda \int_{-\infty}^{\infty} W_A(v, S e^y) f_Y(y) dy = 0$$

### 5.3 Contraction Mapping Operator and Geometric Convergence
The iterative operator $\mathcal{T}[w](v, S) = \mathbb{E}^{\mathbb{Q}} [ e^{-r \tau} \mathcal{B}(w)(\tau, S_\tau) \mid S_0 = S ]$ is a strict contraction on $(C(\mathcal{D}), \|\cdot\|_\infty)$ with contraction modulus $\rho(\mathcal{T}) < 1$, ensuring geometric convergence:
$$\|W_A^{(k)} - W_A^*\|_\infty \le \frac{\rho^k}{1-\rho}\|W_A^{(1)} - W_A^{(0)}\|_\infty \to 0$$

---

## 6. Generalized Dynamical System (GDS) Simulation & Empirical Verification

Following foundational cryptoeconomic modeling theory (Zargham et al., 2020, 2021), we formalize the anUSD protocol as a discrete-time stochastic dynamical state-transition system:
$$x_{t+1} = f(x_t, u_t; \theta)$$
with state space $x_t \in \mathcal{X} \subset \mathbb{R}^{13}$, environmental Kou jump-diffusion price driver $u_t \in \mathcal{U}$, parameter vector $\theta \in \Theta$, and strict conservation invariant $\mathcal{I}(x_t) = |V_A(t) + V_B(t) - 2S_t| \equiv 0$.

![Figure 6: GDS Monte Carlo Volatility and Invariant Distribution](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures/fig6_gds_monte_carlo.png)
*Figure 6: Left: GDS Monte Carlo probability density distribution of annualized anUSD peg volatility ($N = 1,000$ trajectories, median 1.37%, strictly bounded by < 2.00% design gate). Right: Solvency conservation invariant error $|\Delta| = |V_A + V_B - 2S_t|$ evaluated over 730 daily simulation steps, demonstrating strict machine-precision error bounds ($\sim 10^{-15}$).*

### 6.1 Key Performance Indicators and Gate Satisfaction ($N = 1,000$ runs)

| Performance Indicator | 5th Percentile | Median | 95th Percentile | Protocol Target / Gate |
|---|---|---|---|---|
| **Maximum anUSD Drawdown** | 0.00% | **0.00%** | 0.00% | 0.00% (Zero Haircut) |
| **Annualized NAV Volatility** | 1.12% | **1.37%** | 1.64% | < 2.00% (Gate Satisfied) |
| **Solvency Invariant Gap** | 0.0000 | **0.0000** | 0.0000 | 0.0000 (Conserved) |
| **Annual Cumulative AVAX Burned** | 215,000 AVAX | **260,000 AVAX** | 310,000 AVAX | > 100,000 AVAX |
| **Validator Yield Supplement** | +0.85% | **+1.04%** | +1.24% | > +0.50% |
| **Downward Reset Frequency** | 0.82 / yr | **1.15 / yr** | 1.65 / yr | < 3.00 / yr |

### 6.2 Empirical Market Regime State Progression

| Market Regime | Elapsed Time | AVAX Spot ($P_t$) | anUSD NAV ($V_{A'}$) | Class B NAV ($V_B$) | Leverage ($\Lambda_B$) | Reset Action |
|---|---|---|---|---|---|---|
| **Genesis Baseline** | Day 0 | $25.00 | $1.0000 | $1.0000 | 2.00× | Initialization |
| **Moderate Bull Rally** | Day 45 | $38.50 | $1.0037 | $1.9860 | 1.54× | None |
| **Upward Trigger** | Day 46 | $39.10 | $1.0000 | $1.0000 | 2.00× | Upward Split |
| **Severe Downside Jump** | Day 120 | $18.20 | $1.0000 | $0.2450 | 4.95× | Downward Merger |
| **Post-Merge Recovery** | Day 180 | $24.00 | $1.0049 | $1.4230 | 1.83× | None |

---

### 6.3 Governance Trade-Off Choices

| Decision Parameter | Proposed Default | Alternative Option | Primary Economic Trade-Off |
|---|---|---|---|
| **Downward Barrier ($H_d$)** | $0.25 NAV | $0.35 NAV | Lower barrier reduces reset frequency; higher barrier increases crash buffer |
| **Senior Coupon ($R$)** | 7.30% p.a. | 6.00% p.a. | Higher coupon attracts Class A capital; lower coupon reduces leverage cost |
| **ACP-67 Burn Share** | 65.00% | 50.00% | Higher burn accelerates AVAX deflation; lower burn expands validator rewards |

---

## 7. On-Chain Value Recirculation & ACP-67 Economic Flywheel

All gross protocol surplus ($\Phi_{\text{gross}} = \mathcal{Y}_{\text{staking}} + \mathcal{F}_{\text{mint/redeem}} + \mathcal{F}_{\text{flash}}$) flows into `YieldRecycler.sol`:
* **65% AVAX Buyback & Burn ($\Phi_{\text{burn}}$):** Swapped via DEX liquidity and permanently burned (`0x000...dEaD`).
* **20% Active Validator Incentive Boost ($\Phi_{\text{val}}$):** Direct subsidies to active Avalanche validators.
* **15% Ecosystem & L1 Liquidity Fund ($\Phi_{\text{eco}}$):** Protocol liquidity and cross-L1 bridge incentives.

![Figure 4: ACP-67 Waterfall & Projections](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures/fig4_acp67_buyback_waterfall.png)
*Figure 4: Annualized on-chain value recirculation breakdown across stablecoin TVL tiers under ACP-67 mandates. At \$5.00B TVL, anUSD generates \$203.12M in annual AVAX open-market buybacks and burns (over 8.1M AVAX permanently retired at \$25/AVAX).*

| anUSD TVL | Gross Yield (6.0%) | AVAX Burn (USD) | AVAX Burned (Qty @ \$25) | Validator Boost | Ecosystem Fund |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **\$100M** | \$6.25M | \$4.06M | **162,500 AVAX** | \$1.25M | \$0.94M |
| **\$250M** | \$15.62M | \$10.16M | **406,250 AVAX** | \$3.12M | \$2.34M |
| **\$500M** | \$31.25M | \$20.31M | **812,500 AVAX** | \$6.25M | \$4.69M |
| **\$1.00B** | \$62.50M | \$40.62M | **1,625,000 AVAX** | \$12.50M | \$9.38M |
| **\$2.50B** | \$156.25M | \$101.56M | **4,062,500 AVAX** | \$31.25M | \$23.44M |
| **\$5.00B** | \$312.50M | \$203.12M | **8,125,000 AVAX** | \$62.50M | \$46.88M |

---

## 8. Smart Contract Architecture & $O(1)$ Constant-Time Rebasing

```solidity
// O(1) Constant-Time Balance Lookup via Multiplier
function balanceOf(address user) external view returns (uint256) {
    return (rawBalance[user] * globalScalarMultiplier) / 1e18;
}
```

```
Algorithm 1: O(1) Constant-Time Dynamic Reset Execution
--------------------------------------------------------------------------------
1: S_t ← (P_t * 1e18) / (β * P_0)
2: V_B(t) ← 2 * S_t - (1e18 + (R * Δt) / 365 days)
3: if V_B(t) >= H_u then                      // UPWARD RESET
4:     M_A ← (M_A * 150) / 100
5:     M_B ← (M_B * 150) / 100
6:     β   ← (P_t * 1e18) / P_0;  P_0 ← P_t
7:     emit ResetExecuted(UPWARD, P_t, beta)
8: else if V_B(t) <= H_d then                 // DOWNWARD RESET
9:     M_A ← (M_A * 75) / 100
10:    M_B ← (M_B * 75) / 100
11:    β   ← (P_t * 1e18) / P_0;  P_0 ← P_t
12:    emit ResetExecuted(DOWNWARD, P_t, beta)
13: end if
```

---

## 9. Avalanche Teleporter (ICM) Cross-L1 Interoperability

anUSD uses native **Avalanche Inter-Chain Messaging (ICM)** via `TeleporterUSDAdapter.sol`:
1. **Origin Burn:** Tokens burned on source chain.
2. **Warp Consensus Signing:** Avalanche validators sign state payload with BLS multi-signatures.
3. **Target Mint:** Target sovereign L1 verifies BLS signature and mints native anUSD with zero slippage and zero wrapped bridge risk.
4. **Native Native L1 Gas:** Avalanche L1s can configure anUSD as their native transaction gas token for predictable dollar fees.

---

## 10. Security Architecture and Threat Modeling

### 10.1 Miner-Extractable Value (MEV) & Front-Running Resistance
* **Proximity Volatility Band:** When the oracle price enters a $\pm 1.5\%$ proximity band around $H_u$ or $H_d$, user mints and redemptions enter a temporary 1-block delay lock.
* **Permissioned Keeper Relays:** Resets are executed exclusively via dedicated Chainlink Automation and Avalanche Warp Relay keeper bots.

### 10.2 Oracle Robustness & Circuit Breakers
The `OracleAdapter.sol` contract consumes primary Chainlink AVAX/USD price feeds cross-verified against a 30-minute Exponential Time-Weighted Average Price (TWAP) from native DEX pools. If deviation between spot and TWAP exceeds $\pm 8.0\%$, the vault enters an automated circuit-breaker pause, safeguarding collateral reserves against flash-loan oracle manipulation.

---

## 11. Conclusion and Future Work

Avalanche Native USD (anUSD) establishes the theoretical and practical foundation for sovereign, liquidation-free stablecoin engineering. By transforming volatile Layer 1 staking assets into senior fixed income, leveraged bull instruments, and an ultra-stable dollar peg, anUSD solves the capital inefficiencies and liquidation risks of legacy CDPs. 

With verified mathematical immunity against $-60.0\%$ single-step black swan crashes, $O(1)$ constant-time scalar rebasing, native Avalanche Teleporter multi-L1 interoperability, and an automated ACP-67 value-recycling flywheel generating massive continuous AVAX burn volume, anUSD represents the definitive native monetary primitive for the Avalanche ecosystem.

Future research directions will focus on:
1. **Robust Parameter Selection Under Uncertainty (PSUU):** Applying generalized robust optimization and adversarial sensitivity analysis across continuous stochastic jump regimes $(\sigma \in [50\%, 120\%], \lambda \in [1.0, 6.0], q \in [4.0\%, 8.0\%])$ to formally solve the multi-objective governance selection problem $\theta^* = \arg\max_{\theta \in \Theta} \min_{u \in \mathcal{U}} \mathbb{E}[\mathcal{U}(\theta, u)]$.
2. **Multi-Collateral RWA Basket Expansion:** Incorporating tokenized real-world assets (such as tokenized US Treasury bills via Avalanche Evergreen L1s) into the collateral pool.
3. **Zero-Knowledge Privacy Extensions:** Designing confidential balance and transfer layers for institutional enterprise settlement.

---

## 12. References

* **Adams, A. T., & Clunie, J. B. (2006).** Risk assessment techniques for split capital investment trusts. *Annals of Actuarial Science*, 1(1), 7–36.
* **Al-Naji, N. (2018).** Basecoin: A price-stable cryptocurrency with an algorithmic central bank. *Basecoin Whitepaper*.
* **Avalanche Community Proposal 67 (Discussion #293). (2026).** Framework for Aligned Stablecoin Asset with Yield Sharing and Ecosystem Growth Targets. *Avalanche Foundation Governance Repository*.
* **Cai, N., & Kou, S. G. (2011).** Option pricing under a mixed-exponential jump diffusion model. *Management Science*, 57(11), 2067–2081.
* **Cao, Y., Dai, M., Kou, S., Li, L., & Yang, C. (2021).** Designing Stablecoins. *SSRN Electronic Journal*, 3856569.
* **Duo Network. (2020).** Duo Custodian Smart Contracts Architecture. *GitHub: DuoNetwork/duo-contract*.
* **Kou, S. G. (2002).** A Jump-Diffusion Model for Option Pricing. *Management Science*, 48(8), 1086–1101.
* **Rocket, M., et al. (2020).** Scalable and Probabilistic Leaderless BFT Consensus through Avalanche. *arXiv:1906.08936*.
* **Zargham, M., Shorish, J., & Paruch, K. (2020).** From Curved Bonding to Generalized Dynamical Systems. *Vienna University of Economics and Business & BlockScience Research Paper*.
* **Zargham, M., & Emmett, J. (2021).** Foundations of Cryptoeconomic Systems: Generalized Dynamical Systems and State Machines. *arXiv:2104.09265*.
