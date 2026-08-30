"""
Dynamic Countercyclical Validator Income Subsidy Mechanism
Source: BCRG Avalanche Validator Economic Decision Architecture & ACP-67
Governing Standard: BCRG Token Engineering Canon
"""
from typing import Dict, Any, Tuple

def compute_dynamic_validator_allocation(
    P_spot: float,
    P_ema_90d: float,
    savax_base_apr: float,
    base_val_pct: float = 0.20,
    max_val_pct: float = 0.45,
    kappa_drawdown: float = 0.35,
    target_apr: float = 0.060,
    psi_yield: float = 2.50,
    l1_pct: float = 0.15
) -> Dict[str, float]:
    """
    Computes countercyclical dynamic validator income subsidy shares:
    
    1. Drawdown Sensitivity:
       Delta_drawdown = max(0, (P_ema - P_spot) / P_ema)
    
    2. Staking Yield Compression Sensitivity:
       Delta_yield = max(0, target_apr - savax_base_apr)
       
    3. Dynamic Validator Share:
       omega_val(t) = min(max_val_pct, base_val_pct + kappa * Delta_drawdown + psi * Delta_yield)
       
    4. Residual Burn Share:
       omega_burn(t) = 1.0 - omega_val(t) - l1_pct
    """
    # Price Drawdown Ratio
    drawdown = max(0.0, (P_ema_90d - P_spot) / max(1e-4, P_ema_90d))
    
    # Yield Compression Delta
    yield_gap = max(0.0, target_apr - savax_base_apr)
    
    # Dynamic Validator Allocation
    raw_val_pct = base_val_pct + kappa_drawdown * drawdown + psi_yield * yield_gap
    omega_val = min(max_val_pct, max(base_val_pct, raw_val_pct))
    
    # Sovereign L1 Allocation
    omega_l1 = l1_pct
    
    # Residual Deflationary Burn Allocation
    omega_burn = max(0.20, 1.0 - omega_val - omega_l1)
    
    # Re-normalize to ensure exact 1.00 sum
    total = omega_burn + omega_val + omega_l1
    omega_burn /= total
    omega_val /= total
    omega_l1 /= total
    
    return {
        "omega_val": omega_val,
        "omega_burn": omega_burn,
        "omega_l1": omega_l1,
        "drawdown_pct": drawdown * 100.0,
        "yield_gap_bps": yield_gap * 10000.0
    }

def execute_dynamic_acp67_waterfall(
    C_pool_sAVAX: float,
    P_spot: float,
    P_ema_90d: float,
    savax_base_apr: float,
    dt_years: float = 1.0,
    base_val_pct: float = 0.20,
    max_val_pct: float = 0.45,
    l1_pct: float = 0.15
) -> Dict[str, float]:
    """
    Executes the dynamic ACP-67 value recirculation waterfall with countercyclical subsidy.
    """
    allocations = compute_dynamic_validator_allocation(
        P_spot=P_spot,
        P_ema_90d=P_ema_90d,
        savax_base_apr=savax_base_apr,
        base_val_pct=base_val_pct,
        max_val_pct=max_val_pct,
        l1_pct=l1_pct
    )
    
    tvl_usd = C_pool_sAVAX * P_spot
    gross_yield_usd = tvl_usd * savax_base_apr * dt_years
    
    burn_usd = gross_yield_usd * allocations["omega_burn"]
    val_usd = gross_yield_usd * allocations["omega_val"]
    l1_usd = gross_yield_usd * allocations["omega_l1"]
    
    avax_burned = burn_usd / max(0.01, P_spot)
    avax_to_validators = val_usd / max(0.01, P_spot)
    
    return {
        "tvl_usd": tvl_usd,
        "gross_yield_usd": gross_yield_usd,
        "omega_burn": allocations["omega_burn"],
        "omega_val": allocations["omega_val"],
        "omega_l1": allocations["omega_l1"],
        "burn_usd": burn_usd,
        "burn_avax": avax_burned,
        "val_usd": val_usd,
        "val_avax": avax_to_validators,
        "l1_usd": l1_usd,
        "drawdown_pct": allocations["drawdown_pct"]
    }
