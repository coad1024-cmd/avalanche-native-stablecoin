# Dispatch for Worker M3

## Assigned Milestone
Milestone 3 (Requirement R3): End-to-End KPI Calculation & Objective Direction Audit.

## Mandatory Integrity Warning
> DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective
Audit every Stage 2 KPI across its full lifecycle: Mathematical Formulation $\to$ Code Implementation $\to$ Parquet Storage $\to$ Report Synthesis.
1. Formally audit all 11 KPIs:
   - `peg_rmse` (Secondary AMM Peg Volatility / RMSE)
   - `max_depeg` (Maximum Peg Deviation)
   - `rate_volatility` (Interest / Rebalancing Rate Volatility)
   - `recovery_time_days` (Depeg Recovery Time)
   - `haircut_prob` (Solvency Default Loss Frequency across $N=500$ paths)
   - `tail_cvar_99` (Conditional Value at Risk at 99% Confidence)
   - `reset_churn_annual` (Annual Rebalancing / Reset Churn Frequency)
   - `validator_cr_min` (Minimum Validator OpEx Coverage Ratio)
   - `validator_insolvency_prob` (Validator Operational Insolvency Probability)
   - `avax_burned_total` (Cumulative AVAX Token Burn Volume)
   - `collateral_yield_gross` (Gross Collateral Staking Yield Generated)
2. Verify objective directions (minimize vs maximize):
   - Check alignment with `OBJECTIVES_AND_CONSTRAINTS.md` and `DECISION_FRAMEWORK.md`.
3. Check specifically for:
   - Algebraic tautologies and denominator cancellations.
   - Look-ahead bias in simulation time-stepping.
   - Incorrect unit scaling, annualization, or day-count conventions ($\Delta t = 1/365$).
   - Aggregation errors across Monte Carlo paths (arithmetic mean vs geometric mean vs quantile calculations).
   - Survivorship bias in metric aggregation.
   - Sign convention consistency across optimization objectives.

## Key Inputs & References
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md`
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md`
- `audit_artifacts/design_discovery/OBJECTIVES_AND_CONSTRAINTS.md`
- `audit_artifacts/design_discovery/DECISION_FRAMEWORK.md`
- `simulations/design_discovery/stage2_architecture_screening.py`
- `audit_artifacts/execution/STAGE_2_RESULTS.parquet`

## Deliverables
- Working directory: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m3`
- Independent verification script: `/home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/execution/verify_stage2_kpi_mathematics.py`
- Automated test suite: `simulations/design_discovery/test_stage2_kpi_calculations.py`
- Comprehensive report: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m3/m3_kpi_math_report.md`
- `handoff.md` and `progress.md`.
