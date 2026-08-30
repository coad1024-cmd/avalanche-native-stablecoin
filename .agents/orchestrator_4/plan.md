# Plan: anUSD First-Principles Source and Derivation Audit

## Overview
Perform a first-principles, source-critical audit across the entire derivation chain:
Academic Literature (SSRN-3856569) → Design Summaries → Whitepaper (docs/WHITEPAPER.tex) → Generated Reports → Implementation Code (Solidity & cadCAD).

## Audit Methodology & Core Directives
1. **No Document is Source of Truth**: Treat every repository content as unverified evidence subject to rigorous audit.
2. **Zero Trust Transfer**: Reject previous claims of "VERIFIED", "15/15 PASSED", or "PROVED" unless independently established from reproducible mathematics and code.
3. **Lossy Transformation Auditing**: Map all shifts in notation, assumptions, parameter bounds, economic interpretations, and mathematical structures.
4. **Preserve Discrepancies**: Maintain an immutable Contradictions & Open Issues Register.
5. **Phase 0 Stop Rule**: Avoid running large-scale parameter sweeps or final optimization campaigns.

## Work Breakdown & Milestones

### Milestone 0: Survey & Artifact Indexing (Track Exploration)
- Explorers index all repository documents, research papers, LaTeX sources, markdown reports, Python/cadCAD models, and Solidity smart contracts.
- Identify all source files for SSRN-3856569, docs/WHITEPAPER.tex, SSRN-3856569_DESIGN_SUMMARY.md, ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md, OPEN_SOURCE_TOOLING_AUDIT.md, and contracts/simulations.

### Milestone 1: SSRN-3856569 Independent Mathematical Audit (R2)
- Re-derive alpha (0.5 vs 1.0) and leverage formulas.
- Re-derive tranche valuation ($V_A + V_B = V$) and secondary $A'/B'$ tranching.
- Re-derive downward reset mechanics, conversion factor $\beta$, and crash bounds.
- Re-derive continuous-time PIDE valuation and jump-diffusion pricing models.

### Milestone 2: anUSD Whitepaper Derivation & Delta Audit (R3)
- Line-by-line delta matrix comparing SSRN-3856569 vs `docs/WHITEPAPER.tex`.
- Audit specific shifts: $\alpha$ definitions, leverage formulas, collateral yield integration, dynamic validator subsidy ($\omega_{val} \in [20\%, 45\%]$), crash bounds ($-60\%$ vs $-75\%$), discrete EVM scalar rebasing vs continuous share restructuring.

### Milestone 3: Design Summary & Generated Reports Audit (R4)
- Audit `SSRN-3856569_DESIGN_SUMMARY.md`.
- Audit `ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md`.
- Audit `OPEN_SOURCE_TOOLING_AUDIT.md`.
- Challenge claims of "VERIFIED", "PROVED", "1.37% volatility", "zero drawdown".

### Milestone 4: Code Implementation & Provenance Graph Audit (R1)
- Trace all 23 protocol parameters and 6 core claims from academic origin to Solidity smart contracts and cadCAD simulation models.
- Machine-readable provenance graph and semantic audit of contract implementation vs mathematical specifications.

### Milestone 5: Registers & Final Report Synthesis (R5)
- Construct:
  1. Source Map & Provenance Graph (JSON / YAML / Markdown)
  2. Assumptions Register (Explicit & Unstated)
  3. Claims Register (Epistemic Classification: Proved, Claimed, Heuristic, Flawed)
  4. Contradictions & Open Issues Register
  5. Data Requirements Register
- Synthesize the authoritative report: `docs/reports/SOURCE_AND_DERIVATION_AUDIT.md`.

### Milestone 6: Adversarial Review & Forensic Gate
- Reviewers and Forensic Auditor verify completeness, rigorous re-derivations, source-critical adherence, and lack of unverified trust transfers.
