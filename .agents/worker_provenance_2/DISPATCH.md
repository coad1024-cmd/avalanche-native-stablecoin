# DISPATCH — worker_provenance_2

## Mission
Construct the complete Machine-Readable Source-to-Implementation Provenance Graph (R1) and conduct the Line-by-Line Audit of Design Summaries & Generated Reports (R4).

## Authoritative User Request
Read `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md` verbatim.

## Working Directory
`/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_provenance_2`

## Inputs & Evidence Sources
- Survey report: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/survey_academic_whitepaper.md`
- Survey report: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_2/survey_generated_reports.md`
- Survey report: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_3/survey_code_implementation.md`
- Reports to audit:
  - `research/SSRN-3856569_DESIGN_SUMMARY.md`
  - `reports/ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md`
  - `reports/OPEN_SOURCE_TOOLING_AUDIT.md`
  - `reports/MODEL_CARD.md`, `reports/PHASE_0_RECONNAISSANCE.md`, `reports/FORMAL_SPEC_DELTA_AUDIT.md`, `reports/VERIFICATION_AUDIT_TRAIL.md`
- Parameter registry & code: `simulations/robustness_study/parameter_registry.py`, `contracts/src/`, `simulations/cadcad_core/`

## Specific Requirements:
1. **Source-to-Implementation Provenance Graph (R1)**:
   - Construct a machine-readable provenance graph (JSON / YAML / Markdown tables) tracing all **23 protocol parameters** ($\alpha, H_u, H_d, R, R', \omega_{\text{val,min}}, \omega_{\text{val,max}}, \kappa_{\text{drawdown}}, \omega_{\text{eco}}, \omega_{\text{burn,min}}, \text{split}_u, \text{split}_d, \dots$) and **6 core claims** from academic origin (SSRN-3856569) -> Design Summary -> Whitepaper -> Generated Reports -> Solidity smart contracts and cadCAD simulation code.
   - For every parameter, document: Parameter Symbol, Academic Source/Section, Whitepaper Notation, Code Variable Name (Solidity & cadCAD), Canonical Value/Range, Domain Shifts, and Lossy Transformations.
2. **Design Summary & Generated Reports Line-by-Line Audit (R4)**:
   - Audit `SSRN-3856569_DESIGN_SUMMARY.md`, `ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md`, and `OPEN_SOURCE_TOOLING_AUDIT.md`.
   - Explicitly challenge, deconstruct, and falsify unjustified epistemic claims:
     a) "1.37% peg volatility": Prove it is an artifact of noiseless linear coupon accrual in `run_monte_carlo.py` rather than market stability.
     b) Solvency Invariant Tautology ($|V_A + V_B - 2S| \le 10^{-12}$): Prove this is a circular algebraic identity ($V_B \equiv 2S - V_A$), not proof of vault solvency under physical runs.
     c) Damping ratio contradiction ($\zeta = 17.03$ vs $\zeta = 1.42$) and uncalibrated plant parameters ($K, \tau$).
     d) PIDE solver mismatch: Merton log-normal vs Kou double-exponential.
     e) MEV proof facade ($>\$45\text{M}$ MPMC): Expose the hardcoded simulation shortcuts.
     f) Circular gate validation: Expose how `verify_contractual_gates.py` checks `status: PASSED` in `gates.yaml`.
3. Write your output to `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_provenance_2/provenance_graph_and_reports_audit.md` and generate a comprehensive `handoff.md`.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
