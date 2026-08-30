"""
Isolated Control System vs Core Balance-Sheet Stability Analysis
Governing Standard: BCRG Control Theory & Noise Amplification Canon
Answers:
1. How much peg stability comes from the core mechanism vs the controller?
2. Can the controller destabilize the system under thin liquidity?
3. Is PID necessary, or is PI strictly superior (avoiding D-term noise amplification)?
"""
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_controller_isolation_experiment(
    shock_size_usd: float = 10_000_000.0,
    days: int = 60,
    dt_days: float = 0.05, # ~1.2 hours per step
    noise_std: float = 0.003 # 30 bps oracle noise
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Simulates secondary market price dynamics under 4 control configurations:
    1. No Controller (Baseline Primary Vault Arbitrage Only)
    2. P-Only Controller
    3. PI Controller (K_p=0.15, K_i=0.02, K_d=0)
    4. PID Controller (K_p=0.15, K_i=0.02, K_d=0.005)
    
    Across 3 AMM Liquidity Regimes:
    - Deep ($30M pool)
    - Moderate ($10M pool)
    - Severely Constrained / Illiquid ($1.5M pool)
    """
    liquidity_levels = [30_000_000.0, 10_000_000.0, 1_500_000.0]
    configs = [
        {"name": "No Controller (Core Arb Only)", "Kp": 0.0, "Ki": 0.0, "Kd": 0.0},
        {"name": "P-Only Controller", "Kp": 0.15, "Ki": 0.0, "Kd": 0.0},
        {"name": "PI Controller (Recommended)", "Kp": 0.15, "Ki": 0.02, "Kd": 0.0},
        {"name": "PID Controller (With D-Term)", "Kp": 0.15, "Ki": 0.02, "Kd": 0.005}
    ]
    
    steps = int(days / dt_days)
    time_grid = np.linspace(0, days, steps)
    
    results = []
    
    for L in liquidity_levels:
        liq_label = f"${L/1e6:.1f}M"
        for cfg in configs:
            Kp, Ki, Kd = cfg["Kp"], cfg["Ki"], cfg["Kd"]
            
            # Initial condition: $10M sell shock injected at t=0
            # Price impact: Delta P = - shock / (2 * L)
            initial_price_drop = - (shock_size_usd / (2.0 * L))
            P_dex = 1.0000 + max(-0.15, initial_price_drop)
            
            integral_error = 0.0
            prev_error = P_dex - 1.0000
            
            price_series = [P_dex]
            rate_delta_series = [0.0]
            
            # Primary arbitrageur speed (mean-reverting to par via 1:1 redemption)
            # Core mechanism restoration speed tau_arb ~ 5 days (rate = 0.20/day)
            arb_speed_per_day = 0.18
            
            rng = np.random.default_rng(12345)
            
            for step in range(1, steps):
                # Add discrete oracle / DEX microstructure noise
                meas_noise = rng.normal(0.0, noise_std)
                observed_price = P_dex + meas_noise
                error = observed_price - 1.0000
                
                # Update controller state
                integral_error += error * dt_days
                # Anti-windup clamping on integral state
                integral_error = max(-0.50, min(0.50, integral_error))
                
                d_error = (error - prev_error) / dt_days
                prev_error = error
                
                # Compute dynamic rate delta Delta R'
                raw_delta_r = - (Kp * error + Ki * integral_error + Kd * d_error)
                delta_r = max(-0.05, min(0.05, raw_delta_r))
                rate_delta_series.append(delta_r)
                
                # Market response:
                # 1. Core arbitrageur pressure returning to $1.00 par:
                arb_flow = (1.0000 - P_dex) * arb_speed_per_day * dt_days
                
                # 2. Controller-induced secondary demand (higher yield attracts buyers):
                # Demand elasticity: Delta Q_controller = L * 0.8 * delta_r
                controller_flow = (L * 0.8 * delta_r / L) * dt_days
                
                # Update actual spot price
                P_dex += arb_flow + controller_flow
                
                # Boundary clamp
                P_dex = max(0.50, min(1.50, P_dex))
                price_series.append(P_dex)
                
            prices_arr = np.array(price_series)
            peg_deviations = prices_arr - 1.0000
            
            annualized_vol = np.std(peg_deviations) * np.sqrt(365.0 / dt_days) * 100.0
            max_dev = np.max(np.abs(peg_deviations)) * 100.0
            rms_dev = np.sqrt(np.mean(peg_deviations**2)) * 100.0
            
            # Settling time: days until error stays within +/- 0.5%
            settled_idx = np.where(np.abs(peg_deviations) > 0.005)[0]
            settling_days = time_grid[settled_idx[-1]] if len(settled_idx) > 0 else 0.0
            
            # Stability flag (check for runaway oscillation)
            is_stable = True
            if len(prices_arr) > 10:
                recent_vol = np.std(prices_arr[int(steps*0.7):])
                if recent_vol > 0.02:
                    is_stable = False
                    
            results.append({
                "liquidity_usd": L,
                "liquidity_label": liq_label,
                "controller_config": cfg["name"],
                "Kp": Kp, "Ki": Ki, "Kd": Kd,
                "initial_price": price_series[0],
                "annualized_peg_vol": annualized_vol,
                "max_deviation_pct": max_dev,
                "rms_deviation_pct": rms_dev,
                "settling_time_days": settling_days,
                "is_stable": is_stable,
                "prices": prices_arr,
                "rates": np.array(rate_delta_series),
                "time": time_grid
            })
            
    df = pd.DataFrame(results)
    return df

if __name__ == "__main__":
    df = run_controller_isolation_experiment()
    print(df[["liquidity_label", "controller_config", "annualized_peg_vol", "settling_time_days", "is_stable"]])
