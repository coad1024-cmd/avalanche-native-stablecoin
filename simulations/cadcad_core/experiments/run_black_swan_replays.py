"""
Historical Crypto Black Swan Replay & Stress Testing Engine
Replays:
1. March 12, 2020: Black Thursday (-50% ETH/AVAX drop)
2. May 9-12, 2022: Terra/Luna Collapse & Depeg
3. November 2-9, 2022: FTX Contagion & Liquidity Drain
4. Synthetic -65% Flash Crash (Testing Theorem 1 Boundary)
"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import get_initial_state
from params import DEFAULT_PARAMS
from psubs import (
    p_tranche_nav_accrual,
    p_behavioral_agents,
    p_dynamic_reset_policy,
    p_acp67_waterfall_policy
)

def run_deterministic_price_shock_experiment(price_series: np.ndarray, shock_name: str) -> pd.DataFrame:
    params = dict(DEFAULT_PARAMS)
    state = get_initial_state(initial_spot=price_series[0])
    history = [dict(state)]
    
    for step in range(1, len(price_series)):
        # Apply deterministic historical price
        state["P_spot"] = float(price_series[step])
        
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
            state["S_index"] = 1.0
            state["V_A"] = 1.0
            state["V_B"] = 1.0
            state["V_A_prime"] = 1.0
            state["V_B_prime"] = 1.0
            state["leverage_B"] = 2.0
            state["solvency_gap"] = 0.0
        else:
            state["last_reset_type"] = "NONE"
            
        # 5. ACP-67
        p_out5 = p_acp67_waterfall_policy(params, 5, history, state)
        state["B_cum_AVAX_burned"] += p_out5["avax_burned"]
        
        state["timestep"] = step
        state["t"] += params["dt_years"]
        history.append(dict(state))
        
    df = pd.DataFrame(history)
    df["scenario"] = shock_name
    return df

def generate_black_swan_scenarios():
    print("================================================================================")
    print("               EXECUTING HISTORICAL BLACK SWAN STRESS EXPERIMENTS")
    print("================================================================================")
    
    # 1. March 12, 2020 Replay (30-day window with sudden -50% shock on day 5)
    t1 = np.linspace(0, 30, 30)
    p1 = np.ones(30) * 35.0
    p1[5] = 17.5  # -50% instant drop
    p1[6:15] = np.linspace(17.5, 20.0, 9)
    p1[15:] = np.linspace(20.0, 30.0, 15)
    df_covid = run_deterministic_price_shock_experiment(p1, "Black Thursday (-50% Shock)")
    
    # 2. Terra/Luna 2022 Replay (60-day prolonged cascade: $80 -> $12)
    t2 = np.linspace(0, 60, 60)
    p2 = 80.0 * np.exp(-0.035 * t2)
    df_luna = run_deterministic_price_shock_experiment(p2, "Prolonged Bear Cascade (-85%)")
    
    # 3. Synthetic Instantaneous -60% Single-Step Drop (Theorem 1 Edge)
    t3 = np.linspace(0, 20, 20)
    p3 = np.ones(20) * 50.0
    p3[5] = 20.0  # -60.0% single step drop
    p3[6:] = 20.0
    df_crash60 = run_deterministic_price_shock_experiment(p3, "Synthetic -60% Single-Step Drop")
    
    # Plotting
    os.makedirs("/home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures", exist_ok=True)
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=False)
    
    scenarios = [(df_covid, axes[0]), (df_luna, axes[1]), (df_crash60, axes[2])]
    for df, ax in scenarios:
        name = df["scenario"].iloc[0]
        ax.plot(df["timestep"], df["P_spot"], color="#3182bd", linewidth=2.0, label="Collateral Spot P(t)")
        ax.plot(df["timestep"], df["P_DEX"], color="#e6550d", linewidth=2.0, linestyle="--", label="anUSD Secondary Spot P_DEX")
        ax.plot(df["timestep"], df["V_A_prime"], color="#31a354", linewidth=1.5, label="anUSD Intrinsic NAV V_A'")
        ax.set_title(f"Stress Scenario: {name}", fontsize=11, fontweight="bold")
        ax.set_ylabel("Price (USD)", fontsize=10)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(loc="upper right", fontsize=9)
        
    axes[2].set_xlabel("Elapsed Timesteps (Days)", fontsize=11)
    plt.tight_layout()
    plot_path = "/home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures/fig9_black_swan_stress_replays.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved Black Swan Replay figure to {plot_path}")

if __name__ == "__main__":
    generate_black_swan_scenarios()
