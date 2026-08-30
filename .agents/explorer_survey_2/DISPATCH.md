## 2026-08-30T11:10:51Z

You are explorer_survey_2.
Your working directory is: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_2

MANDATORY FIRST STEP:
Read `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md` and `/home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md`.

YOUR MISSION:
Perform a deep-dive code investigation into the existing simulation codebase:
1. Explore all files in `simulations/cadcad_core/` and any other simulation scripts in `simulations/`.
2. Inspect the discrete state-update blocks (PSUBs), policy functions, state update functions, simulation configuration, and execution pipelines.
3. Analyze:
   - How state transitions and reset events are modeled in cadCAD.
   - Performance characteristics, execution bottlenecks, overhead of cadCAD dictionary state copying vs vectorized NumPy array operations.
   - Determinism and PRNG seed management in current simulation code.
   - Numerical precision and stability issues (e.g., float64 truncation, floating point drift during consecutive resets).
   - Invariant check hooks in the current simulation engine.
   - How cadCAD semantics compare with native NumPy/SciPy state-machine engines.

Deliver your detailed report in `.agents/explorer_survey_2/handoff.md` and update `.agents/explorer_survey_2/progress.md`. Send a completion message back when finished.
