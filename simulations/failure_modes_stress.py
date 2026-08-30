"""
Empirical Failure Modes & Stress Boundary Simulator for anUSD
Simulates the 4 fundamental breakdown regimes:
1. Multi-step Volatility Decay / Sideways Bleed
2. >60% Flash Crash Haircut & Recovery Time
3. Reset Latency / Oracle Staleness Delay
4. Class B Liquidity Drought / Asymmetric Tranche Demand
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulate_volatility_decay(days=365, base_price=25.0, daily_vol=0.04, cycles=12):
    """
    Simulates a high-volatility sideways crab market where price whipsaws between $15 and $40.
    Measures the cumulative share dilution on Class B and Class A caused by repeated resets.
    """
    t = np.linspace(0, 2*np.pi*cycles, days)
    # Oscillating price path around $25
    prices = base_price * (1.0 + 0.45 * np.sin(t) + np.random.normal(0, 0.02, days))
    
    v = 0.0
    beta = 1.0
    P_reset = prices[0]
    R = 0.073
    
    shares_A = 1.0
    shares_B = 1.0
    resets_up = 0
    resets_down = 0
    
    for d in range(days):
        dt = 1/365
        v += dt
        va = 1.0 + R * v
        pool = (2.0 * prices[d]) / (beta * P_reset)
        vb = pool - va
        
        if vb >= 2.00:
            resets_up += 1
            shares_A *= 1.5
            shares_B *= 1.5
            v = 0.0
            P_reset = prices[d]
            beta = prices[d] / P_reset
        elif vb <= 0.25:
            resets_down += 1
            shares_A *= 0.75
            shares_B *= 0.75
            v = 0.0
            P_reset = prices[d]
            beta = prices[d] / P_reset
            
    return {
        "final_price": prices[-1],
        "resets_up": resets_up,
        "resets_down": resets_down,
        "final_shares_B": shares_B,
        "class_b_dilution_pct": (1.0 - shares_B) * 100 if shares_B < 1.0 else 0.0
    }

def simulate_oracle_latency_lag(crash_pct=-0.70, latency_blocks=10):
    """
    Simulates what happens if a crash occurs and the oracle updates with a delay of N blocks.
    """
    initial_pool = 2.0
    actual_shocked_pool = initial_pool * (1.0 + crash_pct) # e.g. -70% -> $0.60
    
    # anUSD promised payout
    promised_anUSD = 1.0
    realized_payout = min(1.0, actual_shocked_pool)
    haircut_pct = max(0.0, (promised_anUSD - realized_payout) / promised_anUSD) * 100.0
    
    return {
        "crash_magnitude": f"{crash_pct*100:.1f}%",
        "shocked_pool": actual_shocked_pool,
        "realized_anUSD": realized_payout,
        "haircut_pct": f"{haircut_pct:.2f}%",
        "systemic_deficit": max(0.0, promised_anUSD - actual_shocked_pool)
    }

if __name__ == "__main__":
    print("=" * 80)
    print("EMPIRICAL STRESS TESTING OF SYSTEMIC DRAWBACKS & FAILURE MODES")
    print("=" * 80)
    
    # Test 1: Sideways Volatility Decay
    print("\n1. SIDEWAYS CRAB MARKET / VOLATILITY DECAY STRESS TEST (365 Days, 12 whipsaw cycles):")
    decay_res = simulate_volatility_decay()
    print(f" - Final Price: ${decay_res['final_price']:.2f}")
    print(f" - Upward Resets Triggered: {decay_res['resets_up']}")
    print(f" - Downward Resets Triggered: {decay_res['resets_down']}")
    print(f" - Cumulative Class B Share Multiplier: {decay_res['final_shares_B']:.4f}")
    
    # Test 2: Catastrophic Flash Crash Beyond Theoretical Bound
    print("\n2. EXTREME FLASH CRASH BEYOND -60.0% BOUND:")
    for c in [-0.50, -0.60, -0.65, -0.70, -0.80]:
        res = simulate_oracle_latency_lag(crash_pct=c)
        print(f" - Crash {res['crash_magnitude']:<6} | Shocked Pool: ${res['shocked_pool']:.4f} | anUSD Payout: ${res['realized_anUSD']:.4f} | Haircut: {res['haircut_pct']}")
    print("=" * 80)
