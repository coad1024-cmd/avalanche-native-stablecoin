"""
cadCAD / Discrete-Event Digital Twin Model of Dual-Class Tranche Stablecoin Protocol
"""
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class ProtocolParameters:
    coupon_R: float = 0.073      # Class A coupon (7.3% p.a.)
    coupon_R_prime: float = 0.03 # Class A' coupon (3.0% p.a.)
    H_u: float = 2.00            # Upward reset barrier ($2.00)
    H_d: float = 0.25            # Downward reset barrier ($0.25)
    savax_yield: float = 0.06    # 6.0% p.a. staking yield
    buyback_share: float = 0.65  # 65% of yield to AVAX buyback & burn
    validator_share: float = 0.20# 20% to validator staking boost
    ecosystem_share: float = 0.15# 15% to ecosystem grants

@dataclass
class ProtocolState:
    t: float = 0.0
    v: float = 0.0               # Time elapsed since last reset
    P: float = 25.0              # Current AVAX price ($)
    P_prev_reset: float = 25.0   # Reference price at last reset ($)
    beta: float = 1.0            # Cumulative share multiplier
    V_A: float = 1.0             # Class A NAV ($)
    V_B: float = 1.0             # Class B NAV ($)
    V_A_prime: float = 1.0       # Class A' (anUSD) NAV ($)
    V_B_prime: float = 1.0       # Class B' NAV ($)
    cumulative_resets_up: int = 0
    cumulative_resets_down: int = 0
    total_avax_burned: float = 0.0
    solvency_error: float = 0.0

class DualClassSimulator:
    def __init__(self, params: ProtocolParameters):
        self.params = params
        
    def step(self, state: ProtocolState, next_P: float, dt: float) -> Tuple[ProtocolState, Dict]:
        new_v = state.v + dt
        new_t = state.t + dt
        
        # 1. Update NAVs before reset evaluation
        V_A = 1.0 + self.params.coupon_R * new_v
        pool_value = (2.0 * next_P) / (state.beta * state.P_prev_reset)
        V_B = pool_value - V_A
        
        V_A_prime = 1.0 + self.params.coupon_R_prime * new_v
        V_B_prime = 2.0 * V_A - V_A_prime
        
        event = "NORMAL"
        new_beta = state.beta
        new_P_reset = state.P_prev_reset
        resets_up = state.cumulative_resets_up
        resets_down = state.cumulative_resets_down
        
        # 2. Check Dynamic Reset Barriers
        if V_B >= self.params.H_u:
            # UPWARD RESET
            event = "UPWARD_RESET"
            resets_up += 1
            new_v = 0.0
            new_P_reset = next_P
            new_beta = next_P / state.P_prev_reset
            V_A = 1.0
            V_B = 1.0
            V_A_prime = 1.0
            V_B_prime = 1.0
            
        elif V_B <= self.params.H_d:
            # DOWNWARD RESET
            event = "DOWNWARD_RESET"
            resets_down += 1
            new_v = 0.0
            new_P_reset = next_P
            new_beta = next_P / state.P_prev_reset
            V_A = 1.0
            V_B = 1.0
            V_A_prime = 1.0
            V_B_prime = 1.0
            
        # 3. Solvency Invariant Check
        # V_A + V_B must equal pool_value (or 2.0 immediately post-reset)
        expected_pool = (2.0 * next_P) / (new_beta * new_P_reset) if event != "NORMAL" else pool_value
        current_sum = V_A + V_B
        solvency_error = abs(current_sum - expected_pool)
        
        # 4. Yield Recycling Calculation (assuming $10M pool)
        annual_yield = 10_000_000.0 * self.params.savax_yield * dt
        avax_burned = (annual_yield * self.params.buyback_share) / next_P
        
        new_state = ProtocolState(
            t=new_t,
            v=new_v,
            P=next_P,
            P_prev_reset=new_P_reset,
            beta=new_beta,
            V_A=V_A,
            V_B=V_B,
            V_A_prime=V_A_prime,
            V_B_prime=V_B_prime,
            cumulative_resets_up=resets_up,
            cumulative_resets_down=resets_down,
            total_avax_burned=state.total_avax_burned + avax_burned,
            solvency_error=solvency_error
        )
        
        metrics = {
            "event": event,
            "pool_value": expected_pool,
            "solvency_error": solvency_error,
            "avax_burned": avax_burned
        }
        
        return new_state, metrics

def run_simulation(price_path: np.ndarray, dt: float = 1/365) -> List[ProtocolState]:
    params = ProtocolParameters()
    sim = DualClassSimulator(params)
    state = ProtocolState(P=price_path[0], P_prev_reset=price_path[0])
    
    history = [state]
    for P in price_path[1:]:
        state, _ = sim.step(state, P, dt)
        history.append(state)
        
    return history

if __name__ == "__main__":
    from jump_diffusion import simulate_kou_jump_diffusion
    
    prices = simulate_kou_jump_diffusion(
        S0=25.0, r=0.05, sigma=0.80, lambda_jump=3.0,
        p_up=0.45, eta1=3.5, eta2=2.0, T=2.0, dt=1/365, paths=1
    )[:, 0]
    
    states = run_simulation(prices)
    final_state = states[-1]
    
    print(f"Simulation completed over {len(states)} days.")
    print(f"Final AVAX Price: ${final_state.P:.2f}")
    print(f"Upward Resets: {final_state.cumulative_resets_up}, Downward Resets: {final_state.cumulative_resets_down}")
    print(f"Max Solvency Discrepancy: {max(s.solvency_error for s in states):.2e}")
    print(f"Total AVAX Burned ($10M pool): {final_state.total_avax_burned:.2f} AVAX")
