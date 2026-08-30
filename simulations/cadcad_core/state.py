"""
State Variable Registry for Avalanche Native Stablecoin (anUSD) cadCAD Model
Governing Standard: BlockScience Subspace & GDS State Space Axioms
"""
from typing import Dict, Any, NamedTuple

class SystemState(NamedTuple):
    # Temporal State
    timestep: int
    t: float               # Continuous elapsed time (years)
    epoch_v: float         # Elapsed time within current reset epoch (years)
    
    # Collateral & Spot Market
    P_spot: float          # AVAX spot price (USD)
    P_0: float             # Epoch anchor reference price (USD)
    S_index: float         # Normalized pool index: P_spot / (beta * P_0)
    beta_rebase: float     # Cumulative O(1) share scaling factor
    
    # Primary & Secondary Tranche Net Asset Values (USD)
    V_A: float             # Senior Bond NAV (1 + R*v)
    V_B: float             # Subordinated Leveraged Equity NAV (2S - V_A)
    V_A_prime: float       # anUSD Stablecoin NAV (1 + R'*v)
    V_B_prime: float       # Amplified Yield Sub-Tranche NAV (2V_A - V_A')
    
    # Effective Financial Metrics
    leverage_B: float      # Effective leverage: 2S / V_B
    solvency_gap: float    # Conservation invariant error: |V_A + V_B - 2S|
    
    # Secondary DEX / AMM State (Trader Joe Concentrated / XYK Pool)
    P_DEX: float           # anUSD market trading spot price (USD)
    DEX_reserve_anUSD: float # Stablecoin reserves in AMM
    DEX_reserve_USDC: float  # Base currency reserves in AMM
    AMM_spread: float      # |P_DEX - V_A_prime|
    
    # Physical Token Stocks
    C_pool_sAVAX: float    # Collateral vault stock (sAVAX)
    A_virtual_shares: float # Total virtual Senior shares
    B_virtual_shares: float # Total virtual Equity shares
    
    # Macroeconomic & Governance Sinks (ACP-67)
    B_cum_AVAX_burned: float # Cumulative native AVAX destroyed
    R_cum_val_rewards: float # Cumulative validator staking enhancement (USD)
    G_cum_l1_grants: float   # Cumulative sovereign Avalanche L1 grants (USD)
    
    # Discrete State Transition Counters & Telemetry
    N_upward_resets: int
    N_downward_resets: int
    last_reset_type: str   # 'NONE', 'UPWARD', 'DOWNWARD'
    circuit_breaker_active: bool

def get_initial_state(initial_spot: float = 25.0, initial_tvl_usd: float = 100_000_000.0) -> Dict[str, Any]:
    c_pool = initial_tvl_usd / initial_spot
    return {
        "timestep": 0,
        "t": 0.0,
        "epoch_v": 0.0,
        "P_spot": initial_spot,
        "P_0": initial_spot,
        "S_index": 1.0,
        "beta_rebase": 1.0,
        "V_A": 1.0,
        "V_B": 1.0,
        "V_A_prime": 1.0,
        "V_B_prime": 1.0,
        "leverage_B": 2.0,
        "solvency_gap": 0.0,
        "P_DEX": 1.0,
        "DEX_reserve_anUSD": 10_000_000.0,
        "DEX_reserve_USDC": 10_000_000.0,
        "AMM_spread": 0.0,
        "C_pool_sAVAX": c_pool,
        "A_virtual_shares": initial_tvl_usd / 2.0,
        "B_virtual_shares": initial_tvl_usd / 2.0,
        "B_cum_AVAX_burned": 0.0,
        "R_cum_val_rewards": 0.0,
        "G_cum_l1_grants": 0.0,
        "N_upward_resets": 0,
        "N_downward_resets": 0,
        "last_reset_type": "NONE",
        "circuit_breaker_active": False
    }
