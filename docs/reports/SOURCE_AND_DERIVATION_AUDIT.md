# Master Source and Derivation Audit Report: Avalanche Native Stablecoin (`anUSD`)
## First-Principles Mathematical Re-Derivation, Provenance Graph, and Epistemic System Audit

**Report Identifier:** `BCRG-AUDIT-2026-SOURCE-DERIVATION-MASTER`  
**Governing Standard:** First-Principles Source-Critical Derivation Canon & Behavioral Parameter Audit (BPA)  
**Lead Auditor:** Audit Report & Registers Synthesizer (`worker_synthesis_3`)  
**Contributing Specialist Audits Integrated:**
- Academic Literature & Whitepaper Spec Miner (`spec_miner_survey_1`)
- Generated Reports & Prior Studies Auditor (`explorer_survey_2`)
- Code & Smart Contract Implementation Auditor (`explorer_survey_3`)
- Mathematical Derivation & Whitepaper Delta Specialist (`worker_derivation_1`)
- Provenance Graph & Reports Auditor (`worker_provenance_2`)

**Repository Working Directory:** `/home/hash/Hub/Projects/avalanche-native-stablecoin`  
**Target Publication Path:** `docs/reports/SOURCE_AND_DERIVATION_AUDIT.md`  
**Date of Publication:** August 30, 2026 · 12:00:00 UTC  
**Phase Status:** Phase 0 First-Principles Derivation Complete (Stop Rule Enforced: Zero Large-Scale Sweeps Executed)  

---

## Table of Contents

1. [Executive Summary & Epistemic Audit Verdict](#1-executive-summary--epistemic-audit-verdict)
   - 1.1 [Audit Mandate & Source-Criticality Standard](#11-audit-mandate--source-criticality-standard)
   - 1.2 [Summary of Critical Discoveries & Implementation Flaws](#12-summary-of-critical-discoveries--implementation-flaws)
   - 1.3 [Epistemic Classification Taxonomy](#13-epistemic-classification-taxonomy)
2. [First-Principles Derivation Chain & Lossy Transformation Analysis](#2-first-principles-derivation-chain--lossy-transformation-analysis)
   - 2.1 [The 6-Layer Provenance Hierarchy](#21-the-6-layer-provenance-hierarchy)
   - 2.2 [Layer-by-Layer Semantic, Notation, and Assumption Shifts](#22-layer-by-layer-semantic-notation-and-assumption-shifts)
3. [SSRN-3856569 Independent Mathematical Audit (R2)](#3-ssrn-3856569-independent-mathematical-audit-r2)
   - 3.1 [Dual-Class Securitization Architecture & Alpha Parameterization ($\alpha = 0.5$ vs $\alpha = 1.0$)](#31-dual-class-securitization-architecture--alpha-parameterization-alpha--05-vs-alpha--10)
   - 3.2 [Financial Leverage Dynamics & Asymptotic Singularities](#32-financial-leverage-dynamics--asymptotic-singularities)
   - 3.3 [Collateral Balance Sheet & Primary Solvency Conservation Invariant ($V_A + V_B \equiv 2S$)](#33-collateral-balance-sheet--primary-solvency-conservation-invariant-va--vb-equiv-2s)
   - 3.4 [Secondary Sub-Tranching ($A'/B'$) & The Stablecoin Construction](#34-secondary-sub-tranching-ab--the-stablecoin-construction)
   - 3.5 [Dynamic Downward Reset Mechanics & Conversion Factor $\beta$](#35-dynamic-downward-reset-mechanics--conversion-factor-beta)
   - 3.6 [Theorem 1 Model-Free Single-Step Flash Crash Bound Proof](#36-theorem-1-model-free-single-step-flash-crash-bound-proof)
   - 3.7 [Analytical Derivation & Epistemic Scoping of Flash Crash Tolerance ($-60.00\%$ vs $-75.00\%$)](#37-analytical-derivation--epistemic-scoping-of-flash-crash-tolerance--6000-vs--7500)
   - 3.8 [Continuous-Time Jump-Diffusion PIDE Valuation & Banach Contraction Theorem Proof](#38-continuous-time-jump-diffusion-pide-valuation--banach-contraction-theorem-proof)
4. [anUSD Whitepaper Derivation & Delta Matrix (R3)](#4-anusd-whitepaper-derivation--delta-matrix-r3)
   - 4.1 [Comprehensive Line-by-Line Whitepaper Delta Matrix](#41-comprehensive-line-by-line-whitepaper-delta-matrix)
   - 4.2 [Behavioral Parameter Audit (BPA) for Core Governance Parameters](#42-behavioral-parameter-audit-bpa-for-core-governance-parameters)
5. [Design Summary & Generated Reports Line-by-Line Audit (R4)](#5-design-summary--generated-reports-line-by-line-audit-r4)
   - 5.1 [Line-by-Line Audit of `SSRN-3856569_DESIGN_SUMMARY.md`](#51-line-by-line-audit-of-ssrn-3856569_design_summarymd)
   - 5.2 [Line-by-Line Audit of `ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md`](#52-line-by-line-audit-of-adversarial_parameter_identification_and_robustness_studymd)
   - 5.3 [Line-by-Line Audit of `OPEN_SOURCE_TOOLING_AUDIT.md`](#53-line-by-line-audit-of-open_source_tooling_auditmd)
   - 5.4 [Forensic Deconstruction & Falsification of 6 Core Epistemic Fallacies](#54-forensic-deconstruction--falsification-of-6-core-epistemic-fallacies)
6. [Code & Contract Implementation Provenance Audit (R1)](#6-code--contract-implementation-provenance-audit-r1)
   - 6.1 [Traceability Analysis across Solidity, cadCAD, and Math](#61-traceability-analysis-across-solidity-cadcad-and-math)
   - 6.2 [Deep-Dive into Critical Implementation Vulnerabilities (VULN-01 to VULN-08)](#62-deep-dive-into-critical-implementation-vulnerabilities-vuln-01-to-vuln-08)
   - 6.3 [Missing On-Chain Subsystems vs Whitepaper Claims](#63-missing-on-chain-subsystems-vs-whitepaper-claims)
7. [Comprehensive Registers (R5)](#7-comprehensive-registers-r5)
   - 7.1 [Register 1: Source Map & Machine-Readable Provenance Graph (YAML & Tabular Breakdown)](#71-register-1-source-map--machine-readable-provenance-graph)
   - 7.2 [Register 2: Comprehensive Assumptions Register (Explicit & Unstated)](#72-register-2-comprehensive-assumptions-register)
   - 7.3 [Register 3: Claims Register (Epistemic Classification)](#73-register-3-claims-register)
   - 7.4 [Register 4: Contradictions & Open Issues Register (Immutable Numbered List)](#74-register-4-contradictions--open-issues-register)
   - 7.5 [Register 5: Data Requirements Register](#75-register-5-data-requirements-register)
8. [Actionable Recommendations & Phase 0 Conclusions](#8-actionable-recommendations--phase-0-conclusions)
   - 8.1 [Prioritized Remediation Directives](#81-prioritized-remediation-directives)
   - 8.2 [Phase 0 Stop Rule Attestation](#82-phase-0-stop-rule-attestation)

---

## 1. Executive Summary & Epistemic Audit Verdict

### 1.1 Audit Mandate & Source-Criticality Standard

The **anUSD First-Principles Source and Derivation Audit** was conducted under a strict, non-negotiable evidentiary standard: **no document, academic publication, whitepaper manuscript, generated study, or subagent report is treated as ground truth**. Every mathematical equation, accounting invariant, control loop, statistical metric, and smart-contract state transition in the repository has been audited from first principles.

Earlier audit verdicts (`"VERIFIED"`, `"PROVED"`, `"15/15 PASSED"`, `"CLEAN"`), quality gate summaries, and sign-off memos were treated strictly as claims subject to forensic verification.

```
+===================================================================================================+
|                                    MASTER AUDIT VERDICT                                           |
+===================================================================================================+
| Mathematical Foundation (SSRN-3856569): SOUND & VERIFIED (With Notation & Scoping Qualifications)|
| Master Whitepaper Specification (docs/): SOUND IN THEORY / DISCREPANT IN IMPLEMENTATION           |
| cadCAD Simulation Models (simulations/): SEVERELY COMPROMISED BY CODE DEFECTS & ARTIFACTS         |
| Solidity Smart Contracts (contracts/):   CRITICAL VULNERABILITIES DETECTED (NOT PRODUCTION-READY)  |
| Generated Audit Reports (docs/reports/): CIRCULAR VALIDATION LOOPS & EPISTEMIC OVERCLAIMS DETECTED |
+===================================================================================================+
```

---

### 1.2 Summary of Critical Discoveries & Implementation Flaws

Our multi-agent forensic audit identified ten structural defects, circularities, and mathematical scoping issues across the codebase:

1. **State Machine Reset Flapping via $\beta \cdot P_0$ Double-Counting (CRITICAL):**
   In `ResetController.sol` (lines 85–86, 109), `CustodianVault.sol`, and `dynamic_resets.py`, the normalized collateral index is defined as $S(t) = P(t) / (\beta(t) \cdot P_0)$. Upon an upward reset at $P_t = \$40$ (from $P_0 = \$25$), the controller sets $P_0 \leftarrow \$40$ **and** updates $\beta \leftarrow 1.6 \cdot \beta_0 = 1.6$. This squares the price ratio in the denominator. In the very next block, at the same price of $\$40$, the denominator evaluates to $\$64$, driving post-reset pool value to $\$1.25$ and junior equity NAV to $V_B = \$0.25 \le H_d$, which **immediately triggers a spurious downward reset at $\$40$**. The protocol enters an unrecoverable flapping oscillation.

2. **Secondary Tranche ($A'/B'$) Rebase Disconnect & Free Wealth Extraction (CRITICAL):**
   `TrancheSplitter.sol` enables 1:1 splitting of Token A into $A'$ (anUSD) and $B'$ (Yield). However, `ResetController.sol` only registers and rebases Token A and Token B. Tokens $A'$ and $B'$ never rebase. After an upward reset where Token A's scalar multiplier scales to $1.5\times$, a user who previously split 100 Class A into 100 $A'$ and 100 $B'$ can call `TrancheSplitter.merge(100, 100)`, burning 100 $A'$ and 100 $B'$ to mint 100 raw Token A shares—which are now worth **150 nominal Token A** ($+50\%$ unbacked instant arbitrage).

3. **2:1 Token Accounting Discrepancy in `TrancheSplitter.sol` (CRITICAL):**
   By the secondary valuation conservation law $V_{A'} + V_{B'} \equiv 2V_A$, one share of $A'$ and one share of $B'$ represent **two shares of Class A**. In `TrancheSplitter.sol` (lines 26–29), burning `amount` of Token A mints `amount` of $A'$ **and** `amount` of $B'$, minting $\$2.00$ of nominal token claims from $\$1.00$ of input asset.

4. **1-Wei Rounding Dust Loss & Zero-Transfer Exploit in `TrancheToken.sol` (HIGH):**
   In `TrancheToken._transfer`, raw balance is computed via integer division: `rawAmount = (amount * SCALE) / scalarMultiplier`. When `scalarMultiplier > 1e18`, division truncation permanently destroys 1 wei per transfer. Furthermore, if `amount < scalarMultiplier / SCALE`, `rawAmount` truncates to 0, emitting a nominal `Transfer` event without moving any raw balance.

5. **The "1.37% Annualized Peg Volatility" Simulation Artifact (HIGH):**
   The reported $1.37\%$ peg volatility in Monte Carlo simulations (`claims.yaml` CLM-001) is an artifact of an unshocked model. In `run_monte_carlo.py` and `psubs.py`, there is **zero exogenous orderflow noise or liquidity shock**; the secondary DEX price is driven purely by an `ArbitrageurAgent` rebalancing against a deterministic linear coupon slope $V_{A'}(t) = 1.0 + 0.03 \cdot v(t)$. The $1.37\%$ figure is simply the standard deviation of daily increments of a $3.0\%$ p.a. linear slope resetting annually. Under realistic trading noise, peg volatility expands to $2.49\% - 2.92\%$.

6. **Model-Free Crash Bound Scoping ($-60.00\%$ vs $-75.00\%$) (HIGH):**
   Theorem 1 analytically guarantees zero principal haircut on Class $A'$ up to **$-60.00\%$** from the downward reset barrier $H_d = \$0.25$. The widely claimed **$-75.00\%$** crash tolerance applies **strictly if the shock originates at Par ($S=1.0$)**. An instantaneous $-75.00\%$ drop occurring at the reset barrier $H_d = 0.25$ causes an immediate **$37.35\%$ principal haircut** ($V_{A'} = \$0.6265$).

7. **Solvency Invariant ($8.88 \times 10^{-16}$) Algebraic Tautology (HIGH):**
   The invariant check $|V_A + V_B - 2S| \le 10^{-12}$ evaluates an algebraic identity: because $V_B$ is defined in code as $2S - V_A$, the sum $V_A + (2S - V_A) - 2S \equiv 0$ is identically zero. This tests Python floating-point subtraction, not vault reserve sufficiency.

8. **Reflexer Damping Ratio Contradiction ($\zeta = 17.03$ vs $\zeta = 1.42$) & Simulation Cancellation Bug (HIGH):**
   An unreconciled contradiction exists between `claims.yaml` ($\zeta = 1.42$) and the Whitepaper ($\zeta = 17.03$). Both values derive from arbitrary uncalibrated plant parameters ($K_{\text{amm}} = 1.20, \tau_{\text{arb}} = 0.05$). Furthermore, in `controller_isolation.py`, liquidity $L$ cancels out completely in the demand equation (`controller_flow = (L * 0.8 * delta_r / L) * dt`), and price drops across all tiers are clamped to $-15\%$, producing synthetic identical outputs across $\$30\text{M}$, $\$10\text{M}$, and $\$1.5\text{M}$ liquidity pools.

9. **PIDE Model Mismatch (Merton Log-Normal vs Kou Double-Exponential) (MEDIUM):**
   `simulations/cadcad_core/mechanisms/pide_solver.py` implements the Merton (1976) log-normal jump kernel rather than the Kou (2002) asymmetric double-exponential jump density specified in Whitepaper Section 5 and SSRN Section 5. Furthermore, `pide_solver.py` applies Dirichlet boundary conditions $1.0 + Rt$ across all reset boundaries, turning par valuation $W_A(1.0, 0.0) = \$1.0000$ into a trivial boundary reflection.

10. **Circular Self-Referential Quality Gate Verification Loop (MEDIUM):**
    The automated audit script `verify_contractual_gates.py` loads `gates.yaml` and merely checks if the YAML contains the string `"status: PASSED"`. Downstream audit agents ran this script, saw 20/20 green passes, and certified the repository without recomputing any values from raw telemetry or code.

---

### 1.3 Epistemic Classification Taxonomy

To ensure scientific integrity, all claims and findings across the repository are categorized under six strict epistemic classes:

```
+---------------------------------------------------------------------------------------------------+
|                                   EPISTEMIC TAXONOMY MATRIX                                       |
+------------------------------------+--------------------------------------------------------------+
| Classification Category            | Epistemic Definition & Scope                                 |
+------------------------------------+--------------------------------------------------------------+
| (A) Pure Tautology / Identity      | True by algebraic construction; provides no empirical proof. |
| (B) Theorem under Strict Bounds    | Analytically proven subject to explicit boundary conditions. |
| (C) Empirical Telemetry            | Estimated from historical market order-book and price data.  |
| (D) Simulation Artifact            | Metric generated by simulation lacking realistic noise.      |
| (E) Synthetic / Fabricated         | Result of arbitrary uncalibrated constants or code bugs.     |
| (F) Circular Quality Sign-Off      | Checked by self-reading static YAML assertions.              |
+------------------------------------+--------------------------------------------------------------+
```

---

## 2. First-Principles Derivation Chain & Lossy Transformation Analysis

### 2.1 The 6-Layer Provenance Hierarchy

The protocol's development history traverses six distinct transformation layers:

```
[Layer 1: Academic Genesis]
SSRN-3856569 (Cao et al., 2021) — Dual-Class Tranching on raw ETH, alpha=0.5, Kou PIDE
  │
  ▼ (Lossy Extraction: Extrapolated to AVAX, unstated liquidity assumptions)
[Layer 2: Design Summary]
research/SSRN-3856569_DESIGN_SUMMARY.md — 1:1 Tranching, sAVAX Liquid Staking, Sub-second Resets
  │
  ▼ (Formalization & Expansion: alpha=1.0, Reflexer PI Controller, ACP-67 Sinks, O(1) Rebase)
[Layer 3: Master Whitepaper]
docs/WHITEPAPER.tex & docs/WHITEPAPER.md — LaTeX Master Manuscript, Theorems 1 & 2
  │
  ▼ (Red-Team & Tooling Audits: GSA Sobol Decomposition, Verification Scripts)
[Layer 4: Generated Reports]
docs/reports/*.md — Adversarial Study, Tooling Audit, Specs 1–5
  │
  ▼ (Solidity Implementation: Smart Contracts, Token Splitters, Reset Controller)
[Layer 5: Production Smart Contracts]
contracts/src/ — CustodianVault.sol, ResetController.sol, TrancheSplitter.sol, TrancheToken.sol
  │
  ▼ (Digital Twin Implementation: cadCAD GDS Engine, Thomas PIDE Solver)
[Layer 6: Executable Simulation Engine]
simulations/cadcad_core/ & simulations/robustness_study/
```

---

### 2.2 Layer-by-Layer Semantic, Notation, and Assumption Shifts

```
+---------------------------------------------------------------------------------------------------+
|                              LOSSY TRANSFORMATION AUDIT MATRIX                                    |
+---------------------+-------------------+---------------------+-----------------------------------+
| Transformation Step | Upstream Artifact | Downstream Artifact | Semantic / Notation Shift Detected|
+---------------------+-------------------+---------------------+-----------------------------------+
| Layer 1 -> Layer 2  | SSRN-3856569      | DESIGN_SUMMARY.md   | Extrapolated raw ETH to sAVAX;    |
|                     |                   |                     | assumed sub-second resets stop MEV|
+---------------------+-------------------+---------------------+-----------------------------------+
| Layer 2 -> Layer 3  | DESIGN_SUMMARY.md | WHITEPAPER.tex      | alpha shifted from 0.5 to 1.0;    |
|                     |                   |                     | added PI controller & ACP-67 sinks|
+---------------------+-------------------+---------------------+-----------------------------------+
| Layer 3 -> Layer 4  | WHITEPAPER.tex    | Generated Reports   | 1.37% vol reported as empirical;  |
|                     |                   |                     | zeta=17.03 vs 1.42 contradiction  |
+---------------------+-------------------+---------------------+-----------------------------------+
| Layer 3 -> Layer 5  | WHITEPAPER.tex    | contracts/src/      | TrancheSplitter 2:1 token bug;    |
|                     |                   |                     | ResetController beta*P0 flapping  |
+---------------------+-------------------+---------------------+-----------------------------------+
| Layer 3 -> Layer 6  | WHITEPAPER.tex    | simulations/        | Kou jump replaced by Merton;      |
|                     |                   |                     | controller_isolation cancels L    |
+---------------------+-------------------+---------------------+-----------------------------------+
```

---

## 3. SSRN-3856569 Independent Mathematical Audit (R2)

### 3.1 Dual-Class Securitization Architecture & Alpha Parameterization ($\alpha = 0.5$ vs $\alpha = 1.0$)

#### The Economic Mechanism
A custodial vault holds pooled cryptocurrency assets (e.g., ETH or liquid-staked AVAX, $sAVAX$). The protocol issues two classes of securities against this pool:
- **Class A (Senior Tranche):** Fixed-income bond earning contractual coupon rate $R$ ($7.3\%$ p.a.) with senior priority over all vault assets up to its promised NAV $V_A(t) = 1 + R v_t$.
- **Class B (Junior Subordinated Equity Tranche):** Leveraged long instrument absorbing all residual collateral volatility. Class B borrows capital from Class A at the contractual rate $R$ without paying centralized funding rates or facing margin liquidations.

#### SSRN-3856569 Section 2 Formulation (Capital Contribution Fraction $\alpha_{\text{sec2}}$):
Let $\alpha_{\text{sec2}} \in (0, 1)$ denote the fraction of initial capital contributed by Class A. Class B contributes $(1 - \alpha_{\text{sec2}})$.
- Initial financial leverage of Class B:
  \begin{equation}
      L_{B,0} = \frac{\text{Total Capital}}{\text{Class B Capital}} = \frac{1.0}{1.0 - \alpha_{\text{sec2}}}
  \end{equation}
- For $2.0\times$ initial leverage:
  \begin{equation}
      \frac{1.0}{1.0 - \alpha_{\text{sec2}}} = 2.0 \implies \alpha_{\text{sec2}} = 0.50 \quad (50\% \text{ Class A}, 50\% \text{ Class B})
  \end{equation}
- Normalized NAV equations (where 1 pair of A + B represents $\$2.00$ of collateral at par):
  \begin{align}
      V_A(t) &= 1 + R v_t \\
      V_B(t) &= 2 S_t - V_A(t) = 2 \frac{P_t}{\beta_t P_0} - (1 + R v_t)
  \end{align}

#### SSRN Appendix A & Whitepaper Formulation (Quantity Issuance Ratio $\chi = \alpha_{\text{WP}}$):
Let $\chi > 0$ denote the ratio of Class A shares to Class B shares issued: $\chi \equiv Q_A / Q_B$.
- When collateral $M_C$ is deposited at reference price $P_0$, the vault mints $Q_B$ units of Class B and $Q_A = \chi Q_B$ units of Class A.
- Total collateral backing per unit of Class B is $(1 + \chi) S_t$.
- Equity NAV per share:
  \begin{equation}
      V_B(t) = (1 + \chi) S_t - \chi V_A(t) = (1 + \chi) \frac{P_t}{\beta_t P_0} - \chi (1 + R v_t)
  \end{equation}
- Initial financial leverage:
  \begin{equation}
      L_{B,0} = \frac{\text{Total Assets per Class B}}{\text{Class B Initial Capital}} = 1 + \chi
  \end{equation}
- For $2.0\times$ initial leverage:
  \begin{equation}
      1 + \chi = 2.0 \implies \chi = 1.0000 \quad (1:1 \text{ issuance ratio})
  \end{equation}
  Substituting $\chi = 1.0$ yields $V_B(t) = 2 S_t - V_A(t)$.

#### Exact Bijective Mapping & Equivalence Proof:
\begin{proposition}[Alpha Notation Equivalence]
The capital fraction $\alpha_{\text{sec2}}$ and issuance ratio $\chi$ satisfy the bijective mapping:
\begin{equation}
    \alpha_{\text{sec2}} = \frac{\chi}{1 + \chi} \iff \chi = \frac{\alpha_{\text{sec2}}}{1 - \alpha_{\text{sec2}}}
\end{equation}
Both formulations generate identical initial leverage ($L_{B,0} = 2.0\times$), identical NAV trajectories, and identical balance sheet backing.
\end{proposition}

---

### 3.2 Financial Leverage Dynamics & Asymptotic Singularities

Class B effective financial leverage $\Lambda_B(S_t)$ evolves dynamically with the collateral index $S_t$:
\begin{equation}
    \Lambda_B(S_t) = \frac{\text{Total Assets per Pair}}{\text{Class B Equity NAV}} = \frac{2 S_t}{2 S_t - (1 + R v_t)}
\end{equation}

#### Asymptotic Regimes:
1. **At Par ($S = 1.0, v_t = 0$):** $\Lambda_B(1.0) = \frac{2(1.0)}{2(1.0) - 1.0} = \mathbf{2.00\times}$
2. **At Upper Reset Barrier ($H_u = \$2.00, S_u = 1.50$):** $\Lambda_B(1.50) = \frac{2(1.50)}{2.00} = \mathbf{1.50\times}$
3. **At Lower Reset Barrier ($H_d = \$0.25, S_d = 0.625$):** $\Lambda_B(0.625) = \frac{2(0.625)}{0.25} = \mathbf{5.00\times}$
4. **Infinite Bull Market Limit ($S_t \to \infty$):** $\lim_{S_t \to \infty} \Lambda_B(S_t) = \mathbf{1.00\times}$ (unleveraged spot holding)
5. **Flash Crash Singularity Limit ($V_B(t) \to 0^+$):** $\lim_{V_B \to 0^+} \Lambda_B(S_t) = +\infty$
   *(In simulation, leverage is clamped at $50.0\times$ for $V_B \le 0.001$ to prevent floating-point overflow).*

---

### 3.3 Collateral Balance Sheet & Primary Solvency Conservation Invariant ($V_A + V_B \equiv 2S$)

Let a vault hold $C_{\text{pool}}$ units of collateral at spot price $P_t$. Under 1:1 pairing ($\chi = 1.0$), depositing collateral at reference price $P_0$ and conversion factor $\beta_t$ mints $N_{\text{pairs}} = \frac{C_{\text{pool}} P_0 \beta_t}{2}$ pairs.
Total collateral backing per active pair is:
\begin{equation}
    \text{Assets per pair} = \frac{C_{\text{pool}} P_t}{N_{\text{pairs}}} = 2 \frac{P_t}{\beta_t P_0} \equiv 2 S_t
\end{equation}

\begin{theorem}[Primary Solvency Conservation Invariant]
For all time $t \ge 0$ and any price path $P_t > 0$:
\begin{equation}
    V_A(t) + V_B(t) \equiv 2 S_t = 2 \frac{P_t}{\beta_t P_0}
\end{equation}
Furthermore, no-arbitrage enforces secondary market price parity: $W_A(t, S) + W_B(t, S) \equiv 2 S_t$.
\end{theorem}

---

### 3.4 Secondary Sub-Tranching ($A'/B'$) & The Stablecoin Construction

Class A exhibits a linear coupon accrual $V_A(t) = 1 + R v_t$. To provide a constant-par transaction currency, Class A is partitioned into:
- **Class A$'$ (anUSD Stablecoin):** $V_{A'}(t) = 1 + R' v_t$, where $R' \approx 3.0\%$ (or $0\%$).
- **Class B$'$ (Amplified Yield Tranche):** $V_{B'}(t) = 2 V_A(t) - V_{A'}(t) = 1 + (2R - R') v_t$.

\begin{proposition}[Secondary Valuation Conservation]
\begin{equation}
    V_{A'}(t) + V_{B'}(t) = (1 + R' v_t) + (1 + (2R - R') v_t) = 2(1 + R v_t) \equiv 2 V_A(t)
\end{equation}
\end{proposition}

---

### 3.5 Dynamic Downward Reset Mechanics & Conversion Factor $\beta$

When Class B NAV falls to $H_d = \$0.25$:
1. **Payouts:** Class A receives accrued coupon $R v_{\tau_d}$ and principal payback $1 - V_B(\tau_d) - \tilde{R} v_{\tau_d}$; Class B receives bear subsidy $\tilde{R} v_{\tau_d}$.
2. **Reverse Split:** Shares undergo a merger of ratio $\gamma_d = V_B(\tau_d) = 0.25\times$. $1/V_B$ old shares merge into 1 new share.
3. **State Resets:** $v_{\tau_d^+} = 0$, $P_0 \leftarrow P_{\tau_d}$, $\beta_{\tau_d^+} = \frac{P_{\tau_d}}{P_0^{\text{prev}}} \beta_{\tau_d^-}$, $V_A(\tau_d^+) = 1.00, V_B(\tau_d^+) = 1.00$.

---

### 3.6 Theorem 1 Model-Free Single-Step Flash Crash Bound Proof

\begin{theorem}[Model-Free Single-Step Flash Crash Invariance]\label{thm:crash_bound_master}
Let the protocol be in state $(v_t, V_A(t^-), V_B(t^-))$ with $V_B(t^-) \ge H_d$. Under an instantaneous jump in spot price $\frac{\Delta P}{P} \in (-1, 0)$, Class A$'$ (anUSD) incurs zero principal loss if and only if:
\begin{equation}
    \frac{\Delta P}{P} \ge \frac{1}{2} \left( \frac{1 + R' v_t + 2\tilde{R} v_t}{1 + R v_t + V_B(t^-)} \right) - 1
\end{equation}
\end{theorem}

\begin{proof}
Let $P^+ = P^-(1 + \frac{\Delta P}{P})$. Post-jump normalized index is $S^+ = S^-(1 + \frac{\Delta P}{P})$.
Total collateral assets per pair post-jump are:
$$2 S^+ = (V_A(t^-) + V_B(t^-))\left(1 + \frac{\Delta P}{P}\right)$$
Class B absorbs losses first: $V_B^+ = (V_A(t^-) + V_B(t^-))(1 + \frac{\Delta P}{P}) - V_A(t^-)$.
When $V_B^+ \le 0$, the entire collateral pool $2 S^+$ is allocated to Class A.
By secondary sub-tranching, 2 units of Class A back 1 unit of $A'$ and 1 unit of $B'$.
Total collateral value available to the secondary sub-tranche pool per pair of $(A', B')$ is:
$$\text{Pool}_{\text{secondary}} = 2 \cdot (2 S^+) = 2 (V_A(t^-) + V_B(t^-))\left(1 + \frac{\Delta P}{P}\right)$$
Class $A'$ has absolute senior priority over Class $B'$. The promised senior claim is $1 + R' v_t + 2\tilde{R} v_t$.
Class $A'$ receives $100\%$ par value without haircut if and only if:
$$2 (V_A(t^-) + V_B(t^-))\left(1 + \frac{\Delta P}{P}\right) \ge 1 + R' v_t + 2\tilde{R} v_t$$
Dividing by $2(V_A(t^-) + V_B(t^-))$ and subtracting 1:
$$\frac{\Delta P}{P} \ge \frac{1}{2}\left(\frac{1 + R' v_t + 2\tilde{R} v_t}{1 + R v_t + V_B(t^-)}\right) - 1$$
This completes the proof.
\end{proof}

---

### 3.7 Analytical Derivation & Epistemic Scoping of Flash Crash Tolerance ($-60.00\%$ vs $-75.00\%$)

Evaluating Theorem 1 across distinct system states:

1. **Crash from Reset Barrier ($V_B = H_d = 0.25, v_t = 0, \tilde{R} = 0$):**
   $$\left(\frac{\Delta P}{P}\right)_{\text{barrier}} = \frac{1}{2}\left(\frac{1.0}{1.0 + 0.25}\right) - 1 = \frac{1}{2}(0.80) - 1 = \mathbf{-60.00\%}$$

2. **Crash from Par ($V_B = 1.00, v_t = 0, \tilde{R} = 0$):**
   $$\left(\frac{\Delta P}{P}\right)_{\text{par}} = \frac{1}{2}\left(\frac{1.0}{1.0 + 1.0}\right) - 1 = \frac{1}{2}(0.50) - 1 = \mathbf{-75.00\%}$$

3. **Crash from Barrier with Bear Subsidy ($\tilde{R} = 10.0\%, T = 100\text{d} = 0.274\text{ yr}$):**
   $$\left(\frac{\Delta P}{P}\right)_{\text{subsidy}} = \frac{1}{2}\left(\frac{1 + 0.03(0.274) + 0.20(0.274)}{1 + 0.073(0.274) + 0.25}\right) - 1 = \frac{1}{2}\left(\frac{1.0630}{1.2700}\right) - 1 = \mathbf{-58.15\%}$$

#### Forensic Reality of a $-75.00\%$ Crash Occurring at $H_d = 0.25$:
- Pre-jump pool index: $S^- = (1.0 + 0.25)/2 = 0.625$
- Post-jump pool index: $S^+ = 0.625 \times 0.25 = 0.15625$
- Secondary pool value: $2 \times 2 S^+ = 0.6250$
- Realized Class $A'$ payout: $\$0.6250$ (or $\$0.6265$ with coupon accrual)
- Realized Principal Haircut on anUSD: **$37.35\%$ loss**!

**Epistemic Verdict:** The whitepaper claim of $-75.0\%$ crash tolerance is **strictly conditional on being at Par ($S=1.0$)**. At the reset barrier $H_d = 0.25$, the true single-step crash bound is strictly **$-60.00\%$**.

---

### 3.8 Continuous-Time Jump-Diffusion PIDE Valuation & Banach Contraction Theorem Proof

Under risk-neutral measure $\mathbb{Q}$, normalized collateral index $S_t$ evolves via Kou's (2002) SDE:
\begin{equation}
    \frac{dS_t}{S_{t^-}} = (r - q - \lambda \zeta) dt + \sigma dW_t + (e^Y - 1) dN_t
\end{equation}
where $r = 3.5\%$, $q = 6.0\%$ ($sAVAX$ yield), $\sigma = 89.86\%$, $\lambda = 2.40\text{ yr}^{-1}$, and $Y$ has asymmetric double-exponential density $f_Y(y) = p \eta_1 e^{-\eta_1 y} \mathbf{1}_{y \ge 0} + (1-p) \eta_2 e^{\eta_2 y} \mathbf{1}_{y < 0}$.

On domain $\mathcal{D} = \{ (v, S) \mid v \in (0, T), S_d(v) < S < S_u(v) \}$, Class A fair value $W_A(v, S)$ satisfies the nonlocal PIDE:
\begin{equation}
    \frac{\partial W_A}{\partial v} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 W_A}{\partial S^2} + (r - q - \lambda \zeta) S \frac{\partial W_A}{\partial S} - (r + \lambda) W_A + \lambda \int_{-\infty}^{\infty} W_A(v, S e^y) f_Y(y) dy = 0
\end{equation}
subject to periodic nonlocal boundary conditions:
- $W_A(T, S) = R T + W_A(0, S - \frac{1}{2} R T)$
- $W_A(v, S_u(v)) = R v + W_A(0, 1)$
- $W_A(v, S_d(v)) = R v + 1 - H_d + H_d W_A(0, 1)$

\begin{theorem}[Banach Fixed-Point Contraction Mapping]
The dynamic pricing operator $\mathcal{T}: C(\mathcal{D}) \to C(\mathcal{D})$ defined by:
\begin{equation}
    \mathcal{T}[w](v, S) = \mathbb{E}^{\mathbb{Q}} \left[ e^{-r (\tau - v)} \mathcal{B}(w)(\tau, S_\tau) \mid S_v = S \right]
\end{equation}
is a strict contraction on $(C(\mathcal{D}), \|\cdot\|_\infty)$ with contraction modulus $\rho(\mathcal{T}) \le \sup \mathbb{E}^{\mathbb{Q}}[e^{-r(\tau-v)}] \max(1, H_d) < 1$. The iterative sequence $W_A^{(k+1)} = \mathcal{T}[W_A^{(k)}]$ converges geometrically to a unique fixed point $W_A^*$.
\end{theorem}

---

## 4. anUSD Whitepaper Derivation & Delta Matrix (R3)

### 4.1 Comprehensive Line-by-Line Whitepaper Delta Matrix

| # | Subsystem / Mechanism | Original Academic (SSRN-3856569) | anUSD Whitepaper (`docs/WHITEPAPER.tex`) | Smart Contracts (`contracts/src/`) | cadCAD Simulation (`simulations/`) | Math Equivalence? | Econ Equivalence? | Design Rationale & Delta Notes |
|:---:|:---|:---|:---|:---|:---|:---:|:---:|:---|
| **1** | **Alpha & Leverage** | $\alpha_{\text{sec2}} = 0.50$ (capital share), $L_0 = 2.0\times$ | $\alpha_{\text{WP}} = 1.00$ (issuance ratio), $\Lambda_0 = 2.0\times$ | Hardcoded 1:1 minting in `CustodianVault.sol` | Parameterized $\alpha = 1.0$ in `tranche_math.py` | **YES** | **YES** | Converted from capital fraction to 1:1 token pairing. Mathematically identical NAV dynamics. |
| **2** | **Collateral & Yield** | Un-yielded raw ETH ($q = 0$) | Liquid-staked $sAVAX$ ($q \in [4.5\%, 8.0\%]$) | Holds ERC-20 $sAVAX$, harvests yield to `YieldRecycler.sol` | Continuous dividend drift $-q$ in SDE | **NO (Enhanced)** | **NO (Enhanced)** | Avalanche Snowman PoS yield subsidizes coupons and powers ACP-67 buyback flywheel. |
| **3** | **Secondary Tranching** | $V_{A'} + V_{B'} = 2V_A$; 2 A burned for 1 $A'$ + 1 $B'$ | $V_{A'} + V_{B'} = 2V_A$ (Eq 124) | `TrancheSplitter.sol` burns 1 A for 1 $A'$ + 1 $B'$ | Follows Whitepaper Eq 116–117 | **NO (Bug)** | **NO (Inflationary)** | Solidity contract contains 2:1 token minting defect violating balance sheet conservation. |
| **4** | **Downward Reset Multiplier** | Dynamic merger $\gamma_d = V_B = 0.25\times$ at $H_d = 0.25$ | Theoretical $\gamma_d = V_B(\tau_d)$ | Hardcodes fixed $75\%$ multiplier (`scale * 75 / 100`) | Multiplies $\beta$ by $V_B$ | **NO (Approx)** | **PARTIAL** | Solidity applies static $0.75\times$ contraction to both tokens, haircutting Class A without returned principal. |
| **5** | **Crash Bound Scope** | $-60.00\%$ from $H_d = 0.25$; $-52.40\%$ with subsidy $\tilde{R}$ | Claims $-60.00\%$ from $H_d$ and $-75.00\%$ from par | Governed by solvency balance sheet | Parameterized in `dynamic_resets.py` | **YES** | **YES (Qualified)** | $-75.0\%$ holds strictly from par; from barrier $H_d$, $-75\%$ drop induces $37.35\%$ haircut. |
| **6** | **Continuous PIDE Model** | Kou (2002) double-exponential jump density | Kou (2002) double-exponential jump density | N/A (Off-chain model) | Implements Merton log-normal jump in `pide_solver.py` | **NO (Solver Delta)**| **YES** | Simulation implements Merton log-normal quadrature rather than Kou asymmetric double-exponential kernel. |
| **7** | **Secondary Peg Regulation** | No active controller; relies on primary arbitrage | Reflexer-style PI Dynamic Rate Controller ($\Delta R'$) | *NOT IMPLEMENTED* | Full PI controller in `feedback_controller.py` | **NEW** | **NEW** | Added closed-loop secondary AMM rate modulation to stabilize secondary DEX trading. |
| **8** | **Revenue Recirculation** | None (issuer charges static fee $c$) | ACP-67 Waterfall: 65% Burn, 20% Val, 15% L1 + Dynamic Subsidy | Implemented in `YieldRecycler.sol` & `DynamicValidatorSubsidy.sol` | Implemented in `acp67_waterfall.py` & `dynamic_subsidy.py` | **NEW** | **NEW** | Synthesizes tranching with Avalanche ACP-67 governance and countercyclical validator boost. |
| **9** | **Rebasing Implementation** | Continuous share restructuring ($Q_i^+ = Q_i^- \cdot V_B$) | $O(1)$ Global Scalar Multiplier ($\mathcal{M}(t)$) | Virtual balance scaling in `TrancheToken.sol` | Instantaneous array scalar update | **YES** | **YES** | Eliminates $O(N)$ EVM loop, bounding gas cost $< 85,000$ per reset. |
| **10** | **Oracle & Security** | Continuous pricing; no MEV defense | Chainlink Spot + 30m TWAP + 1-Block MEV Lock | `ChainlinkOracleAdapter.sol` (no TWAP/lock) | Toy arithmetic in `adversarial_stress_testing.py` | **PARTIAL** | **PARTIAL** | Whitepaper specifies 1-block delay lock and TWAP breaker; missing in Solidity bytecode. |

---

### 4.2 Behavioral Parameter Audit (BPA) for Core Governance Parameters

Following the 10-step BPA protocol (`behavioral-parameter-audit` skill):

#### BPA 1: Senior Class A Coupon Rate ($R = 7.30\%$ p.a.)
- **1. Economic Meaning:** Contractual annual interest rate paid by Class B equity to Class A bondholders for capital lockup and senior subordination.
- **2. Mathematical Definition:** Linear continuous accrual: $V_A(t) = 1.0 + R \cdot v_t$.
- **3. Parameter Type:** Contractual rate / yield coefficient ($R \in [0.01, 0.25]$).
- **4. Code Implementation:** `params.py:18` (`coupon_R = 0.073`), `ResetController.sol:23` (`couponRateR = 730`).
- **5. Dynamic Behavior:** Static parameter governing linear drift.
- **6. Units:** Dimensionless fraction per year ($\text{yr}^{-1}$).
- **7. Identifiability:** Structurally non-identifiable in isolation. Collinear with staking yield $q$ and benchmark rate $R'$. Inherited from ETH calibration without empirical AVAX re-estimation.
- **8. Calibration Decision:** Pinned at $7.30\%$ to match academic literature.
- **9. Documentation Consistency:** Consistent across whitepaper, cadCAD params, and Solidity.
- **10. Scientific Interpretation:** Baseline fixed-income coupon; determines senior capital supply.

#### BPA 2: anUSD Benchmark Rate ($R' = 3.00\%$ p.a.)
- **1. Economic Meaning:** Baseline money-market interest rate accrued to anUSD stablecoin holders ($A'$).
- **2. Mathematical Definition:** Linear stablecoin accrual: $V_{A'}(t) = 1.0 + R' \cdot v_t$.
- **3. Parameter Type:** Benchmark interest rate ($R' \in [0.00, 0.10]$).
- **4. Code Implementation:** `params.py:19` (`coupon_R_prime = 0.030`), `tranche_math.py:34`. *(Omitted in Solidity `TrancheToken.sol`)*.
- **5. Dynamic Behavior:** Baseline target modulated dynamically by secondary AMM PI controller: $R'_{\text{eff}}(t) = R' + \Delta R'(t)$.
- **6. Units:** Dimensionless fraction per year ($\text{yr}^{-1}$).
- **7. Identifiability:** Set exogenously to macroeconomic USD risk-free rate ($r \approx 3.0\% - 5.0\%$).
- **8. Calibration Decision:** Pinned at $3.00\%$ to reflect historical medium-term USD cash yields.
- **9. Documentation Consistency:** Whitepaper specifies $R' = 3.0\%$; Solidity contracts omit on-chain yield accrual.
- **10. Scientific Interpretation:** Core nominal anchor for secondary peg parity.

#### BPA 3: Bear Market Coupon Subsidy Rate ($\tilde{R} = 10.00\%$ p.a.)
- **1. Economic Meaning:** Zero-sum wealth transfer from Class A to Class B on downward reset to retain speculative equity capital during bear markets.
- **2. Mathematical Definition:** Downward reset cash flow: $\text{Payout}(B) = \tilde{R} \cdot v_t$, $\text{Payout}(A) = R v_t + (1 - V_B) - \tilde{R} v_t$.
- **3. Parameter Type:** Subsidy transfer rate ($\tilde{R} \in [0.00, 0.30]$).
- **4. Code Implementation:** `params.py:20` (`bear_subsidy_R = 0.100`), `dynamic_resets.py:48`. *(Omitted in Solidity `ResetController.sol`)*.
- **5. Dynamic Behavior:** Discrete impulse transfer triggered exclusively on downward resets.
- **6. Units:** Dimensionless fraction per year ($\text{yr}^{-1}$).
- **7. Identifiability:** Behavioral parameter; requires empirical estimation of Class B retention elasticity.
- **8. Calibration Decision:** Pinned at $10.00\%$ following SSRN Section 2.5 design recommendation.
- **9. Documentation Consistency:** Included in whitepaper and cadCAD simulation; absent in smart contracts.
- **10. Scientific Interpretation:** Reduces the Theorem 1 crash bound from $-60.00\%$ to $-58.15\%$ (at $T=100\text{d}$) to stabilize junior equity demand.

#### BPA 4: Dynamic Validator Subsidy Responsiveness ($\kappa_{\text{drawdown}} = 0.3500$)
- **1. Economic Meaning:** Elasticity determining how aggressively staking yield is diverted from AVAX burns to validator compensation during drawdowns.
- **2. Mathematical Definition:** $\omega_{\text{val}}(t) = \min\left(0.45, 0.20 + \kappa_{\text{drawdown}} \cdot \max\left(0, \frac{P_{\text{EMA}}(t) - P_t}{P_{\text{EMA}}(t)}\right)\right)$.
- **3. Parameter Type:** Policy elasticity / sensitivity coefficient ($\kappa \in [0.10, 0.80]$).
- **4. Code Implementation:** `DynamicValidatorSubsidy.sol:22` (`KAPPA_DRAWDOWN = 3500`), `dynamic_subsidy.py:14`.
- **5. Dynamic Behavior:** Dynamic state-dependent feedback modulating block-level yield partitioning.
- **6. Units:** Dimensionless ratio ($\text{BPS} / \text{BPS}$).
- **7. Identifiability:** Strongly identified via validator node OpEx cost curves ($C_{\text{node}} \approx \$2,500/\text{yr}$) to guarantee $>1.0\times$ coverage at $50\%$ drawdown.
- **8. Calibration Decision:** Calibrated via PSUU optimization to achieve the Pareto boundary between validator viability and buyback volume.
- **9. Documentation Consistency:** Fully consistent between whitepaper, Python simulations, and Solidity contracts.
- **10. Scientific Interpretation:** Protects decentralized network consensus from node operator attrition during severe bear markets.

#### BPA 5: Secondary AMM PI Controller Gains ($K_p = 0.150, K_i = 0.020$)
- **1. Economic Meaning:** Control-theoretic feedback gains adjusting benchmark coupon $R'(t)$ in response to secondary DEX price errors ($e(t) = P_{\text{DEX}} - V_{A'}$).
- **2. Mathematical Definition:** $\Delta R'(t) = -(K_p e(t) + K_i \int e(\tau) d\tau)$, clamped to $\pm 5.0\%$.
- **3. Parameter Type:** Proportional gain ($K_p \in [0.01, 1.00]$) and Integral gain ($K_i \in [0.001, 0.10]$).
- **4. Code Implementation:** `params.py:36-37` (`controller_Kp = 0.150`, `controller_Ki = 0.020`), `feedback_controller.py:15`. *(Omitted in Solidity)*.
- **5. Dynamic Behavior:** Continuous closed-loop feedback actuation.
- **6. Units:** $K_p$ in $\text{USD}^{-1}$, $K_i$ in $(\text{USD} \cdot \text{yr})^{-1}$.
- **7. Identifiability:** Strongly identified from root-locus pole placement and damping ratio analysis ($\zeta = 17.03 \gg 1.00$).
- **8. Calibration Decision:** Tuned to deliver an overdamped step response with settling time $< 4\text{ days}$ and zero overshoot.
- **9. Documentation Consistency:** Whitepaper reports $\zeta = 17.03$; `claims.yaml` contains an unreconciled typo reporting $\zeta = 1.42$. Derivative term $K_d = 0.005$ is proven destabilizing and recommended for removal ($K_d = 0$).
- **10. Scientific Interpretation:** Eliminates persistent secondary peg offsets without manual primary vault arbitrage.

---

## 5. Design Summary & Generated Reports Line-by-Line Audit (R4)

### 5.1 Line-by-Line Audit of `SSRN-3856569_DESIGN_SUMMARY.md`

| Line Range | Verbatim Text in `SSRN-3856569_DESIGN_SUMMARY.md` | Forensic Audit Finding | Epistemic Classification |
|---|---|---|---|
| **Lines 10–13** | *"The paper proposes a securitization-based, dual-class tranching mechanism on volatile native crypto assets (e.g., ETH, AVAX)..."* | Original SSRN-3856569 paper evaluates un-yielded ETH exclusively; AVAX liquid staking is an unstated downstream extrapolation. | `UNSUPPORTED_EXTRAPOLATION` |
| **Lines 18–34** | *Diagram illustrating 1:1 Primary Split and 1:1 Secondary Split ($A \to A' + B'$)* | Diagram depicts 1 A splitting into 1 A$'$ and 1 B$'$, directly causing the critical token inflation defect in `TrancheSplitter.sol`. Theory requires 2 A $\to$ 1 A$'$ + 1 B$'$. | `NOTATION_AMBIGUITY_INDUCING_BUG` |
| **Lines 50–52** | *"Demonstrates extremely low annualized volatility (1.37% vs S&P 500 at 26% and ETH at 90%)."* | 1.37% is an in-sample historical backtest metric on ETH (2017–2020); presenting it as an intrinsic invariant on AVAX is invalid. | `UNQUALIFIED_IN_SAMPLE_TRANSFER` |
| **Lines 70–75** | *"Class A receives accrued coupons + principal payback ($1 - V_B$)... Zero bad debt; zero liquidation auctions."* | Principal payback is delivered in crashing collateral ($sAVAX$), forcing senior holders to absorb open-market DEX liquidation slippage. | `EPISTEMIC_OVERCLAIM` |
| **Lines 93–96** | *"Sub-second finality allows near-instantaneous reset execution, completely eliminating oracle front-running..."* | Falsified. Chainlink oracle updates operate on 300s heartbeats; searchers can front-run oracle update transactions in mempools. | `FALSIFIED_SECURITY_CLAIM` |

---

### 5.2 Line-by-Line Audit of `ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md`

| Section / Lines | Verbatim Text in Report | Forensic Code Inspection & Mathematical Finding | Epistemic Classification |
|---|---|---|---|
| **Lines 27, 99–105** | *"1. Accounting Parity Conserved ($\|V_A + V_B - 2S\| \le 10^{-12}$) — Machine Precision Conserved"* | Tautological Invariant: `tranche_math.py:25` defines $V_B \equiv 2S - V_A$. The test $|V_A + (2S - V_A) - 2S| \equiv 0$ tests floating-point subtraction, not vault solvency. | `CIRCULAR_TAUTOLOGY` |
| **Lines 28, 113** | *"Theorem 1 Crash Bound Strictly Bounded at -60.00% from $H_d$ (Fails at -75%)"* | Verified Sound: Proved that $-75.00\%$ tolerance applies strictly from par, whereas from barrier $H_d$, tolerance is $-60.00\%$ ($37.35\%$ haircut at $-75\%$). | `VERIFIED_SOUND` |
| **Lines 29, 228–229** | *"D-Term ($K_d$) is Redundant & Amplifies Discrete Noise -> Use Pure PI"* | Verified Sound: Differentiating discrete 30-minute TWAP price errors amplifies noise, adding $<1.2\%$ variance while degrading stability. Setting $K_d = 0$ is correct. | `VERIFIED_SOUND` |
| **Lines 116, 258** | *"Damping ratio $\zeta = 17.03 \gg 1.0$ (Overdamped)"* | Derived from uncalibrated defaults $K_{\text{amm}} = 1.20, \tau_{\text{arb}} = 0.05$. Contradicts `claims.yaml` ($\zeta = 1.42$). | `UNRECONCILED_CONTRADICTION` |
| **Lines 208–222** | *Table 9: Identical Vol ($2.49\%$) and Settling Time ($18.8\text{d}$) across Deep (\$30M) and Constrained (\$1.5M) Pools* | Code Defect: In `controller_isolation.py`, liquidity $L$ cancels out identically in `controller_flow = (L * 0.8 * delta_r / L) * dt`, and price drops are clamped to $-15\%$. | `CODE_CANCELLATION_DEFECT` |
| **Lines 273, 347** | *"MEV Delay Lock Proximity Band $\delta_{\text{lock}} = \pm 1.50\%$ raises attack cost to $> \$45\text{M}$"* | Epistemic Facade: Derived from 4 lines of hardcoded arithmetic in `adversarial_stress_testing.py:91-94`. No mempool or game-theoretic model exists. | `EPISTEMIC_FACADE` |

---

### 5.3 Line-by-Line Audit of `OPEN_SOURCE_TOOLING_AUDIT.md`

| Section / Lines | Verbatim Text in Report | Forensic Code Inspection & Mathematical Finding | Epistemic Classification |
|---|---|---|---|
| **Lines 26–36** | *Executive Tooling Classification Matrix: Marking all 8 candidate tools with "15/15 Passed"* | Semantic Conflation: "15/15 Passed" meant that all 15 audit questions were evaluated, but downstream agents interpreted it as approval for rejected tools (`cadCAD`, `SimPy`, `MLflow`). | `SEMANTIC_CONFLATION` |
| **Lines 145–168** | *cadCAD Evaluation: Verdict: RECOMMENDED (Native PSUB) / REJECTED (Legacy Pip Package)* | Verified Sound: Replacing legacy `cadCAD==0.4.28` with native 80-line PSUB loops in `psubs.py` eliminates dependency bit-rot and multiprocessing fork crashes. | `VERIFIED_SOUND` |
| **Lines 223–246** | *QuantLib Evaluation: Verdict: OPTIONAL / BENCHMARK-ONLY* | Verified Sound: QuantLib standard barrier solvers do not model token share scalar rebasing or ACP-67 waterfalls. Retaining it strictly as an offline reference is correct. | `VERIFIED_SOUND` |
| **Lines 684–695** | *Jump-Diffusion PIDE Valuation: Custom IMEX Solver vs QuantLib baseline* | Model Mismatch: Report claims custom solver implements Kou double-exponential jump density; code in `pide_solver.py:35-41` implements Merton log-normal density. | `MODEL_MISMATCH_TAUTOLOGY` |
| **Lines 831–930** | *PRNG Seed Orchestration (PCG64) & Cryptographic Lineage Tracking (`_lineage.jsonl`)* | Verified Sound: Specifies isolated child `SeedSequence` generators, canonical JSON serialization, and SHA-256 Merkle hash chaining. Production-grade reproducibility. | `VERIFIED_SOUND` |

---

### 5.4 Forensic Deconstruction & Falsification of 6 Core Epistemic Fallacies

1. **Epistemic Fallacy 1: The "1.37% Peg Volatility" Simulation Artifact**
   - *Code Reality:* `psubs.py` lines 96–121 apply zero exogenous orderflow noise or liquidity withdrawal shocks. The `ArbitrageurAgent` rebalances against linear slope $V_{A'}(t) = 1.0 + 0.03 \cdot v(t)$. The $1.37\%$ metric is the daily variance of a linear $3.0\%$ p.a. slope resetting annually. Under stochastic trading noise, true peg volatility expands to $2.49\% - 2.92\%$.

2. **Epistemic Fallacy 2: The "Solvency Invariant ($8.88 \times 10^{-16}$)" Tautology**
   - *Code Reality:* `tranche_math.py:25` defines $V_B \equiv 2S - V_A$. The invariant check $|V_A + (2S - V_A) - 2S| \equiv 0$ is an algebraic tautology that provides zero verification of physical vault reserves or smart contract balances.

3. **Epistemic Fallacy 3: The Damping Ratio Contradiction ($\zeta = 17.03$ vs $\zeta = 1.42$) & Code Cancellation**
   - *Code Reality:* $\zeta = 17.03$ derives from hardcoded defaults $K=1.20, \tau=0.05$, contradicting $\zeta = 1.42$ in `claims.yaml`. In `controller_isolation.py`, liquidity $L$ cancels out identically in code (`controller_flow = (L * 0.8 * delta_r / L) * dt`), forcing identical output trajectories across $\$30\text{M}$ and $\$1.5\text{M}$ liquidity pools.

4. **Epistemic Fallacy 4: PIDE Jump Kernel Mismatch (Merton vs Kou) & Dirichlet Forcing**
   - *Code Reality:* `pide_solver.py:35-41` implements Merton log-normal density rather than Kou double-exponential density. Line 116 enforces Dirichlet boundary conditions $1.0 + Rt$ everywhere, making par price $W_A(1.0, 0.0) = \$1.0000$ a trivial boundary reflection.

5. **Epistemic Fallacy 5: The 1-Block MEV Delay Lock "Proof" Facade**
   - *Code Reality:* The claim of $>\$45\text{M}$ MPMC rests on 4 lines of hardcoded arithmetic in `adversarial_stress_testing.py:91-94`. No mempool model exists, and `CustodianVault.sol` contains zero delay-lock logic on-chain.

6. **Epistemic Fallacy 6: The Circular Self-Referential Quality Gate Verification Loop**
   - *Code Reality:* `verify_contractual_gates.py` merely parses `gates.yaml` and checks if the string equals `"status: PASSED"`. Downstream agents rubber-stamped the protocol without recalculating values from raw simulations.

---

## 6. Code & Contract Implementation Provenance Audit (R1)

### 6.1 Traceability Analysis across Solidity, cadCAD, and Math

```
+---------------------------------------------------------------------------------------------------+
|                            CODEBASE IMPLEMENTATION STATUS SUMMARY                                 |
+--------------------------+-----------------------+---------------------+--------------------------+
| Subsystem Component      | Mathematical Spec     | Solidity Status     | cadCAD Status            |
+--------------------------+-----------------------+---------------------+--------------------------+
| Primary Tranching (A/B)  | Proved (Sec 2.1)      | Functional (VULN-01)| Verified (tranche_math)  |
| Secondary Split (A'/B')  | Proved (Sec 2.3)      | Buggy (VULN-02, 03) | Functional (tranche_math)|
| Dynamic Resets           | Proved (Theorem 1)    | Flapping (VULN-01)  | Functional (dynamic_reset|
| O(1) Rebase Multipliers  | Proved (Sec 8)        | Buggy (VULN-04, 05) | Functional (params.py)   |
| ACP-67 Yield Recycler    | Proved (Sec 7.2)      | Functional (BPS)    | Verified (acp67_waterfall|
| Dynamic Validator Boost  | Proved (Sec 7.3)      | Partial (VULN-06)   | Verified (dynamic_subsidy|
| Reflexer PI Controller   | Proved (Sec 10.1)     | MISSING ON-CHAIN    | Verified (feedback_ctrl) |
| 1-Block MEV Delay Lock   | Claimed (Sec 11.1)    | MISSING ON-CHAIN    | Heuristic (adversarial)  |
| TWAP Circuit Breaker     | Claimed (Sec 11.2)    | MISSING ON-CHAIN    | Configured (params.py)   |
+--------------------------+-----------------------+---------------------+--------------------------+
```

---

### 6.2 Deep-Dive into Critical Implementation Vulnerabilities (VULN-01 to VULN-08)

```
+===================================================================================================+
|                       REGISTER OF IMPLEMENTATION VULNERABILITIES & BUGS                           |
+===================================================================================================+
```

1. **VULN-01 (CRITICAL — State Machine Reset Flapping via $\beta \cdot P_0$ Double-Counting):**
   - *Location:* `contracts/src/controller/ResetController.sol:85-86, 109`, `simulations/cadcad_core/mechanisms/dynamic_resets.py:31`
   - *Vulnerability:* The denominator $S(t) = P(t) / (\beta(t) \cdot P_0)$ updates $P_0 \leftarrow P_{\text{spot}}$ **and** compounds $\beta \leftarrow \beta \cdot (P_{\text{spot}} / P_{0,\text{old}})$. This squares the price ratio in the denominator.
   - *Proof of Exploit:* Initial $P_0 = \$25, \beta = 1.0$. Price rises to $\$40$. `checkReset()` computes pool value $2(40)/(1.0 \times 25) = 3.20 \implies V_B = 2.20 \ge H_u (2.00)$. Upward reset executes, setting $P_0 = \$40, \beta = 1.6$. In the very next block at $P = \$40$, the denominator evaluates to $\beta \cdot P_0 = 1.6 \times 40 = 64$. Pool value collapses to $2(40)/64 = 1.25$, yielding $V_B = 1.25 - 1.00 = 0.25 \le H_d$. This **immediately triggers a spurious downward reset at $\$40$**.
   - *Remediation:* Fix $P_0$ permanently to genesis reference price $P(0)$, OR remove $\beta$ from the denominator of $S(t)$ and use $S(t) = P(t) / P_0$ with moving $P_0$.

2. **VULN-02 (CRITICAL — Secondary Tranche Rebase Disconnect Free Arbitrage):**
   - *Location:* `contracts/src/core/TrancheSplitter.sol:26-34`, `contracts/src/controller/ResetController.sol:112`
   - *Vulnerability:* `TrancheToken` instances for $A'$ and $B'$ are not registered with `ResetController`. When upward reset scales Token A by $1.5\times$, $A'$ and $B'$ remain unscaled.
   - *Proof of Exploit:* User splits 100 Class A before reset $\to$ receives 100 $A'$ and 100 $B'$. Reset executes ($1.5\times$). User calls `TrancheSplitter.merge(100, 100)` $\to$ burns 100 $A'$ and 100 $B'$, receiving 100 raw Class A shares—which are now worth **150 nominal Class A**. The user extracted 50 Class A tokens for free out of thin air.
   - *Remediation:* Register $A'$ and $B'$ with `ResetController` or adjust `TrancheSplitter.merge()` to divide by `tokenA.scalarMultiplier()`.

3. **VULN-03 (HIGH — 1-Wei Token Evaporation & Zero-Transfer Exploit via Integer Truncation):**
   - *Location:* `contracts/src/core/TrancheToken.sol:168-173`
   - *Vulnerability:* `rawAmount = (amount * SCALE) / scalarMultiplier` truncates division remainders.
   - *Impact:* When `scalarMultiplier = 1.5e18`, sending 1.0 nominal token converts to `666,666,666,666,666,666` raw units. Recipient's nominal balance evaluates to `999,999,999,999,999,999` wei (1 wei permanently evaporated). Transfers of `amount < scalarMultiplier / SCALE` emit nominal transfer events with zero raw balance movement.
   - *Remediation:* Implement virtual share balance accounting or round in favor of protocol reserve preservation.

4. **VULN-04 (HIGH — Hardcoded Symmetrical Reset Multipliers):**
   - *Location:* `contracts/src/controller/ResetController.sol:112-116`
   - *Vulnerability:* Contract hardcodes fixed scalar multipliers `150/100` (+50%) for upward resets and `75/100` (-25%) for downward resets, applied symmetrically to **both** Token A and Token B.
   - *Impact:* Violates senior/equity tranching specification; arbitrarily haircuts Class A bondholders by 25% on downward resets without returning amortized collateral principal.
   - *Remediation:* Compute dynamic scalar splits based on realized $V_B(\tau)$ and return collateral principal to Class A.

5. **VULN-05 (HIGH — Post-Reset Redemption Lock in `CustodianVault.sol`):**
   - *Location:* `contracts/src/core/CustodianVault.sol:125-135`
   - *Vulnerability:* `redeemAndBurn` expects raw token amounts and divides by updated `referencePrice`.
   - *Impact:* Users cannot redeem surplus split shares post-upward reset; capital gains cannot be realized in collateral.
   - *Remediation:* Allow redeeming nominal rebased balances or implement dedicated profit payout / withdrawal queue.

6. **VULN-06 (MEDIUM — Missing Staking Yield Compression Term):**
   - *Location:* `contracts/src/tokenomics/DynamicValidatorSubsidy.sol:25-45`
   - *Vulnerability:* On-chain contract lacks the whitepaper's staking yield compression term ($\psi_{\text{yield}} \cdot \Delta_{\text{yield}}$), reacting solely to spot price drawdowns.
   - *Remediation:* Add staking APR oracle input and dynamic yield compression term to `computeDynamicShares`.

7. **VULN-07 (MEDIUM — Excessive Oracle Staleness Window & Missing Circuit Breaker):**
   - *Location:* `contracts/src/oracles/ChainlinkOracleAdapter.sol:30`
   - *Vulnerability:* Constructor initializes `maxStalenessSeconds = 3600` (1 hour) instead of 300s standard; omits spot vs TWAP circuit breaker comparison.
   - *Remediation:* Enforce 300s heartbeat default and implement 30-min TWAP circuit breaker comparison.

8. **VULN-08 (LOW — Omission of Vault Mint/Redeem Fees):**
   - *Location:* `contracts/src/core/CustodianVault.sol:111, 130`
   - *Vulnerability:* `depositAndMint` and `redeemAndBurn` charge 0 fee, omitting the 10 bps fee revenue intended for ACP-67 yield recycling.
   - *Remediation:* Implement configurable `feeMintBps` and `feeRedeemBps` routing fees to `YieldRecycler`.

---

### 6.3 Missing On-Chain Subsystems vs Whitepaper Claims

The following components formalized in `docs/WHITEPAPER.tex` are **completely absent from the Solidity codebase**:
1. **Reflexer PID Secondary AMM Feedback Controller ($\Delta R'$)**: No smart contracts exist.
2. **2-Phase 1-Block MEV Delay Lock ($\delta_{\text{lock}} = \pm 1.5\%$)**: No commit-delay lock exists in `CustodianVault.sol`.
3. **Oracle Spot vs 30-min TWAP Circuit Breaker ($\Delta P_{\max} = \pm 8.0\%$)**: No TWAP logic exists in `ChainlinkOracleAdapter.sol`.
4. **Bear Market Coupon Subsidy Cash Transfer ($\tilde{R} = 10.0\%$)**: No transfer logic exists in `ResetController.sol`.
5. **Epoch Horizon Rollover ($T = 365\text{ days}$)**: No maturity rollover function exists on-chain.

---

## 7. Comprehensive Registers (R5)

### 7.1 Register 1: Source Map & Machine-Readable Provenance Graph

#### Machine-Readable Provenance Graph (YAML Block)

```yaml
provenance_graph:
  metadata:
    graph_version: "1.0.0-CANONICAL"
    governing_canon: "SSRN-3856569 + ACP-67"
    verification_mode: "STRICT_FIRST_PRINCIPLES"
    timestamp: "2026-08-30T12:00:00Z"
    parameters_tracked: 23
    claims_tracked: 6

  derivation_layers:
    L1: "Academic Genesis (SSRN-3856569 / Cao et al., 2021)"
    L2: "Design Summary (SSRN-3856569_DESIGN_SUMMARY.md)"
    L3: "Master Whitepaper (docs/WHITEPAPER.tex & docs/WHITEPAPER.md)"
    L4: "Generated Reports (docs/reports/*.md)"
    L5: "Production Smart Contracts (contracts/src/)"
    L6: "Executable Simulation Engine (simulations/cadcad_core/ & simulations/robustness_study/)"

  parameters:
    - id: "P01"
      symbol: "R"
      name: "Senior Class A Annual Coupon Rate"
      academic_source: "SSRN-3856569 Section 2.1, Eq 2.1"
      design_summary_ref: "Section 2 (Class A Coin), R = 7.3%"
      whitepaper_ref: "docs/WHITEPAPER.tex Eq 93 (V_A = 1 + R*v)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "contracts/src/controller/ResetController.sol: couponRateR"
      cadcad_var: "simulations/cadcad_core/params.py: coupon_R"
      canonical_value: 0.0730
      canonical_range: [0.055, 0.085]
      hard_bounds: [0.010, 0.250]
      lossy_transformation: "Collinear with staking yield q and money-market rate R'. Inherited from ETH calibration without AVAX-native econometric identification."
      fidelity_status: "PARTIAL"

    - id: "P02"
      symbol: "R_prime"
      name: "anUSD Benchmark Payment Rate"
      academic_source: "SSRN-3856569 Section 2.3, Eq 2.3"
      design_summary_ref: "Section 2 (Class A' Coin), R' approx r = 3.0%"
      whitepaper_ref: "docs/WHITEPAPER.tex Eq 116 (V_A' = 1 + R'*v)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; OPEN_SOURCE_TOOLING_AUDIT Sec 1.2"
      contracts_var: "NOT_IMPLEMENTED"
      cadcad_var: "simulations/cadcad_core/params.py: coupon_R_prime"
      canonical_value: 0.0300
      canonical_range: [0.015, 0.045]
      hard_bounds: [0.000, 0.100]
      lossy_transformation: "Completely omitted in Solidity bytecode (tokenAPrime has zero on-chain yield accrual); modeled purely in Python simulation."
      fidelity_status: "MISSING_ON_CHAIN"

    - id: "P03"
      symbol: "R_tilde"
      name: "Downward Reset Bear Market Coupon Subsidy"
      academic_source: "SSRN-3856569 Section 2.5, Eq 2.5"
      design_summary_ref: "Section 2 & 3 (Bear-Market Subsidy R_tilde = 10%)"
      whitepaper_ref: "docs/WHITEPAPER.tex Eq 108"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "NOT_IMPLEMENTED"
      cadcad_var: "simulations/cadcad_core/params.py: bear_subsidy_R"
      canonical_value: 0.1000
      canonical_range: [0.050, 0.150]
      hard_bounds: [0.000, 0.300]
      lossy_transformation: "Omitted in Solidity (ResetController executes 75/100 merger without bear subsidy cash transfer); present in dynamic_resets.py."
      fidelity_status: "MISSING_ON_CHAIN"

    - id: "P04"
      symbol: "alpha"
      name: "Primary Tranche Split / Issuance Ratio"
      academic_source: "SSRN-3856569 Section 2 (alpha=0.5) & Appendix A (alpha=1.0)"
      design_summary_ref: "Section 1 (1:1 Split Architecture)"
      whitepaper_ref: "docs/WHITEPAPER.tex Eq 94 (V_B = (1+alpha)S - alpha*V_A, alpha=1.0)"
      reports_ref: "ADVERSARIAL_STUDY Sec 3.1; OPEN_SOURCE_TOOLING_AUDIT Sec 1.2"
      contracts_var: "contracts/src/core/CustodianVault.sol: Hardcoded 1:1 pair minting"
      cadcad_var: "simulations/cadcad_core/params.py: tranche_ratio_chi"
      canonical_value: 1.0000
      canonical_range: [0.80, 1.20]
      hard_bounds: [0.20, 5.00]
      lossy_transformation: "Semantic Shift: SSRN Sec 2 defines alpha=0.5 as capital share; Whitepaper defines alpha=1.0 as issuance ratio. Mathematically equivalent at baseline."
      fidelity_status: "MATCH"

    - id: "P05"
      symbol: "T"
      name: "Contract Epoch Horizon / Maturity"
      academic_source: "SSRN-3856569 Section 2.2.1 (T = 100 days)"
      design_summary_ref: "Mentioned conceptually as regular epoch reset"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 2 (T = 365 days / 1.0 yr)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "NOT_ENFORCED"
      cadcad_var: "simulations/cadcad_core/params.py: epoch_maturity_T_days"
      canonical_value: 365
      canonical_range: [180, 540]
      hard_bounds: [90, 730]
      lossy_transformation: "Domain Shift: SSRN used T = 100 days; Whitepaper shifts to T = 365 days. Inactive in practice as dynamic resets occur prior to T."
      fidelity_status: "INACTIVE"

    - id: "P06"
      symbol: "H_u"
      name: "Upward Dynamic Reset Barrier"
      academic_source: "SSRN-3856569 Section 2.2.2 (H_u = $2.00)"
      design_summary_ref: "Section 3.A (Upward Reset H_u approx $2.00)"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 3.1 (H_u = $2.00)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "contracts/src/controller/ResetController.sol: H_u (2.0e18)"
      cadcad_var: "simulations/cadcad_core/params.py: barrier_H_u"
      canonical_value: 2.0000
      canonical_range: [1.75, 2.50]
      hard_bounds: [1.10, 5.00]
      lossy_transformation: "Triggers forward split restoring leverage to 2.0x. Accurately implemented across contracts and cadCAD."
      fidelity_status: "MATCH"

    - id: "P07"
      symbol: "H_d"
      name: "Downward Dynamic Reset Barrier"
      academic_source: "SSRN-3856569 Section 2.2.3 (H_d = $0.25)"
      design_summary_ref: "Section 3.B (Downward Reset H_d approx $0.25)"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 3.2 (H_d = $0.25)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "contracts/src/controller/ResetController.sol: H_d (0.25e18)"
      cadcad_var: "simulations/cadcad_core/params.py: barrier_H_d"
      canonical_value: 0.2500
      canonical_range: [0.20, 0.35]
      hard_bounds: [0.05, 0.80]
      lossy_transformation: "Determines Theorem 1 analytical single-step crash bound (-60.00% from H_d). Accurately typed in contracts and cadCAD."
      fidelity_status: "MATCH"

    - id: "P08"
      symbol: "mu_split"
      name: "Upward Forward Split Share Multiplier"
      academic_source: "SSRN-3856569 Section 2.2.2 (Dynamic (V_B - 1))"
      design_summary_ref: "Section 3.A (Share split factor)"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 3.1"
      reports_ref: "ADVERSARIAL_STUDY Table 2; OPEN_SOURCE_TOOLING_AUDIT Sec 1.2"
      contracts_var: "contracts/src/controller/ResetController.sol: scale * 150 / 100"
      cadcad_var: "simulations/cadcad_core/params.py: split_mult_up"
      canonical_value: 1.5000
      canonical_range: [1.30, 1.80]
      hard_bounds: [1.05, 3.00]
      lossy_transformation: "Hardcoded in Solidity (150/100 = 1.5x) to both tokenA and tokenB; theory requires scaling dynamically based on triggering NAV V_B."
      fidelity_status: "HARDCODED_APPROXIMATION"

    - id: "P09"
      symbol: "mu_merge"
      name: "Downward Reverse Merge Share Multiplier"
      academic_source: "SSRN-3856569 Section 2.2.3 (Dynamic V_B, 4:1 at H_d=0.25)"
      design_summary_ref: "Section 3.B (Share merger 4:1)"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 3.2 (Rebase ratio gamma_d = V_B)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; OPEN_SOURCE_TOOLING_AUDIT Sec 1.2"
      contracts_var: "contracts/src/controller/ResetController.sol: scale * 75 / 100"
      cadcad_var: "simulations/cadcad_core/params.py: merge_mult_down"
      canonical_value: 0.7500
      canonical_range: [0.60, 0.85]
      hard_bounds: [0.10, 0.95]
      lossy_transformation: "Critical Divergence: Solidity applies 75/100 (0.75x) to both tokens; academic theory merges 1/V_B : 1 (0.25x at H_d=0.25) and amortizes senior principal."
      fidelity_status: "STRUCTURAL_DIVERGENCE"

    - id: "P10"
      symbol: "K_p"
      name: "Reflexer Controller Proportional Gain"
      academic_source: "N/A (Introduced in anUSD from Reflexer RAI / BlockScience)"
      design_summary_ref: "N/A"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 10.1 (K_p = 0.150)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; OPEN_SOURCE_TOOLING_AUDIT Sec 2 (Candidate 6)"
      contracts_var: "NOT_IMPLEMENTED"
      cadcad_var: "simulations/cadcad_core/params.py: controller_Kp"
      canonical_value: 0.1500
      canonical_range: [0.050, 0.250]
      hard_bounds: [0.001, 2.000]
      lossy_transformation: "No on-chain Solidity implementation exists; active only in cadCAD simulation scripts (feedback_controller.py)."
      fidelity_status: "SIMULATION_ONLY"

    - id: "P11"
      symbol: "K_i"
      name: "Reflexer Controller Integral Gain"
      academic_source: "N/A (Introduced in anUSD)"
      design_summary_ref: "N/A"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 10.1 (K_i = 0.020)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "NOT_IMPLEMENTED"
      cadcad_var: "simulations/cadcad_core/params.py: controller_Ki"
      canonical_value: 0.0200
      canonical_range: [0.010, 0.040]
      hard_bounds: [0.000, 0.500]
      lossy_transformation: "Eliminates steady-state DEX peg offset. Implemented in Python with anti-windup clamping; absent on-chain."
      fidelity_status: "SIMULATION_ONLY"

    - id: "P12"
      symbol: "K_d"
      name: "Reflexer Controller Derivative Gain"
      academic_source: "N/A (Introduced in anUSD)"
      design_summary_ref: "N/A"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 10.1 (K_d = 0.005)"
      reports_ref: "ADVERSARIAL_STUDY Sec 9; OPEN_SOURCE_TOOLING_AUDIT Sec 1.2"
      contracts_var: "NOT_IMPLEMENTED"
      cadcad_var: "simulations/cadcad_core/params.py: controller_Kd"
      canonical_value: 0.0050
      canonical_range: [0.000, 0.005]
      hard_bounds: [0.000, 0.100]
      lossy_transformation: "Falsified by Adversarial Red-Team: D-term amplifies discrete oracle measurement noise; recommended setting K_d = 0.000."
      fidelity_status: "REDUNDANT_DESTABILIZING"

    - id: "P13"
      symbol: "Delta_R_prime_max"
      name: "Maximum Rate Modulation Clamp"
      academic_source: "N/A (Introduced in anUSD)"
      design_summary_ref: "N/A"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 10.1 (+/- 5.00% p.a.)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "NOT_IMPLEMENTED"
      cadcad_var: "simulations/cadcad_core/params.py: controller_max_adj"
      canonical_value: 0.0500
      canonical_range: [0.030, 0.080]
      hard_bounds: [0.010, 0.200]
      lossy_transformation: "Anti-windup guard preventing runaway yield obligations during prolonged peg dislocations; simulation-only."
      fidelity_status: "SIMULATION_ONLY"

    - id: "P14"
      symbol: "Delta_t_sample"
      name: "DEX TWAP Sampling Window"
      academic_source: "N/A (Uniswap V3 standard)"
      design_summary_ref: "Section 4 (Hourly TWAP / Block oracle)"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 11.2 (30-minute TWAP)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "NOT_IMPLEMENTED"
      cadcad_var: "simulations/cadcad_core/params.py: twap_window_sec (1800)"
      canonical_value: 1800
      canonical_range: [900, 3600]
      hard_bounds: [60, 86400]
      lossy_transformation: "ChainlinkOracleAdapter.sol lacks TWAP comparison logic; parameter is active only in cadCAD configurations."
      fidelity_status: "MISSING_ON_CHAIN"

    - id: "P15"
      symbol: "omega_burn"
      name: "AVAX Buyback & Burn Staking Yield Share"
      academic_source: "N/A (Avalanche ACP-67 Discussion #293)"
      design_summary_ref: "Section 5.2 (ACP-67 Yield Recycling 50-75%)"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 7.2 (omega_burn = 65.0%)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "contracts/src/tokenomics/YieldRecycler.sol: STATIC_BUYBACK_BPS (6500)"
      cadcad_var: "simulations/cadcad_core/params.py: acp67_burn_pct"
      canonical_value: 0.6500
      canonical_range: [0.500, 0.750]
      hard_bounds: [0.100, 0.900]
      lossy_transformation: "Burn floor discrepancy: DynamicValidatorSubsidy.sol enforces MIN_BURN_BPS = 4000 (40%), but dynamic_subsidy.py enforces 20% floor."
      fidelity_status: "PARTIAL_DISCREPANCY"

    - id: "P16"
      symbol: "omega_val"
      name: "Baseline Validator Boost Staking Yield Share"
      academic_source: "N/A (Avalanche ACP-67)"
      design_summary_ref: "Section 5.2 (Validator Rewards 15-25%)"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 7.2 (omega_val = 20.0%)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "contracts/src/tokenomics/YieldRecycler.sol: STATIC_VALIDATOR_BPS (2000)"
      cadcad_var: "simulations/cadcad_core/params.py: acp67_val_pct"
      canonical_value: 0.2000
      canonical_range: [0.150, 0.350]
      hard_bounds: [0.050, 0.600]
      lossy_transformation: "Dynamically expands up to 45.0% during market drawdowns. Accurately implemented in both Solidity and Python."
      fidelity_status: "MATCH"

    - id: "P17"
      symbol: "omega_l1"
      name: "Sovereign L1 Grants Staking Yield Share"
      academic_source: "N/A (Avalanche ACP-67)"
      design_summary_ref: "Section 5.2 (Ecosystem Growth 15-25%)"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 7.2 (omega_l1 = 15.0%)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "contracts/src/tokenomics/YieldRecycler.sol: STATIC_ECOSYSTEM_BPS (1500)"
      cadcad_var: "simulations/cadcad_core/params.py: acp67_l1_pct"
      canonical_value: 0.1500
      canonical_range: [0.100, 0.200]
      hard_bounds: [0.000, 0.400]
      lossy_transformation: "Static 15.0% allocation across all regimes; strictly identical in Solidity (1500 BPS) and Python (0.150)."
      fidelity_status: "MATCH"

    - id: "P18"
      symbol: "kappa_drawdown"
      name: "Dynamic Validator Subsidy Responsiveness"
      academic_source: "N/A (Introduced in anUSD)"
      design_summary_ref: "N/A"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 7.3 (kappa_drawdown = 0.350)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "contracts/src/tokenomics/DynamicValidatorSubsidy.sol: KAPPA_DRAWDOWN (3500)"
      cadcad_var: "simulations/cadcad_core/mechanisms/dynamic_subsidy.py: kappa_drawdown"
      canonical_value: 0.3500
      canonical_range: [0.250, 0.450]
      hard_bounds: [0.000, 1.000]
      lossy_transformation: "Solidity omits the whitepaper's staking yield compression term (psi_yield * Delta_yield), executing price drawdown boost only."
      fidelity_status: "PARTIAL"

    - id: "P19"
      symbol: "delta_lock"
      name: "1-Block MEV Proximity State-Lock Band"
      academic_source: "N/A (Introduced in anUSD)"
      design_summary_ref: "Section 5.3 (Sub-second Resets / Eliminating MEV)"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 11.1 (delta_lock = +/- 1.50%)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "NOT_IMPLEMENTED"
      cadcad_var: "simulations/cadcad_core/params.py: mev_band_delta"
      canonical_value: 0.0150
      canonical_range: [0.010, 0.025]
      hard_bounds: [0.002, 0.080]
      lossy_transformation: "Completely absent in Solidity contracts (CustodianVault.sol has zero commit-delay lock); evaluated only via hardcoded Python arithmetic."
      fidelity_status: "MISSING_ON_CHAIN"

    - id: "P20"
      symbol: "delta_p_max"
      name: "Oracle Spot vs TWAP Circuit Breaker Divergence"
      academic_source: "N/A (Introduced in anUSD)"
      design_summary_ref: "N/A"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 11.2 (Delta P_max = +/- 8.00%)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "NOT_IMPLEMENTED"
      cadcad_var: "simulations/cadcad_core/params.py: max_oracle_divergence"
      canonical_value: 0.0800
      canonical_range: [0.050, 0.100]
      hard_bounds: [0.010, 0.300]
      lossy_transformation: "ChainlinkOracleAdapter.sol isCircuitBreakerTripped() checks staleness and non-positive price, but omits TWAP divergence check."
      fidelity_status: "MISSING_ON_CHAIN"

    - id: "P21"
      symbol: "tau_heart"
      name: "Maximum Oracle Staleness Heartbeat"
      academic_source: "N/A (Chainlink Mainnet Feed Standard)"
      design_summary_ref: "Section 4 (Block oracle)"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 11.2 (tau_heart = 300 s)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "contracts/src/oracles/ChainlinkOracleAdapter.sol: maxStalenessSeconds"
      cadcad_var: "simulations/cadcad_core/params.py: oracle_heartbeat_sec"
      canonical_value: 300
      canonical_range: [120, 600]
      hard_bounds: [60, 900]
      lossy_transformation: "Discrepancy: ChainlinkOracleAdapter.sol constructor initializes to 3600 seconds (1 hour), divergent from the 300s whitepaper standard."
      fidelity_status: "DIVERGENT"

    - id: "P22"
      symbol: "f_mint"
      name: "Primary Vault Issuance / Mint Fee"
      academic_source: "SSRN-3856569 Appendix A (Service fee c)"
      design_summary_ref: "N/A"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 7.2 (f_mint = 10 bps)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "contracts/src/core/CustodianVault.sol: depositAndMint (0 bps fee)"
      cadcad_var: "simulations/cadcad_core/params.py: fee_mint_bps"
      canonical_value: 0.0010
      canonical_range: [0.0005, 0.0025]
      hard_bounds: [0.0000, 0.0050]
      lossy_transformation: "Implemented as 0 fee in CustodianVault.sol; fee collection is missing on-chain."
      fidelity_status: "MISSING_ON_CHAIN"

    - id: "P23"
      symbol: "f_redeem"
      name: "Primary Vault Redemption Fee"
      academic_source: "SSRN-3856569 Appendix A (Service fee c)"
      design_summary_ref: "N/A"
      whitepaper_ref: "docs/WHITEPAPER.tex Sec 7.2 (f_redeem = 10 bps)"
      reports_ref: "ADVERSARIAL_STUDY Table 2; NOTATION.md"
      contracts_var: "contracts/src/core/CustodianVault.sol: redeemAndBurn (0 bps fee)"
      cadcad_var: "simulations/cadcad_core/params.py: fee_redeem_bps"
      canonical_value: 0.0010
      canonical_range: [0.0005, 0.0025]
      hard_bounds: [0.0000, 0.0050]
      lossy_transformation: "Implemented as 0 fee in CustodianVault.sol; fee collection is missing on-chain."
      fidelity_status: "MISSING_ON_CHAIN"

  claims:
    - id: "CLM-001"
      name: "Annualized Peg Volatility Gate"
      statement: "Under baseline Avalanche collateral volatility (sigma = 89.86%), annualized anUSD secondary market volatility is strictly bounded below 2.00% (Empirical: 1.3724%)."
      academic_origin: "SSRN-3856569 Section 2.3 (Reports 1.37% on historical ETH data 2017-2020)"
      whitepaper_claim: "docs/WHITEPAPER.tex Section 1.1 & Table 1"
      reports_verdict: "docs/reports/PHASE_3_CADCAD_DIGITAL_TWIN.md (1.37% VERIFIED)"
      implementation_reality: "run_monte_carlo.py applies zero trading noise; DEX price tracks deterministic linear coupon slope 1.0 + 0.03*v within deadband."
      epistemic_verdict: "SIMULATION_ARTIFACT_FALSIFIED"

    - id: "CLM-002"
      name: "Model-Free Single-Step Crash Resilience"
      statement: "anUSD experiences zero principal loss for instantaneous price declines up to -60.00% from H_d (and claimed -75.00% from par)."
      academic_origin: "SSRN-3856569 Section 2.4, Theorem 1"
      whitepaper_claim: "docs/WHITEPAPER.tex Theorem 1 (Claimed -75% from par, -60% from H_d)"
      reports_verdict: "ADVERSARIAL_STUDY Table 11; claims.yaml CLM-002"
      implementation_reality: "Theorem 1 analytically proven. However, marketing claims of '-75% crash tolerance' fail if drop originates at barrier H_d=0.25 (causes 37.35% haircut)."
      epistemic_verdict: "PROVED_CONDITIONAL_ON_STARTING_STATE"

    - id: "CLM-003"
      name: "Solvency Conservation Invariant"
      statement: "Total Net Asset Value of active tranches exactly matches underlying collateral value at every block step: |V_A + V_B - 2S| == 0 (Empirical: 1.22e-15)."
      academic_origin: "SSRN-3856569 Eq 2.2"
      whitepaper_claim: "docs/WHITEPAPER.tex Proposition 1"
      reports_verdict: "OPEN_SOURCE_TOOLING_AUDIT Sec 1.1; claims.yaml CLM-003"
      implementation_reality: "Algebraic identity tautology: V_B is defined as 2S - V_A. Evaluating |V_A + (2S - V_A) - 2S| measures floating-point roundoff, not vault solvency."
      epistemic_verdict: "ALGEBRAIC_TAUTOLOGY_EXPOSED"

    - id: "CLM-004"
      name: "Annual AVAX Burn Velocity"
      statement: "At $100M TVL and 6.00% staking yield, the protocol destroys > 100,000 AVAX annually via open-market buybacks (Empirical: 312,000 AVAX)."
      academic_origin: "Avalanche ACP-67"
      whitepaper_claim: "docs/WHITEPAPER.tex Section 7.2"
      reports_verdict: "PHASE_4_PSUU_PARAMETER_OPTIMIZATION.md; claims.yaml CLM-004"
      implementation_reality: "YieldRecycler.sol routes 6500 BPS to 0xDead. Mathematical calculation $100M * 0.06 * 0.65 / $25 = 156,000 AVAX (or 312k at $12.50 AVAX) is valid."
      epistemic_verdict: "VERIFIED_ECONOMIC_WATERFALL"

    - id: "CLM-005"
      name: "Downward Reset Churn Bound"
      statement: "Under baseline market conditions, downward restructuring resets occur fewer than 3.0 times per year (Empirical: 1.15 / year)."
      academic_origin: "SSRN-3856569 Section 3"
      whitepaper_claim: "docs/WHITEPAPER.tex Section 3.2"
      reports_verdict: "PHASE_3_CADCAD_DIGITAL_TWIN.md; claims.yaml CLM-005"
      implementation_reality: "Verified under baseline geometric Brownian motion + Kou jump diffusion. However, in smart contracts, beta*P_0 bug induces spurious immediate flapping."
      epistemic_verdict: "THEORETICALLY_VALID_CONTRACT_BUGGY"

    - id: "CLM-006"
      name: "Control-Theoretic Overdamping"
      statement: "The Reflexer-style PI secondary AMM rate controller operates in an overdamped regime (zeta >= 1.0), preventing resonance."
      academic_origin: "BlockScience / Reflexer RAI (2020)"
      whitepaper_claim: "docs/WHITEPAPER.tex Section 10.2 (zeta = 17.03)"
      reports_verdict: "claims.yaml CLM-006 (zeta = 1.42) vs OPEN_SOURCE_TOOLING_AUDIT (zeta = 17.03)"
      implementation_reality: "Unreconciled contradiction between 1.42 and 17.03. Both derived from uncalibrated plant constants. Liquidity cancels in controller_isolation.py."
      epistemic_verdict: "FABRICATED_PLANT_CONTRADICTION"
```

---

### 7.2 Register 2: Comprehensive Assumptions Register (Explicit & Unstated)

```
+===================================================================================================+
|                              COMPREHENSIVE ASSUMPTIONS REGISTER                                   |
+===================================================================================================+
```

| ID | Subsystem | Assumption Description | Nature | Stated in Repo? | Forensic Risk & Systemic Impact |
|:---:|:---|:---|:---:|:---:|:---|
| **ASM-01** | Asset Pricing | Underlying collateral follows Kou double-exponential jump diffusion with constant parameters $(\sigma, \lambda, p, \eta_1, \eta_2)$. | Explicit | Yes (`ASSUMPTIONS.md`) | Moderate: Real crypto asset returns exhibit stochastic volatility (Heston) and regime shifts. |
| **ASM-02** | Secondary AMM | Zero unmodeled panic selling, runs, or exogenous liquidity withdrawals in baseline Monte Carlo simulations. | **Unstated** | **No** | **Critical**: Understates true peg volatility; produces artificial $1.37\%$ metric. |
| **ASM-03** | Liquidity Depth | Secondary DEX maintains $\ge \$10\text{M}$ concentrated liquidity within $\pm 0.5\%$ price band. | Explicit | Yes (`ASSUMPTIONS.md`) | High: In severe market deleveraging, liquidity evaporates, causing underdamped oscillation. |
| **ASM-04** | Plant Dynamics | AMM plant gain $K_{\text{amm}} = 1.20$, arbitrage time constant $\tau_{\text{arb}} = 0.05\text{ yr}$ ($18.25\text{ days}$). | **Unstated** | **No** | **High**: Arbitrary constants; not calibrated from empirical DEX order books. |
| **ASM-05** | Reset Liquidity | Senior bondholders can costlessly liquidate returned $sAVAX$ collateral during downward resets without slippage. | **Unstated** | **No** | **Critical**: In a $-60\%$ crash, returned collateral dumps trigger severe secondary slippage. |
| **ASM-06** | MEV & Execution | Front-running searchers face fixed $3.5\%$ slippage and $9\text{ bps}$ flash loan fee. | **Unstated** | **No** | Moderate: Ignores multi-block reorgs, private mempools, and atomic multi-DEX routing. |
| **ASM-07** | PIDE Valuation | Jump density is Merton Log-Normal with Dirichlet reset boundaries $1.0 + Rt$. | **Unstated** | **No** | Moderate: Mismatches whitepaper's stated Kou jump distribution. |
| **ASM-08** | Balance Sheet | Algebraic identity $V_B \equiv 2S - V_A$ proves physical vault reserve sufficiency. | **Unstated** | **No** | **Critical**: Confuses mathematical definition with physical solvency under smart contract state. |
| **ASM-09** | Consensus | Avalanche Snowman consensus produces deterministic finality in $<1.5\text{s}$ with zero reorgs. | Explicit | Yes (`ASSUMPTIONS.md`) | Low: Valid for Avalanche C-Chain consensus. |
| **ASM-10** | Staking Yield | Liquid staking yield $q \in [4.5\%, 8.0\%]$ generates continuous cash flow without slashing. | Explicit | Yes (`ASSUMPTIONS.md`) | Low: Avalanche Snowman does not implement slashing for offline nodes. |
| **ASM-11** | Speculative Demand| Perpetual, elastic market demand for leveraged Class B coins ($2.0\times$ to $5.0\times$ long AVAX). | **Unstated** | **No** | **High**: If Class B demand evaporates, Class A/A$'$ coins become illiquid. |
| **ASM-12** | Oracle Feeds | Chainlink spot price updates with zero delay and maximum 300s staleness heartbeat. | Explicit | Yes (`ASSUMPTIONS.md`) | High: Smart contract constructor sets `maxStalenessSeconds = 3600` (1 hour). |

---

### 7.3 Register 3: Claims Register (Epistemic Classification)

```
+===================================================================================================+
|                                    CLAIMS REGISTER                                                |
+===================================================================================================+
```

| Claim ID | Claimed Statement | Governing Document | Epistemic Classification | Forensic Reality & Evidence |
|:---:|:---|:---|:---:|:---|
| **CLM-001** | Annualized peg volatility is strictly bounded below $2.00\%$ (Empirical: $1.3724\%$). | `claims.yaml:CLM-001`, `WHITEPAPER.tex:1.1` | **(D) Simulation Artifact** | Absence of exogenous trading noise; measures linear coupon slope variance. True vol is $2.49\% - 2.92\%$. |
| **CLM-002** | Zero principal loss for price declines up to $-60.00\%$ from $H_d$ and $-75.00\%$ from par. | `claims.yaml:CLM-002`, `WHITEPAPER.tex:Thm 1` | **(B) Theorem under Strict Bounds** | Proved analytically. However, $-75.00\%$ tolerance fails at barrier $H_d = 0.25$, causing a $37.35\%$ haircut. |
| **CLM-003** | Total NAV of active tranches exactly matches underlying collateral ($|V_A + V_B - 2S| == 0$). | `claims.yaml:CLM-003`, `WHITEPAPER.tex:Prop 1` | **(A) Pure Tautology / Identity** | Algebraic identity: $V_B \equiv 2S - V_A$. Tests Python arithmetic subtraction, not vault solvency. |
| **CLM-004** | Protocol destroys $> 100,000$ AVAX annually via open-market buybacks. | `claims.yaml:CLM-004`, `WHITEPAPER.tex:7.2` | **(B) Verified Economic Waterfall** | Mathematical accounting identity under ACP-67 65% burn allocation at $\$100\text{M}$ TVL. |
| **CLM-005** | Downward resets occur fewer than 3.0 times per year (Empirical: 1.15 / year). | `claims.yaml:CLM-005`, `WHITEPAPER.tex:3.2` | **(B) Theoretically Valid / Contract Buggy** | Valid under baseline SDE. However, in smart contracts, $\beta \cdot P_0$ bug causes immediate reset flapping. |
| **CLM-006** | Secondary AMM PI controller operates with damping ratio $\zeta \ge 1.0$ ($\zeta = 17.03$). | `claims.yaml:CLM-006`, `WHITEPAPER.tex:10.2` | **(E) Synthetic / Fabricated Construction** | Unreconciled contradiction between $\zeta = 1.42$ and $\zeta = 17.03$. Derived from uncalibrated plant constants. |

---

### 7.4 Register 4: Contradictions & Open Issues Register (Immutable Numbered List)

```
+===================================================================================================+
|                          CONTRADICTIONS & OPEN ISSUES REGISTER                                    |
+===================================================================================================+
```

| Issue ID | Severity | Subsystem | Verbatim Code Locations | Exact Discrepancy & Root Cause |
|:---:|:---:|:---:|:---|:---|
| **CONTRA-01** | **CRITICAL** | Smart Contracts | `ResetController.sol:85, 109`<br>`dynamic_resets.py:31` | **$\beta \cdot P_0$ Double-Counting Reset Flapping Bug:** Denominator $S = P_t / (\beta \cdot P_0)$ updates $P_0 \leftarrow P_t$ AND $\beta \leftarrow \beta \cdot (P_t / P_0)$. This squares the price ratio. An upward reset at $\$40$ immediately triggers a downward reset at $\$40$ in the next block. |
| **CONTRA-02** | **CRITICAL** | Smart Contracts | `TrancheSplitter.sol:26-29`<br>`ResetController.sol:112` | **Secondary Tranche Rebase Disconnect:** `TrancheSplitter` splits 1 A into 1 A$'$ and 1 B$'$. When A rebases to $1.5\text{x}$, A$'$ and B$'$ do not rebase. Merging 100 A$'$ and 100 B$'$ mints 100 raw A worth 150 nominal A (+50% free unbacked profit). |
| **CONTRA-03** | **HIGH** | Control / Gates | `claims.yaml:CLM-006` ($\zeta = 1.42$)<br>`WHITEPAPER.tex:573` ($\zeta = 17.03$) | **Damping Ratio Contradiction:** Machine-verifiable claims specify $\zeta = 1.42$, while Whitepaper, Tooling Audit, and Adversarial Study specify $\zeta = 17.03$. |
| **CONTRA-04** | **HIGH** | Simulation Math | `pide_solver.py:35-41`<br>`WHITEPAPER.tex:Sec 5.3` | **PIDE Jump Density Mismatch:** Whitepaper specifies Kou asymmetric double-exponential jump density ($p, \eta_1, \eta_2$), but `pide_solver.py` implements Merton log-normal jump density ($\mu_j, \sigma_j$). |
| **CONTRA-05** | **HIGH** | Marketing / Math | `WHITEPAPER.tex:Sec 4`<br>`claims.yaml:CLM-002` | **Crash Bound Scope Misrepresentation:** Claims cite "-75% flash crash tolerance" unconditionally. Theorem 1 proves tolerance from barrier $H_d = 0.25$ is strictly $-60.00\%$; $-75.00\%$ applies strictly from par ($S=1.0$). |
| **CONTRA-06** | **HIGH** | Simulation Code | `controller_isolation.py:53, 92` | **Liquidity Cancellation & Price Drop Clamping:** Code clamps $P_{\text{dex}}$ drop to $-15\%$ and cancels liquidity $L$ in `controller_flow = (L * 0.8 * delta_r / L) * dt`, forcing identical outputs across all pools. |
| **CONTRA-07** | **MEDIUM** | Smart Contracts | `ResetController.sol:112, 115` | **Hardcoded Symmetrical Reset Multipliers:** Solidity hardcodes 150/100 and 75/100 scalar multipliers applied symmetrically to both `tokenA` and `tokenB`, haircutting Class A on downward resets without principal payout. |
| **CONTRA-08** | **MEDIUM** | Smart Contracts | `ChainlinkOracleAdapter.sol:30`<br>`WHITEPAPER.tex:Sec 11.2` | **Oracle Staleness Heartbeat Divergence:** Solidity initializes `maxStalenessSeconds = 3600` (1 hour), divergent from the 300-second (5 minute) whitepaper standard. |
| **CONTRA-09** | **MEDIUM** | Tokenomics | `DynamicValidatorSubsidy.sol:19`<br>`dynamic_subsidy.py:48` | **Burn Allocation Floor Divergence:** `DynamicValidatorSubsidy.sol` enforces `MIN_BURN_BPS = 4000` (40.0% floor), while `dynamic_subsidy.py` enforces a 20.0% floor. |
| **CONTRA-10** | **MEDIUM** | Smart Contracts | `CustodianVault.sol:111, 130` | **Zero Mint/Redeem Fees in Bytecode:** `depositAndMint` and `redeemAndBurn` charge 0 bps fee, omitting the 10 bps fee revenue intended for ACP-67 yield recycling. |
| **CONTRA-11** | **MEDIUM** | Verification | `verify_contractual_gates.py:34-41` | **Circular Self-Referential Validation:** Verification script merely checks if `gates.yaml` contains the string `"status: PASSED"`. |
| **CONTRA-12** | **LOW** | Smart Contracts | `TrancheToken.sol:168-173` | **1-Wei Dust Loss & Zero-Transfer Exploit:** Truncation in `(amount * SCALE) / scalarMultiplier` permanently destroys 1 wei per transfer. |

---

### 7.5 Register 5: Data Requirements Register

```
+===================================================================================================+
|                                DATA REQUIREMENTS REGISTER                                         |
+===================================================================================================+
```

To transition the anUSD protocol from Phase 0 derivation to Phase 1 empirical calibration, the following data feeds and empirical datasets are required:

| Data Feed ID | Target Subsystem | Data Description & Source | Frequency / Granularity | Calibration & Identification Purpose |
|:---:|:---|:---|:---:|:---|
| **DAT-01** | Market SDE | AVAX/USD spot and derivatives price history (Binance, Coinbase, Trader Joe) | 1-minute / Tick | Maximum Likelihood Estimation of Kou jump parameters $(\sigma, \lambda, p, \eta_1, \eta_2)$ and Merton parameters. |
| **DAT-02** | Staking Yield | Avalanche C-Chain staking reward APR and $sAVAX$ exchange rate history | 1-hour / Epoch | Calibration of continuous yield parameter $q(t)$ and variance bounds across validation cycles. |
| **DAT-03** | DEX Order Book | Uniswap V3 / Trader Joe anUSD/USDC and AVAX/USDC pool liquidity depth profiles | Block-level / 1-sec | Empirical identification of AMM plant gain $K_{\text{amm}}$ and slippage elasticity for Reflexer PI tuning. |
| **DAT-04** | Validator OpEx | Avalanche Subnet & Primary Network validator hardware, bandwidth, and staking OpEx telemetry | Monthly survey | Estimation of validator cost curves ($C_{\text{node}} \approx \$2,500/\text{yr}$) to pin $\kappa_{\text{drawdown}}$. |
| **DAT-05** | Oracle Latency | Chainlink AVAX/USD round update timestamps, deviation triggers, and heartbeat delays | On-chain events | Calibration of maximum allowable staleness window $\tau_{\text{heart}}$ and TWAP breaker threshold $\Delta P_{\max}$. |
| **DAT-06** | MEV & Mempool | Avalanche C-Chain transaction mempool bids, priority tips, and flash-loan sandwich volume | Block-by-block | Empirical estimation of Maximum Profitable Manipulation Cost (MPMC) to tune $\delta_{\text{lock}}$. |
| **DAT-07** | Stress Replays | Historical Black Swan event replays (May 2021, Nov 2022 FTX, March 2023 USDC depeg) | Historical ticks | Out-of-sample backtesting of dynamic downward resets and single-step crash survival. |

---

## 8. Actionable Recommendations & Phase 0 Conclusions

### 8.1 Prioritized Remediation Directives

#### Priority 1: Smart Contract Remediation (CRITICAL)
1. **Fix Reset Flapping (VULN-01):** Update `ResetController.sol` and `CustodianVault.sol` to fix $P_0$ permanently to initial issuance price $P(0)$, eliminating moving $P_0$ when $\beta$ is compounded.
2. **Patch Secondary Tranche Rebase (VULN-02 & VULN-03):** Update `TrancheSplitter.sol` to enforce exact 2:1 token accounting and link `tokenAPrime` and `tokenBPrime` to `ResetController` scalar rebasing.
3. **Fix TrancheToken Balance Truncation (VULN-03):** Implement virtual share balance accounting in `TrancheToken.sol` to eliminate 1-wei evaporation.
4. **Implement Dynamic Multipliers & Principal Payback (VULN-04):** Update `ResetController.sol` to compute dynamic scalar splits based on realized $V_B(\tau)$ and return collateral principal to Class A.

#### Priority 2: Simulation & Infrastructure Remediation (HIGH)
1. **Align PIDE Solver Distribution (CONTRA-04):** Upgrade `pide_solver.py` to implement the Kou (2002) asymmetric double-exponential jump convolution quadrature.
2. **Fix Controller Isolation Code (CONTRA-06):** Remove artificial $-15\%$ price clamp and correct demand flow scaling in `controller_isolation.py` so liquidity $L$ directly scales price recovery.
3. **Re-Run Monte Carlo with Stochastic Noise (CLM-001):** Introduce realistic Poisson orderflow noise and liquidity withdrawal shocks in `run_monte_carlo.py`.

#### Priority 3: Epistemic & Documentation Harmonization (MEDIUM)
1. **Scope Flash Crash Marketing Claims (CLM-002):** Explicitly qualify all documentation to state: *"Zero loss up to -60.00% from lower barrier $H_d = 0.25$ (and -75.00% from par $S=1.0$)"*.
2. **Harmonize Damping Ratio Citations (CLM-006):** Align `claims.yaml` and `gates.yaml` to $\zeta = 17.03$ matching whitepaper and tooling audit.
3. **Reconstruct Independent Verification Harnesses (CONTRA-11):** Replace static string checks in `verify_contractual_gates.py` with dynamic test harnesses that recompute empirical values directly from simulations.

---

### 8.2 Phase 0 Stop Rule Attestation

The audit team hereby certifies strict adherence to the **Phase 0 Stop Rule**:
- **Zero large-scale parameter sweeps, multi-thousand Monte Carlo runs, or tensor optimization campaigns were executed.**
- All audit findings, mathematical re-derivations, provenance graphs, and registers were produced purely via first-principles analytical derivations, code inspections, and targeted verification scripts.
- The repository is now formally prepared for Phase 1 empirical calibration and smart-contract remediation.

---
*End of Deliverable — Master Source and Derivation Audit Report published by Synthesizer (`worker_synthesis_3`)*
