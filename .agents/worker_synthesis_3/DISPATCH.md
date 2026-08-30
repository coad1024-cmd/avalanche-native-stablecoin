# DISPATCH — worker_synthesis_3

## Mission
Synthesize all 5 comprehensive audit registers and author the definitive, authoritative Master Source and Derivation Audit Report published to `docs/reports/SOURCE_AND_DERIVATION_AUDIT.md`.

## Authoritative User Request
Read `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md` verbatim.

## Working Directory
`/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_synthesis_3`

## Evidence Sources to Integrate
1. `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/survey_academic_whitepaper.md`
2. `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_2/survey_generated_reports.md`
3. `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_3/survey_code_implementation.md`
4. `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_derivation_1/math_rederivations_and_delta_matrix.md`
5. `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_provenance_2/provenance_graph_and_reports_audit.md`

## Required Report Structure (`docs/reports/SOURCE_AND_DERIVATION_AUDIT.md`):
1. **Executive Summary & Epistemic Audit Verdict**:
   - High-level verdict on mathematical consistency, codebase implementation, and previous report claims.
   - Summary of key critical discoveries (State machine flapping defect in `ResetController.sol`, `TrancheSplitter.sol` 2:1 token bug, 1.37% volatility artifact, $-60\%$ vs $-75\%$ crash bound scoping, circular gate validations, damping ratio contradictions).
2. **First-Principles Derivation Chain & Lossy Transformation Analysis**:
   - Full derivation trace: SSRN-3856569 $\to$ Design Summary $\to$ Whitepaper $\to$ Generated Reports $\to$ Solidity/cadCAD.
   - Notation, assumption, and semantic shifts at each layer.
3. **SSRN-3856569 Independent Mathematical Audit (R2)**:
   - Full re-derivations of $\alpha$ (0.5 vs 1.0), leverage, $V_A+V_B=2S$, $V_{A'}+V_{B'}=2V_A$, downward resets, conversion factor $\beta$, single-step crash bounds ($-60\%$ from barrier vs $-75\%$ from par), and PIDE jump-diffusion pricing.
4. **anUSD Whitepaper Derivation & Delta Matrix (R3)**:
   - Complete line-by-line delta matrix across all parameters, mechanisms, yield recycling, dynamic validator subsidy ($\omega_{\text{val}} \in [20\%, 45\%]$), and EVM scalar multiplier rebasing.
5. **Design Summary & Generated Reports Line-by-Line Audit (R4)**:
   - Comprehensive audit of `SSRN-3856569_DESIGN_SUMMARY.md`, `ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md`, and `OPEN_SOURCE_TOOLING_AUDIT.md`.
   - Complete deconstruction of unverified claims ("VERIFIED", "PROVED", "1.37% volatility", "solvency invariant tautology", $\zeta=17.03$ vs $1.42$, MPMC facade).
6. **Code & Contract Implementation Provenance Audit (R1)**:
   - Full tracing of all 23 parameters and 6 claims into Solidity contracts and cadCAD simulation code.
   - Full analysis of code vulnerabilities (Reset flapping, secondary tranche rebase disconnect, rounding dust).
7. **Comprehensive Registers (R5)**:
   - Register 1: Source Map & Machine-Readable Provenance Graph (YAML & Markdown tables for all 23 parameters and 6 claims).
   - Register 2: Assumptions Register (Explicit & Unstated Assumptions cataloged with validity, risk level, and empirical status).
   - Register 3: Claims Register (Epistemic Classification: PROVED, CLAIMED, HEURISTIC, FLAWED, TAUTOLOGICAL).
   - Register 4: Contradictions & Open Issues Register (Immutable, numbered list of all discovered contradictions, bugs, and notation shifts).
   - Register 5: Data Requirements Register (Empirical data feeds, calibration requirements, oracle specifications, and stress testing scenarios).
8. **Actionable Recommendations & Phase 0 Conclusions**:
   - Exact remediation steps for Solidity contracts, cadCAD simulation scripts, and whitepaper revisions.
   - Phase 0 Stop Rule adherence confirmation.

## Target Output File:
- Write the final comprehensive deliverable to: `/home/hash/Hub/Projects/avalanche-native-stablecoin/docs/reports/SOURCE_AND_DERIVATION_AUDIT.md`.
- Write your working handoff report to: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_synthesis_3/handoff.md`.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
