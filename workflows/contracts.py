"""
Pydantic Evidence and Data Contracts for Avalanche Native Stablecoin (anUSD)
Governing Standard: BCRG Data Foundation & Verification Canon
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

class GovernanceParametersContract(BaseModel):
    coupon_R: float = Field(..., ge=0.01, le=0.20, description="Class A Senior Coupon (annualized fraction)")
    coupon_R_prime: float = Field(..., ge=0.00, le=0.10, description="anUSD Benchmark Coupon (annualized fraction)")
    bear_subsidy_R: float = Field(..., ge=0.00, le=0.30, description="Bear Market Subsidy Rate")
    barrier_H_u: float = Field(..., ge=1.20, le=5.00, description="Upward Split Barrier ($ NAV)")
    barrier_H_d: float = Field(..., ge=0.05, le=0.80, description="Downward Merge Barrier ($ NAV)")
    acp67_burn_pct: float = Field(..., ge=0.0, le=1.0, description="AVAX Buyback & Burn Share")
    acp67_val_pct: float = Field(..., ge=0.0, le=1.0, description="Validator Boost Share")
    acp67_l1_pct: float = Field(..., ge=0.0, le=1.0, description="Sovereign L1 Grants Share")
    
    @field_validator("acp67_l1_pct")
    @classmethod
    def validate_waterfall_shares(cls, v, info):
        burn = info.data.get("acp67_burn_pct", 0.0)
        val = info.data.get("acp67_val_pct", 0.0)
        total = burn + val + v
        if abs(total - 1.0) > 1e-5:
            raise ValueError(f"ACP-67 waterfall shares must sum to 1.00 (got {total})")
        return v

class SystemStateContract(BaseModel):
    timestep: int = Field(..., ge=0)
    P_spot: float = Field(..., gt=0.0)
    P_0: float = Field(..., gt=0.0)
    epoch_v: float = Field(..., ge=0.0)
    beta_rebase: float = Field(..., gt=0.0)
    S_index: float = Field(..., gt=0.0)
    V_A: float = Field(..., gt=0.0)
    V_B: float = Field(...)
    V_A_prime: float = Field(..., gt=0.0)
    V_B_prime: float = Field(...)
    leverage_B: float = Field(..., ge=1.0)
    P_DEX: float = Field(..., gt=0.0)
    C_pool_sAVAX: float = Field(..., ge=0.0)
    B_cum_AVAX: float = Field(..., ge=0.0)
    R_cum_val_USD: float = Field(..., ge=0.0)
    G_cum_l1_USD: float = Field(..., ge=0.0)

class InvariantCheckResult(BaseModel):
    is_valid: bool
    solvency_gap: float
    sub_tranche_gap: float
    message: str
