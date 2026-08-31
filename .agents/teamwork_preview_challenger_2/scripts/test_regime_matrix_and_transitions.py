"""
Empirical Verification & Stress Test Harness 3: 11-Regime Parameter Matrix & Transition Dynamics
Tests parameter admissibility across all 11 regimes, Markov generator Q matrix,
matrix exponential transition matrix P(t), ergodicity, and absence of absorbing states.
"""

import sys
sys.path.append("/home/hash/Hub/Projects/avalanche-native-stablecoin")

import numpy as np
import scipy.linalg as la
from simulations.robustness_study.market_regimes import MARKET_REGIMES, generate_regime_price_path

def test_regime_parameters():
    print("=== STARTING 11-REGIME PARAMETER INTEGRITY TESTS ===")
    
    assert len(MARKET_REGIMES) == 11, f"Expected 11 regimes, got {len(MARKET_REGIMES)}"
    
    for key, r in MARKET_REGIMES.items():
        sigma = r["sigma"]
        lam = r["lambda_jump"]
        p_up = r["p_up"]
        eta1 = r["eta_1"]
        eta2 = r["eta_2"]
        drift = r["drift"]
        q = r["q_savax"]
        liq = r["liquidity_usd"]
        
        # Test mathematical bounds
        assert sigma > 0.0, f"[{key}] Invalid sigma: {sigma}"
        assert lam >= 0.0, f"[{key}] Invalid lambda: {lam}"
        assert 0.0 <= p_up <= 1.0, f"[{key}] Invalid p_up: {p_up}"
        assert eta1 > 1.0, f"[{key}] CRITICAL: eta1 must be > 1.0, got {eta1}"
        assert eta2 > 0.0, f"[{key}] CRITICAL: eta2 must be > 0.0, got {eta2}"
        assert q > 0.0, f"[{key}] Invalid staking yield: {q}"
        assert liq > 0.0, f"[{key}] Invalid liquidity: {liq}"
        
        # Compute compensator zeta
        if eta1 > 1.0 and eta2 > 0.0:
            zeta = (p_up * eta1 / (eta1 - 1.0)) + ((1.0 - p_up) * eta2 / (eta2 + 1.0)) - 1.0
        else:
            zeta = np.nan
            
        print(f"{key:<26}: sigma={sigma:.2f}, lam={lam:.1f}, p={p_up:.2f}, eta1={eta1:.1f}, eta2={eta2:.1f}, zeta={zeta:+.4f} - PASS")
        
    print("All 11 Regimes Satisfy Strict Admissibility (eta1 > 1.0, eta2 > 0.0, sigma > 0).")

def test_markov_generator_and_transitions():
    print("\n=== TESTING CONTINUOUS-TIME MARKOV REGIME SWITCHING (Q & P matrices) ===")
    
    # Define realistic transition rates Q (11x11) based on section 3.2
    # Regime index mapping:
    # 0: CALM_BULL, 1: NORMAL, 2: HIGH_VOLATILITY, 3: SEVERE_BEAR, 4: FLASH_CRASH,
    # 5: MULTI_JUMP_CASCADE, 6: V_SHAPED_RECOVERY, 7: PROLONGED_STAGNANT_BEAR,
    # 8: HIGH_YIELD, 9: LOW_YIELD_COMPRESSION, 10: ILLIQUID_AMM
    
    Q = np.zeros((11, 11))
    
    # Baseline expected durations (1/rate in years)
    # NORMAL (idx 1): half-life ~1.5 yr -> rate 0.67
    # CALM_BULL (idx 0): half-life ~1.0 yr -> rate 1.0
    # SEVERE_BEAR (idx 3): half-life ~0.8 yr -> rate 1.25
    # FLASH_CRASH (idx 4): half-life 14 days (0.038 yr) -> rate 26.0 (transitions rapidly to recovery or normal)
    # MULTI_JUMP_CASCADE (idx 5): half-life 14 days -> rate 26.0
    # V_SHAPED_RECOVERY (idx 6): half-life 30 days (0.082 yr) -> rate 12.0
    # PROLONGED_STAGNANT_BEAR (idx 7): half-life ~2.0 yr -> rate 0.50
    # Other stress regimes: half-life 30-60 days -> rate 6.0 to 12.0
    
    holding_rates = [1.0, 0.67, 2.0, 1.25, 26.0, 26.0, 12.0, 0.50, 1.5, 2.0, 4.0]
    
    # Fill transition probabilities to other states
    for i in range(11):
        # distribute holding rate to adjacent / logical regimes
        rate = holding_rates[i]
        for j in range(11):
            if i != j:
                # Give higher transition weight to NORMAL (idx 1) and logical next states
                if j == 1:
                    Q[i, j] = rate * 0.40
                elif abs(i - j) == 1:
                    Q[i, j] = rate * 0.30
                else:
                    Q[i, j] = rate * (0.30 / 9.0)
        # Enforce exact row zero-sum: q_ii = -sum_{j != i} q_ij
        Q[i, i] = -np.sum(Q[i, :])
        
    print("Markov Generator Matrix Q (11x11) constructed.")
    assert np.all(np.isclose(np.sum(Q, axis=1), 0.0)), "Row sums of Q must be 0"
    assert np.all(Q - np.diag(np.diag(Q)) >= 0), "Off-diagonal elements of Q must be non-negative"
    assert np.all(np.diag(Q) < 0), "Diagonal elements of Q must be strictly negative (no absorbing states)"
    print("Row zero-sum & off-diagonal non-negativity: PASSED.")
    
    # Compute Transition Matrix P(t) = exp(Q * t) for t = 1.0 day (1/365), 30 days, 1 year
    for days in [1.0, 30.0, 365.0]:
        t = days / 365.0
        P_t = la.expm(Q * t)
        
        # Verify row stochasticity
        assert np.all(P_t >= -1e-12), f"Negative probabilities in P({days}d)"
        assert np.all(np.isclose(np.sum(P_t, axis=1), 1.0)), f"Row sums != 1.0 in P({days}d)"
        print(f"P({days:3.0f} days) Row Stochasticity: Sums = {np.sum(P_t, axis=1)[:3]}... ALL 1.000000 - PASS")
        
    # Check ergodicity and stationary distribution
    eigvals, eigvecs = la.eig(Q.T)
    # Find eigenvalue close to 0
    zero_idx = np.argmin(np.abs(eigvals))
    assert np.isclose(eigvals[zero_idx].real, 0.0, atol=1e-10), "No zero eigenvalue found"
    
    # Verify all other eigenvalues have negative real parts
    other_eigvals = np.delete(eigvals, zero_idx)
    assert np.all(other_eigvals.real < 0), "Chain not strictly ergodic (eigenvalues with non-negative real part)"
    print("Generator Spectrum: Exactly 1 zero eigenvalue, all other Re(lambda) < 0 -> STRICTLY ERGODIC.")
    
    pi = eigvecs[:, zero_idx].real
    pi = pi / np.sum(pi)
    assert np.all(pi > 0), "Stationary distribution must be strictly positive"
    print(f"Stationary Distribution pi: {np.round(pi, 4)}")
    print(f"Stationary Persistence: Normal={pi[1]*100:.1f}%, CalmBull={pi[0]*100:.1f}%, Bear={pi[3]*100:.1f}%")

def test_price_trajectories():
    print("\n=== TESTING REGIME TRAJECTORY SIMULATION ACROSS ALL 11 REGIMES ===")
    for k in MARKET_REGIMES.keys():
        prices, reg = generate_regime_price_path(k, days=365, seed=42)
        assert len(prices) == 366
        assert np.all(prices > 0), f"Price went non-positive in regime {k}"
        assert not np.any(np.isnan(prices)), f"NaN price in regime {k}"
        print(f"{k:<26}: Min=${prices.min():.2f}, Max=${prices.max():.2f}, Final=${prices[-1]:.2f} - PASS")

if __name__ == "__main__":
    test_regime_parameters()
    test_markov_generator_and_transitions()
    test_price_trajectories()
