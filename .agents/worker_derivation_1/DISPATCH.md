# DISPATCH — worker_derivation_1

## 2026-08-30T11:51:24Z

### Mission
Perform the rigorous, first-principles mathematical re-derivation (R2) and construct the line-by-line whitepaper delta matrix (R3) for the anUSD First-Principles Source and Derivation Audit.

### Authoritative User Request
Read `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md` verbatim.

### Working Directory
`/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_derivation_1`

### Inputs & Evidence Sources
- Survey report: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/survey_academic_whitepaper.md`
- Survey report: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_2/survey_generated_reports.md`
- Survey report: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_3/survey_code_implementation.md`
- Original literature & design summary: `research/SSRN-3856569_DESIGN_SUMMARY.md`
- Whitepaper source: `docs/WHITEPAPER.tex` and `docs/WHITEPAPER.md`
- Simulation math: `simulations/cadcad_core/mechanisms/tranche_math.py`, `dynamic_resets.py`, `pide_solver.py`

### Specific Requirements:
1. **SSRN-3856569 Independent Mathematical Re-Derivations (R2)**:
   - Provide complete, self-contained mathematical proofs and step-by-step derivations for:
     a) $\alpha = 0.5$ (capital share) vs $\alpha = 1.0$ (tranche ratio) and leverage formula $L_B = 1/(1-\alpha) = 1 + \chi$.
     b) Primary tranche valuation conservation $V_A(t) + V_B(t) = 2 S_t$ and secondary $A'/B'$ tranching $V_{A'} + V_{B'} = 2 V_A$.
     c) Downward reset mechanics: threshold $H_d$, conversion factor $\beta$, and the single-step crash bound theorem $\Delta P / P \ge \frac{1}{2}\left(\frac{1 + R' v_t + 2\tilde{R} v_t}{1 + R v_t + H_d}\right) - 1$.
     d) Explicitly derive and contrast the crash bound from barrier $H_d = 0.25$ ($-60.00\%$) vs from par $S=1.0$ ($-75.00\%$).
     e) Continuous-time PIDE valuation and jump-diffusion pricing models (Kou double-exponential vs Merton log-normal, boundary conditions, and viscosity solutions).
2. **anUSD Whitepaper Derivation & Delta Audit (R3)**:
   - Construct a comprehensive, line-by-line delta matrix comparing SSRN-3856569 vs `docs/WHITEPAPER.tex` across:
     - Alpha definition & parameterization
     - Leverage mechanics
     - Collateral yield integration ($y_{\text{AVAX}}$ / $R_{\text{val}}$)
     - Dynamic countercyclical validator subsidy ($\omega_{\text{val}} \in [20\%, 45\%]$)
     - Crash tolerance bounds ($-60\%$ vs $-75\%$)
     - Discrete EVM scalar multiplier rebasing vs continuous share restructuring
     - Price discovery & oracle integration (Pyth + Chainlink EMA vs continuous asset price $S_t$)
3. Write your output to `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_derivation_1/math_rederivations_and_delta_matrix.md` and generate a comprehensive `handoff.md`.

### Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
