import pandas as pd
df = pd.read_parquet("audit_artifacts/execution/STAGE_2_RESULTS.parquet")
print("Columns:", df.columns.tolist())
# Check how candidates are sampled per arch and policy:
for aid in range(8):
    sub = df[(df["arch_id"] == aid) & (df["policy_id"] == 0)]
    print(f"Arch {aid}, Policy 0: First 3 R values: {sub['R'].values[:3]}")

