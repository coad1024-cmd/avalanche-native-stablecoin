"""
Partial State Update Blocks (PSUBs) Pipeline
Governing Standard: CADLabs & BlockScience cadCAD Architecture
"""
import math
from typing import Dict, Any, Tuple
from mechanisms.tranche_math import (
    compute_normalized_pool_index,
    evaluate_primary_navs,
    evaluate_secondary_navs,
    compute_effective_leverage,
    verify_solvency_invariant
)
from mechanisms.dynamic_resets import (
    check_reset_condition,
    execute_upward_reset,
    execute_downward_reset
)
from mechanisms.acp67_waterfall import execute_acp67_yield_distribution
from agents.arbitrageur import ArbitrageurAgent
from agents.speculator import SpeculatorAgent

# Instantiate agent singletons
arbitrageur = ArbitrageurAgent()
speculator = SpeculatorAgent()

# -------------------------------------------------------------------------
# PSUB 1: Exogenous Environment & Spot Price Dynamics
# -------------------------------------------------------------------------
def p_exogenous_price_step(params: Dict[str, Any], substep: int, state_history: list, previous_state: Dict[str, Any]) -> Dict[str, Any]:
    dt = params["dt_years"]
    mu = params["drift_mu"]
    sigma = params["diffusion_sigma"]
    lambda_j = params["jump_intensity_lambda"]
    mu_j = params["jump_mean_mu_j"]
    sigma_j = params["jump_vol_sigma_j"]
    
    rng = params.get("rng")
    if rng is None:
        import numpy as np
        rng = np.random.RandomState()
        
    kappa = math.exp(mu_j + 0.5 * sigma_j**2) - 1.0
    drift = (mu - 0.5 * sigma**2 - lambda_j * kappa) * dt
    diff = sigma * math.sqrt(dt) * rng.normal(0, 1)
    
    num_jumps = rng.poisson(lambda_j * dt)
    jump_factor = 1.0
    if num_jumps > 0:
        jump_log = rng.normal(mu_j, sigma_j, size=num_jumps).sum()
        jump_factor = math.exp(jump_log)
        
    P_new = previous_state["P_spot"] * math.exp(drift + diff) * jump_factor
    P_new = max(0.01, P_new)
    
    momentum = (P_new - previous_state["P_spot"]) / previous_state["P_spot"]
    return {"P_spot_new": P_new, "momentum": momentum}

def s_update_spot_and_index(params: Dict[str, Any], substep: int, state_history: list, previous_state: Dict[str, Any], policy_input: Dict[str, Any]) -> Tuple[str, Any]:
    return "P_spot", policy_input["P_spot_new"]

# -------------------------------------------------------------------------
# PSUB 2: Primary & Secondary Tranche NAV Accrual
# -------------------------------------------------------------------------
def p_tranche_nav_accrual(params: Dict[str, Any], substep: int, state_history: list, previous_state: Dict[str, Any]) -> Dict[str, Any]:
    dt = params["dt_years"]
    v_new = previous_state["epoch_v"] + dt
    P_spot = previous_state["P_spot"]
    P_0 = previous_state["P_0"]
    beta = previous_state["beta_rebase"]
    
    S_new = compute_normalized_pool_index(P_spot, beta, P_0)
    V_A, V_B = evaluate_primary_navs(S_new, v_new, params["coupon_R"])
    V_A_prime, V_B_prime = evaluate_secondary_navs(V_A, v_new, params["coupon_R_prime"], params["coupon_R"])
    leverage_B = compute_effective_leverage(S_new, V_B)
    _, solvency_gap = verify_solvency_invariant(V_A, V_B, S_new)
    
    return {
        "epoch_v_new": v_new,
        "S_index": S_new,
        "V_A": V_A,
        "V_B": V_B,
        "V_A_prime": V_A_prime,
        "V_B_prime": V_B_prime,
        "leverage_B": leverage_B,
        "solvency_gap": solvency_gap
    }

def s_update_tranche_navs(params: Dict[str, Any], substep: int, state_history: list, previous_state: Dict[str, Any], policy_input: Dict[str, Any]) -> Tuple[str, Any]:
    # Returns updated dict mapping
    return "tranche_metrics", policy_input

# -------------------------------------------------------------------------
# PSUB 3: Behavioral Agent Policies (Secondary DEX AMM & Speculation)
# -------------------------------------------------------------------------
def p_behavioral_agents(params: Dict[str, Any], substep: int, state_history: list, previous_state: Dict[str, Any]) -> Dict[str, Any]:
    action, dx_anUSD, trade_usd = arbitrageur.compute_arbitrage_action(
        previous_state["DEX_reserve_anUSD"],
        previous_state["DEX_reserve_USDC"],
        previous_state["V_A_prime"]
    )
    
    res_anUSD = previous_state["DEX_reserve_anUSD"]
    res_USDC = previous_state["DEX_reserve_USDC"]
    
    if action == "MINT_AND_SELL":
        res_anUSD += dx_anUSD
        res_USDC -= trade_usd
    elif action == "BUY_AND_REDEEM":
        res_anUSD -= dx_anUSD
        res_USDC += trade_usd
        
    P_DEX_new = res_USDC / max(1.0, res_anUSD)
    spread = abs(P_DEX_new - previous_state["V_A_prime"])
    
    return {
        "DEX_reserve_anUSD": res_anUSD,
        "DEX_reserve_USDC": res_USDC,
        "P_DEX": P_DEX_new,
        "AMM_spread": spread
    }

def s_update_amm_state(params: Dict[str, Any], substep: int, state_history: list, previous_state: Dict[str, Any], policy_input: Dict[str, Any]) -> Tuple[str, Any]:
    return "amm_state", policy_input

# -------------------------------------------------------------------------
# PSUB 4: Dynamic Reset Restructuring
# -------------------------------------------------------------------------
def p_dynamic_reset_policy(params: Dict[str, Any], substep: int, state_history: list, previous_state: Dict[str, Any]) -> Dict[str, Any]:
    reset_type = check_reset_condition(previous_state["V_B"], params["barrier_H_u"], params["barrier_H_d"])
    
    if reset_type == "UPWARD":
        res = execute_upward_reset(
            previous_state["P_spot"],
            previous_state["P_0"],
            previous_state["beta_rebase"],
            previous_state["epoch_v"],
            previous_state["V_B"],
            params["coupon_R"]
        )
        return res
    elif reset_type == "DOWNWARD":
        res = execute_downward_reset(
            previous_state["P_spot"],
            previous_state["beta_rebase"],
            previous_state["epoch_v"],
            previous_state["V_B"],
            params["coupon_R"],
            params["bear_subsidy_R_tilde"]
        )
        return res
        
    return {
        "new_beta": previous_state["beta_rebase"],
        "new_P_0": previous_state["P_0"],
        "new_epoch_v": previous_state["epoch_v"],
        "reset_type": "NONE"
    }

def s_execute_resets(params: Dict[str, Any], substep: int, state_history: list, previous_state: Dict[str, Any], policy_input: Dict[str, Any]) -> Tuple[str, Any]:
    return "reset_state", policy_input

# -------------------------------------------------------------------------
# PSUB 5: ACP-67 Yield Recirculation Waterfall
# -------------------------------------------------------------------------
def p_acp67_waterfall_policy(params: Dict[str, Any], substep: int, state_history: list, previous_state: Dict[str, Any]) -> Dict[str, Any]:
    dist = execute_acp67_yield_distribution(
        previous_state["C_pool_sAVAX"],
        previous_state["P_spot"],
        params["savax_base_apr"],
        params["dt_years"],
        params["acp67_burn_share"],
        params["acp67_val_share"],
        params["acp67_l1_share"]
    )
    return dist

def s_update_governance_sinks(params: Dict[str, Any], substep: int, state_history: list, previous_state: Dict[str, Any], policy_input: Dict[str, Any]) -> Tuple[str, Any]:
    return "acp67_sinks", policy_input

# Master Partial State Update Block Pipeline Definition
PARTIAL_STATE_UPDATE_BLOCKS = [
    {
        "policies": {"exogenous_price": p_exogenous_price_step},
        "variables": {"P_spot": s_update_spot_and_index}
    },
    {
        "policies": {"tranche_navs": p_tranche_nav_accrual},
        "variables": {"tranche_metrics": s_update_tranche_navs}
    },
    {
        "policies": {"behavioral_agents": p_behavioral_agents},
        "variables": {"amm_state": s_update_amm_state}
    },
    {
        "policies": {"reset_policy": p_dynamic_reset_policy},
        "variables": {"reset_state": s_execute_resets}
    },
    {
        "policies": {"acp67_waterfall": p_acp67_waterfall_policy},
        "variables": {"acp67_sinks": s_update_governance_sinks}
    }
]
