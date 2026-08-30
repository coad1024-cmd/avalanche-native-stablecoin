# DISPATCH — explorer_survey_3

## 2026-08-30T11:13:00Z
Initial dispatch for Open Source Tooling Audit.

## 2026-08-30T11:46:18Z
<USER_REQUEST>
You are the Code Implementation Auditor for the anUSD First-Principles Source and Derivation Audit.
Your working directory is: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_3`.
You MUST read the authoritative user request at `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md` before starting work.
You MUST also read your dispatch instructions at `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_3/DISPATCH.md`.

Your mission:
1. Search and index all codebase components:
   - Solidity smart contracts in `contracts/` (or wherever located in repo)
   - cadCAD and Python simulation code in `src/`, `sim/`, `models/`, `scripts/`
   - Test suites (Foundry/Hardhat/pytest)
2. Trace all 23 protocol parameters and core mechanisms to their exact variable names, constants, state variables, and functions in code.
3. Compare implementation semantics against mathematical specifications:
   - Discrete EVM fixed-point math vs continuous formulas
   - Tranche minting, burning, splitting, and rebasing mechanisms
   - Reset execution, oracle updates, and fee distribution
4. Document all semantic divergences, lossy transformations, rounding vulnerabilities, and unstated implementation shortcuts.
5. Output your detailed findings to `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_3/survey_code_implementation.md` and write a comprehensive `handoff.md`. Send a message when complete.
</USER_REQUEST>

