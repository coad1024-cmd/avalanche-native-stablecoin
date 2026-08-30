"""
Reflexer-Style Control Theory Stability and Step-Response Audit Experiment
Simulates secondary AMM market response to sudden $10M whale sell shocks with and without PI controller.
Exports: docs/figures/fig11_control_theory_step_response.png
"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mechanisms.feedback_controller import ReflexerPIDController
from agents.arbitrageur import ArbitrageurAgent

def run_step_response_experiment():
    print("================================================================================")
    print("        RUNNING CONTROL-THEORETIC STEP-RESPONSE AUDIT (REFLEXER BENCHMARK)")
    print("================================================================================")
    
    timesteps = 60 # 60 daily steps
    dt_years = 1.0 / 365.0
    
    # 1. Uncontrolled System (Fixed R' = 3.0%)
    res_anUSD_fixed = 10_000_000.0
    res_USDC_fixed = 10_000_000.0
    arb_fixed = ArbitrageurAgent(arb_speed_alpha=0.60)
    
    history_fixed = []
    
    # 2. Controlled System (PI Controller R'(t))
    res_anUSD_ctrl = 10_000_000.0
    res_USDC_ctrl = 10_000_000.0
    arb_ctrl = ArbitrageurAgent(arb_speed_alpha=0.60)
    controller = ReflexerPIDController(K_p=0.150, K_i=0.020, K_d=0.005)
    
    history_ctrl = []
    
    # Base rates
    base_R_prime = 0.0300
    
    for t in range(timesteps):
        # Whale Shock at Day 5: $10M anUSD sold into pool
        if t == 5:
            res_anUSD_fixed += 3_500_000.0
            res_USDC_fixed -= 2_800_000.0
            res_anUSD_ctrl += 3_500_000.0
            res_USDC_ctrl -= 2_800_000.0
            
        p_dex_fixed = res_USDC_fixed / max(1.0, res_anUSD_fixed)
        p_dex_ctrl = res_USDC_ctrl / max(1.0, res_anUSD_ctrl)
        
        # Fixed System Arbitrage Step
        action_f, dx_f, trade_f = arb_fixed.compute_arbitrage_action(res_anUSD_fixed, res_USDC_fixed, 1.0)
        if action_f == "MINT_AND_SELL":
            res_anUSD_fixed += dx_f
            res_USDC_fixed -= trade_f
        elif action_f == "BUY_AND_REDEEM":
            res_anUSD_fixed -= dx_f
            res_USDC_fixed += trade_f
            
        history_fixed.append({
            "step": t,
            "P_DEX": p_dex_fixed,
            "R_prime": base_R_prime,
            "error": p_dex_fixed - 1.0
        })
        
        # Controlled System Modulation Step
        delta_R, error, _ = controller.compute_rate_modulation(p_dex_ctrl, 1.0, dt_years)
        effective_R_prime = base_R_prime + delta_R
        
        # Controlled Arbitrage Step (faster demand response due to higher yield)
        effective_alpha = 0.60 + 5.0 * max(0.0, delta_R)
        arb_ctrl.alpha = effective_alpha
        
        action_c, dx_c, trade_c = arb_ctrl.compute_arbitrage_action(res_anUSD_ctrl, res_USDC_ctrl, 1.0)
        if action_c == "MINT_AND_SELL":
            res_anUSD_ctrl += dx_c
            res_USDC_ctrl -= trade_c
        elif action_c == "BUY_AND_REDEEM":
            res_anUSD_ctrl -= dx_c
            res_USDC_ctrl += trade_c
            
        history_ctrl.append({
            "step": t,
            "P_DEX": p_dex_ctrl,
            "R_prime": effective_R_prime,
            "error": p_dex_ctrl - 1.0
        })
        
    df_fixed = pd.DataFrame(history_fixed)
    df_ctrl = pd.DataFrame(history_ctrl)
    
    zeta = controller.compute_system_damping_ratio()
    print(f"Controller Closed-Loop Damping Ratio zeta = {zeta:.2f} (Overdamped: >= 1.0)")
    
    # Plotting
    os.makedirs("/home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures", exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Top Plot: Price Response
    ax1.plot(df_fixed["step"], df_fixed["P_DEX"], color="#e6550d", linestyle="--", linewidth=2.0, label="Uncontrolled Fixed Yield (R'=3.0%)")
    ax1.plot(df_ctrl["step"], df_ctrl["P_DEX"], color="#31a354", linewidth=2.5, label="Reflexer-Style PI Controller")
    ax1.axhline(1.0, color="black", linestyle=":", alpha=0.7, label="Target Parity ($1.0000)")
    ax1.set_title("Step-Response to $10M Liquidity Shock: AMM Spot Price Recovery", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Secondary DEX Price ($)", fontsize=11)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="lower right", fontsize=10)
    
    # Bottom Plot: Dynamic Yield Modulation R'(t)
    ax2.plot(df_ctrl["step"], df_ctrl["R_prime"] * 100.0, color="#3182bd", linewidth=2.0, label="Modulated anUSD Yield R'(t)")
    ax2.axhline(3.0, color="gray", linestyle="--", label="Baseline Target Yield (3.0%)")
    ax2.set_title("Autonomous Yield Modulation Actuation Signal R'(t)", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Elapsed Days", fontsize=11)
    ax2.set_ylabel("Annualized Yield (%)", fontsize=11)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right", fontsize=10)
    
    plt.tight_layout()
    plot_path = "/home/hash/Hub/Projects/avalanche-native-stablecoin/docs/figures/fig11_control_theory_step_response.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved Control Theory Step-Response figure to {plot_path}")

if __name__ == "__main__":
    run_step_response_experiment()
