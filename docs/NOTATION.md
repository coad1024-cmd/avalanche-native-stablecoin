# Notation Registry — Avalanche Native Stablecoin (`anUSD`)

**Governing Standard:** BCRG Mathematical & Economic Paper Standard  
**Owner:** Bonding Curve Research Group (BCRG)  
**Status:** Canonical Single Source of Truth · August 2026  
**Related Specs:** SSRN-3856569, ACP-67 (Discussion #293), Subspace PSUU Canon  

---

## 1. Ground-Truth Hierarchy & Precedence

1. **Avalanche Network Protocols & Filed ACPs:** On-chain EVM rules, Snowman consensus finality (< 1.5s), Avalanche Inter-Chain Messaging (ICM / Teleporter), and ACP-67 economic targets.
2. **Academic Foundations (SSRN-3856569 & Option Pricing Canon):** Merton-Kou jump-diffusion SDEs, dual-class Net Asset Value (NAV) identities, PIDE valuation, and Theorem 1 crash bounds.
3. **BlockScience / Token Engineering Canon:** Generalized Dynamical Systems (GDS) notation, state·stock·flow taxonomy, parameter spaces ($\Theta \subset \mathbb{R}^{23}$), control policies ($\mathcal{U}$), and exogenous inputs ($\mathcal{W}$).
4. **Internal Codebase Identifiers:** Exact Python and Solidity variable names mapping 1:1 to mathematical glyphs.

---

## 2. Canonical Registry Table: State Space ($\mathcal{X}$) & Environmental Variables ($\mathcal{W}$)

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
| $G_{\text{eco}}(t)$ | `G_cum_l1_USD` | State·Sink | $\mathbb{R}_{\ge 0}$ | USD | Cumulative sovereign Avalanche L1 liquidity grants | ACP-67 / Grants Pool |

---

## 3. Canonical Registry Table: 20 Governance Levers ($\Theta \subset \mathbb{R}^{23}$)

| Subsystem | Symbol | Code Name | Baseline | Domain / Bounds | Physical Unit | Definition & Role |
|---|---|---|---|---|---|---|
| **Tranching** | $R$ | `coupon_R` | **$7.30\%$** | $[4.0\%, 12.0\%]$ | Fraction/year | Senior Class A coupon rate |
| | $R'$ | `coupon_R_prime` | **$3.00\%$** | $[1.0\%, 5.0\%]$ | Fraction/year | anUSD benchmark coupon rate |
| | $\tilde{R}$ | `bear_subsidy_R` | **$10.00\%$** | $[0.0\%, 20.0\%]$ | Fraction/year | Bear-market coupon subsidy transferred from A to B |
| | $\chi$ | `tranche_ratio_chi`| **$1.00$** | $[0.50, 2.00]$ | Ratio | Initial Class A to Class B issuance ratio ($1:1$) |
| | $T$ | `epoch_maturity_T_days`| **$365$** | $[90, 730]$ | Days | Contractual epoch horizon |
| **Resets** | $H_u$ | `barrier_H_u` | **$\$2.00$** | $[\$1.50, \$3.00]$ | USD / Share | Upward share-split barrier threshold |
| | $H_d$ | `barrier_H_d` | **$\$0.25$** | $[\$0.15, \$0.40]$ | USD / Share | Downward reverse-split barrier threshold |
| | $\mu_{\text{split}}$ | `split_mult_up` | **$1.50\times$** | $[1.20, 2.00]$ | Scalar | Upward share split expansion factor |
| | $\mu_{\text{merge}}$ | `merge_mult_down` | **$0.75\times$** | $[0.50, 0.90]$ | Scalar | Downward share merge contraction factor |
| | $\delta_{\text{lock}}$ | `mev_band_delta` | **$\pm 1.50\%$** | $[\pm 0.5\%, \pm 3.0\%]$ | Fraction | MEV 1-block delay lock proximity band |
| **Control** | $K_p$ | `controller_Kp` | **$0.150$** | $[0.01, 1.00]$ | 1 / USD | Reflexer-style Proportional rate controller gain |
| | $K_i$ | `controller_Ki` | **$0.020$** | $[0.001, 0.10]$ | 1 / (USD·yr) | Reflexer-style Integral rate controller gain |
| | $K_d$ | `controller_Kd` | **$0.005$** | $[0.000, 0.05]$ | 1 / (USD/yr) | Derivative damping controller gain |
| | $\Delta R'_{\max}$ | `controller_max_adj`| **$\pm 5.00\%$** | $[\pm 2.0\%, \pm 10.0\%]$| Fraction/year | Anti-windup rate adjustment ceiling |
| | $\Delta t_{\text{sample}}$ | `twap_window_sec` | **$1800$** | $[600, 7200]$ | Seconds | DEX TWAP sampling window length (30 min) |
| **Waterfall** | $\omega_{\text{burn}}$ | `acp67_burn_pct` | **$65.00\%$** | $[40.0\%, 80.0\%]$ | Fraction | Staking yield share allocated to AVAX buyback/burn |
| | $\omega_{\text{val}}$ | `acp67_val_pct` | **$20.00\%$** | $[10.0\%, 35.0\%]$ | Fraction | Staking yield share allocated to Validator boost |
| | $\omega_{\text{l1}}$ | `acp67_l1_pct` | **$15.00\%$** | $[5.0\%, 25.0\%]$ | Fraction | Staking yield share allocated to Sovereign L1 grants |
| | $f_{\text{mint}}$ | `fee_mint_bps` | **$10\text{ bps}$** | $[0, 50\text{ bps}]$ | Basis points | Vault minting fee ($0.10\%$) |
| | $f_{\text{redeem}}$ | `fee_redeem_bps` | **$10\text{ bps}$** | $[0, 50\text{ bps}]$ | Basis points | Vault redemption fee ($0.10\%$) |
| | $f_{\text{flash}}$ | `fee_flash_bps` | **$9\text{ bps}$** | $[1, 20\text{ bps}]$ | Basis points | Flash-loan protocol fee ($0.09\%$) |
| **Breakers** | $\Delta P_{\max}$ | `max_oracle_divergence`| **$\pm 8.00\%$** | $[\pm 3.0\%, \pm 15.0\%]$| Fraction | Spot vs TWAP circuit breaker pause threshold |
| | $\tau_{\text{heart}}$ | `oracle_heartbeat_sec`| **$300$** | $[60, 900]$ | Seconds | Maximum Chainlink oracle update staleness |
| | $L_{\text{cap}}$ | `daily_mint_cap_usd`| **$\$50\text{M}$** | $[\$10\text{M}, \$500\text{M}]$ | USD / Day | Daily gross deposit inflow throttle |
