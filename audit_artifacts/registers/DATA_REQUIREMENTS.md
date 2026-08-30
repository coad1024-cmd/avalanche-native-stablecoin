# Data Requirements Register

> **Source:** Extracted from [`SOURCE_AND_DERIVATION_AUDIT.md`](../reports/SOURCE_AND_DERIVATION_AUDIT.md) Section 7.5  
> **Last Updated:** 2026-08-30  
> **Status:** Phase 0 — No datasets ingested yet  

---

Required empirical datasets for Phase 1 calibration:

| Data Feed ID | Target Subsystem | Data Description & Source | Frequency / Granularity | Calibration & Identification Purpose |
|:---:|:---|:---|:---:|:---|
| **DAT-01** | Market SDE | AVAX/USD spot and derivatives price history (Binance, Coinbase, Trader Joe) | 1-minute / Tick | Maximum Likelihood Estimation of Kou jump parameters $(\sigma, \lambda, p, \eta_1, \eta_2)$ and Merton parameters. |
| **DAT-02** | Staking Yield | Avalanche C-Chain staking reward APR and $sAVAX$ exchange rate history | 1-hour / Epoch | Calibration of continuous yield parameter $q(t)$ and variance bounds across validation cycles. |
| **DAT-03** | DEX Order Book | Uniswap V3 / Trader Joe anUSD/USDC and AVAX/USDC pool liquidity depth profiles | Block-level / 1-sec | Empirical identification of AMM plant gain $K_{\text{amm}}$ and slippage elasticity for Reflexer PI tuning. |
| **DAT-04** | Validator OpEx | Avalanche Subnet & Primary Network validator hardware, bandwidth, and staking OpEx telemetry | Monthly survey | Estimation of validator cost curves ($C_{\text{node}} \approx \$2{,}500/\text{yr}$) to pin $\kappa_{\text{drawdown}}$. |
| **DAT-05** | Oracle Latency | Chainlink AVAX/USD round update timestamps, deviation triggers, and heartbeat delays | On-chain events | Calibration of maximum allowable staleness window $\tau_{\text{heart}}$ and TWAP breaker threshold $\Delta P_{\max}$. |
| **DAT-06** | MEV & Mempool | Avalanche C-Chain transaction mempool bids, priority tips, and flash-loan sandwich volume | Block-by-block | Empirical estimation of Maximum Profitable Manipulation Cost (MPMC) to tune $\delta_{\text{lock}}$. |
| **DAT-07** | Stress Replays | Historical Black Swan event replays (May 2021, Nov 2022 FTX, March 2023 USDC depeg) | Historical ticks | Out-of-sample backtesting of dynamic downward resets and single-step crash survival. |
