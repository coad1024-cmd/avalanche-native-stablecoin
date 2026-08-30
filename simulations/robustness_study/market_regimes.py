"""
Stochastic Market Regime Generator for Out-of-Sample Uncertainty Quantification
Governing Standard: BCRG Token Engineering & Robustness Canon
Generates 11 distinct empirical and adversarial market regimes.
"""
from typing import Dict, Any, List, Tuple
import numpy as np

MARKET_REGIMES = {
    "CALM_BULL": {
        "name": "Calm Bull Market",
        "sigma": 0.45,
        "lambda_jump": 0.8,
        "p_up": 0.60,
        "eta_1": 4.0,
        "eta_2": 3.0,
        "drift": 0.35,
        "q_savax": 0.070,
        "liquidity_usd": 30_000_000.0,
        "description": "Low volatility, positive drift, high staking yield."
    },
    "NORMAL": {
        "name": "Normal Calibrated Market",
        "sigma": 0.8986,
        "lambda_jump": 2.4,
        "p_up": 0.40,
        "eta_1": 3.5,
        "eta_2": 2.0,
        "drift": 0.10,
        "q_savax": 0.060,
        "liquidity_usd": 20_000_000.0,
        "description": "Historical 5-year Avalanche baseline calibration."
    },
    "HIGH_VOLATILITY": {
        "name": "Turbulent High Volatility",
        "sigma": 1.35,
        "lambda_jump": 4.5,
        "p_up": 0.40,
        "eta_1": 2.5,
        "eta_2": 1.8,
        "drift": -0.05,
        "q_savax": 0.060,
        "liquidity_usd": 15_000_000.0,
        "description": "Severe market turbulence, frequent large jumps."
    },
    "SEVERE_BEAR": {
        "name": "Severe Bear Market",
        "sigma": 1.10,
        "lambda_jump": 5.0,
        "p_up": 0.25,
        "eta_1": 3.0,
        "eta_2": 1.5,
        "drift": -0.55,
        "q_savax": 0.050,
        "liquidity_usd": 10_000_000.0,
        "description": "Sustained downward price trend (-55% annual drift)."
    },
    "FLASH_CRASH": {
        "name": "Instantaneous Flash Crash (-60%)",
        "sigma": 0.90,
        "lambda_jump": 1.0,
        "p_up": 0.00,
        "eta_1": 3.5,
        "eta_2": 1.1,
        "drift": 0.00,
        "q_savax": 0.060,
        "liquidity_usd": 8_000_000.0,
        "description": "Single-step catastrophic flash crash testing Theorem 1 bound."
    },
    "MULTI_JUMP_CASCADE": {
        "name": "Multi-Jump Cascading Crash",
        "sigma": 1.25,
        "lambda_jump": 8.0,
        "p_up": 0.15,
        "eta_1": 2.5,
        "eta_2": 1.4,
        "drift": -0.70,
        "q_savax": 0.055,
        "liquidity_usd": 6_000_000.0,
        "description": "3+ rapid consecutive downward jumps testing reset lag."
    },
    "V_SHAPED_RECOVERY": {
        "name": "V-Shaped Crash & Rapid Recovery",
        "sigma": 1.15,
        "lambda_jump": 3.0,
        "p_up": 0.50,
        "eta_1": 2.0,
        "eta_2": 1.5,
        "drift": 0.20,
        "q_savax": 0.065,
        "liquidity_usd": 18_000_000.0,
        "description": "-50% drop followed by rapid +100% rebound."
    },
    "PROLONGED_STAGNANT_BEAR": {
        "name": "Prolonged Stagnant Bear (2-Year)",
        "sigma": 0.50,
        "lambda_jump": 1.2,
        "p_up": 0.30,
        "eta_1": 4.0,
        "eta_2": 2.2,
        "drift": -0.30,
        "q_savax": 0.045,
        "liquidity_usd": 12_000_000.0,
        "description": "Slow, grinding multi-year bear market testing coupon drag."
    },
    "HIGH_YIELD": {
        "name": "High Staking Yield Regime (q = 10%)",
        "sigma": 0.85,
        "lambda_jump": 2.0,
        "p_up": 0.45,
        "eta_1": 3.5,
        "eta_2": 2.0,
        "drift": 0.15,
        "q_savax": 0.100,
        "liquidity_usd": 25_000_000.0,
        "description": "High staking cash flow expanding ACP-67 revenue."
    },
    "LOW_YIELD_COMPRESSION": {
        "name": "Low Yield Compression Regime (q = 3.5%)",
        "sigma": 0.95,
        "lambda_jump": 3.0,
        "p_up": 0.35,
        "eta_1": 3.5,
        "eta_2": 1.9,
        "drift": -0.10,
        "q_savax": 0.035,
        "liquidity_usd": 12_000_000.0,
        "description": "Yield compression testing validator subsidy sustainability."
    },
    "ILLIQUID_AMM": {
        "name": "Severely Constrained AMM Liquidity ($1.5M)",
        "sigma": 0.90,
        "lambda_jump": 2.5,
        "p_up": 0.40,
        "eta_1": 3.5,
        "eta_2": 2.0,
        "drift": 0.00,
        "q_savax": 0.060,
        "liquidity_usd": 1_500_000.0,
        "description": "Thin secondary AMM liquidity testing controller destabilization."
    }
}

def generate_regime_price_path(
    regime_key: str,
    days: int = 365,
    dt_days: float = 1.0,
    seed: int = 42,
    p_initial: float = 25.0
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Generates a continuous Kou jump-diffusion spot price path under specified market regime.
    """
    regime = MARKET_REGIMES[regime_key]
    rng = np.random.default_rng(seed)
    
    dt = dt_days / 365.0
    num_steps = int(days / dt_days)
    
    sigma = regime["sigma"]
    lam = regime["lambda_jump"]
    p_up = regime["p_up"]
    eta1 = regime["eta_1"]
    eta2 = regime["eta_2"]
    drift = regime["drift"]
    
    # Expected jump size: E[e^Y - 1]
    zeta = (p_up * eta1 / (eta1 - 1.0)) + ((1.0 - p_up) * eta2 / (eta2 + 1.0)) - 1.0
    
    prices = np.zeros(num_steps + 1)
    prices[0] = p_initial
    
    for t in range(num_steps):
        # Brownian innovation
        dW = rng.normal(0.0, np.sqrt(dt))
        
        # Poisson jump count
        num_jumps = rng.poisson(lam * dt)
        jump_factor = 1.0
        
        if num_jumps > 0:
            for _ in range(num_jumps):
                # Kou asymmetric double exponential jump
                if rng.uniform(0.0, 1.0) < p_up:
                    y = rng.exponential(1.0 / eta1)
                else:
                    y = -rng.exponential(1.0 / eta2)
                jump_factor *= np.exp(y)
                
        # Deterministic + stochastic log drift
        log_ret = (drift - 0.5 * sigma**2 - lam * zeta) * dt + sigma * dW
        prices[t + 1] = prices[t] * np.exp(log_ret) * jump_factor
        
        # Guard minimum price floor
        if prices[t + 1] < 0.001:
            prices[t + 1] = 0.001

    # Special deterministic shock injections for extreme test regimes
    if regime_key == "FLASH_CRASH":
        # Inject -60% drop at day 100
        crash_idx = min(100, num_steps - 1)
        prices[crash_idx:] *= 0.40
    elif regime_key == "MULTI_JUMP_CASCADE":
        # Inject 3 consecutive 30% drops at days 100, 102, 104
        idx1 = min(100, num_steps - 1)
        idx2 = min(102, num_steps - 1)
        idx3 = min(104, num_steps - 1)
        prices[idx1:] *= 0.70
        prices[idx2:] *= 0.70
        prices[idx3:] *= 0.70
        
    return prices, regime
