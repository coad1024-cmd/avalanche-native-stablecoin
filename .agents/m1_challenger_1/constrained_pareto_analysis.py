import pandas as pd
import numpy as np

df = pd.read_parquet("audit_artifacts/execution/STAGE_2_RESULTS.parquet")

objs_5d = np.column_stack([
    df["haircut_prob"].values,
    df["tail_cvar_99"].values,
    df["reset_churn_annual"].values,
    -df["validator_cr_min"].values,
    -df["avax_burned_total"].values
])

def pareto_filter(objs, eps=1e-9):
    N, M = objs.shape
    is_dominated = np.zeros(N, dtype=bool)
    for i in range(N):
        diff = objs - objs[i]
        dom_mask = np.all(diff <= eps, axis=1) & np.any(diff < -eps, axis=1)
        if np.any(dom_mask):
            is_dominated[i] = True
    return ~is_dominated

# 1. Unconstrained 5D Pareto Frontier (178 candidates)
nd_unconstrained = pareto_filter(objs_5d)
df["nd_unconstrained"] = nd_unconstrained

# 2. Gate-Compliant Subsets:
# Gate 1: peg_rmse <= 0.05
# Gate 2: reset_churn_annual <= 5.0
# Gate 4: haircut_prob <= 0.01
g124_mask = (df["peg_rmse"] <= 0.05) & (df["reset_churn_annual"] <= 5.0) & (df["haircut_prob"] <= 0.01)
df_g124 = df[g124_mask].copy().reset_index(drop=True)
objs_g124 = objs_5d[g124_mask]
nd_constrained = pareto_filter(objs_g124)
df_g124["nd_constrained"] = nd_constrained

print("=== UNCONSTRAINED VS CONSTRAINED PARETO FRONTIER ANALYSIS ===")
print(f"Total Configurations: {len(df)}")
print(f"Unconstrained Non-Dominated Count: {nd_unconstrained.sum()} / 1600 ({nd_unconstrained.mean()*100:.2f}%)")
print(f"Feasible Subset (G1+G2+G4 Pass): {len(df_g124)} / 1600 ({len(df_g124)/1600*100:.2f}%)")
print(f"Constrained Non-Dominated Count: {nd_constrained.sum()} / {len(df_g124)} ({nd_constrained.mean()*100:.2f}%)")

print("\n--- Unconstrained vs Constrained by Architecture ---")
arch_names = {0: "A0", 1: "A1", 2: "A2", 3: "A3", 4: "A4", 5: "A5.1", 6: "A5.2", 7: "A5.3"}
for aid in range(8):
    uncon_cnt = df[df["arch_id"] == aid]["nd_unconstrained"].sum()
    feas_cnt = (df_g124["arch_id"] == aid).sum()
    con_cnt = df_g124[df_g124["arch_id"] == aid]["nd_constrained"].sum() if feas_cnt > 0 else 0
    print(f"  Arch {aid:d} ({arch_names[aid]:4s}): Feasible={feas_cnt:3d}/200 | Unconstrained ND={uncon_cnt:3d}/200 | Constrained ND={con_cnt:3d}/{feas_cnt:3d}")

print("\n--- Unconstrained vs Constrained by Policy ---")
policy_names = {0: "POL-01", 1: "POL-02", 2: "POL-03", 3: "POL-04", 4: "POL-05"}
for pid in range(5):
    uncon_cnt = df[df["policy_id"] == pid]["nd_unconstrained"].sum()
    feas_cnt = (df_g124["policy_id"] == pid).sum()
    con_cnt = df_g124[df_g124["policy_id"] == pid]["nd_constrained"].sum() if feas_cnt > 0 else 0
    print(f"  Policy {pid:d} ({policy_names[pid]:6s}): Feasible={feas_cnt:3d}/320 | Unconstrained ND={uncon_cnt:3d}/320 | Constrained ND={con_cnt:3d}/{feas_cnt:3d}")

# Let's inspect the intersection of unconstrained non-dominated and feasible
df["is_feasible_g124"] = g124_mask
df["nd_and_feasible"] = df["nd_unconstrained"] & df["is_feasible_g124"]
print(f"\nCandidates that are BOTH unconstrained Pareto-optimal AND Gate-compliant: {df['nd_and_feasible'].sum()} / 1600")
print("Breakdown of unconstrained Pareto-optimal & feasible candidates:")
for aid in range(8):
    cnt = df[df["arch_id"] == aid]["nd_and_feasible"].sum()
    if cnt > 0:
        print(f"  Arch {aid} ({arch_names[aid]}): {cnt} candidates")
for pid in range(5):
    cnt = df[df["policy_id"] == pid]["nd_and_feasible"].sum()
    if cnt > 0:
        print(f"  Policy {pid} ({policy_names[pid]}): {cnt} candidates")

