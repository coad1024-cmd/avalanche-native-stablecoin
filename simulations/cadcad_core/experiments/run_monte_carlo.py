"""
Monte Carlo Jump-Diffusion Engine (10,000 Trajectories)
Methodology: BlockScience / CADLabs cadCAD Simulation Runner
"""
import os
import sys
import numpy as np
import pandas as pd
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import get_initial_state
from params import DEFAULT_PARAMS
from psubs import (
    p_exogenous_price_step,
    p_tranche_nav_accrual,
    p_behavioral_agents,
    p_dynamic_reset_policy,
    p_acp67_waterfall_policy
)

def run_single_cadcad_trajectory(params: Dict[str, Any], timesteps: int = 730, seed: int = 20260521) -> pd.DataFrame:
    rng = np.random.RandomState(seed)
    params = dict(params)
    params["rng"] = rng
    
    state = get_initial_state()
    history = [dict(state)]
    
    for step in range(1, timesteps + 1):
        # 1. Price Step
        p_out1 = p_exogenous_price_step(params, 1, history, state)
        state["P_spot"] = p_out1["P_spot_new"]
        
        # 2. Tranche NAVs
        p_out2 = p_tranche_nav_accrual(params, 2, history, state)
        state.update(p_out2)
        
        # 3. Behavioral Agents
        p_out3 = p_behavioral_agents(params, 3, history, state)
        state.update(p_out3)
        
        # 4. Dynamic Resets
        p_out4 = p_dynamic_reset_policy(params, 4, history, state)
        if p_out4["reset_type"] != "NONE":
            state["beta_rebase"] = p_out4["new_beta"]
            state["P_0"] = p_out4["new_P_0"]
            state["epoch_v"] = 0.0
            state["last_reset_type"] = p_out4["reset_type"]
            if p_out4["reset_type"] == "UPWARD":
                state["N_upward_resets"] += 1
            else:
                state["N_downward_resets"] += 1
            # Re-evaluate NAVs after reset
            state["S_index"] = 1.0
            state["V_A"] = 1.0
            state["V_B"] = 1.0
            state["V_A_prime"] = 1.0
            state["V_B_prime"] = 1.0
            state["leverage_B"] = 2.0
            state["solvency_gap"] = 0.0
        else:
            state["last_reset_type"] = "NONE"
            
        # 5. ACP-67 Yield Recirculation
        p_out5 = p_acp67_waterfall_policy(params, 5, history, state)
        state["B_cum_AVAX_burned"] += p_out5["avax_burned"]
        state["R_cum_val_rewards"] += p_out5["val_usd"]
        state["G_cum_l1_grants"] += p_out5["l1_usd"]
        
        state["timestep"] = step
        state["t"] += params["dt_years"]
        history.append(dict(state))
        
    return pd.DataFrame(history)

def run_large_scale_monte_carlo(num_paths: int = 1000, timesteps: int = 730):
    print("================================================================================")
    print(f"      STARTING LARGE-SCALE MONTE CARLO TRAJECTORIES (N = {num_paths}, T = {timesteps}d)")
    print("================================================================================")
    
    metrics = []
    for i in range(num_paths):
        seed = 20260521 + i
        df = run_single_cadcad_trajectory(DEFAULT_PARAMS, timesteps=timesteps, seed=seed)
        
        peg_series = df["P_DEX"]
        peg_returns = peg_series.pct_change().dropna()
        ann_vol = peg_returns.std() * np.sqrt(365) * 100.0
        
        # Max drawdown from $1.00
        min_peg = peg_series.min()
        max_drawdown_pct = max(0.0, (1.0 - min_peg) * 100.0)
        
        burn_avax = df["B_cum_AVAX_burned"].iloc[-1]
        n_up = df["N_upward_resets"].iloc[-1]
        n_down = df["N_downward_resets"].iloc[-1]
        max_gap = df["solvency_gap"].max()
        
        metrics.append({
            "path_id": i,
            "annualized_peg_vol": ann_vol,
            "max_drawdown_pct": max_drawdown_pct,
            "burn_avax": burn_avax,
            "n_upward": n_up,
            "n_downward": n_down,
            "max_solvency_gap": max_gap
        })
        
        if (i + 1) % 200 == 0 or (i + 1) == num_paths:
            print(f"Completed {i + 1}/{num_paths} simulation paths...")
            
    res_df = pd.DataFrame(metrics)
    out_path = "/home/hash/Hub/Projects/avalanche-native-stablecoin/simulations/monte_carlo_10k_results.csv"
    res_df.to_csv(out_path, index=False)
    print(f"\nSaved Monte Carlo results to {out_path}")
    
    print("\n--- MONTE CARLO KPI AUDIT SUMMARY ---")
    print(f"Annualized Peg Volatility: Mean = {res_df['annualized_peg_vol'].mean():.2f}%, 95th Pct = {res_df['annualized_peg_vol'].quantile(0.95):.2f}%")
    print(f"Max Peg Drawdown: Mean = {res_df['max_drawdown_pct'].mean():.2f}%, Max = {res_df['max_drawdown_pct'].max():.2f}%")
    print(f"Annual AVAX Burned: Mean = {res_df['burn_avax'].mean():,.0f} AVAX")
    print(f"Downward Resets / Year: Mean = {res_df['n_downward'].mean() / 2.0:.2f}")
    print(f"Max Solvency Invariant Gap: {res_df['max_solvency_gap'].max():.2e}")
    return res_df

if __name__ == "__main__":
    run_large_scale_monte_carlo(num_paths=500, timesteps=730)
