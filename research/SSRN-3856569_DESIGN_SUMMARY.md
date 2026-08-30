# Research Note: Dual-Class Tranche Stablecoin Architecture (SSRN-3856569)

**Paper Title:** *Designing Stablecoins*  
**Authors:** Yizhou Cao, Min Dai, Steven Kou, Lewei Li, Chen Yang (Hong Kong Polytechnic University, Boston University, CUHK)  
**File Location:** [`research/ssrn-3856569.pdf`](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/research/ssrn-3856569.pdf)  
**Reference Smart Contract:** [Duo Network Custodian](https://github.com/DuoNetwork/duo-contract)

---

## 1. Core Concept & Architectural Overview

The paper proposes a **securitization-based, dual-class tranching mechanism** on volatile native crypto assets (e.g., ETH, AVAX) to create a true dollar-pegged stablecoin without requiring off-chain bank reserves or overcollateralized debt liquidation auctions (like MakerDAO/DAI).

```
                      ┌─────────────────────────────────┐
                      │    Underlying Pool (e.g., AVAX) │
                      └────────────────┬────────────────┘
                                       │ 1:1 Split
                      ┌────────────────┴────────────────┐
                      ▼                                 ▼
           ┌──────────────────────┐          ┌──────────────────────┐
           │     Class A Coin     │          │     Class B Coin     │
           │ (Senior Fixed-Income)│          │  (Leveraged Equity)  │
           │   Coupon Rate = R    │          │  Initial Leverage 2x │
           └──────────┬───────────┘          └──────────────────────┘
                      │ Secondary Split (1:1)
             ┌────────┴────────┐
             ▼                 ▼
  ┌──────────────────────┐   ┌──────────────────────┐
  │    Class A′ Coin     │   │    Class B′ Coin     │
  │  ★ THE STABLECOIN ★  │   │(Yield-Seeking Tranche│
  │ Pegged to USD (R'≈r) │   │ Coupon = 2R - R' )   │
  └──────────────────────┘   └──────────────────────┘
```

---

## 2. Tranching Breakdown

### Primary Tranches (Class A & Class B)
1. **Class A (Senior Fixed-Income Bond)**:
   - Receives fixed periodic coupon rate $R$ (e.g., 7.3% annualized).
   - Backed by the asset pool with priority over Class B.
2. **Class B (Leveraged Long / Equity)**:
   - Absorbs the underlying crypto volatility.
   - Borrowing cost equals the coupon $R$ paid to Class A.
   - Starts at $2\times$ leverage and provides leveraged upside exposure for traders without funding fee decay.

### Secondary Tranches (Class A′ & Class B′)
1. **Class A′ (The USD Stablecoin)**:
   - Pegged to USD ($1.00$) with a low money-market coupon $R' \approx r$ (e.g., 3.0% or 0%).
   - Demonstrates extremely low annualized volatility (**1.37%** vs S&P 500 at 26% and ETH at 90%).
2. **Class B′ (High-Yield Tranche)**:
   - Receives the leveraged spread coupon $(2R - R')$, making it an attractive yield-bearing instrument for DeFi liquidity providers.

---

## 3. Dynamic Reset Mechanism (The Core Innovation)

Unlike standard CLOs with monthly tests or MakerDAO with auction liquidations, this protocol uses **real-time state resets**:

### A. Upward Reset ($H_u \approx \$2.00$)
- **Trigger**: When the underlying crypto surges and Class B NAV reaches $H_u$.
- **Action**:
  - Class B locks in profits ($V_B - 1.00$) and receives payouts in underlying crypto.
  - Class A receives accrued coupon payments.
  - Both tranches undergo share splits to reset their Net Asset Value (NAV) back to **$1.00$**, restoring leverage to $2\times$.

### B. Downward Reset ($H_d \approx \$0.25$)
- **Trigger**: When underlying crypto falls and Class B NAV drops to $H_d$.
- **Action**:
  - Class A receives accrued coupons + principal payback ($1 - V_B$).
  - Both tranches execute a reverse split (share merger, e.g. 4:1) resetting NAV back to **$1.00$**, restoring leverage to $2\times$.
  - **No bad debt or auction delays**: Prevents liquidation cascade death spirals.

---

## 4. Black Swan Protection & Model-Free Bounds

The paper mathematically derives model-free bounds for catastrophic market crashes:

| Metric | MakerDAO (DAI) | SSRN Dual-Class (Class A′) |
| :--- | :--- | :--- |
| **Mechanism** | Liquidation Auctions & Vault CR | Structured Downward Resets & Mergers |
| **Capital Efficiency** | High capital lockup ($150\%$ CR) | $100\%$ capital utilized in market tranches |
| **Instant Jump Tolerance** | Loss occurs on **$-33\%$** sudden drop | No loss until instantaneous drop exceeds **$-60\%$** |
| **Monitoring Frequency** | Continuous / Mempool auction | Hourly TWAP / Block oracle |

---

## 5. Application to Avalanche Native Stablecoin

1. **AVAX as Underlying Asset**: Replace ETH with AVAX / `sAVAX`.
2. **sAVAX Yield Integration**: The base liquid staking yield of `sAVAX` (~5-7%) can subsidize Class A coupons natively, reducing the cost of leverage for Class B.
3. **Sub-second Resets via Avalanche C-Chain**: Avalanche’s sub-second finality allows near-instantaneous reset execution, completely eliminating oracle front-running and arbitrage lag during high volatility.
4. **Teleporter / ICM Interoperability**: Class A′ stablecoins can be teleported natively to any Avalanche L1 as a zero-slippage liquidity standard.
