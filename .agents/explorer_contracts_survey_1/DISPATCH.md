## 2026-08-29T08:56:32Z
You are an Explorer investigating the Smart Contract Architecture & Foundry Infrastructure for the Avalanche Native Stablecoin Protocol.
Your Working Directory is: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_contracts_survey_1
Workspace Root: /home/hash/Hub/Projects/avalanche-native-stablecoin
Authoritative User Request: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md

Task:
1. Read /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md, /home/hash/Hub/Projects/avalanche-native-stablecoin/research/SSRN-3856569_DESIGN_SUMMARY.md, and inspect the repository structure.
2. Investigate the smart contract architecture required to implement the dual-class reset stablecoin on Avalanche:
   - Core Custodian / Vault: collateral deposit (AVAX / sAVAX), minting tranches in pairs (1 Class A + 1 Class B per 2 units NAV collateral), redemption in pairs, fee handling.
   - Dual-Class ERC-20 Tokens: Class A (TokenA), Class B (TokenB), Class A' (StablecoinUSD / TokenAPrime), Class B' (YieldTranche / TokenBPrime).
   - Secondary Tranche Splitter/Merger: 1 Class A <-> 1 Class A' + 1 Class B'.
   - Dynamic Reset Controller: Automated execution of upward reset (split & payout) and downward reset (reverse split & principal payback) based on oracle price feeds.
   - Avalanche Inter-Chain Messaging (ICM / Teleporter) Adapter: Cross-L1 transfer/mint/burn of Class A' USD stablecoin.
   - Oracle Adapter: Price feed integration with TWAP / Chainlink / Pyth, staleness and circuit breakers.
   - Foundry Project Setup: foundry.toml, dependencies (OpenZeppelin, forge-std, Teleporter/ICM interfaces), compilation settings.
   - Testing Strategy: Unit tests, fuzz tests, invariant testing harnesses (handler-based testing for total pool balance invariant).
3. Produce a detailed architectural and contract specification report in `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_contracts_survey_1/survey_contracts.md`.
4. Write a self-contained handoff report in `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_contracts_survey_1/handoff.md`.
5. Send a message to the caller with a summary of findings and the path to your reports.
