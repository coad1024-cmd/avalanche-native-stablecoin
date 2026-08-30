# Incident Log & Modeling Anti-Pattern Ledger

**Governing Standard:** BCRG Institutional Memory Canon  
**Owner:** Bonding Curve Research Group (BCRG)  
**Status:** Living Document · August 2026  

---

## Purpose
This document records every modeling error, false assumption, and edge-case failure mode discovered during the design, simulation, and verification of the **Avalanche Native Stablecoin (`anUSD`)**. Each entry records:
1. **Summary:** The symptom and how it manifested.
2. **Root Cause:** The mathematical or code error.
3. **Resolution:** The structural fix applied.
4. **Prevention Gate:** The automated test or check added to permanently prevent recurrence.

---

## Logged Incidents

### INC-001: Premature Reset Triggered by Single-Block AMM Flash Loans
* **Date:** 2026-08-15
* **Symptom:** In early simulation runs, a sudden large AMM swap pushed $V_B$ past $H_u = \$2.00$, executing an instantaneous share split and allowing the attacker to extract arbitrage profits before reverting the swap.
* **Root Cause:** The reset check evaluated raw instantaneous spot price without requiring block persistence or TWAP filtering.
* **Resolution:** Introduced the **1-Block State Delay Lock** in `ResetController.sol` and a 30-minute DEX TWAP sanity check ($\pm 8.0\%$).
* **Prevention Gate:** Gate G17 (Maximum Profitable Manipulation Cost proof).

---

### INC-002: Invariant Creep Under Naive Floating-Point Share Division
* **Date:** 2026-08-18
* **Symptom:** After 500 daily simulation steps, the solvency invariant error $|V_A + V_B - 2S|$ accumulated to $1.4 \times 10^{-4}$, violating conservation of value.
* **Root Cause:** Performing discrete token division on user share balances created compounding rounding truncation errors.
* **Resolution:** Adopted the **$O(1)$ global index rebase pattern** ($\beta(t)$ accumulator). User balances remain fixed in virtual shares, and real balances are computed on-the-fly as $\text{VirtualShares} \times \beta(t)$.
* **Prevention Gate:** Gate G10 (Machine-precision invariant check $|V_A + V_B - 2S| \le 10^{-12}$).

---

### INC-003: Double-Discounting Prorated Yields on Epoch Restarts
* **Date:** 2026-08-20
* **Symptom:** Upon upward resets, senior coupons accrued at twice the intended rate ($14.6\%$ instead of $7.3\%$).
* **Root Cause:** The temporal counter $v(t)$ was not re-anchored to $0.0$ upon epoch reset while $\beta(t)$ was simultaneously scaled.
* **Resolution:** Strictly decoupled epoch elapsed duration ($v \leftarrow 0$) from cumulative scaling factor ($\beta \leftarrow \beta \cdot \frac{P}{P_0}$).
* **Prevention Gate:** Gate G04 (PSUB 4 atomic state re-anchoring assertion).

---

### INC-004: Class B Demand Flight in Prolonged Bear Markets
* **Date:** 2026-08-22
* **Symptom:** In a 1-year downward drift scenario, speculative demand for Class $B$ dropped to zero, causing secondary AMM liquidity fragmentation.
* **Root Cause:** Class $B$ equity holders absorbed downside leverage without any cash flow cushion during downward resets.
* **Resolution:** Incorporated the **Bear-Market Coupon Subsidy ($\tilde{R} = 10.00\%$)** from SSRN-3856569 Section 2.5, transferring a positive cash distribution to Class $B$ during downward reverse splits.
* **Prevention Gate:** Gate G07 (Speculator agent demand elasticity verification).

---

### INC-005: Double-Counting Staking Yields on Buyback Conversion
* **Date:** 2026-08-24
* **Symptom:** Cumulative AVAX burned exceeded total staking yield generation by $100.0\%$.
* **Root Cause:** The yield recycler applied the $65.0\%$ buyback allocation to gross USD yield and then re-multiplied by $P_{\text{spot}}$ instead of dividing.
* **Resolution:** Standardized all token conversion equations: $\Delta B_{\text{AVAX}} = \frac{\omega_{\text{burn}} \cdot \text{Yield}_{\text{USD}}}{P_{\text{spot}}}$.
* **Prevention Gate:** Gate G13 (ACP-67 annual burn rate validation).
