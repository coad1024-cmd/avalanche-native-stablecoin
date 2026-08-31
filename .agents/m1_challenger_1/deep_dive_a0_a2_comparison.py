#!/usr/bin/env python3
import pandas as pd
import numpy as np

df = pd.read_parquet("audit_artifacts/execution/STAGE_2_RESULTS.parquet")

a0_df = df[df["arch_id"] == 0].reset_index(drop=True)
a2_df = df[df["arch_id"] == 2].reset_index(drop=True)
a53_df = df[df["arch_id"] == 7].reset_index(drop=True)

print("=== DEEP DIVE: A0 vs A2 vs A5.3 PARAMETER-MATCHED COMPARISON ===")

# Check the 1 instance where A0 had lower haircut prob than A2 on matched config:
haircut_diff = a0_df["haircut_prob"] - a2_df["haircut_prob"]
weird_idx = np.where(haircut_diff < 0)[0]
print(f"Indices where A0 has lower haircut prob than A2 on matched config: {weird_idx}")
for idx in weird_idx:
    print(f"\nMatched Config Index {idx}:")
    print("A0 row:")
    print(a0_df.loc[idx, ["policy_id", "R", "R_prime", "H_d", "H_u", "omega_burn", "omega_val", "omega_res", "omega_l1", "haircut_prob", "tail_cvar_99", "reset_churn_annual", "validator_cr_min", "avax_burned_total"]])
    print("A2 row:")
    print(a2_df.loc[idx, ["policy_id", "R", "R_prime", "H_d", "H_u", "omega_burn", "omega_val", "omega_res", "omega_l1", "haircut_prob", "tail_cvar_99", "reset_churn_annual", "validator_cr_min", "avax_burned_total"]])

print("\n=== GLOBAL DOMINATION PROOF FOR ALL 200 A0 CANDIDATES ===")
# Objectives matrix for 1600 rows:
objs = np.column_stack([
    df["haircut_prob"].values,
    df["tail_cvar_99"].values,
    df["reset_churn_annual"].values,
    -df["validator_cr_min"].values,
    -df["avax_burned_total"].values
])

# For each A0 candidate, let's find the TOP dominators:
a0_indices = df[df["arch_id"] == 0].index
for i, a0_idx in enumerate(a0_indices[:10]): # Print first 10
    diff = objs - objs[a0_idx]
    dom_mask = np.all(diff <= 1e-9, axis=1) & np.any(diff < -1e-9, axis=1)
    dom_indices = np.where(dom_mask)[0]
    print(f"\nA0 Row {a0_idx} (Config {i}): Total Dominators = {len(dom_indices)}")
    dom_sub = df.loc[dom_indices]
    print(f"  Dominating Architectures: {dom_sub['arch_id'].value_counts().to_dict()}")
    # Show one representative dominator:
    best_dom = dom_indices[0]
    print(f"  Sample Dominator Row {best_dom} (Arch {df.loc[best_dom, 'arch_id']}, Policy {df.loc[best_dom, 'policy_id']}):")
    print(f"    A0 vals  : haircut={df.loc[a0_idx, 'haircut_prob']:.4f}, cvar={df.loc[a0_idx, 'tail_cvar_99']:.4f}, churn={df.loc[a0_idx, 'reset_churn_annual']:.2f}, val={df.loc[a0_idx, 'validator_cr_min']:.4f}, burn={df.loc[a0_idx, 'avax_burned_total']:.1f}")
    print(f"    Dom vals : haircut={df.loc[best_dom, 'haircut_prob']:.4f}, cvar={df.loc[best_dom, 'tail_cvar_99']:.4f}, churn={df.loc[best_dom, 'reset_churn_annual']:.2f}, val={df.loc[best_dom, 'validator_cr_min']:.4f}, burn={df.loc[best_dom, 'avax_burned_total']:.1f}")

