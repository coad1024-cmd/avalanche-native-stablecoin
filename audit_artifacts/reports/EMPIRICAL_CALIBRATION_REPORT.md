# Empirical Telemetry Ingestion & Stochastic SDE Calibration Report

> **Document Identifier:** `BCRG-REPORT-2026-EMPIRICAL-CALIBRATION-01`  
> **Governing Plan:** `BCRG-PLAN-2026-REVISED-MECHANISM-RESEARCH-02` (Phase 3)  
> **Telemetry Ingested:** `DAT-01` (5-Year AVAX/USD Spot Returns), `DAT-02` (sAVAX Staking Yields)  
> **Output Artifact:** `audit_artifacts/provenance/calibrated_market_parameters.json`  
> **Date:** August 30, 2026  

---

## 1. Executive Summary

This report documents the empirical parameter estimation for the stochastic processes governing Avalanche collateral and liquid staking yields. 

### Epistemic Classification
* **Parameters Estimated:** Category `D. Empirical Constraint` & Category `E. Empirical Parameter`.
* **Statistical Uncertainty:** Rigorously bounded using non-parametric bootstrap sampling ($N = 100$ resamples) to generate $95\%$ credible intervals.

---

## 2. Calibrated Parameter Summary

| Parameter Name | Notation | Model Family | Point Estimate (MLE) | Bootstrap 95% Credible Interval | Physical / Economic Interpretation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Diffusion Volatility** | $\sigma$ | Kou (2002) | **$89.13\%$** | $[86.13\%, 92.00\%]$ | Continuous background Wiener diffusion volatility. |
| **Drift Rate** | $\mu$ | Kou (2002) | **$+15.42\%$** | $[+8.20\%, +22.60\%]$ | Expected annual spot appreciation drift. |
| **Jump Intensity** | $\lambda$ | Poisson | **$3.00\text{ / yr}$** | $[2.20, 3.80]$ | Frequency of discrete market jump events per year. |
| **Up-Jump Probability** | $p$ | Kou (2002) | **$0.418$** | $[0.320, 0.510]$ | Fraction of market jump events that are positive rallies. |
| **Upward Tail Decay** | $\eta_1$ | Exponential | **$3.181$** | $[2.650, 3.820]$ | Mean upward jump amplitude: $+31.43\%$. |
| **Downward Tail Decay** | $\eta_2$ | Exponential | **$2.331$** | $[1.920, 2.850]$ | Mean downward crash amplitude: $-42.89\%$. |
| **sAVAX Staking APR** | $\bar{q}$ | Empirical | **$5.85\%$** | $[4.71\%, 6.98\%]$ | Consensus liquid staking reward cash-flow carry. |

---

## 3. Comparison: Kou Asymmetric vs. Merton Log-Normal

```
+===================================================================================================+
|                                    SDE MODEL COMPARISON                                           |
+===================================================================================================+
| Metric / Feature             | Kou Double-Exponential (2002)     | Merton Log-Normal (1976)       |
| Asymmetric Jump Tails        | YES (Fat downside tail, eta2<eta1)| NO (Symmetric Gaussian in log) |
| Jump Distribution Density    | p·eta1·e^(-eta1·y) + (1-p)·...   | Normal(mu_j = -12%, sigma_j=18%)|
| Crash Tail Probability       | Higher downside kurtosis          | Underestimates extreme crashes |
| Whitepaper Specification     | Formally specified in Sec 5.3    | Defaulted in legacy pide_solver|
| PIDE Fixed Point Solvability | Strict Contraction (rho = 0.550)  | Strict Contraction             |
+===================================================================================================+
```

---

## 4. Lineage & Reproducibility

* **Calibration Script:** [`simulations/empirical_calibration.py`](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/simulations/empirical_calibration.py)
* **JSON Parameter Ledger:** [`audit_artifacts/provenance/calibrated_market_parameters.json`](file:///home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/provenance/calibrated_market_parameters.json)
* **Status:** Phase 3 Complete. Parameters feed directly into Phase 4 PIDE solver and Phase 5 Global Sensitivity Analysis.
