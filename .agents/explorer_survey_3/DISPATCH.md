## 2026-08-30T11:10:51Z
You are explorer_survey_3.
Your working directory is: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_survey_3

MANDATORY FIRST STEP:
Read `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md` and `/home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md`.

YOUR MISSION:
Perform a systematic survey and evaluation of candidate open-source software libraries for the anUSD adversarial research study.

Evaluate:
- Primary Candidates:
  1. cadCAD
  2. SALib (Sensitivity Analysis Library in Python)
  3. PyMC + ArviZ (Bayesian Modeling & Probabilistic Programming)
  4. QuantLib (via QuantLib-Python / pyql)
- Auxiliary Scientific Libraries:
  5. SciPy (specifically scipy.stats.qmc, scipy.optimize, scipy.integrate)
  6. control (Python Control Systems Library)
  7. SimPy (Process-based discrete-event simulation)
  8. MLflow (Experiment tracking & model registry)

For each candidate, investigate against the 15 criteria in R1:
1. Exact problem solved
2. Research component requiring it
3. Whitepaper necessity
4. Semantic fidelity to canonical model
5. Mathematical/numerical methods used
6. Maintenance & activity status
7. Open-source license
8. Reproducibility implications
9. Determinism & random-seed management
10. Numerical stability & precision bounds
11. Performance & scaling throughput
12. Integration & dependency complexity
13. Hidden assumptions or default biases
14. Simpler native implementation trade-off
15. Recommended formal verdict (REQUIRED | RECOMMENDED | OPTIONAL | REJECTED)

Deliver your detailed evaluation report in `.agents/explorer_survey_3/handoff.md` and update `.agents/explorer_survey_3/progress.md`. Send a completion message back when finished.
