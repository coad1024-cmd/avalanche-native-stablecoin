"""
2D Continuous-Time PIDE Tranche Pricing Surface Experiment
Solves the IMEX jump-diffusion PIDE and exports 3D mesh and contour diagrams.
"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mechanisms.pide_solver import TranchePIDESolver

def run_pide_experiment():
    print("================================================================================")
    print("              SOLVING CONTINUOUS-TIME TRANCHE PRICING PIDE SURFACE")
    print("================================================================================")
    
    solver = TranchePIDESolver(
        r=0.05,
        sigma=0.8986,
        lambda_j=2.4,
        mu_j=-0.12,
        sigma_j=0.18,
        R=0.073,
        H_u=2.0,
        H_d=0.25
    )
    
    N_S = 60
    N_T = 60
    S_grid, T_grid, W_surface = solver.solve_tranche_pricing_grid(S_min=0.1, S_max=3.0, N_S=N_S, T_epoch=1.0, N_T=N_T)
    
    # Plotting 3D surface and 2D contour
    os.makedirs("/home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures", exist_ok=True)
    fig = plt.figure(figsize=(14, 6))
    
    # 3D Surface
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    S_mesh, T_mesh = np.meshgrid(S_grid, T_grid)
    surf = ax1.plot_surface(S_mesh, T_mesh, W_surface, cmap="viridis", edgecolor="none", alpha=0.9)
    ax1.set_xlabel("Normalized Collateral Index S", fontsize=10)
    ax1.set_ylabel("Epoch Time t (Years)", fontsize=10)
    ax1.set_zlabel("Class A Fair Value W_A(S, t)", fontsize=10)
    ax1.set_title("3D Tranche Pricing Surface W_A(S, t)", fontsize=11, fontweight="bold")
    fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=10)
    
    # 2D Contour
    ax2 = fig.add_subplot(1, 2, 2)
    contour = ax2.contourf(S_mesh, T_mesh, W_surface, levels=20, cmap="viridis")
    ax2.set_xlabel("Normalized Collateral Index S", fontsize=10)
    ax2.set_ylabel("Epoch Time t (Years)", fontsize=10)
    ax2.set_title("PIDE Valuation Iso-Value Contours", fontsize=11, fontweight="bold")
    fig.colorbar(contour, ax=ax2)
    
    # Mark reset boundaries
    S_u_curve = (2.00 + 1.0 + 0.073 * T_grid) / 2.0
    S_d_curve = (0.25 + 1.0 + 0.073 * T_grid) / 2.0
    ax2.plot(S_u_curve, T_grid, color="red", linestyle="--", linewidth=2.0, label="Upward Reset Barrier (H_u)")
    ax2.plot(S_d_curve, T_grid, color="orange", linestyle="--", linewidth=2.0, label="Downward Reset Barrier (H_d)")
    ax2.legend(loc="upper left", fontsize=9)
    
    plt.tight_layout()
    plot_path = "/home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures/fig10_pide_pricing_surface.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved PIDE Pricing Surface to {plot_path}")

if __name__ == "__main__":
    run_pide_experiment()
