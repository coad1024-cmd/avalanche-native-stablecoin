# Dual-Implementation Cross-Validation & Remediation Benchmark

> **Document Identifier:** `BCRG-VERIFY-2026-DUAL-IMPLEMENTATION-01`  
> **Governing Plan:** `BCRG-PLAN-2026-REVISED-MECHANISM-RESEARCH-02` (Phases 1 & 2)  
> **Date:** August 30, 2026  
> **Status:** Verified (15/15 Tests Passed in Foundry)  

---

## 1. Executive Summary

This report delivers the verification evidence for **Phase 1 (Canonical Accounting & Physical Balance Sheet)** and **Phase 2 (Dual Reference Implementation)** of the revised research program.

1. **Physical Balance Sheet Solvency vs. Model Identities:**  
   Implemented `simulations/canonical_accounting.py`. Proved that starting from unreset Par ($100\text{M}$ assets, $\$50.4\text{M}$ senior debt obligation), an instantaneous unamortized single-step drop inflicts haircuts at $\Delta P \le -49.60\%$. Intermediate downward resets amortize debt and expand safety margins.
2. **Dual-Implementation Smart Contract Verification:**  
   Preserved permanent `Reference / Bug-Preserving` and `Corrected Candidate` implementations in `contracts/src/remediation/` and `audit_artifacts/remediation/`.
3. **Foundry Regression Test Suite:**  
   `contracts/test/unit/DualImplementationComparison.t.sol` verified 4/4 assertions (15/15 across the entire test suite), reproducing `VULN-01`, `VULN-02`, and `VULN-03` in the buggy reference contracts and proving clean normalization and $2:1$ value conservation in the corrected candidate contracts.

---

## 2. Physical Balance Sheet Stress Test Results (`simulations/canonical_accounting.py`)

Evaluating a $\$100\text{M}$ vault across the discrete shock spectrum without prior downward reset:

```
=== Physical Balance Sheet Stress Test Across Shock Spectrum ===
Shock: -20.0% | Price: $20.00 | Assets: $ 80.0M | Debt: $ 50.4M | CR_phys:  1.59 | Haircut:  0.00% | Invariants: True
Shock: -40.0% | Price: $15.00 | Assets: $ 60.0M | Debt: $ 50.4M | CR_phys:  1.19 | Haircut:  0.00% | Invariants: True
Shock: -50.0% | Price: $12.50 | Assets: $ 50.0M | Debt: $ 50.4M | CR_phys:  0.99 | Haircut:  0.74% | Invariants: False
Shock: -60.0% | Price: $10.00 | Assets: $ 40.0M | Debt: $ 50.4M | CR_phys:  0.79 | Haircut: 20.60% | Invariants: False
Shock: -75.0% | Price: $ 6.25 | Assets: $ 25.0M | Debt: $ 50.4M | CR_phys:  0.50 | Haircut: 50.37% | Invariants: False
Shock: -85.0% | Price: $ 3.75 | Assets: $ 15.0M | Debt: $ 50.4M | CR_phys:  0.30 | Haircut: 70.22% | Invariants: False
Shock: -95.0% | Price: $ 1.25 | Assets: $  5.0M | Debt: $ 50.4M | CR_phys:  0.10 | Haircut: 90.07% | Invariants: False
```

### Key Epistemic Finding
* Treating crash survival as a **continuous response function** reveals that unreset vaults incur senior haircuts at $\Delta P \le -49.6\%$.
* When reset barriers ($H_d = 0.25$) trigger and return collateral, senior liabilities shrink, extending model-free survival up to $-60.00\%$ from the barrier.

---

## 3. Side-by-Side Smart Contract Comparison (`contracts/test/unit/DualImplementationComparison.t.sol`)

| Test Name | Target Defect / Invariant | Buggy Reference Behavior | Corrected Candidate Behavior | Test Verdict |
| :--- | :--- | :--- | :--- | :---: |
| `test_BuggyResetFlappingReproduced` | `VULN-01` ($\beta \cdot P_0$ Denominator Squaring) | After upward reset at $\$52$, next block at $\$52$ evaluates $V_B = 0 \le H_d$, **spuriously triggering downward reset flapping**. | Evaluates normalized index $S = 52/52 = 1.00$, yielding $V_B = 1.00$ (Par). **Zero flapping.** | **PASSED** |
| `test_BuggySplitterCreatesUnbackedClaims` | `VULN-02` / `VULN-03` (2:1 Value Backing & Rebase Disconnect) | Burning 100 Token A ($100) mints 100 $A'$ and 100 $B'$ (**$200 nominal claims from $100 input**). | Burning 100 Token A ($100) mints 50 $A'$ and 50 $B'$ (**$100 in = $100 out**). | **PASSED** |
| `test_CorrectedResetCleanNormalization` | Post-Reset NAV Normalization | Fails (spurious reset) | Normalizes cleanly to Par ($V_B = 1.000$) | **PASSED** |
| `test_CorrectedSplitterEnforces2To1Conservation` | Merging & Value Parity | Unbacked extraction (+50%) | Merging 50 pairs returns exactly 100 Token A ($100 = $100). | **PASSED** |

---

## 4. Foundry Test Suite Execution Log

```
Ran 5 test suites in 78.80ms (29.60ms CPU time): 15 tests passed, 0 failed, 0 skipped (15 total tests)

[PASS] testDownwardResetExecution() (gas: 3642945)
[PASS] testUpwardResetExecution() (gas: 3642883)
[PASS] test_DynamicDrawdownSubsidyBoost() (gas: 1089733)
[PASS] test_InitialStaticDistribution() (gas: 1085525)
[PASS] test_MaxDynamicValidatorCeiling() (gas: 882440)
[PASS] testEmpiricalProof_ResetFlappingDefect() (gas: 5683683)
[PASS] testEmpiricalProof_SecondaryTrancheRebaseDisconnect() (gas: 5699606)
[PASS] testEmpiricalProof_TrancheSplitterTwoToOneAccounting() (gas: 5740935)
[PASS] testDepositAndMint() (gas: 5635505)
[PASS] testSecondaryTrancheSplit() (gas: 5681515)
[PASS] testSolvencyInvariant() (gas: 5636145)
[PASS] test_BuggyResetFlappingReproduced() (gas: 11613175)
[PASS] test_BuggySplitterCreatesUnbackedClaims() (gas: 11832356)
[PASS] test_CorrectedResetCleanNormalization() (gas: 11611722)
[PASS] test_CorrectedSplitterEnforces2To1Conservation() (gas: 11811883)
```

---

## 5. File Inventory & Traceability

* `simulations/canonical_accounting.py`: Double-entry physical balance sheet ledger.
* `audit_artifacts/remediation/reference_buggy/ResetControllerBuggy.sol`: Preserves `VULN-01`.
* `audit_artifacts/remediation/reference_buggy/TrancheSplitterBuggy.sol`: Preserves `VULN-02` & `VULN-03`.
* `audit_artifacts/remediation/candidate_corrected/ResetControllerCorrected.sol`: Candidate patch for `VULN-01`.
* `audit_artifacts/remediation/candidate_corrected/TrancheSplitterCorrected.sol`: Candidate patch for `VULN-02` & `VULN-03`.
* `contracts/test/unit/DualImplementationComparison.t.sol`: Master side-by-side benchmark test suite.
