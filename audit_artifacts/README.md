# `audit_artifacts/` — Adversarial Audit Research Program

> **Project:** Avalanche Native Stablecoin (`anUSD`)  
> **Program:** First-Principles Source & Derivation Audit  
> **Started:** 2026-08-30  
> **Status:** Phase 0 Complete — Awaiting Plan Approval for Phase 1  

All new research deliverables produced by the adversarial audit program
live here. This folder is the single point of access for auditors,
reviewers, and the project lead.

---

## Directory Layout

```
audit_artifacts/
│
├── README.md                   ← You are here
├── RESEARCH_PLAN.md            ← Master research plan & validation sequence
│
├── reports/                    ← Completed audit reports
│   ├── SOURCE_AND_DERIVATION_AUDIT.md      (1,179 lines — Phase 0 master deliverable)
│   ├── OPEN_SOURCE_TOOLING_AUDIT.md        (1,046 lines — 15-point tooling evaluation)
│   └── ADVERSARIAL_PARAMETER_IDENTIFICATION_AND_ROBUSTNESS_STUDY.md
│
├── registers/                  ← Canonical epistemic registers
│   ├── ASSUMPTIONS.md          (ASM-01 through ASM-12)
│   ├── CLAIMS_REGISTER.md      (CLM-001 through CLM-006)          ← to be extracted
│   ├── CONTRADICTIONS.md       (CONTRA-01 through CONTRA-12)      ← to be extracted
│   └── DATA_REQUIREMENTS.md    (DAT-01 through DAT-07)            ← to be extracted
│
├── provenance/                 ← Source chain & derivation tracking
│   ├── SSRN-3856569_DESIGN_SUMMARY.md      (Derived summary of original paper)
│   ├── claims.yaml                          (Machine-readable claims definitions)
│   ├── gates.yaml                           (Verification gate definitions)
│   ├── _lineage.jsonl                       (Git-native experiment lineage ledger)
│   └── teamwork_prompt_draft.md             (Prompt used to launch Phase 0 audit)
│
├── cross_validation/           ← Dual-implementation cross-validation results
│   └── (Phase 1+: cadCAD vs NumPy, SALib vs SciPy QMC, etc.)
│
├── figures/                    ← Generated plots, diagrams, surfaces
│   └── (Phase 1+: sensitivity heatmaps, regime trajectories, etc.)
│
└── remediation/                ← Smart contract patches & exploit tests
    └── (Phase 1+: VULN-01 to VULN-08 fix diffs & Foundry PoC tests)
```

---

## How This Folder Relates to the Rest of the Repo

| Location | Role | Status |
|:---|:---|:---|
| `research/ssrn-3856569.pdf` | Original academic source (read-only) | External ground truth |
| `docs/WHITEPAPER.tex` | Protocol specification (audited, not modified here) | Under audit |
| `docs/reports/` | Legacy location of generated reports | Mirrored here for convenience |
| `simulations/` | cadCAD models & robustness engine (audited, not modified here) | Under audit |
| `contracts/src/` | Solidity smart contracts (patches go in `remediation/`) | Under audit |
| **`audit_artifacts/`** | **All new adversarial audit work lives here** | **Active** |

---

## Workflow Rules

1. **All new deliverables** from this research program go into `audit_artifacts/`.
2. **Subdirectory ownership** is strict — reports in `reports/`, registers in `registers/`, etc.
3. **No file in this folder is ground truth.** Every file is a research artifact subject to review.
4. **Naming convention:** `UPPERCASE_SNAKE_CASE.md` for major deliverables, `lowercase_snake.{csv,yaml,py}` for data and scripts.
