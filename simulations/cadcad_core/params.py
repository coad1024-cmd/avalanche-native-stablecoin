"""
Comprehensive Governance Levers and Model Parameters Registry
Governing Standard: BCRG Enterprise Parameter Canon & Zero Magic Numbers Rule
"""
from typing import Dict, Any, List

DAYS_PER_YEAR: float = 365.0
SECONDS_PER_YEAR: int = 31536000
MACHINE_EPSILON: float = 1e-12

# ==============================================================================
# 20-DIMENSIONAL GOVERNANCE LEVER REGISTRY (THETA in R^23)
# ==============================================================================
DEFAULT_GOVERNANCE_LEVERS: Dict[str, Any] = {
    # --------------------------------------------------------------------------
    # Subsystem 1: Tranching & Yield Levers (Theta_tranche)
    # --------------------------------------------------------------------------
    "coupon_R": 0.0730,             # Senior Class A coupon rate (7.30% p.a. - SSRN-3856569)
    "coupon_R_prime": 0.0300,       # anUSD benchmark rate (3.00% p.a. - SSRN-3856569)
    "bear_subsidy_R": 0.1000,       # Bear market coupon subsidy from A to B (10.00% - SSRN-3856569 Sec 2.5)
    "tranche_ratio_chi": 1.00,      # Initial Class A to Class B issuance ratio (1:1)
    "epoch_maturity_T_days": 365,   # Maximum contractual epoch duration (365 days)
    
    # --------------------------------------------------------------------------
    # Subsystem 2: Dynamic Resets & Safety Barriers (Theta_reset)
    # --------------------------------------------------------------------------
    "barrier_H_u": 2.00,            # Upward share split threshold ($2.00 NAV - SSRN-3856569)
    "barrier_H_d": 0.25,            # Downward reverse split threshold ($0.25 NAV - SSRN-3856569)
    "split_mult_up": 1.50,          # Upward split share expansion factor (1.50x)
    "merge_mult_down": 0.75,        # Downward merge share contraction factor (0.75x)
    "mev_band_delta": 0.0150,       # Proximity band for 1-block delay lock (+-1.50%)
    
    # --------------------------------------------------------------------------
    # Subsystem 3: Reflexer-Style Feedback Controller (Theta_control)
    # --------------------------------------------------------------------------
    "controller_Kp": 0.150,         # Proportional gain for secondary AMM rate steering
    "controller_Ki": 0.020,         # Integral gain for steady-state error elimination
    "controller_Kd": 0.005,         # Derivative damping gain
    "controller_max_adj": 0.050,    # Maximum rate adjustment clamp (+-5.00% p.a.)
    "twap_window_sec": 1800,        # DEX TWAP sampling duration (30 minutes)
    
    # --------------------------------------------------------------------------
    # Subsystem 4: ACP-67 Value Recirculation Waterfall (Theta_waterfall)
    # --------------------------------------------------------------------------
    "acp67_burn_pct": 0.650,        # 65.00% of staking yield to AVAX buyback & burn (ACP-67)
    "acp67_val_pct": 0.200,         # 20.00% of staking yield to Validator boost (ACP-67)
    "acp67_l1_pct": 0.150,          # 15.00% of staking yield to Sovereign L1 grants (ACP-67)
    "fee_mint_bps": 10,             # Primary vault deposit fee (10 bps = 0.10%)
    "fee_redeem_bps": 10,           # Primary vault redemption fee (10 bps = 0.10%)
    "fee_flash_bps": 9,             # Flash-loan protocol fee (9 bps = 0.09%)
    
    # --------------------------------------------------------------------------
    # Subsystem 5: Oracle & Circuit Breakers (Theta_circuit)
    # --------------------------------------------------------------------------
    "max_oracle_divergence": 0.080, # Spot vs TWAP divergence breaker (+-8.00%)
    "oracle_heartbeat_sec": 300,    # Maximum Chainlink price staleness (300s)
    "daily_mint_cap_usd": 50_000_000.0 # Max daily deposit inflow throttle ($50M/day)
}

# Environmental Stochastic Parameters (W in R^7)
DEFAULT_ENV_PARAMS: Dict[str, Any] = {
    "savax_base_apr": 0.0600,       # Underlying sAVAX staking yield (6.00% p.a. - Avalanche Primary)
    "risk_free_rate": 0.0350,       # Benchmark risk-free interest rate (3.50% p.a.)
    "diffusion_sigma": 0.8986,      # Collateral price annualized diffusion volatility (89.86%)
    "drift_mu": 0.1500,             # Collateral annualized drift (15.00%)
    "jump_intensity_lambda": 2.40,  # Poisson jump frequency (2.4 jumps / year)
    "jump_mean_mu_j": -0.1200,      # Mean log jump amplitude (-12.00%)
    "jump_vol_sigma_j": 0.1800      # Standard deviation of jump amplitude (18.00%)
}

# Unified Master Parameter Registry for cadCAD Experiment Pipelines
DEFAULT_PARAMS: Dict[str, Any] = {
    **DEFAULT_GOVERNANCE_LEVERS,
    **DEFAULT_ENV_PARAMS,
    "dt_years": 1.0 / DAYS_PER_YEAR,
    "bear_subsidy_R_tilde": 0.1000,
    "acp67_burn_share": 0.650,
    "acp67_val_share": 0.200,
    "acp67_l1_share": 0.150,
}

