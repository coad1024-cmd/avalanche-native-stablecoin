#!/usr/bin/env python3
"""
Dynamic Countercyclical Validator Subsidy Simulation and Policy Audit
Governing Standard: BCRG Avalanche Validator Economic Decision Architecture & ACP-67
Source: G.VALIDATOR_MARKET & G.VALUE_CAPTURE Objectives
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

REPO_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO_DIR, "simulations", "cadcad_core"))

from mechanisms.dynamic_subsidy import compute_dynamic_validator_allocation, execute_dynamic_acp67_waterfall
from agents.validator_pool import ValidatorPoolAgent

def run_validator_subsidy_simulation():
    print("================================================================================")
    print("      RUNNING DYNAMIC COUNTERCYCLICAL VALIDATOR INCOME SUBSIDY AUDIT")
    print("================================================================================")
    
    # 1-Year Market Trajectory: Bull -> Severe Drawdown -> Recovery
    timesteps = 365
    t = np.linspace(0, 1.0, timesteps)
    
    # AVAX Spot Price trajectory: starts at $40, drops to $12 in day 180, recovers to $25
    p_initial = 40.0
    p_t = 25.0 + 15.0 * np.cos(2 * np.pi * t) - 8.0 * np.sin(np.pi * t)
    
    # 90-day Exponential Moving Average
    ema_window = 90
    p_ema = pd.Series(p_t).ewm(span=ema_window, adjust=False).mean().values
    
    # Staking APR: Compresses during bear regime from 7.5% down to 5.0%
    savax_apr = 0.065 - 0.015 * np.sin(np.pi * t)
    
    # Stablecoin TVL: $500M baseline
    tvl_usd = 500_000_000.0
    
    agent = ValidatorPoolAgent(baseline_active_stake_avax=240_000_000.0, total_validator_nodes=1450)
    
    records = []
    for day in range(timesteps):
        spot = p_t[day]
        ema = p_ema[day]
        apr = savax_apr[day]
        
        # 1. Static 20% Policy
        static_waterfall = {
            "omega_val": 0.20,
            "omega_burn": 0.65,
            "omega_l1": 0.15,
            "val_usd": tvl_usd * apr * (1.0 / 365.0) * 0.20,
            "burn_usd": tvl_usd * apr * (1.0 / 365.0) * 0.65
        }
        
        # 2. Dynamic Countercyclical Subsidy Policy
        dynamic_alloc = compute_dynamic_validator_allocation(
            P_spot=spot,
            P_ema_90d=ema,
            savax_base_apr=apr,
            base_val_pct=0.20,
            max_val_pct=0.45,
            kappa_drawdown=0.35,
            target_apr=0.060
        )
        
        gross_yield_day = tvl_usd * apr * (1.0 / 365.0)
        dynamic_val_usd = gross_yield_day * dynamic_alloc["omega_val"]
        dynamic_burn_usd = gross_yield_day * dynamic_alloc["omega_burn"]
        
        # Viability Evaluation
        viab_static = agent.evaluate_validator_operator_viability(spot, static_waterfall["val_usd"] * 365.0)
        viab_dynamic = agent.evaluate_validator_operator_viability(spot, dynamic_val_usd * 365.0)
        
        records.append({
            "day": day,
            "spot_price": spot,
            "ema_price": ema,
            "savax_apr": apr,
            "drawdown_pct": dynamic_alloc["drawdown_pct"],
            "static_val_pct": 0.20,
            "dynamic_val_pct": dynamic_alloc["omega_val"],
            "dynamic_burn_pct": dynamic_alloc["omega_burn"],
            "static_val_usd": static_waterfall["val_usd"],
            "dynamic_val_usd": dynamic_val_usd,
            "static_burn_usd": static_waterfall["burn_usd"],
            "dynamic_burn_usd": dynamic_burn_usd,
            "static_opex_coverage": viab_static["opex_coverage_ratio"],
            "dynamic_opex_coverage": viab_dynamic["opex_coverage_ratio"]
        })
        
    df = pd.DataFrame(records)
    
    print(f"Total Dynamic Annual Validator Subsidy: ${df['dynamic_val_usd'].sum():,.2f} USD")
    print(f"Total Static Annual Validator Subsidy:  ${df['static_val_usd'].sum():,.2f} USD")
    print(f"Net Subsidy Boost During Drawdown:      +${(df['dynamic_val_usd'].sum() - df['static_val_usd'].sum()):,.2f} USD")
    print(f"Total Dynamic Annual AVAX Burned:       ${df['dynamic_burn_usd'].sum():,.2f} USD")
    
    # --------------------------------------------------------------------------
    # GENERATE SCIENTIFIC PLOT: FIG 12 DYNAMIC VALIDATOR SUBSIDY
    # --------------------------------------------------------------------------
    fig, axes = plt.subplots(3, 1, figsize=(11, 10), sharex=True, gridspec_kw={'height_ratios': [1.2, 1.2, 1.2]})
    
    # Panel 1: Spot Price and Drawdown
    ax1 = axes[0]
    ax1.plot(df['day'], df['spot_price'], label='AVAX Spot Price ($)', color='#1F77B4', lw=2.2)
    ax1.plot(df['day'], df['ema_price'], label='90-Day Price EMA ($)', color='#6B7280', ls='--', lw=1.8)
    ax1.set_ylabel('Price ($ USD)', fontsize=11, fontweight='bold')
    ax1.set_title('Dynamic Countercyclical Validator Income Subsidy Mechanism (ACP-67)', fontsize=13, fontweight='bold', pad=12)
    ax1.legend(loc='upper right', frameon=True)
    ax1.grid(True, alpha=0.25)
    
    # Panel 2: Dynamic Allocation Shares
    ax2 = axes[1]
    ax2.plot(df['day'], df['dynamic_val_pct'] * 100.0, label='Dynamic Validator Share (omega_val)', color='#2CA02C', lw=2.5)
    ax2.plot(df['day'], df['dynamic_burn_pct'] * 100.0, label='Residual AVAX Burn Share (omega_burn)', color='#D94801', lw=2.2)
    ax2.axhline(y=20.0, color='#2CA02C', ls=':', alpha=0.7, label='Static Baseline Validator Share (20%)')
    ax2.set_ylabel('Allocation Share (%)', fontsize=11, fontweight='bold')
    ax2.legend(loc='center right', frameon=True)
    ax2.grid(True, alpha=0.25)
    
    # Panel 3: Validator OpEx Coverage Ratio
    ax3 = axes[2]
    ax3.plot(df['day'], df['dynamic_opex_coverage'], label='Dynamic Policy OpEx Coverage', color='#2CA02C', lw=2.5)
    ax3.plot(df['day'], df['static_opex_coverage'], label='Static Policy OpEx Coverage', color='#D62728', ls='--', lw=2.0)
    ax3.axhline(y=1.0, color='black', ls='-', lw=1.2, label='OpEx Insolvency Floor (1.0x)')
    ax3.set_xlabel('Simulation Day (365 Days)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('OpEx Coverage Ratio', fontsize=11, fontweight='bold')
    ax3.legend(loc='lower right', frameon=True)
    ax3.grid(True, alpha=0.25)
    
    plt.tight_layout()
    fig_path = os.path.join(REPO_DIR, "docs", "figures", "fig12_dynamic_validator_subsidy_waterfall.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved Figure 12 to {fig_path}")

if __name__ == "__main__":
    run_validator_subsidy_simulation()
