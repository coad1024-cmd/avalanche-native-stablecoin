# Dispatch History

## 2026-08-30T11:10:51Z
You are spec_miner_survey_1.
Your working directory is: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1

MANDATORY FIRST STEP:
Read `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md` and `/home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md`.

YOUR MISSION:
Perform a comprehensive specification mining of the authoritative mathematical, economic, control-theoretic, and smart contract models for the anUSD (Avalanche-native stablecoin) research study.

Investigate:
1. `docs/WHITEPAPER.md` & `docs/WHITEPAPER.tex`
2. `contracts/src/` (Foundry smart contracts: Vault, Tranche tokens, ResetController, Teleporter adapters)
3. `docs/reports/` and any accompanying economic models

Document in detail:
- Complete dual-class tranche accounting equations (NAV, $W_A$, $W_B$, Class A senior bond, Class B leveraged long equity, Class A' USD stablecoin, Class B' yield tranche).
- Invariant equations: Solvency invariant ($W_A + W_B = 2P_t / (\beta_t P_0)$), peg parity, yield distribution conservation.
- Reset trigger conditions: Upward reset ($P_t \ge H_u$), Downward reset ($P_t \le H_d$), automated share splits/mergers, baseline adjustment $\beta_{t+1}$.
- Coupon rates ($R, R'$), coupon subsidies ($\tilde{R}$), and `sAVAX` liquid staking yield recycling parameters (ACP-67: 50-75% buybacks, 15-25% validator rewards, 15-25% ecosystem growth).
- Jump-diffusion asset price dynamics ($dS_t / S_{t-} = \mu dt + \sigma dW_t + J dN_t$), jump amplitude distributions (Kou double exponential / Merton lognormal), PIDE formulation for barrier pricing.
- Feedback control systems (PID peg stability, interest rate feedback, dynamic reset bounds).
- State variables required for simulation and exact type/precision definitions (e.g. 18-decimal fixed-point vs float64 vs arbitrary precision).

Deliver your detailed report in `.agents/spec_miner_survey_1/handoff.md` and update `.agents/spec_miner_survey_1/progress.md`. Send a completion message back when finished.
