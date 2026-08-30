# DISPATCH

## 2026-08-30T11:45:33Z

You are the Project Orchestrator for the anUSD First-Principles Source and Derivation Audit.

Your working directory is: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/orchestrator_4`
Project root: `/home/hash/Hub/Projects/avalanche-native-stablecoin`
Authoritative User Request: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md`

Perform a first-principles, source-critical audit of the repository's research materials, mathematical derivations, design summaries, whitepapers, generated reports, simulation code, and smart contracts. Treat all repository contents as evidence to be audited rather than ground truth, constructing an end-to-end derivation and provenance graph that traces every major mechanism, equation, theorem, and claim back to its earliest known source while identifying every notation change, assumption shift, and unexplained modification.

### Core Principles & Source-Criticality Rules:
1. No Document is Source of Truth: Do not treat original academic papers, design summaries, whitepapers, generated reports, or implementation code as authoritative. Every layer must be independently audited and verified.
2. No Trust Transfer: Never accept an earlier agent's claim or report verdict ("VERIFIED", "15/15 PASSED", "PROVED") as ground truth. Every claim must be traced to reproducible source evidence, code, or mathematics.
3. Lossy Transformation Auditing: Evaluate each step in the derivation chain:
   Original Literature (SSRN-3856569) -> Design Summary -> anUSD Whitepaper -> Generated Reports -> Code Implementation
   Identify every shift in notation, parameterization, assumptions, economic interpretation, mathematical structure, and implementation semantics.
4. Preserve Discrepancies: Never silently reconcile or smooth over inconsistencies. Record them explicitly in an immutable Open Issues & Contradictions Register.

### Requirements:
- R1. Source-to-Implementation Provenance Graph: machine-readable provenance graph tracing all 23 protocol parameters and 6 core claims from academic origin to Solidity/cadCAD code.
- R2. Original SSRN-3856569 Independent Audit: Re-derive alpha (0.5 vs 1.0), leverage, VA+VB, secondary A'/B' tranching, downward reset mechanics & conversion beta & crash bounds, continuous-time PIDE valuation & jump-diffusion pricing.
- R3. anUSD Whitepaper Derivation & Delta Audit: Line-by-line delta matrix comparing SSRN-3856569 vs docs/WHITEPAPER.tex across alpha, leverage, collateral yield, dynamic validator subsidy (omega_val in [20%, 45%]), crash bounds (-60% vs -75%), and discrete EVM scalar rebasing vs continuous share restructuring.
- R4. Design Summary & Generated Reports Line-by-Line Audit: Audit SSRN-3856569_DESIGN_SUMMARY.md, ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md, and OPEN_SOURCE_TOOLING_AUDIT.md. Challenge claims of "VERIFIED", "PROVED", "1.37% volatility", "zero drawdown".
- R5. Comprehensive Registers & Deliverables:
  - Source Map & Provenance Graph
  - Assumptions Register (Explicit & Unstated)
  - Claims Register (Epistemic Classification)
  - Contradictions & Open Issues Register
  - Data Requirements Register
  - Final Source and Derivation Audit Report published to `docs/reports/SOURCE_AND_DERIVATION_AUDIT.md`.
  - Phase 0 Stop Rule: Do not run large-scale parameter sweeps or final optimization campaigns during this phase.

Maintain your `plan.md` and `progress.md` in your working directory. Report completion back to the sentinel when finished.
