# Project: anUSD Open-Source Tooling Audit & Research-Infrastructure Evaluation

## Architecture
This project conducts a formal, mathematically rigorous open-source tooling audit and research-infrastructure evaluation for the anUSD (Avalanche-native stablecoin) research study.
The architecture establishes:
1. Canonical Model Sovereignty (No silent semantic shift across simulation engines).
2. Dual-Implementation Cross-Validation for state dynamics, sensitivity indices, control stability, and jump-diffusion PIDE pricing.
3. Type-safe interface contracts between the canonical mathematical specification and external tools.
4. Minimal Reproducible Research Stack with environment pinning and cryptographic lineage tracking (`_lineage.jsonl`).

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | R1 15-Point Audit (Primary Candidates) | cadCAD, SALib, PyMC+ArviZ, QuantLib across 15 criteria | M1 | ORIGINAL_REQUEST.md §R1 |
| 2 | R1 15-Point Audit (Auxiliary Candidates) | SciPy, control, SimPy, MLflow across 15 criteria | M1 | ORIGINAL_REQUEST.md §R1 |
| 3 | R2 Interface Contracts Specification | Pydantic/dataclass schemas, state boundaries, invariant hooks | M2 | ORIGINAL_REQUEST.md §R2 |
| 4 | R3 Dual-Implementation Cross-Validation | Protocols for cadCAD vs Native, SALib vs Native, Control vs Discrete, PIDE Custom vs QuantLib | M3 | ORIGINAL_REQUEST.md §R3 |
| 5 | R4 Minimal Research Stack & Dependency Graph | Minimal stack formulation, rejection rationales, milestone mapping | M4 | ORIGINAL_REQUEST.md §R4 |
| 6 | R5 Reproducibility & Lineage Tracking | Seed orchestration, environment pinning, _lineage.jsonl specification | M4 | ORIGINAL_REQUEST.md §R4/Acceptance |
| 7 | R6 Final Audit Deliverable | Publication of docs/reports/OPEN_SOURCE_TOOLING_AUDIT.md | M5 | ORIGINAL_REQUEST.md §Acceptance |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1: 15-Point Candidate Audit | Comprehensive evaluation of 8 tools across 15 criteria with verdicts | Survey | DONE |
| 2 | M2: Canonical Interface Specs | Type-safe interface contracts & state boundary validation hooks | M1 | DONE |
| 3 | M3: Dual-Implementation Protocols | Cross-validation protocols & numerical tolerance criteria | M2 | DONE |
| 4 | M4: Minimal Stack & Reproducibility | Minimal toolchain, dependency graph, lineage architecture | M3 | DONE |
| 5 | M5: Synthesis & Report Delivery | Final OPEN_SOURCE_TOOLING_AUDIT.md compilation & verification | M1, M2, M3, M4 | DONE |


## Code Layout & Deliverables
- `docs/reports/OPEN_SOURCE_TOOLING_AUDIT.md`: Primary deliverable report.
- `simulations/cadcad_core/`: Existing cadCAD simulation models (reference).
- `contracts/src/`: Production Solidity smart contracts (reference).
- `docs/WHITEPAPER.md` & `docs/WHITEPAPER.tex`: Master Whitepaper specification (reference).
