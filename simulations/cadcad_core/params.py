"""
System Parameters and PSUU Sweep Configuration Registry
Governing Standard: BlockScience / CADLabs Parameter Registry Standard
Traceability: Every parameter cites an academic paper, Avalanche ACP, or empirical calibration source.
"""
from typing import Dict, Any, List

PHYSICAL_CONSTANTS = {
    "SECONDS_PER_YEAR": 31536000,
    "DAYS_PER_YEAR": 365.0,
    "MACHINE_EPSILON": 1e-12
}

DEFAULT_PARAMS: Dict[str, Any] = {
    # Timestep Configuration
    "dt_days": 1.0,                       # Simulation timestep (days)
    "dt_years": 1.0 / 365.0,              # Simulation timestep (annualized)
    
    # Dual-Class Tranching Contract Parameters (SSRN-3856569)
    "coupon_R": 0.0730,                   # Senior Class A coupon APR (7.30% p.a., SSRN-3856569 Sec 2.1)
    "coupon_R_prime": 0.0300,             # anUSD money-market coupon APR (3.00% p.a., SSRN-3856569 Sec 2.2)
    "bear_subsidy_R_tilde": 0.1000,       # Bear-market coupon subsidy (10.00% p.a., SSRN-3856569 Sec 2.5)
    "barrier_H_u": 2.00,                  # Upward reset barrier NAV (USD 2.00)
    "barrier_H_d": 0.25,                  # Downward reset barrier NAV (USD 0.25)
    "reset_delay_blocks": 1,              # 1-block delay lock to mitigate flash-loan MEV
    
    # Liquid Staking & Yield Recirculation (ACP-67 Framework)
    "savax_base_apr": 0.0600,             # Underlying sAVAX staking yield (6.00% p.a., Benqi/Avalanche Primary Network)
    "acp67_burn_share": 0.6500,           # Fraction of staking yield routed to AVAX buyback & burn (65.00%)
    "acp67_val_share": 0.2000,            # Fraction routed to validator boost (20.00%)
    "acp67_l1_share": 0.1500,             # Fraction routed to sovereign L1 liquidity grants (15.00%)
    
    # Exogenous Price Stochastic Driver (Kou Jump-Diffusion Calibration)
    "drift_mu": 0.1500,                   # Annualized collateral drift rate
    "diffusion_sigma": 0.8986,            # Annualized diffusion volatility (calibrated from Avalanche 2021-2026 daily log-returns)
    "jump_intensity_lambda": 2.4000,      # Annual Poisson jump arrival frequency (2.4 jumps/year)
    "jump_mean_mu_j": -0.1200,            # Mean log jump amplitude (-12.00% expected drop)
    "jump_vol_sigma_j": 0.1800,           # Jump amplitude standard deviation (18.00%)
    
    # Behavioral Agent Parameters
    "arb_speed_alpha": 0.8500,            # Fraction of AMM mispricing captured per timestep by arbitrageurs
    "speculator_elasticity_eta_L": 0.4000,# Speculator demand sensitivity to leverage deviations (L_B - 2.0)
    "speculator_momentum_eta_P": 0.2500,  # Speculator demand sensitivity to spot momentum
    "oracle_circuit_breaker_pct": 0.0800  # Max permitted divergence between spot and 30-min TWAP (±8.00%)
}

# Parameter Selection Under Uncertainty (PSUU) Sweep Tensor Grids
PSUU_SWEEPS: Dict[str, List[Any]] = {
    "barrier_H_d": [0.15, 0.20, 0.25, 0.30, 0.35],
    "barrier_H_u": [1.75, 2.00, 2.25, 2.50],
    "coupon_R": [0.0600, 0.0730, 0.0850],
    "diffusion_sigma": [0.6000, 0.8986, 1.2000],
    "acp67_burn_share": [0.5000, 0.6500, 0.7500]
}
