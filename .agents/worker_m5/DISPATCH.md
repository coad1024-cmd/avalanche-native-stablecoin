# Dispatch for Worker M5

## Assigned Milestone
Milestone 5 (Requirement R5): Sampling Error, Stage-1 Selection Bias, and Lambda Provisionality Assessment.

## Mandatory Integrity Warning
> DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective
Execute statistical quantification, selection bias auditing, and jump intensity sensitivity analysis for Stage 2:
1. Monte Carlo Sampling Error Quantification:
   - Compute Monte Carlo standard errors (MCSE) and 95% confidence intervals across the $N=500$ simulation paths for all key metrics (`haircut_prob`, `tail_cvar_99`, `reset_churn_annual`, `validator_cr_min`, `avax_burned_total`).
   - Determine whether ranking differences between top candidates (A2 vs A5.3 vs A5.2) and policy rankings (POL-02 vs POL-05 vs POL-03) are statistically significant ($p < 0.01$) or statistically tied.
2. Stage-1 Analytical Pruning Selection Bias:
   - Programmatically analyze `STAGE_1_CORRECTED_SURVIVORS.parquet` ($N=64,052$) vs initial population ($N_0=100,000$).
   - Audit whether Stage 1 pruning ($35.95\%$ pruned) disproportionately eliminated parameter subspaces favorable to specific architectures or policies.
   - Verify that all 8 architectures received uniform/balanced candidate representation in Stage 1 survivors ($\sim 7,900 - 8,100$ survivors per architecture).
3. Sensitivity to Provisional Jump Intensity ($\lambda = 15.00\text{ yr}^{-1}$):
   - Evaluate whether architecture/policy rankings depend materially on the provisional jump intensity $\lambda = 15.00\text{ yr}^{-1}$ without running an ungrounded continuous parameter sweep.
   - Explain why the ranking ordering ($A_2 \succ A_{5.3} \succ A_{5.2} \succ A_0 \succ A_1/A_3/A_4$) remains invariant under varying jump intensity regimes while reset churn magnitudes scale with $\lambda$.

## Key Inputs & References
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md`
- `/home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md`
- `audit_artifacts/execution/STAGE_1_ANALYTICAL_PRUNING_MANIFEST.json`
- `audit_artifacts/execution/STAGE_1_CORRECTED_SURVIVORS.parquet`
- `audit_artifacts/execution/STAGE_2_RESULTS.parquet`
- `simulations/design_discovery/stage2_architecture_screening.py`

## Deliverables
- Working directory: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m5`
- Independent verification script: `/home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/execution/verify_stage2_statistical_sampling_bias.py`
- Automated test suite: `simulations/design_discovery/test_stage2_statistical_sampling_bias.py`
- Comprehensive report: `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_m5/m5_statistical_bias_report.md`
- `handoff.md` and `progress.md`.
