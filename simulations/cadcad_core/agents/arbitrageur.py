"""
Behavioral Agent Archetype: Rational Secondary AMM Arbitrageur
Role: Exploits price discrepancies between primary CustodianVault NAV (V_A_prime) and secondary AMM (Trader Joe / Solidly).
"""
import math
from typing import Dict, Any, Tuple

class ArbitrageurAgent:
    def __init__(self, arb_speed_alpha: float = 0.85, max_slippage_tolerance: float = 0.05):
        self.alpha = arb_speed_alpha
        self.max_slippage = max_slippage_tolerance

    def compute_arbitrage_action(
        self,
        DEX_reserve_anUSD: float,
        DEX_reserve_USDC: float,
        V_A_prime: float
    ) -> Tuple[str, float, float]:
        """
        Calculates optimal trade size to restore secondary AMM price to fair NAV V_A_prime:
        P_DEX = DEX_reserve_USDC / DEX_reserve_anUSD
        Returns:
            action: 'MINT_AND_SELL' | 'BUY_AND_REDEEM' | 'NO_ACTION'
            trade_volume_anUSD: token amount
            dollar_impact: total USD value traded
        """
        P_DEX = DEX_reserve_USDC / max(1.0, DEX_reserve_anUSD)
        price_spread = P_DEX - V_A_prime
        
        # Dead-band filter (0.05% gas/fee friction threshold)
        if abs(price_spread) < 0.0005:
            return "NO_ACTION", 0.0, 0.0
            
        # Target constant product formula: (R_usdc - dy) / (R_anusd + dx) = V_A_prime
        # dx_optimal = (sqrt(R_usdc * R_anusd / V_A_prime) - R_anusd) * alpha
        k = DEX_reserve_anUSD * DEX_reserve_USDC
        target_anUSD_reserves = math.sqrt(k / V_A_prime)
        
        if P_DEX > V_A_prime:
            # Secondary AMM price is too high -> Mint anUSD at V_A' and sell into DEX
            dx = (target_anUSD_reserves - DEX_reserve_anUSD) * self.alpha
            dx = max(0.0, min(dx, DEX_reserve_anUSD * self.max_slippage))
            return "MINT_AND_SELL", dx, dx * V_A_prime
        else:
            # Secondary AMM price is too low -> Buy anUSD on DEX and redeem at V_A'
            dx = (DEX_reserve_anUSD - target_anUSD_reserves) * self.alpha
            dx = max(0.0, min(dx, DEX_reserve_anUSD * self.max_slippage))
            return "BUY_AND_REDEEM", dx, dx * V_A_prime
