"""
Canonical Physical Balance Sheet & Accounting Ledger for anUSD Protocol.

Phase 1 Deliverable: BCRG-PLAN-2026-REVISED-MECHANISM-RESEARCH-02
Strictly distinguishes between:
  1. Internal Mathematical/Model Definitions (V_A, V_B, V_A', V_B')
  2. Physical Vault Reserve Accounting (sAVAX assets, USDC buffer, net redemptions)
  3. Solvency & Collateralization Invariants (CR_phys, Redemption Margin, Haircut)
"""

from dataclasses import dataclass
from typing import Dict, Any, Tuple, Optional
import math


@dataclass(frozen=True)
class TrancheNAV:
    """Mathematical Model NAV Definitions (Per-Share Claim Values)."""
    V_A: float     # Senior Class A NAV (1 + Rv)
    V_B: float     # Junior Class B NAV (2S - V_A)
    V_A_prime: float  # anUSD Stablecoin NAV (1 + R'v)
    V_B_prime: float  # Class B' Yield NAV (2 V_A - V_A_prime)
    S: float       # Normalized collateral price index (P / P_0)
    v: float       # Elapsed normalized time since last reset (t - t_reset)


@dataclass
class PhysicalBalanceSheet:
    """
    Double-Entry Physical Vault Balance Sheet.
    Tracks actual on-chain token reserves, claims, liabilities, and surplus.
    """
    # Assets
    collateral_savax: float     # Physical sAVAX units held in vault
    spot_price_avax: float      # Current spot price P_avax ($ / AVAX)
    savax_rate: float           # sAVAX to AVAX exchange rate (AVAX / sAVAX)
    surplus_reserve_usd: float  # Accumulated yield surplus buffer ($)
    
    # Liabilities & Token Supplies (Nominal Token Counts)
    supply_A: float             # Total circulating Class A token shares
    supply_B: float             # Total circulating Class B token shares
    supply_A_prime: float       # Total circulating anUSD (Class A') shares
    supply_B_prime: float       # Total circulating Class B' shares
    
    # Scalar Rebase Multipliers (O(1) on-chain accounting)
    rebase_multiplier_A: float = 1.0
    rebase_multiplier_B: float = 1.0
    rebase_multiplier_A_prime: float = 1.0
    rebase_multiplier_B_prime: float = 1.0

    @property
    def spot_price_savax(self) -> float:
        """Effective sAVAX price in USD."""
        return self.spot_price_avax * self.savax_rate

    @property
    def total_collateral_value_usd(self) -> float:
        """Physical spot market value of liquid collateral reserves."""
        return self.collateral_savax * self.spot_price_savax

    @property
    def total_assets_usd(self) -> float:
        """Total protocol assets = Physical Collateral + Surplus Reserve Buffer."""
        return self.total_collateral_value_usd + self.surplus_reserve_usd

    def compute_model_navs(self, R: float, R_prime: float, P_0: float, v: float) -> TrancheNAV:
        """
        Computes nominal claim values from canonical mathematical equations.
        Note: S is normalized relative to base price P_0.
        """
        S = self.spot_price_savax / P_0 if P_0 > 0 else 1.0
        V_A = 1.0 + R * v
        V_B = max(0.0, 2.0 * S - V_A)
        V_A_prime = 1.0 + R_prime * v
        V_B_prime = max(0.0, 2.0 * V_A - V_A_prime)
        return TrancheNAV(V_A=V_A, V_B=V_B, V_A_prime=V_A_prime, V_B_prime=V_B_prime, S=S, v=v)

    def evaluate_liabilities_and_equity(self, nav: TrancheNAV) -> Dict[str, float]:
        """
        Computes nominal liabilities, junior equity claims, and balance sheet balance.
        """
        # Senior obligations
        effective_supply_A_prime = self.supply_A_prime * self.rebase_multiplier_A_prime
        effective_supply_B_prime = self.supply_B_prime * self.rebase_multiplier_B_prime
        effective_supply_A = self.supply_A * self.rebase_multiplier_A
        effective_supply_B = self.supply_B * self.rebase_multiplier_B

        # Nominal senior debt obligations
        debt_A_prime = effective_supply_A_prime * nav.V_A_prime
        debt_B_prime = effective_supply_B_prime * nav.V_B_prime
        debt_A = effective_supply_A * nav.V_A
        
        # Total Senior Liability (direct Class A + split sub-tranches)
        total_senior_debt = debt_A + 0.5 * (debt_A_prime + debt_B_prime)
        
        # Junior Equity Claim (residual value up to nominal B NAV)
        nominal_equity_B = effective_supply_B * nav.V_B
        physical_equity_B = max(0.0, self.total_collateral_value_usd - total_senior_debt)
        
        # Total liabilities and equity claims
        total_claims = total_senior_debt + physical_equity_B
        
        # Solvency metrics
        cr_phys = (self.total_assets_usd / total_senior_debt) if total_senior_debt > 0 else float('inf')
        redemption_solvency_margin = self.total_collateral_value_usd - (effective_supply_A_prime * 1.0)
        solvency_deficit = max(0.0, total_senior_debt - self.total_assets_usd)
        
        # Haircut on stablecoin if physically insolvent
        haircut_fraction = max(0.0, (total_senior_debt - self.total_assets_usd) / total_senior_debt) if total_senior_debt > 0 else 0.0

        return {
            "debt_A_prime": debt_A_prime,
            "debt_B_prime": debt_B_prime,
            "debt_A": debt_A,
            "total_senior_debt": total_senior_debt,
            "nominal_equity_B": nominal_equity_B,
            "physical_equity_B": physical_equity_B,
            "total_claims": total_claims,
            "cr_phys": cr_phys,
            "redemption_solvency_margin": redemption_solvency_margin,
            "solvency_deficit": solvency_deficit,
            "haircut_fraction": haircut_fraction,
            "total_assets_usd": self.total_assets_usd
        }

    def verify_all_invariants(self, nav: TrancheNAV, tol: float = 1e-10) -> Dict[str, Tuple[bool, float, str]]:
        """
        Executes explicit, independent invariant checks:
          1. Algebraic Model Conservation: |V_A + V_B - 2S|
          2. Secondary Sub-Tranche Parity: |V_A' + V_B' - 2V_A|
          3. Physical Asset-Liability Conservation: |Total_Assets - (Senior_Debt + Residual_Equity + Surplus)|
          4. Redemption Solvency Check: Spot_Collateral >= Stablecoin_Principal
        """
        results = {}
        
        # 1. Model Primary Identity
        model_primary_err = abs((nav.V_A + nav.V_B) - 2.0 * nav.S)
        results["INV_MODEL_PRIMARY"] = (
            model_primary_err <= tol,
            model_primary_err,
            f"|V_A + V_B - 2S| = {model_primary_err:.2e}"
        )
        
        # 2. Model Secondary Sub-Tranche Identity
        model_sec_err = abs((nav.V_A_prime + nav.V_B_prime) - 2.0 * nav.V_A)
        results["INV_MODEL_SECONDARY"] = (
            model_sec_err <= tol,
            model_sec_err,
            f"|V_A' + V_B' - 2V_A| = {model_sec_err:.2e}"
        )
        
        # 3. Physical Asset-Liability Balance
        sheet = self.evaluate_liabilities_and_equity(nav)
        phys_balance_err = abs(sheet["total_assets_usd"] - (sheet["total_senior_debt"] + sheet["physical_equity_B"] + self.surplus_reserve_usd))
        results["INV_PHYSICAL_BALANCE"] = (
            phys_balance_err <= tol,
            phys_balance_err,
            f"|Assets - (Debt + Equity + Buffer)| = {phys_balance_err:.2e}"
        )
        
        # 4. Redemption Solvency Margin
        is_solvent = sheet["redemption_solvency_margin"] >= -tol
        results["INV_REDEMPTION_SOLVENCY"] = (
            is_solvent,
            sheet["redemption_solvency_margin"],
            f"Redemption Margin = ${sheet['redemption_solvency_margin']:,.2f} (CR_phys = {sheet['cr_phys']:.3f})"
        )
        
        return results


def run_balance_sheet_stress_test(
    initial_savax_price: float = 25.0,
    initial_tvl_usd: float = 100_000_000.0,
    R: float = 0.03,
    R_prime: float = 0.02,
    shocks: Tuple[float, ...] = (-0.20, -0.40, -0.50, -0.60, -0.75, -0.85, -0.95)
) -> Dict[str, Any]:
    """
    Evaluates physical balance sheet solvency across a discrete shock spectrum.
    """
    initial_savax = initial_tvl_usd / initial_savax_price
    initial_units = initial_tvl_usd / 2.0  # 50M units each of A and B at par ($1.00 each)
    
    summary_results = []
    
    for shock in shocks:
        shocked_price = initial_savax_price * (1.0 + shock)
        bs = PhysicalBalanceSheet(
            collateral_savax=initial_savax,
            spot_price_avax=shocked_price,
            savax_rate=1.0,
            surplus_reserve_usd=0.0,
            supply_A=initial_units * 0.5,       # 25M unsplit Class A
            supply_B=initial_units,             # 50M Class B
            supply_A_prime=initial_units * 0.5, # 25M anUSD
            supply_B_prime=initial_units * 0.5  # 25M B' Yield
        )
        nav = bs.compute_model_navs(R=R, R_prime=R_prime, P_0=initial_savax_price, v=0.25)
        sheet = bs.evaluate_liabilities_and_equity(nav)
        invariants = bs.verify_all_invariants(nav)
        
        summary_results.append({
            "shock": shock,
            "shocked_price": shocked_price,
            "collateral_value": sheet["total_assets_usd"],
            "senior_debt": sheet["total_senior_debt"],
            "junior_equity": sheet["physical_equity_B"],
            "cr_phys": sheet["cr_phys"],
            "haircut_fraction": sheet["haircut_fraction"],
            "all_invariants_pass": all(v[0] for v in invariants.values())
        })
        
    return {"initial_tvl": initial_tvl_usd, "results": summary_results}


if __name__ == "__main__":
    test_run = run_balance_sheet_stress_test()
    print("=== Physical Balance Sheet Stress Test Across Shock Spectrum ===")
    for row in test_run["results"]:
        print(
            f"Shock: {row['shock']:+6.1%} | Price: ${row['shocked_price']:5.2f} | "
            f"Assets: ${row['collateral_value']/1e6:5.1f}M | Debt: ${row['senior_debt']/1e6:5.1f}M | "
            f"CR_phys: {row['cr_phys']:5.2f} | Haircut: {row['haircut_fraction']:6.2%} | Invariants: {row['all_invariants_pass']}"
        )
