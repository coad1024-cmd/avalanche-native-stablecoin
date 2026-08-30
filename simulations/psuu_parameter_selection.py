#!/usr/bin/env python3
"""
Parameter Selection Under Uncertainty (PSUU) Multi-Objective Optimization Engine
Methodology: BlockScience Subspace / TE Academy PSUU Framework

Sweeps:
- Downward Reset Barrier H_d in [0.15, 0.20, 0.25, 0.30, 0.35]
- Upward Reset Barrier H_u in [1.75, 2.00, 2.25, 2.50]
- Senior Coupon R in [0.060, 0.073, 0.085]
- Collateral Volatility sigma in [0.60, 0.90, 1.20]
"""

import itertools
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cadcad_omnipool_style_model import OmnipoolStyleStablecoinGDS

def run_psuu_tensor_sweep(num_runs_per_param=5, timesteps=365):
    print("================================================================================")
    print("          STARTING PSUU MULTIDIMENSIONAL PARAMETER SWEEP (BLOCKSCIENCE STANDARD)")
    print("================================================================================")

    hd_grid = [0.15, 0.20, 0.25, 0.30, 0.35]
    hu_grid = [1.75, 2.00, 2.25, 2.50]
    r_grid = [0.060, 0.073, 0.085]
    sigma_grid = [0.60, 0.8986, 1.20]

    combinations = list(itertools.product(hd_grid, hu_grid, r_grid, sigma_grid))
    print(f"Total Parameter Permutations: {len(combinations)} | Runs/perm: {num_runs_per_param}")

    results = []

    for i, (hd, hu, r, sig) in enumerate(combinations):
        metrics_list = []
        for run_idx in range(num_runs_per_param):
            seed = 20260521 + i * 10 + run_idx
            params = {
                "H_d": hd,
                "H_u": hu,
                "R": r,
                "sigma": sig
            }
            model = OmnipoolStyleStablecoinGDS(params)
            df = model.run_simulation(timesteps=timesteps, seed=seed)

            peg_returns = df["P_DEX"].pct_change().dropna()
            annualized_vol = peg_returns.std() * np.sqrt(365) * 100.0
            total_burn = df["B_cum_AVAX"].iloc[-1]
            n_down = df["N_down"].iloc[-1]
            n_up = df["N_up"].iloc[-1]
            max_solvency_gap = df["solvency_gap"].max()

            metrics_list.append({
                "vol": annualized_vol,
                "burn": total_burn,
                "n_down": n_down,
                "n_up": n_up,
                "gap": max_solvency_gap
            })

        mean_vol = np.mean([m["vol"] for m in metrics_list])
        mean_burn = np.mean([m["burn"] for m in metrics_list])
        mean_down = np.mean([m["n_down"] for m in metrics_list])
        mean_up = np.mean([m["n_up"] for m in metrics_list])

        results.append({
            "H_d": hd,
            "H_u": hu,
            "R": r,
            "sigma": sig,
            "mean_peg_vol": mean_vol,
            "mean_burn_avax": mean_burn,
            "mean_n_down": mean_down,
            "mean_n_up": mean_up
        })

    res_df = pd.DataFrame(results)
    out_csv = "/home/hash/Hub/Projects/avalanche-native-stablecoin/simulations/psuu_sweep_results.csv"
    res_df.to_csv(out_csv, index=False)
    print(f"Sweep completed. Saved dataset to {out_csv}")
    return res_df

def generate_psuu_plots(res_df):
    os.makedirs("/home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures", exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    baseline = res_df[res_df["sigma"] == 0.8986]
    scatter = ax1.scatter(
        baseline["mean_n_down"],
        baseline["mean_peg_vol"],
        c=baseline["mean_burn_avax"] / 1000.0,
        cmap="viridis",
        s=80,
        alpha=0.85,
        edgecolors="black"
    )
    cbar = plt.colorbar(scatter, ax=ax1)
    cbar.set_label("Annual AVAX Burned (k AVAX)", fontsize=11)
    ax1.set_xlabel("Average Downward Resets / Year", fontsize=11)
    ax1.set_ylabel("Annualized anUSD Peg Volatility (%)", fontsize=11)
    ax1.set_title("PSUU Pareto Surface: Volatility vs Reset Frequency", fontsize=12, fontweight="bold")
    ax1.axhline(2.0, color="red", linestyle="--", label="Max Volatility Gate (2.0%)")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend()

    pivot = res_df[res_df["sigma"] == 0.8986].pivot_table(
        index="H_d",
        columns="H_u",
        values="mean_peg_vol",
        aggfunc="mean"
    )
    im = ax2.imshow(pivot.values, cmap="magma_r", aspect="auto", origin="lower")
    ax2.set_xticks(range(len(pivot.columns)))
    ax2.set_xticklabels([f"${x:.2f}" for x in pivot.columns])
    ax2.set_yticks(range(len(pivot.index)))
    ax2.set_yticklabels([f"${y:.2f}" for y in pivot.index])
    ax2.set_xlabel("Upward Barrier H_u", fontsize=11)
    ax2.set_ylabel("Downward Barrier H_d", fontsize=11)
    ax2.set_title("Stability Region Heatmap: Peg Volatility across Barriers", fontsize=12, fontweight="bold")
    cbar2 = plt.colorbar(im, ax=ax2)
    cbar2.set_label("Annualized Peg Volatility (%)", fontsize=11)

    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.values[i, j]
            ax2.text(j, i, f"{val:.2f}%", ha="center", va="center", color="white" if val > 1.4 else "black", fontsize=10, fontweight="bold")

    plt.tight_layout()
    plot_path = "/home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures/fig7_psuu_pareto_frontier.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved PSUU visualization to {plot_path}")

if __name__ == "__main__":
    df_results = run_psuu_tensor_sweep(num_runs_per_param=3, timesteps=365)
    generate_psuu_plots(df_results)
