# Notation Registry — Avalanche Native Stablecoin (`anUSD`)

**Governing Standard:** BCRG Mathematical & Economic Paper Standard  
**Owner:** Bonding Curve Research Group (BCRG)  
**Status:** Canonical Single Source of Truth · August 2026  
**Related Specs:** SSRN-3856569, ACP-67 (Discussion #293), Subspace PSUU Canon  

---

## 1. Ground-Truth Hierarchy & Precedence

1. **Avalanche Network Protocols & Filed ACPs:** On-chain EVM rules, Snowman consensus finality (< 1.5s), Avalanche Inter-Chain Messaging (ICM / Teleporter), and ACP-67 economic targets.
2. **Academic Foundations (SSRN-3856569 & Option Pricing Canon):** Merton-Kou jump-diffusion SDEs, dual-class Net Asset Value (NAV) identities, PIDE valuation, and Theorem 1 crash bounds.
3. **BlockScience / Token Engineering Canon:** Generalized Dynamical Systems (GDS) notation, state·stock·flow taxonomy, parameter spaces ($\Theta$), control policies ($\mathcal{U}$), and exogenous inputs ($\mathcal{W}$).
4. **Internal Codebase Identifiers:** Exact Python and Solidity variable names mapping 1:1 to mathematical glyphs.

---

## 2. Canonical Registry Table

| Symbol | Code Name | Category | Mathematical Domain | Physical Unit | Definition & Role | Source of Truth |
|---|---|---|---|---|---|---|
| $P(t)$ | `P_spot` | State·Exogenous | $\mathbb{R}_{>0}$ | USD / AVAX | External market spot price of collateral | Primary Oracle (Chainlink/Pyth) |
| $P_0$ | `P_0` | State·Internal | $\mathbb{R}_{>0}$ | USD / AVAX | Reference collateral price at start of current reset epoch | `CustodianVault.sol` |
| $v(t)$ | `epoch_v` | State·Temporal | $[0, \infty)$ | Years | Continuous elapsed time within current reset epoch | `ResetController.sol` |
| $\beta(t)$ | `beta_rebase` | State·Accumulator| $\mathbb{R}_{>0}$ | Dimensionless | Cumulative $O(1)$ global share scaling factor | `TrancheToken.sol` |
| $S(t)$ | `S_index` | State·Derived | $\mathbb{R}_{>0}$ | Dimensionless | Normalized collateral pool index: $P(t) / (\beta(t) P_0)$ | SSRN-3856569 Eq (1) |
| $V_A(t)$ | `V_A` | State·NAV | $\mathbb{R}_{>0}$ | USD / Share | Class A Senior Bond Net Asset Value ($1 + Rv$) | SSRN-3856569 Eq (2) |
| $V_B(t)$ | `V_B` | State·NAV | $\mathbb{R}$ | USD / Share | Class B Leveraged Equity Net Asset Value ($2S - V_A$) | SSRN-3856569 Eq (3) |
| $V_{A'}(t)$| `V_A_prime` | State·NAV | $\mathbb{R}_{>0}$ | USD / Share | Class A' (`anUSD` Stablecoin) Net Asset Value ($1 + R'v$) | SSRN-3856569 Eq (4) |
| $V_{B'}(t)$| `V_B_prime` | State·NAV | $\mathbb{R}$ | USD / Share | Class B' Amplified Yield Net Asset Value ($2V_A - V_{A'}$) | SSRN-3856569 Eq (5) |
| $\mathcal{L}_B(t)$ | `leverage_B` | State·Derived | $[1.0, \infty)$ | Dimensionless | Effective financial leverage of Class B: $2S / V_B$ | SSRN-3856569 Eq (6) |
| $P_{\text{DEX}}(t)$ | `P_DEX` | State·Market | $\mathbb{R}_{>0}$ | USD / anUSD | Secondary AMM market trading price | Secondary DEX Pool |
| $C_{\text{pool}}(t)$ | `C_pool_sAVAX` | State·Stock | $\mathbb{R}_{\ge 0}$ | sAVAX | Physical collateral tokens held in custodian vault | `CustodianVault.sol` |
| $B_{\text{cum}}(t)$ | `B_cum_AVAX` | State·Sink | $\mathbb{R}_{\ge 0}$ | AVAX | Cumulative native AVAX destroyed via buyback & burn | ACP-67 / Burn Address |
| $R_{\text{val}}(t)$ | `R_cum_val_USD`| State·Sink | $\mathbb{R}_{\ge 0}$ | USD | Cumulative validator staking rewards distributed | ACP-67 / Escrow |
| $G_{\text{eco}}(t)$ | `G_cum_l1_USD` | State·Sink | $\mathbb{R}_{\ge 0}$ | USD | Cumulative sovereign Subnet / L1 liquidity grants | ACP-67 / Grants Pool |
| $R$ | `coupon_R` | Param·Gov | $[0.05, 0.10]$ | Annual Fraction | Contracted Senior Class A coupon rate ($7.30\%$) | SSRN-3856569 |
| $R'$ | `coupon_R_prime`| Param·Gov | $[0.02, 0.045]$| Annual Fraction | anUSD benchmark money-market coupon rate ($3.00\%$) | SSRN-3856569 |
| $\tilde{R}$ | `bear_subsidy_R`| Param·Gov | $[0.00, 0.15]$ | Annual Fraction | Bear-market coupon subsidy transferred from A to B ($10.00\%$) | SSRN-3856569 Sec 2.5 |
| $H_u$ | `barrier_H_u` | Param·Gov | $[\$1.75, \$2.50]$| USD NAV | Upward reset barrier threshold ($\$2.00$) | SSRN-3856569 |
| $H_d$ | `barrier_H_d` | Param·Gov | $[\$0.15, \$0.35]$| USD NAV | Downward reset barrier threshold ($\$0.25$) | SSRN-3856569 |
| $r_{\text{savax}}$ | `savax_base_apr`| Param·Env | $[0.04, 0.08]$ | Annual Fraction | Underlying sAVAX staking yield ($6.00\%$) | Benqi / Avalanche Primary |
| $\omega_{\text{burn}}$ | `acp67_burn_pct`| Param·Gov | $[0.50, 0.75]$ | Fraction | Fraction of staking yield routed to AVAX burn ($65.00\%$) | ACP-67 |
| $\omega_{\text{val}}$ | `acp67_val_pct` | Param·Gov | $[0.15, 0.25]$ | Fraction | Fraction routed to validator yield boost ($20.00\%$) | ACP-67 |
| $\omega_{\text{l1}}$ | `acp67_l1_pct` | Param·Gov | $[0.10, 0.20]$ | Fraction | Fraction routed to sovereign L1 grants ($15.00\%$) | ACP-67 |
| $\mu$ | `drift_mu` | Param·Env | $\mathbb{R}$ | Annual Fraction | Collateral price annualized drift ($15.00\%$) | Historical Calibration |
| $\sigma$ | `diffusion_sigma`| Param·Env | $[0.40, 1.50]$| Annual Fraction | Collateral annualized diffusion volatility ($89.86\%$) | Avalanche Historical Ret |
| $\lambda$ | `jump_intensity`| Param·Env | $[1.0, 5.0]$ | 1 / Year | Poisson jump arrival frequency ($2.40\text{ jumps/yr}$) | Kou Jump Calibration |
| $\mu_J$ | `jump_mean_mu_j`| Param·Env | $[-0.30, 0.00]$| Log Return | Mean log-normal jump amplitude ($-0.1200$) | Historical Stress Events |
| $\sigma_J$ | `jump_vol_sigma`| Param·Env | $[0.05, 0.30]$ | Log Return | Jump amplitude standard deviation ($0.1800$) | Historical Stress Events |
| $K_p$ | `controller_Kp` | Param·Control | $[0.01, 1.00]$ | 1 / USD | Reflexer-style Proportional rate controller gain ($0.15$) | BlockScience PID Canon |
| $K_i$ | `controller_Ki` | Param·Control | $[0.001, 0.10]$| 1 / (USD·yr) | Reflexer-style Integral rate controller gain ($0.02$) | BlockScience PID Canon |
