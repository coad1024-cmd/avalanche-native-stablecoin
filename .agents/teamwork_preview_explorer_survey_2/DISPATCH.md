## 2026-08-31T02:41:54Z
<USER_REQUEST>
You are the Invariants & Control Explorer.
Your working directory is: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_explorer_survey_2/
You must read:
- /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md
- /home/hash/Hub/Projects/avalanche-native-stablecoin/simulations/canonical_accounting.py
- /home/hash/Hub/Projects/avalanche-native-stablecoin/contracts/src/remediation/
- /home/hash/Hub/Projects/avalanche-native-stablecoin/contracts/test/unit/DualImplementationComparison.t.sol
- Relevant simulation files and controller code in the repository.

Your Tasks:
1. Extract the canonical double-entry stock-flow accounting equations, balance sheet invariants, conservation laws, and solvency conditions.
2. Formulate true physical hard constraints (stock non-negativity, zero balance sheet drift, realizable solvency, simplex weight conservation) vs optimization objectives / aspirational targets.
3. Extract smart contract remediation invariants, liquidation/reset mechanics, fee routing, and numerical safety bounds.
4. Formalize closed-loop controller dynamics: plant transfer function for CPMM AMM K_amm(L), error dynamics e(t) = P(t) - P_target, control laws u(t) for P, PI, PID, and anti-windup / saturation limits.
5. Formulate parameter spaces, stability criteria (Routh-Hurwitz / Lyapunov / Bode gain margins), and failure boundary definitions d Omega_fail.
6. Write a detailed, rigorous handoff report with exact equations and invariants to `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/teamwork_preview_explorer_survey_2/handoff.md`.
7. Send a completion message to the parent with a summary of your findings.
</USER_REQUEST>
