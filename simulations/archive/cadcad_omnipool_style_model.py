#!/usr/bin/env python3
"""
cadCAD-Style Behavioral Multi-Agent Simulation Engine for Avalanche Native Stablecoin (anUSD)
Methodology: Token Engineering Academy & BlockScience Omnipool Framework

Agents:
1. Rational Arbitrageur (closes DEX AMM spread against primary vault NAV)
2. Leveraged Speculator (buys/sells Class B based on leverage L_B and price momentum)
3. Staking Delegator / Validator Sink (receives ACP-67 yield boost)
"""

import math
import numpy as np
import pandas as pd

class OmnipoolStyleStablecoinGDS:
    def __init__(self, params=None):
        self.params = {
            "R": 0.0730,          # Class A coupon APR (7.3%)
            "R_prime": 0.0300,    # anUSD money market benchmark APR (3.0%)
            "R_tilde": 0.1000,    # Bear-market coupon subsidy (10.0%)
            "H_u": 2.00,          # Upward reset barrier NAV
            "H_d": 0.25,          # Downward reset barrier NAV
            "r_savax": 0.0600,    # sAVAX staking yield APR (6.0%)
            "omega_burn": 0.65,   # ACP-67 burn share (65%)
            "omega_val": 0.20,    # ACP-67 validator share (20%)
            "omega_l1": 0.15,     # ACP-67 sovereign L1 share (15%)
            "mu": 0.1500,         # AVAX annualized drift
            "sigma": 0.8986,      # AVAX annualized volatility
            "lambda_j": 2.4000,   # Annual jump arrival intensity
            "mu_j": -0.1200,      # Mean log jump amplitude
            "sigma_j": 0.1800,    # Jump volatility
            "dt": 1.0 / 365.0,    # Daily timestep
            "arb_efficiency": 0.85, # Arbitrageur speed (0.85 of spread closed per step)
            "spec_elasticity": 0.40 # Speculator leverage response elasticity
        }
        if params:
            self.params.update(params)

    def initialize_state(self, initial_spot=25.0, initial_tvl_usd=100_000_000.0):
        c_pool = initial_tvl_usd / initial_spot
        return {
            "t": 0.0,
            "step": 0,
            "P": initial_spot,
            "P_0": initial_spot,
            "v": 0.0,
            "beta": 1.0,
            "V_A": 1.0,
            "V_B": 1.0,
            "V_A_prime": 1.0,
            "V_B_prime": 1.0,
            "C_pool": c_pool,
            "A_shares": initial_tvl_usd / 2.0,
            "B_shares": initial_tvl_usd / 2.0,
            "P_DEX": 1.0,
            "DEX_reserves_anUSD": 5_000_000.0,
            "DEX_reserves_USDC": 5_000_000.0,
            "B_cum_AVAX": 0.0,
            "R_val_USD": 0.0,
            "G_eco_USD": 0.0,
            "N_up": 0,
            "N_down": 0,
            "reset_event": "NONE",
            "solvency_gap": 0.0
        }

    def policy_exogenous_price(self, state, rng):
        dt = self.params["dt"]
        mu = self.params["mu"]
        sigma = self.params["sigma"]
        lambda_j = self.params["lambda_j"]
        mu_j = self.params["mu_j"]
        sigma_j = self.params["sigma_j"]

        kappa = math.exp(mu_j + 0.5 * sigma_j**2) - 1.0
        drift = (mu - 0.5 * sigma**2 - lambda_j * kappa) * dt
        diff = sigma * math.sqrt(dt) * rng.normal(0, 1)

        num_jumps = rng.poisson(lambda_j * dt)
        jump_factor = 1.0
        if num_jumps > 0:
            jump_log = rng.normal(mu_j, sigma_j, size=num_jumps).sum()
            jump_factor = math.exp(jump_log)

        new_P = state["P"] * math.exp(drift + diff) * jump_factor
        return {"new_P": max(0.01, new_P)}

    def policy_behavioral_agents(self, state, primary_nav):
        p_dex = state["DEX_reserves_USDC"] / state["DEX_reserves_anUSD"]
        v_a_prime = primary_nav["V_A_prime"]
        spread = p_dex - v_a_prime

        arb_volume_usd = 0.0
        if abs(spread) > 0.001:
            arb_volume_usd = spread * state["DEX_reserves_USDC"] * self.params["arb_efficiency"]

        l_b = 2.0
        if primary_nav["V_B"] > 0.05:
            l_b = (2.0 * primary_nav["S"]) / primary_nav["V_B"]
        spec_sentiment = 1.0 + self.params["spec_elasticity"] * (l_b - 2.0)

        return {
            "arb_volume_usd": arb_volume_usd,
            "spec_sentiment": spec_sentiment,
            "p_dex": p_dex
        }

    def state_update_engine(self, state, exog_signals, agent_signals):
        dt = self.params["dt"]
        new_P = exog_signals["new_P"]
        new_v = state["v"] + dt
        beta = state["beta"]
        P_0 = state["P_0"]

        S = new_P / (beta * P_0)
        V_A = 1.0 + self.params["R"] * new_v
        V_B = 2.0 * S - V_A
        V_A_prime = 1.0 + self.params["R_prime"] * new_v
        V_B_prime = 2.0 * V_A - V_A_prime

        reset_event = "NONE"
        n_up = state["N_up"]
        n_down = state["N_down"]

        if V_B >= self.params["H_u"]:
            reset_event = "UPWARD_RESET"
            n_up += 1
            beta = beta * (new_P / P_0)
            P_0 = new_P
            new_v = 0.0
            S = 1.0
            V_A = 1.0
            V_B = 1.0
            V_A_prime = 1.0
            V_B_prime = 1.0
        elif V_B <= self.params["H_d"]:
            reset_event = "DOWNWARD_RESET"
            n_down += 1
            beta = beta * max(0.01, V_B)
            P_0 = new_P
            new_v = 0.0
            S = 1.0
            V_A = 1.0
            V_B = 1.0
            V_A_prime = 1.0
            V_B_prime = 1.0

        tvl_usd = state["C_pool"] * new_P
        daily_yield_usd = tvl_usd * self.params["r_savax"] * dt
        daily_burn_avax = (daily_yield_usd * self.params["omega_burn"]) / new_P
        daily_val_usd = daily_yield_usd * self.params["omega_val"]
        daily_eco_usd = daily_yield_usd * self.params["omega_l1"]

        dex_anUSD = state["DEX_reserves_anUSD"] + (agent_signals["arb_volume_usd"] / max(0.01, V_A_prime))
        dex_USDC = state["DEX_reserves_USDC"] - agent_signals["arb_volume_usd"]
        p_dex_updated = dex_USDC / max(1.0, dex_anUSD)

        solvency_gap = abs(V_A + V_B - 2.0 * S) if reset_event == "NONE" else 0.0

        return {
            "t": state["t"] + dt,
            "step": state["step"] + 1,
            "P": new_P,
            "P_0": P_0,
            "v": new_v,
            "beta": beta,
            "V_A": V_A,
            "V_B": V_B,
            "V_A_prime": V_A_prime,
            "V_B_prime": V_B_prime,
            "C_pool": state["C_pool"],
            "A_shares": state["A_shares"],
            "B_shares": state["B_shares"],
            "P_DEX": p_dex_updated,
            "DEX_reserves_anUSD": dex_anUSD,
            "DEX_reserves_USDC": dex_USDC,
            "B_cum_AVAX": state["B_cum_AVAX"] + daily_burn_avax,
            "R_val_USD": state["R_val_USD"] + daily_val_usd,
            "G_eco_USD": state["G_eco_USD"] + daily_eco_usd,
            "N_up": n_up,
            "N_down": n_down,
            "reset_event": reset_event,
            "solvency_gap": solvency_gap
        }

    def run_simulation(self, timesteps=730, seed=20260521):
        rng = np.random.RandomState(seed)
        state = self.initialize_state()
        history = [dict(state)]

        for _ in range(timesteps):
            exog = self.policy_exogenous_price(state, rng)
            dt = self.params["dt"]
            temp_v = state["v"] + dt
            temp_S = exog["new_P"] / (state["beta"] * state["P_0"])
            temp_VA = 1.0 + self.params["R"] * temp_v
            temp_VB = 2.0 * temp_S - temp_VA
            temp_VA_prime = 1.0 + self.params["R_prime"] * temp_v

            agent_sig = self.policy_behavioral_agents(state, {
                "S": temp_S,
                "V_A": temp_VA,
                "V_B": temp_VB,
                "V_A_prime": temp_VA_prime
            })

            state = self.state_update_engine(state, exog, agent_sig)
            history.append(dict(state))

        return pd.DataFrame(history)

if __name__ == "__main__":
    model = OmnipoolStyleStablecoinGDS()
    df = model.run_simulation(timesteps=730)
    print(f"Simulation completed: {len(df)} daily steps.")
    print(f"Final Peg P_DEX: ${df['P_DEX'].iloc[-1]:.4f}")
    print(f"Total AVAX Burned: {df['B_cum_AVAX'].iloc[-1]:,.2f} AVAX")
    print(f"Total Resets: Up={df['N_up'].iloc[-1]}, Down={df['N_down'].iloc[-1]}")
    print(f"Max Solvency Gap: {df['solvency_gap'].max():.2e}")
