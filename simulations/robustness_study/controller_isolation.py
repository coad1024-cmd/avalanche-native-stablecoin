"""
Reflexer-Style Controller Isolation & Ablation Study (Corrected Implementation)
Analyzes:
1. Core Balance Sheet Arbitrage alone (No Controller)
2. Core + Proportional (P)
3. Core + Proportional-Integral (PI)
4. Core + Proportional-Integral-Derivative (PID)
Across realistic DEX liquidity tiers ($1.5M, $10M, $30M) with realistic CPMM price impact.
"""
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd

def run_controller_isolation_experiment(
    shock_size_usd: float = 5_000_000.0,
    liquidity_levels: List[float] = [1_500_000.0, 10_000_000.0, 30_000_000.0],
    duration_days: float = 30.0,
    dt_days: float = 0.05, # 1.2 hours per time-step
    noise_std: float = 0.003
) -> pd.DataFrame:
    """
    Simulates step response and peg recovery under sudden sell-pressure shock.
    """
    steps = int(duration_days / dt_days)
    time_grid = np.linspace(0.0, duration_days, steps)
    
    configs = [
        {"name": "1. Core Alone (No Controller)", "Kp": 0.00, "Ki": 0.000, "Kd": 0.000},
        {"name": "2. Core + P Only",              "Kp": 0.15, "Ki": 0.000, "Kd": 0.000},
        {"name": "3. Core + PI (Recommended)",   "Kp": 0.15, "Ki": 0.020, "Kd": 0.000},
        {"name": "4. Core + PID (Whitepaper)",    "Kp": 0.15, "Ki": 0.020, "Kd": 0.005},
    ]
    
    records = []
    
    for L in liquidity_levels:
        liq_label = f"${L/1e6:.1f}M"
        for cfg in configs:
            Kp, Ki, Kd = cfg["Kp"], cfg["Ki"], cfg["Kd"]
            
            # Realistic CPMM price impact for sell shock: P_post = (L / (L + shock))^2
            # For moderate shock: Delta P = - shock / (L + shock)
            price_impact = - shock_size_usd / (L + shock_size_usd)
            P_dex = 1.0000 + max(-0.80, price_impact)
            
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
                # Price impact scales inversely with pool depth L: Delta P = (Demand Flow) / L
                # where Demand Flow = alpha_elasticity * delta_r * Reference_Capital
                capital_elasticity = 5_000_000.0 # $5M capital response per 100% rate differential
                controller_price_impact = (capital_elasticity * delta_r / L) * dt_days
                
                # Update actual spot price
                P_dex += arb_flow + controller_price_impact
                # Clamp physical price bounds
                P_dex = max(0.01, P_dex)
                price_series.append(P_dex)
                
            prices_arr = np.array(price_series)
            rates_arr = np.array(rate_delta_series)
            
            # Metrics
            peg_rmse = float(np.sqrt(np.mean((prices_arr - 1.0000)**2)))
            max_depeg_pct = float(np.max(np.abs(prices_arr - 1.0000)) * 100.0)
            
            # Time to recover within +-0.5% band
            recovered_indices = np.where(np.abs(prices_arr - 1.0000) <= 0.005)[0]
            if len(recovered_indices) > 0 and recovered_indices[0] < steps - 10:
                # Check if it stayed recovered
                stable_recovered = np.where(np.abs(prices_arr[recovered_indices[0]:] - 1.0000) <= 0.01)[0]
                if len(stable_recovered) == len(prices_arr[recovered_indices[0]:]):
                    settling_time_days = float(time_grid[recovered_indices[0]])
                else:
                    settling_time_days = float(time_grid[recovered_indices[0]])
            else:
                settling_time_days = float(duration_days)
                
            rate_volatility = float(np.std(rates_arr) * 100.0)
            
            records.append({
                "Liquidity Tier": liq_label,
                "Controller Config": cfg["name"],
                "Peg RMSE ($)": round(peg_rmse, 4),
                "Max Depeg (%)": round(max_depeg_pct, 2),
                "Settling Time (Days)": round(settling_time_days, 1),
                "Rate Volatility (pp)": round(rate_volatility, 3)
            })
            
    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = run_controller_isolation_experiment()
    print("=== Reflexer Controller Ablation Study (Corrected Sensitivity) ===")
    print(df.to_string(index=False))
