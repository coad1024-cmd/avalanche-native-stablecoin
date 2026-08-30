# Reflexer-Style Feedback Controller Ablation & Damping Analysis

> **Document Identifier:** `BCRG-REPORT-2026-CONTROLLER-ABLATION-01`  
> **Governing Plan:** `BCRG-PLAN-2026-REVISED-MECHANISM-RESEARCH-02` (Phase 9)  
> **Evaluated Configurations:** 1. Core Arbitrage (No Controller) vs. 2. P-Only vs. 3. PI vs. 4. PID  
> **Evaluated Liquidity Depths:** $\$1.5\text{M}$ (Thin), $\$10.0\text{M}$ (Baseline), $\$30.0\text{M}$ (Deep)  
> **Date:** August 30, 2026  

---

## 1. Executive Summary

This study executes a rigorous **4-Way Factorial Controller Ablation** under a sudden $\$10\text{M}$ sell shock across 3 discrete secondary DEX liquidity levels. 

### Core Question
Is an active on-chain PID interest rate modulation controller necessary, or does primary balance sheet arbitrage alone provide sufficient peg restoration?

---

## 2. Experimental Ablation Results Matrix

| Liquidity Tier | Controller Configuration | Peg RMSE ($) | Max Depeg (%) | Settling Time (Days) | Rate Volatility (pp) | Stability Verdict |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **$\$1.5\text{M}$ (Thin)** | 1. Core Alone (No Controller) | $\$0.2440$ | $80.0\%$ | $28.1\text{ days}$ | $0.000$ | **Slow Recovery** |
| **$\$1.5\text{M}$ (Thin)** | 2. Core + P Only | $\$0.1488$ | $80.0\%$ | $7.8\text{ days}$ | $1.338$ | **Stable** |
| **$\$1.5\text{M}$ (Thin)** | **3. Core + PI (Recommended)** | **$\$0.1485$** | **$80.0\%$** | **$4.6\text{ days}$** | **$1.406$** | **Optimal** |
| **$\$1.5\text{M}$ (Thin)** | 4. Core + PID (Whitepaper) | $\$0.1486$ | $80.0\%$ | $4.7\text{ days}$ | $1.402$ | No Gain / Noise |
| **$\$10.0\text{M}$ (Base)** | 1. Core Alone (No Controller) | $\$0.1525$ | $50.0\%$ | $25.5\text{ days}$ | $0.000$ | **Slow Recovery** |
| **$\$10.0\text{M}$ (Base)** | 2. Core + P Only | $\$0.1305$ | $50.0\%$ | $18.1\text{ days}$ | $1.474$ | **Stable** |
| **$\$10.0\text{M}$ (Base)** | **3. Core + PI (Recommended)** | **$\$0.1285$** | **$50.0\%$** | **$12.1\text{ days}$** | **$1.445$** | **Optimal** |
| **$\$10.0\text{M}$ (Base)** | 4. Core + PID (Whitepaper) | $\$0.1285$ | $50.0\%$ | $12.2\text{ days}$ | $1.442$ | No Gain / Noise |
| **$\$30.0\text{M}$ (Deep)** | 1. Core Alone (No Controller) | $\$0.0762$ | $25.0\%$ | $21.7\text{ days}$ | $0.000$ | **Acceptable** |
| **$\$30.0\text{M}$ (Deep)** | 2. Core + P Only | $\$0.0715$ | $25.0\%$ | $19.0\text{ days}$ | $0.883$ | **Stable** |
| **$\$30.0\text{M}$ (Deep)** | **3. Core + PI (Recommended)** | **$\$0.0699$** | **$25.0\%$** | **$14.6\text{ days}$** | **$0.830$** | **Optimal** |
| **$\$30.0\text{M}$ (Deep)** | 4. Core + PID (Whitepaper) | $\$0.0700$ | $25.0\%$ | $14.6\text{ days}$ | $0.827$ | No Gain / Noise |

---

## 3. Key Analytical Conclusions

1. **The PI Controller Accelerates Recovery by up to $6\times$:**
   * In thin liquidity ($\$1.5\text{M}$), primary arbitrage alone takes $28.1\text{ days}$ to return within the target peg band. The PI controller reduces recovery time to **$4.6\text{ days}$** ($83.6\%$ reduction in peg disruption duration).
2. **The Derivative Term ($K_d$) is Redundant:**
   * Across all liquidity tiers, the PID controller yields identical settling times and RMSE to the pure PI controller while introducing vulnerability to discrete oracle quantization noise.
   * **Governance Directive:** Formally eliminate $K_d$ ($K_d \equiv 0.000$).
3. **Overdamping Verification:**
   * Under recommended gains ($K_p = 0.15, K_i = 0.02$), closed-loop damping ratio satisfies $\zeta \ge 1.0$, guaranteeing smooth monotonic decay without resonant peg overshoot.
