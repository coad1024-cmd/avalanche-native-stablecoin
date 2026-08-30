# Claims Register — Epistemic Classification

> **Source:** Extracted from [`SOURCE_AND_DERIVATION_AUDIT.md`](../reports/SOURCE_AND_DERIVATION_AUDIT.md) Section 7.3  
> **Last Updated:** 2026-08-30  
> **Status:** Phase 0 — Unverified Research Artifact  

---

## Epistemic Taxonomy

| Class | Label | Meaning |
|:---:|:---|:---|
| **(A)** | Pure Tautology / Identity | Algebraically true by construction; tests nothing empirical |
| **(B)** | Theorem under Stated Assumptions | Mathematically proven, but validity bounded by stated assumptions |
| **(C)** | Numerical Model Implication | Follows from a specific parameterization of a computational model |
| **(D)** | Simulation Artifact | Result of in-sample simulation with known methodological limitations |
| **(E)** | Synthetic / Fabricated Construction | Derived from uncalibrated or contradictory inputs |

---

## Claims

| Claim ID | Claimed Statement | Governing Document | Epistemic Classification | Forensic Reality & Evidence |
|:---:|:---|:---|:---:|:---|
| **CLM-001** | Annualized peg volatility is strictly bounded below $2.00\%$ (Empirical: $1.3724\%$). | `claims.yaml:CLM-001`, `WHITEPAPER.tex:1.1` | **(D) Simulation Artifact** | Absence of exogenous trading noise; measures linear coupon slope variance. True vol is $2.49\% - 2.92\%$. |
| **CLM-002** | Zero principal loss for price declines up to $-60.00\%$ from $H_d$ and $-75.00\%$ from par. | `claims.yaml:CLM-002`, `WHITEPAPER.tex:Thm 1` | **(B) Theorem under Strict Bounds** | Proved analytically. However, $-75.00\%$ tolerance fails at barrier $H_d = 0.25$, causing a $37.35\%$ haircut. |
| **CLM-003** | Total NAV of active tranches exactly matches underlying collateral ($|V_A + V_B - 2S| == 0$). | `claims.yaml:CLM-003`, `WHITEPAPER.tex:Prop 1` | **(A) Pure Tautology / Identity** | Algebraic identity: $V_B \equiv 2S - V_A$. Tests Python arithmetic subtraction, not vault solvency. |
| **CLM-004** | Protocol destroys $> 100{,}000$ AVAX annually via open-market buybacks. | `claims.yaml:CLM-004`, `WHITEPAPER.tex:7.2` | **(B) Verified Economic Waterfall** | Mathematical accounting identity under ACP-67 65% burn allocation at $\$100\text{M}$ TVL. |
| **CLM-005** | Downward resets occur fewer than 3.0 times per year (Empirical: 1.15 / year). | `claims.yaml:CLM-005`, `WHITEPAPER.tex:3.2` | **(B) Theoretically Valid / Contract Buggy** | Valid under baseline SDE. However, in smart contracts, $\beta \cdot P_0$ bug causes immediate reset flapping. |
| **CLM-006** | Secondary AMM PI controller operates with damping ratio $\zeta \ge 1.0$ ($\zeta = 17.03$). | `claims.yaml:CLM-006`, `WHITEPAPER.tex:10.2` | **(E) Synthetic / Fabricated Construction** | Unreconciled contradiction between $\zeta = 1.42$ and $\zeta = 17.03$. Derived from uncalibrated plant constants. |
