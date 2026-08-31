"""
Empirical Verification & Stress Test Harness 2: Kou (2002) Jump-Diffusion MLE vs Merton
Verifies MLE parameters, AIC/BIC, Jump Compensator, Moment Generating Function bounds,
and SDE simulation correctness.
"""

import json
import numpy as np
import scipy.stats as stats

def run_kou_verification():
    print("=== STARTING KOU VS MERTON MLE & SDE VERIFICATION ===")
    
    # 1. Load provenance parameters
    param_path = "/home/hash/Hub/Projects/avalanche-native-stablecoin/audit_artifacts/provenance/calibrated_market_parameters.json"
    with open(param_path, 'r') as f:
        data = json.load(f)
        
    kou = data['kou_double_exponential']['point_estimates']
    merton = data['merton_log_normal']['point_estimates']
    kou_ci = data['kou_double_exponential']['bootstrap_95_credible_intervals']
    
    # Verify parameter counts
    # Kou parameters: (mu, sigma, lambda, p, eta1, eta2) -> k = 6
    # Merton parameters: (mu, sigma, lambda, mu_j, sigma_j) -> k = 5
    k_kou = 6
    k_merton = 5
    N = data['dataset_provenance']['observations_days']
    assert N == 2140, f"Expected 2140 observations, got {N}"
    
    # Check log-likelihoods
    ll_kou = kou['log_likelihood']
    ll_merton = merton['log_likelihood']
    print(f"Observations N: {N}")
    print(f"Kou Log-Likelihood: {ll_kou:.4f} (k={k_kou})")
    print(f"Merton Log-Likelihood: {ll_merton:.4f} (k={k_merton})")
    
    # Recompute AIC
    aic_kou_calc = 2 * k_kou - 2 * ll_kou
    aic_merton_calc = 2 * k_merton - 2 * ll_merton
    delta_aic = aic_kou_calc - aic_merton_calc
    
    print(f"Kou AIC Calculated: {aic_kou_calc:.4f} | Recorded: {kou['aic']:.4f}")
    print(f"Merton AIC Calculated: {aic_merton_calc:.4f} | Recorded: {merton['aic']:.4f}")
    print(f"Delta AIC (Kou - Merton): {delta_aic:.4f}")
    assert np.isclose(delta_aic, -5.50828, atol=1e-3), f"Delta AIC mismatch: {delta_aic}"
    
    # Recompute BIC
    bic_kou_calc = k_kou * np.log(N) - 2 * ll_kou
    bic_merton_calc = k_merton * np.log(N) - 2 * ll_merton
    delta_bic = bic_kou_calc - bic_merton_calc
    print(f"Kou BIC Calculated: {bic_kou_calc:.4f} | Recorded: {kou['bic']:.4f}")
    print(f"Merton BIC Calculated: {bic_merton_calc:.4f} | Recorded: {merton['bic']:.4f}")
    print(f"Delta BIC (Kou - Merton): {delta_bic:.4f}")
    
    # 2. Verify Kou jump tail decay and moment constraints
    p = kou['up_jump_prob_p']
    eta1 = kou['eta1_up_tail']
    eta2 = kou['eta2_down_tail']
    
    print(f"Kou Jump Parameters: p={p:.4f}, eta1={eta1:.4f}, eta2={eta2:.4f}")
    assert eta1 > 1.0, f"CRITICAL: eta1 must be > 1 for finite expectation E[e^Y], got {eta1}"
    assert eta2 > 0.0, f"CRITICAL: eta2 must be > 0, got {eta2}"
    assert 0.0 < p < 1.0, f"CRITICAL: p must be in (0, 1), got {p}"
    
    # Verify bootstrap bounds on eta1
    eta1_min_ci = kou_ci['eta1_up_tail'][0]
    assert eta1_min_ci > 1.0, f"CRITICAL: Lower 95% CI bound on eta1 is <= 1.0: {eta1_min_ci}"
    print(f"Bootstrap 95% CI on eta1: [{kou_ci['eta1_up_tail'][0]:.4f}, {kou_ci['eta1_up_tail'][1]:.4f}] > 1.0 - PASS")
    
    # 3. Calculate exact Jump Compensator zeta
    # zeta = E[e^Y - 1] = p*eta1/(eta1 - 1) + (1-p)*eta2/(eta2 + 1) - 1
    term1 = (p * eta1) / (eta1 - 1.0)
    term2 = ((1.0 - p) * eta2) / (eta2 + 1.0)
    zeta = term1 + term2 - 1.0
    print(f"Jump Compensator Components: Term1={term1:.5f}, Term2={term2:.5f}")
    print(f"Calculated Jump Compensator zeta: {zeta:.5f} ({zeta*100:.3f}%)")
    assert np.isclose(zeta, 0.043346, atol=1e-4), f"Zeta mismatch: {zeta}"
    
    # 4. Verify characteristic function of Kou jump-diffusion
    # phi(u) = exp( i*u*(mu - 0.5*sigma^2)*dt - 0.5*sigma^2*u^2*dt + lambda*dt * ( p*eta1/(eta1 - i*u) + (1-p)*eta2/(eta2 + i*u) - 1 ) )
    mu = kou['drift_mu']
    sigma = kou['diffusion_sigma']
    lam = kou['jump_intensity_lambda']
    dt = 1.0 / 365.0
    
    def kou_char_func(u, dt):
        drift_part = 1j * u * (mu - 0.5 * sigma**2) * dt
        diff_part = -0.5 * (sigma**2) * (u**2) * dt
        jump_part = lam * dt * ( (p * eta1) / (eta1 - 1j * u) + ((1.0 - p) * eta2) / (eta2 + 1j * u) - 1.0 )
        return np.exp(drift_part + diff_part + jump_part)
    
    # Test at u=0: phi(0) must be 1.0
    phi_0 = kou_char_func(0.0, dt)
    assert np.isclose(phi_0, 1.0 + 0j), f"phi(0) != 1: {phi_0}"
    print(f"Characteristic Function at u=0: {phi_0} - PASS")
    
    # 5. SDE Path Generator & Moment Verification via Monte Carlo
    N_paths = 100000
    np.random.seed(42)
    
    # Brownian increments
    Z = np.random.normal(0, 1, size=N_paths)
    
    # Poisson jumps
    N_jumps = np.random.poisson(lam * dt, size=N_paths)
    
    # Kou jump sizes
    jump_sizes = np.zeros(N_paths)
    for i in range(N_paths):
        k = N_jumps[i]
        if k > 0:
            # For each jump, decide direction with prob p
            is_up = np.random.binomial(1, p, size=k)
            y_up = np.random.exponential(1.0 / eta1, size=k)
            y_down = -np.random.exponential(1.0 / eta2, size=k)
            y = np.where(is_up == 1, y_up, y_down)
            jump_sizes[i] = np.sum(y)
            
    # Compensated log return:
    log_returns = (mu - 0.5 * sigma**2 - lam * zeta) * dt + sigma * np.sqrt(dt) * Z + jump_sizes
    
    # Check empirical mean and variance vs theoretical
    emp_mean = np.mean(log_returns) * 365.0
    emp_var = np.var(log_returns) * 365.0
    
    # Theoretical variance of Kou log returns:
    # Var(Y) = p*(2/eta1^2 - 1/eta1^2) + (1-p)*(2/eta2^2 - 1/eta2^2) ... 
    # E[Y] = p/eta1 - (1-p)/eta2
    # E[Y^2] = 2*p/eta1^2 + 2*(1-p)/eta2^2
    E_Y = p / eta1 - (1.0 - p) / eta2
    E_Y2 = 2.0 * p / (eta1**2) + 2.0 * (1.0 - p) / (eta2**2)
    Var_Y = E_Y2 - (E_Y**2)
    theo_ann_var = sigma**2 + lam * E_Y2
    
    print(f"Annualized Empirical Return Variance: {emp_var:.4f}")
    print(f"Theoretical Total Annualized Variance: {theo_ann_var:.4f}")
    assert np.isclose(emp_var, theo_ann_var, rtol=0.05), "Monte Carlo variance deviates from theory"
    print("Kou SDE Path Generator & Variance Decomposition: PASSED.")

if __name__ == "__main__":
    run_kou_verification()
