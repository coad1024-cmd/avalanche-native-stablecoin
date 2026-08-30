# System Architecture & Design Options

## 1. Stablecoin Archetypes under Evaluation

### A. Over-Collateralized CDP Model (Native Maker/Liquity Style)
- **Collateral Assets**: `AVAX`, `sAVAX` / Liquid Staked AVAX, BTC.b, WETH.
- **Mechanism**: Users deposit collateral into vaults and borrow the native stablecoin against their positions.
- **Key Feature**: Native staking yield from `sAVAX` collateral can automatically pay down debt or accrue to protocol reserves.

### B. Aligned Reserve Yield-Sharing Model (Inspired by ACP-67 / Discussion #293)
- **Collateral / Reserves**: Regulated dollar assets (Treasury bills, cash, USDC backing).
- **Mechanism**: Peg maintained 1:1 with institutional mint/redeem and PSM (Peg Stability Module).
- **Economic Flywheel**: 80–90% of reserve yield recycled into:
  - AVAX buyback & burn
  - Staking / validator rewards
  - Stablecoin liquidity depth incentives

### C. Hybrid Delta-Neutral / Synthetic Dollar Model
- **Collateral**: Staked AVAX long spot + short perpetual futures hedge.
- **Mechanism**: Generates basis yield from funding rates + staking yield, distributed to stablecoin holders and protocol treasury.

---

## 2. Avalanche Specific Integrations

- **Avalanche ICM & Teleporter**: Native cross-chain routing between C-Chain and sovereign Avalanche L1s without third-party bridge risks.
- **Subnet / L1 Gas Subsidies**: Native stablecoin can serve as custom gas token or liquidity quote asset on partner L1s.
- **Sub-Second Finality**: Instant liquidation settlement minimizing bad debt exposure during high volatility.
