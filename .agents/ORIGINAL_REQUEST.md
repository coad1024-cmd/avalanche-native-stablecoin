# Original User Request

## Initial Request — 2026-08-29T08:52:19Z

Use a very large team of agents. Design and build the Avalanche-native stablecoin protocol, simulation engine, smart contracts, and commercial acquisition package from scratch, synthesizing the dual-class reset securitization mechanics (SSRN-3856569) with Avalanche community proposal economics (ACP-67 / Discussion #293).

Working directory: `/home/hash/Hub/Projects/avalanche-native-stablecoin`
Integrity mode: development

## References & Context
- Dual-Class Tranching Paper: `research/ssrn-3856569.pdf` & `research/SSRN-3856569_DESIGN_SUMMARY.md`
- Reference Smart Contracts: `https://github.com/DuoNetwork/duo-contract`
- Avalanche ACP-67 (Discussion #293): Yield recycling (50-75% AVAX buybacks, 15-25% validator rewards, 15-25% ecosystem growth)

## Requirements

### R1. Mathematical & Economic Protocol Specification
Formalize the complete dual-class tranching mechanism (Class A senior bond tranche, Class B leveraged long equity tranche, Class A′ USD stablecoin, Class B′ yield tranche) with upward and downward reset barriers ($H_u, H_d$), coupon rates ($R, R'$), coupon subsidies ($\tilde{R}$), and `sAVAX` liquid staking yield integration.

### R2. cadCAD Economic Simulation & Black Swan Stress Suite
Implement a reproducible Python simulation suite in `simulations/` featuring:
1. Monte Carlo jump-diffusion asset price models.
2. Invariant verification across consecutive upward/downward resets.
3. Stress testing black swan market plunges (>60% single-step drops) verifying zero principal loss on Class A′ stablecoins.
4. AVAX buyback & burn volume modeling across various TVL tiers ($100M to $5B).

### R3. Production-Ready Foundry Smart Contracts
Implement the smart contract architecture in `contracts/` using Foundry:
1. Core Custodian / Vault contract managing collateral deposits, minting, and redemptions.
2. Dual-Class and Secondary Tranche tokens (ERC-20).
3. Dynamic Upward/Downward Reset Controller executing automated share splits and mergers.
4. Avalanche Inter-Chain Messaging (ICM / Teleporter) cross-L1 dispatch adapter.
5. Invariant, fuzz, and unit test suites reaching full test passing status.

### R4. Whitepaper, Governance ACP, & Foundation Acquisition Package
Produce publication-grade documentation in `docs/`:
1. Comprehensive Technical Whitepaper (`docs/WHITEPAPER.md`).
2. Official Avalanche Community Proposal draft formatted for GitHub (`docs/ACP_PROPOSAL.md`).
3. Executive Acquisition & Ecosystem Investment Memo (`docs/ACQUISITION_MEMO.md`) for the Avalanche Foundation and Blizzard Fund.

## Acceptance Criteria

### Simulation & Verification
- [ ] cadCAD simulation script executes cleanly via Python and outputs summary figures / metrics confirming peg stability and model-free bounds.
- [ ] Jump crash tests prove Class A′ stablecoin survives up to a -60% instant drop without breaking the $1.00 peg parity.

### Smart Contract Verification
- [ ] Foundry project compiles with `forge build` with zero errors.
- [ ] `forge test` runs with 100% passing tests across unit, fuzz, and state invariant tests verifying total pool solvency ($W_A + W_B = 2P_t / \beta_t P_0$).

### Governance & Pitch Package
- [ ] `WHITEPAPER.md` contains full LaTeX mathematical formulations, architecture diagrams, and security proofs.
- [ ] `ACP_PROPOSAL.md` adheres to Avalanche Foundation governance formatting standards.
- [ ] `ACQUISITION_MEMO.md` provides complete tokenomics modeling, value accrual mechanics, and integration roadmap for Ava Labs.

## Follow-up Request — 2026-08-30T11:09:17Z

Perform a formal, rigorous open-source tooling audit and research-infrastructure evaluation for the anUSD adversarial research study. Evaluate candidate open-source software libraries against mathematical, simulation, statistical, control, and reproducibility requirements, establishing a minimal, reproducible toolchain with dual-implementation cross-validation and strict model-integrity enforcement.

Working directory: /home/hash/Hub/Projects/avalanche-native-stablecoin
Integrity mode: development

---

## Reference Material
- Master Whitepaper: docs/WHITEPAPER.md & docs/WHITEPAPER.tex
- Existing Models & Simulations: simulations/cadcad_core/
- Production Smart Contracts: contracts/src/

---

## Core Principles & Model-Integrity Architecture

1. Model-First Sovereignty (No Silent Semantic Shift): External libraries must NEVER redefine the canonical anUSD model. The workflow is strictly:
   Canonical Model -> Tool Implementation -> Validation against Canonical Model
2. Dual-Implementation Cross-Validation: Every critical numerical result must be cross-verified using at least two independent implementations (e.g., cadCAD dynamical system vs. native NumPy/SciPy state-machine; SALib Sobol decomposition vs. independent Saltelli bootstrap).
3. Reproducibility Standard: Every experiment configuration must record exact library versions, Python runtime, parameter configurations, PRNG seeds, numerical tolerances, and lineage hashes.

---

## Candidate Tooling under Investigation

1. cadCAD: Generalized Dynamical Systems (GDS), discrete state-update blocks (PSUBs), stochastic Monte Carlo loops, and multi-agent coordination.
2. SALib: Global Sensitivity Analysis (GSA), Sobol variance decomposition (Si, STi), Morris screening, and parameter interaction matrices.
3. PyMC + ArviZ: Bayesian parameter estimation, MCMC posterior sampling, hierarchical market-regime modeling, and credible interval uncertainty quantification.
4. QuantLib: Quantitative finance pricing, PIDE jump-diffusion benchmarks, term-structure curves, and numerical PDE solvers.
5. Additional Candidates: SciPy (QMC Sobol/LHS & optimization), Control-Systems (Python Control Systems Library for root-locus/Bode/Nyquist), SimPy (discrete event simulation), MLflow (lineage/experiment tracking).

---

## Requirements

### R1. 15-Point Multi-Criteria Evaluation per Tool
Evaluate every candidate tool across all 15 explicit criteria:
1. Exact problem solved
2. Research component requiring it
3. Whitepaper necessity
4. Semantic fidelity to canonical model
5. Mathematical/numerical methods used
6. Maintenance & activity status
7. Open-source license (MIT, Apache-2.0, BSD)
8. Reproducibility implications
9. Determinism & random-seed management
10. Numerical stability & precision bounds
11. Performance & scaling throughput
12. Integration & dependency complexity
13. Hidden assumptions or default biases
14. Simpler native implementation trade-off
15. Formal Verdict: REQUIRED | RECOMMENDED | OPTIONAL | REJECTED

### R2. Canonical Model / Tool Interface Specification
Define explicit, type-safe interface contracts between the canonical mathematical/accounting model and external tool APIs to prevent library defaults from altering state-transition semantics.

### R3. Dual-Implementation Cross-Validation Protocol
Design concrete cross-validation protocols for:
- State-machine & reset trajectories (cadCAD vs. Native NumPy Vectorized Engine)
- Sensitivity indices (SALib vs. Native Saltelli/Sobol QMC Engine)
- Control stability & root-locus (Python-Control / SciPy ODE vs. Discrete Differential Approximations)
- Jump-diffusion PIDE valuation (Custom Crank-Nicolson / Feynman-Kac vs. QuantLib / SciPy)

### R4. Minimal Reproducible Research Stack
Formulate the recommended minimal toolchain, documenting rejected candidates with explicit technical rationales, along with a full dependency graph mapping tools to specific research milestones.

---

## Acceptance Criteria

### Audit Deliverables & Verification Rubric
- [ ] Comprehensive 15-point evaluation completed for all 4 primary candidates (cadCAD, SALib, PyMC + ArviZ, QuantLib) plus auxiliary scientific libraries (SciPy, control).
- [ ] Formal classification of every evaluated tool as REQUIRED, RECOMMENDED, OPTIONAL, or REJECTED with clear justification.
- [ ] Explicit documentation of any hidden assumptions or semantic drift risks identified in candidate libraries.
- [ ] Concrete Dual-Implementation Cross-Validation specification for state dynamics and sensitivity indices.
- [ ] Canonical Model / Tool Interface Specification detailing schemas, state boundaries, and invariant validation hooks.
- [ ] Reproducibility strategy detailing seed orchestration, environment pinning, and cryptographic lineage tracking (_lineage.jsonl).
## Follow-up — 2026-08-30T11:44:54Z

Perform a first-principles, source-critical audit of the repository's research materials, mathematical derivations, design summaries, whitepapers, generated reports, simulation code, and smart contracts. Treat all repository contents as evidence to be audited rather than ground truth, constructing an end-to-end derivation and provenance graph that traces every major mechanism, equation, theorem, and claim back to its earliest known source while identifying every notation change, assumption shift, and unexplained modification.

Working directory: /home/hash/Hub/Projects/avalanche-native-stablecoin
Integrity mode: development

---

## Reference Materials to Audit
- Original Academic Literature: SSRN-3856569 ("Designing Stablecoins", Cao et al., 2021)
- Summary Extraction: SSRN-3856569_DESIGN_SUMMARY.md
- Protocol Whitepapers: docs/WHITEPAPER.md & docs/WHITEPAPER.tex
- Generated Audit Reports: docs/reports/ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md & docs/reports/OPEN_SOURCE_TOOLING_AUDIT.md
- Simulation & Mathematical Models: simulations/cadcad_core/, simulations/robustness_study/, workflows/
- Smart Contracts & Invariants: contracts/src/, contracts/test/

---

## Core Principles & Source-Criticality Rules

1. No Document is Source of Truth: Do not treat original academic papers, design summaries, whitepapers, generated reports, or implementation code as authoritative. Every layer must be independently audited and verified.
2. No Trust Transfer: Never accept an earlier agent's claim or report verdict ("VERIFIED", "15/15 PASSED", "PROVED") as ground truth. Every claim must be traced to reproducible source evidence, code, or mathematics.
3. Lossy Transformation Auditing: Evaluate each step in the derivation chain:
   Original Literature (SSRN-3856569) -> Design Summary -> anUSD Whitepaper -> Generated Reports -> Code Implementation
   Identify every shift in notation, parameterization, assumptions, economic interpretation, mathematical structure, and implementation semantics.
4. Preserve Discrepancies: Never silently reconcile or smooth over inconsistencies. Record them explicitly in an immutable Open Issues & Contradictions Register.

---

## Requirements

### R1. Source-to-Implementation Provenance Graph
Construct a complete, machine-readable provenance graph:
SOURCE -> CLAIM -> EQUATION -> MODIFICATION -> IMPLEMENTATION -> SIMULATION -> RESULT
Trace every major claim (leverage, reset boundaries, crash bounds, PIDE valuation, ACP-67 distributions, and feedback damping) through this graph.

### R2. Original SSRN-3856569 Independent Audit
Independently audit and re-derive the mathematical and economic claims of the original "Designing Stablecoins" paper:
- The original definition of alpha (alpha = 0.5 vs. alpha = 1.0) and its relationship to leverage.
- The economic meaning of Class B borrowing from Class A to invest in the underlying asset.
- The meaning of VA + VB and its exact relationship to collateral assets.
- Secondary A'/B' tranching and the claim that A' behaves like a risk-free money-market account.
- Downward reset mechanics, conversion factor beta, and the theoretical crash bound.
- Continuous-time periodic PDE/PIDE valuation, jump-diffusion pricing measure, and required boundary conditions.

### R3. anUSD Whitepaper Derivation & Delta Audit
Compare the current anUSD whitepaper line-by-line against the original SSRN design, producing an explicit delta matrix:
ORIGINAL | CURRENT | DIFFERENCE | MATH EQUIVALENCE? | ECON EQUIVALENCE? | JUSTIFICATION | NEW ASSUMPTIONS | EFFECT ON RESULTS
Investigate specific divergences:
- alpha = 0.5 (SSRN) vs. alpha = 1.0 (VB = 2S - VA in anUSD).
- Raw ETH collateral vs. Liquid Staked AVAX (sAVAX) collateral and yield subsidy economics.
- Dynamic countercyclical validator subsidy (omega_val in [20%, 45%]) and ACP-67 recirculation sinks.
- Theoretical crash bounds (-60.0% from barrier Hd vs. claimed -75.0% from par).
- Discrete EVM smart contract scalar rebasing (O(1)) vs. theoretical continuous share restructuring.

### R4. Design Summary & Generated Reports Line-by-Line Audit
Audit SSRN-3856569_DESIGN_SUMMARY.md, ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md, and OPEN_SOURCE_TOOLING_AUDIT.md against original source code and math to identify unsupported simplifications, extrapolations, circular in-sample calibrations, or newly introduced unstated assumptions.

### R5. Comprehensive Registers & Deliverables (Phase 0 Stop Rule)
Compile and publish the canonical audit registers:
- Source Map & Provenance Graph
- Assumptions Register (Explicit & Unstated)
- Claims Register (Epistemic Classification)
- Contradictions & Open Issues Register
- Data Requirements Register
- Stop rule: Do not run large-scale parameter sweeps or final optimization campaigns during this phase.

---

## Acceptance Criteria

### Verification & Audit Rubric
- [ ] Explicit stop condition: No large-scale parameter sweeps, final Monte Carlo runs, or parameter optimizations executed.
- [ ] Complete Source Map & Provenance Graph tracing all 23 protocol parameters and 6 core claims from academic origin to Solidity/cadCAD code.
- [ ] Rigorous line-by-line delta audit comparing SSRN-3856569, SSRN-3856569_DESIGN_SUMMARY.md, and docs/WHITEPAPER.tex across alpha, leverage, collateral yield, and reset formulas.
- [ ] Epistemic audit of all generated reports challenging claims of "VERIFIED", "PROVED", "1.37% volatility", and "zero drawdown".
- [ ] Comprehensive Assumptions Register detailing all behavioral, liquidity, oracle, and market assumptions across the derivation chain.
- [ ] Comprehensive Open Issues & Contradictions Register documenting all mathematical, notation, and structural discrepancies without silent repairs.
- [ ] Final Source and Derivation Audit Report published to docs/reports/SOURCE_AND_DERIVATION_AUDIT.md.

