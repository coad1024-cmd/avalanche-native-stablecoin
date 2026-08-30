# DISPATCH — spec_miner_survey_1

## 2026-08-30T11:46:18Z

You are the Academic & Whitepaper Spec Miner for the anUSD First-Principles Source and Derivation Audit.
Your working directory is: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1`.
You MUST read the authoritative user request at `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md` before starting work.
You MUST also read your dispatch instructions at `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/DISPATCH.md`.

Your mission:
1. Search the repository for all copies or excerpts of SSRN-3856569, `docs/WHITEPAPER.tex`, `SSRN-3856569_DESIGN_SUMMARY.md`, and related research files.
2. Independently extract, catalog, and analyze all mathematical formulations:
   - Alpha parameter definition (alpha = 0.5 vs alpha = 1.0)
   - Leverage calculation formulas
   - Tranche valuation and preservation (VA + VB = V)
   - Secondary A'/B' tranching
   - Downward reset mechanics, conversion factor beta, and crash bounds (-60% vs -75%)
   - Continuous-time PIDE valuation & jump-diffusion pricing models
   - Collateral yield handling and dynamic validator subsidy (omega_val in [20%, 45%])
   - Discrete EVM scalar rebasing vs continuous share restructuring
3. Identify all 23 protocol parameters defined across these documents and record notation shifts, parameter domain changes, and unstated assumptions.
4. Output your detailed findings to `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/survey_academic_whitepaper.md` and write a comprehensive `handoff.md`. Send a message when complete.
