# Plan: anUSD Open-Source Tooling Audit & Research-Infrastructure Evaluation

## Objective
Deliver a publication-grade, formal, and rigorous open-source tooling audit and research-infrastructure evaluation report in `docs/reports/OPEN_SOURCE_TOOLING_AUDIT.md` adhering strictly to R1–R6.

## Milestones & Execution Phases

### Phase 1: Survey & Mapping (Explorer / Spec Miner Dispatch)
- Explore existing codebase: `docs/WHITEPAPER.md`, `docs/WHITEPAPER.tex`, `simulations/cadcad_core/`, `contracts/src/`, `docs/reports/`.
- Mine exact mathematical, simulation, statistical, control, and reproducibility requirements for anUSD.
- Map the 8 candidate tools (cadCAD, SALib, PyMC + ArviZ, QuantLib, SciPy, control, SimPy, MLflow) against the anUSD canonical model.

### Phase 2: R1 Evaluation & Technical Deep-Dive (Workers)
- Draft 15-Point Multi-Criteria Evaluation across all 8 candidates against the 15 required criteria.
- Rigorous analysis of semantic fidelity, numerical stability, random-seed determinism, licensing, hidden assumptions, and native alternatives.
- Explicit verdicts: REQUIRED | RECOMMENDED | OPTIONAL | REJECTED.

### Phase 3: R2 Interface Contracts & R3 Cross-Validation Protocols (Workers)
- R2: Canonical Model / Tool Interface Specification (type-safe Python schemas, state boundaries, invariant validation hooks).
- R3: Dual-Implementation Cross-Validation Protocols:
  1. State-machine & reset trajectories (cadCAD vs Native NumPy Engine)
  2. Sensitivity indices (SALib vs Native Saltelli/Sobol QMC Engine)
  3. Control stability & root-locus (Python-Control / SciPy ODE vs Discrete Differential Approximations)
  4. Jump-diffusion PIDE valuation (Custom Crank-Nicolson / Feynman-Kac vs QuantLib / SciPy)

### Phase 4: R4 Minimal Stack, R5 Lineage Architecture & Deliverable Synthesis (Workers)
- Formulate the Minimal Reproducible Research Stack and dependency graph.
- Define Cryptographic Lineage Tracking (`_lineage.jsonl`), Seed Orchestration, and Environment Pinning.
- Synthesize all sections into `docs/reports/OPEN_SOURCE_TOOLING_AUDIT.md`.

### Phase 5: Adversarial Review, Challenger Verification & Forensic Audit
- Spawn Reviewers to review report for mathematical soundness, completeness, and formatting.
- Spawn Challengers to verify schemas, interface contracts, and numerical protocols.
- Spawn Forensic Auditor (`teamwork_preview_auditor`) for integrity verification.
- Final gate evaluation and sign-off.
