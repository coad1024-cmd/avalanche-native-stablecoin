# DISPATCH Log

## 2026-08-30T11:09:59Z
You are the Project Orchestrator for the anUSD Open-Source Tooling Audit & Research-Infrastructure Evaluation.

Working directory: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/orchestrator_3
Project root: /home/hash/Hub/Projects/avalanche-native-stablecoin
Original request: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md

Your mission is to perform a formal, rigorous open-source tooling audit and research-infrastructure evaluation for the anUSD adversarial research study, and publish the final comprehensive deliverable to `docs/reports/OPEN_SOURCE_TOOLING_AUDIT.md`.

Context & References:
- Master Whitepaper: docs/WHITEPAPER.md & docs/WHITEPAPER.tex
- Existing Models & Simulations: simulations/cadcad_core/
- Production Smart Contracts: contracts/src/
- Existing reports & specs: docs/reports/

Core Requirements:
1. R1: 15-Point Multi-Criteria Evaluation per candidate tool across all 15 explicit criteria:
   - Primary candidates: cadCAD, SALib, PyMC + ArviZ, QuantLib
   - Auxiliary scientific libraries: SciPy, control (Python Control Systems Library), SimPy, MLflow
   - Across all 15 criteria: (1) Exact problem solved, (2) Research component requiring it, (3) Whitepaper necessity, (4) Semantic fidelity to canonical model, (5) Mathematical/numerical methods used, (6) Maintenance & activity status, (7) Open-source license, (8) Reproducibility implications, (9) Determinism & random-seed management, (10) Numerical stability & precision bounds, (11) Performance & scaling throughput, (12) Integration & dependency complexity, (13) Hidden assumptions or default biases, (14) Simpler native implementation trade-off, (15) Formal Verdict: REQUIRED | RECOMMENDED | OPTIONAL | REJECTED.
2. R2: Canonical Model / Tool Interface Specification: Define explicit, type-safe interface contracts between the canonical mathematical/accounting model and external tool APIs to prevent library defaults from altering state-transition semantics. Detail schemas, state boundaries, invariant validation hooks.
3. R3: Dual-Implementation Cross-Validation Protocol: Design concrete cross-validation protocols for:
   - State-machine & reset trajectories (cadCAD vs. Native NumPy Vectorized Engine)
   - Sensitivity indices (SALib vs. Native Saltelli/Sobol QMC Engine)
   - Control stability & root-locus (Python-Control / SciPy ODE vs. Discrete Differential Approximations)
   - Jump-diffusion PIDE valuation (Custom Crank-Nicolson / Feynman-Kac vs. QuantLib / SciPy)
4. R4: Minimal Reproducible Research Stack: Formulate the recommended minimal toolchain, documenting rejected candidates with explicit technical rationales, along with a full dependency graph mapping tools to specific research milestones.
5. Reproducibility strategy: Seed orchestration, environment pinning, cryptographic lineage tracking (_lineage.jsonl).
6. Output Deliverable: Publish the final audit report to `docs/reports/OPEN_SOURCE_TOOLING_AUDIT.md`.
