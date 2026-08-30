# Teamwork Project Prompt — Draft

> Status: Launched  
> Goal: Craft prompt → get user approval → delegate to `teamwork_preview`  
> Requested team: Source & Derivation Audit Taskforce (Document Review & Epistemic Provenance Team)  

Perform a first-principles, source-critical audit of the repository's research materials, mathematical derivations, design summaries, whitepapers, generated reports, simulation code, and smart contracts. Treat all repository contents as evidence to be audited rather than ground truth, constructing an end-to-end derivation and provenance graph that traces every major mechanism, equation, theorem, and claim back to its earliest known source while identifying every notation change, assumption shift, and unexplained modification.

Working directory: `/home/hash/Hub/Projects/avalanche-native-stablecoin`  
Integrity mode: `development`  

---

## Reference Materials to Audit
- Original Academic Literature: SSRN-3856569 ("Designing Stablecoins", Cao et al., 2021)
- Summary Extraction: `SSRN-3856569_DESIGN_SUMMARY.md`
- Protocol Whitepapers: `docs/WHITEPAPER.md` & `docs/WHITEPAPER.tex`
- Generated Audit Reports: `docs/reports/ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md` & `docs/reports/OPEN_SOURCE_TOOLING_AUDIT.md`
- Simulation & Mathematical Models: `simulations/cadcad_core/`, `simulations/robustness_study/`, `workflows/`
- Smart Contracts & Invariants: `contracts/src/`, `contracts/test/`

---

## Core Principles & Source-Criticality Rules

1. **No Document is Source of Truth:** Do not treat original academic papers, design summaries, whitepapers, generated reports, or implementation code as authoritative. Every layer must be independently audited and verified.
2. **No Trust Transfer:** Never accept an earlier agent's claim or report verdict ("VERIFIED", "15/15 PASSED", "PROVED") as ground truth. Every claim must be traced to reproducible source evidence, code, or mathematics.
3. **Lossy Transformation Auditing:** Evaluate each step in the derivation chain:
   $$\text{Original Literature (SSRN-3856569)} \longrightarrow \text{Design Summary} \longrightarrow \text{anUSD Whitepaper} \longrightarrow \text{Generated Reports} \longrightarrow \text{Code Implementation}$$
   Identify every shift in notation, parameterization, assumptions, economic interpretation, mathematical structure, and implementation semantics.
4. **Preserve Discrepancies:** Never silently reconcile or smooth over inconsistencies. Record them explicitly in an immutable Open Issues & Contradictions Register.

---

## Requirements

### R1. Source-to-Implementation Provenance Graph
Construct a complete, machine-readable provenance graph:
$$\text{SOURCE} \longrightarrow \text{CLAIM} \longrightarrow \text{EQUATION} \longrightarrow \text{MODIFICATION} \longrightarrow \text{IMPLEMENTATION} \longrightarrow \text{SIMULATION} \longrightarrow \text{RESULT}$$
Trace every major claim (leverage, reset boundaries, crash bounds, PIDE valuation, ACP-67 distributions, and feedback damping) through this graph.

### R2. Original SSRN-3856569 Independent Audit
Independently audit and re-derive the mathematical and economic claims of the original "Designing Stablecoins" paper:
- The original definition of $\alpha$ ($\alpha = 0.5$ vs. $\alpha = 1.0$) and its relationship to leverage.
- The economic meaning of Class B borrowing from Class A to invest in the underlying asset.
- The meaning of $V_A + V_B$ and its exact relationship to collateral assets.
- Secondary $A'/B'$ tranching and the claim that $A'$ behaves like a risk-free money-market account.
- Downward reset mechanics, conversion factor $\beta$, and the theoretical crash bound.
- Continuous-time periodic PDE/PIDE valuation, jump-diffusion pricing measure, and required boundary conditions.

### R3. anUSD Whitepaper Derivation & Delta Audit
Compare the current `anUSD` whitepaper line-by-line against the original SSRN design, producing an explicit delta matrix:
$$\text{ORIGINAL} \;\big|\; \text{CURRENT} \;\big|\; \text{DIFFERENCE} \;\big|\; \text{MATH EQUIVALENCE?} \;\big|\; \text{ECON EQUIVALENCE?} \;\big|\; \text{JUSTIFICATION} \;\big|\; \text{NEW ASSUMPTIONS} \;\big|\; \text{EFFECT ON RESULTS}$$
Investigate specific divergences:
- $\alpha = 0.5$ (SSRN) vs. $\alpha = 1.0$ ($V_B = 2S - V_A$ in anUSD).
- Raw ETH collateral vs. Liquid Staked AVAX ($sAVAX$) collateral and yield subsidy economics.
- Dynamic countercyclical validator subsidy ($\omega_{\text{val}} \in [20\%, 45\%]$) and ACP-67 recirculation sinks.
- Theoretical crash bounds ($-60.0\%$ from barrier $H_d$ vs. claimed $-75.0\%$ from par).
- Discrete EVM smart contract scalar rebasing ($O(1)$) vs. theoretical continuous share restructuring.

### R4. Design Summary & Generated Reports Line-by-Line Audit
Audit `SSRN-3856569_DESIGN_SUMMARY.md`, `ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md`, and `OPEN_SOURCE_TOOLING_AUDIT.md` against original source code and math to identify unsupported simplifications, extrapolations, circular in-sample calibrations, or newly introduced unstated assumptions.

### R5. Comprehensive Registers & Deliverables (Phase 0 Stop Rule)
Compile and publish the canonical audit registers:
- Source Map & Provenance Graph
- Assumptions Register (Explicit & Unstated)
- Claims Register (Epistemic Classification)
- Contradictions & Open Issues Register
- Data Requirements Register
- Stop rule: Do not run large-scale parameter sweeps or final optimization campaigns during this phase.

---

## Acceptance Criteria

### Verification & Audit Rubric
- [ ] Explicit stop condition: No large-scale parameter sweeps, final Monte Carlo runs, or parameter optimizations executed.
- [ ] Complete Source Map & Provenance Graph tracing all 23 protocol parameters and 6 core claims from academic origin to Solidity/cadCAD code.
- [ ] Rigorous line-by-line delta audit comparing SSRN-3856569, `SSRN-3856569_DESIGN_SUMMARY.md`, and `docs/WHITEPAPER.tex` across $\alpha$, leverage, collateral yield, and reset formulas.
- [ ] Epistemic audit of all generated reports challenging claims of "VERIFIED", "PROVED", "1.37% volatility", and "zero drawdown".
- [ ] Comprehensive Assumptions Register detailing all behavioral, liquidity, oracle, and market assumptions across the derivation chain.
- [ ] Comprehensive Open Issues & Contradictions Register documenting all mathematical, notation, and structural discrepancies without silent repairs.
- [ ] Final Source and Derivation Audit Report published to `docs/reports/SOURCE_AND_DERIVATION_AUDIT.md`.
