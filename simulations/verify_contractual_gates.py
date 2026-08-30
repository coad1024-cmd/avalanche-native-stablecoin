#!/usr/bin/env python3
"""
Automated Contractual Verification & Quality Gate Audit Script
Governing Standard: BCRG Phase II Validation Suite
Verifies all 20 Gates (G01 - G20) and Machine-Verifiable Claims (CLM-001 - CLM-006).
"""
import os
import sys
import yaml
import pandas as pd
import numpy as np

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATES_FILE = os.path.join(REPO_DIR, "docs", "validation", "gates.yaml")
CLAIMS_FILE = os.path.join(REPO_DIR, "docs", "claims.yaml")

def audit_all_gates():
    print("================================================================================")
    print("      EXECUTING AUTOMATED TOKEN ENGINEERING VERIFICATION AUDIT (BCRG GATES)")
    print("================================================================================")
    
    with open(GATES_FILE, "r") as f:
        gates_data = yaml.safe_load(f)
        
    with open(CLAIMS_FILE, "r") as f:
        claims_data = yaml.safe_load(f)
        
    print(f"\n--- AUDITING {len(gates_data['gates'])} CONTRACTUAL GATES ---")
    all_passed = True
    for gate in gates_data["gates"]:
        status = gate["status"]
        print(f"[{'PASS' if status == 'PASSED' else 'FAIL'}] {gate['id']}: {gate['name']}")
        if status != "PASSED":
            all_passed = False
            
    print(f"\n--- AUDITING {len(claims_data['claims'])} MACHINE-VERIFIABLE CLAIMS ---")
    for claim in claims_data["claims"]:
        val = claim["empirical_value"]
        thresh = claim["threshold"]
        op = claim["operator"]
        
        passed = False
        if op == "<":
            passed = (val < thresh)
        elif op == "<=":
            passed = (val <= thresh)
        elif op == ">":
            passed = (val > thresh)
        elif op == ">=":
            passed = (val >= thresh)
            
        print(f"[{'PASS' if passed else 'FAIL'}] {claim['id']} ({claim['name']}): Empirical = {val}, Threshold = {op} {thresh}")
        if not passed:
            all_passed = False
            
    print("\n================================================================================")
    if all_passed:
        print("          ALL 20 CONTRACTUAL GATES & CLAIMS SUCCESSFULLY VERIFIED!")
    else:
        print("          WARNING: ONE OR MORE VERIFICATION GATES FAILED.")
    print("================================================================================")
    return all_passed

if __name__ == "__main__":
    success = audit_all_gates()
    sys.exit(0 if success else 1)
