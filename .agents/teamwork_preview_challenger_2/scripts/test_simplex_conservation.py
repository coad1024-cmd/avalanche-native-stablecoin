"""
Empirical Verification & Stress Test Harness 1: 3-Simplex Conservation & Policy Robustness
Tests POL-01 to POL-05 under standard and pathological boundary conditions.
"""

import numpy as np

def pol01():
    return np.array([0.65, 0.20, 0.00, 0.15])

def pol02(P_spot, P_EMA, w_val_0=0.20, w_val_max=0.45, kappa_dd=0.35, w_l1_0=0.15, w_res_0=0.05):
    # Avoid div-by-zero if P_EMA is 0 or negative
    if P_EMA <= 0:
        D = 1.0 # maximal drawdown if baseline is 0
    else:
        D = max(0.0, (P_EMA - P_spot) / P_EMA)
    
    w_val = min(w_val_max, w_val_0 + kappa_dd * D)
    w_l1 = w_l1_0
    w_res = w_res_0
    w_burn = 1.0 - w_val - w_l1 - w_res
    return np.array([w_burn, w_val, w_res, w_l1])

def pol03(B_res, B_target, w_res_priority=0.50, w_res_maint=0.05):
    if B_target <= 0:
        xi_res = 1.0 # full if target is zero
    else:
        xi_res = B_res / B_target
    
    if xi_res < 1.0:
        w_res = w_res_priority
    else:
        w_res = w_res_maint
    
    w_val = 0.25 * (1.0 - w_res)
    w_l1 = 0.15 * (1.0 - w_res)
    w_burn = 0.60 * (1.0 - w_res)
    return np.array([w_burn, w_val, w_res, w_l1])

def pol04():
    return np.array([0.80, 0.10, 0.05, 0.05])

def pol05_naive(s, W, b):
    logits = np.dot(W, s) + b
    exp_logits = np.exp(logits)
    return exp_logits / np.sum(exp_logits)

def pol05_stabilized(s, W, b):
    logits = np.dot(W, s) + b
    max_logit = np.max(logits)
    exp_logits = np.exp(logits - max_logit)
    return exp_logits / np.sum(exp_logits)

def integer_routing(Y_total, omega):
    # Y_val, Y_res, Y_l1, Y_burn
    w_burn, w_val, w_res, w_l1 = omega
    y_val = int(np.floor(Y_total * w_val))
    y_res = int(np.floor(Y_total * w_res))
    y_l1 = int(np.floor(Y_total * w_l1))
    y_burn = Y_total - (y_val + y_res + y_l1)
    return np.array([y_burn, y_val, y_res, y_l1])

def run_tests():
    print("=== STARTING EMPIRICAL SIMPLEX STRESS TESTS ===")
    
    # 1. Standard tests for POL-01 to POL-04
    w1 = pol01()
    assert np.isclose(np.sum(w1), 1.0), "POL-01 sum != 1"
    assert np.all(w1 >= 0), "POL-01 negative weight"
    print(f"POL-01: {w1}, Sum: {np.sum(w1):.6f} - PASS")
    
    w4 = pol04()
    assert np.isclose(np.sum(w4), 1.0), "POL-04 sum != 1"
    assert np.all(w4 >= 0), "POL-04 negative weight"
    print(f"POL-04: {w4}, Sum: {np.sum(w4):.6f} - PASS")
    
    # 2. Stress POL-02 under extreme inputs
    test_drawdowns = [
        (100.0, 100.0), # No drawdown
        (120.0, 100.0), # Negative drawdown (spot > EMA)
        (0.0, 100.0),   # Total collapse to 0
        (-10.0, 100.0), # Negative spot
        (10.0, 0.0),    # EMA is 0
        (10.0, -50.0),  # Negative EMA
        (1e-18, 100.0), # Tiny spot
        (1e9, 100.0),   # Massive spot
    ]
    for p_spot, p_ema in test_drawdowns:
        w2 = pol02(p_spot, p_ema)
        assert np.isclose(np.sum(w2), 1.0), f"POL-02 sum != 1 for spot={p_spot}, ema={p_ema}"
        assert np.all(w2 >= 0), f"POL-02 negative weight for spot={p_spot}, ema={p_ema}"
    print("POL-02 Extreme Boundary Tests: ALL 8 EDGE CASES PASSED.")
    
    # 3. Stress POL-03 under extreme buffer states
    test_buffers = [
        (0.0, 1000.0),    # Empty buffer
        (500.0, 1000.0),  # Half buffer
        (1000.0, 1000.0), # Full buffer
        (2000.0, 1000.0), # Overflow buffer
        (0.0, 0.0),       # Target is zero
        (100.0, 0.0),     # Buffer exists, target 0
        (-50.0, 1000.0),  # Negative buffer (insolvency deficit)
    ]
    for b_res, b_target in test_buffers:
        w3 = pol03(b_res, b_target)
        assert np.isclose(np.sum(w3), 1.0), f"POL-03 sum != 1 for res={b_res}, target={b_target}"
        assert np.all(w3 >= 0), f"POL-03 negative weight for res={b_res}, target={b_target}"
    print("POL-03 Extreme Buffer Tests: ALL 7 EDGE CASES PASSED.")
    
    # 4. Stress POL-05 Softmax
    W = np.array([
        [-1.50, -0.80, -2.00, -1.80],
        [+2.50, +0.50, -0.50, +3.00],
        [+0.20, +1.50, +3.50, -0.50],
        [-0.50, -0.50, -0.50, -0.50]
    ])
    b = np.array([+0.65, -0.50, -1.20, -0.80])
    
    # Standard state
    s_normal = np.array([0.0, 0.89, 1.0, 0.0]) # normal market
    w5_norm = pol05_stabilized(s_normal, W, b)
    assert np.isclose(np.sum(w5_norm), 1.0)
    print(f"POL-05 Normal State: {w5_norm}, Sum: {np.sum(w5_norm):.6f} - PASS")
    
    # Severe crash state
    s_crash = np.array([0.90, 2.50, 1.0, 1.0])
    w5_crash = pol05_stabilized(s_crash, W, b)
    assert np.isclose(np.sum(w5_crash), 1.0)
    print(f"POL-05 Severe Crash State: {w5_crash}, Sum: {np.sum(w5_crash):.6f} - PASS")
    
    # Extreme pathological state (testing potential numerical overflow)
    s_extreme = np.array([100.0, 500.0, 100.0, 100.0])
    
    # Test naive vs stabilized
    try:
        w5_naive = pol05_naive(s_extreme, W, b)
        print(f"POL-05 Naive Extreme: {w5_naive}")
    except Exception as e:
        print(f"POL-05 Naive Overflowed as expected: {e}")
        
    w5_stab = pol05_stabilized(s_extreme, W, b)
    assert np.isclose(np.sum(w5_stab), 1.0), "POL-05 Stabilized sum != 1"
    assert not np.any(np.isnan(w5_stab)), "POL-05 Stabilized produced NaN"
    print(f"POL-05 Stabilized Extreme (s=[100,500,100,100]): {w5_stab}, Sum: {np.sum(w5_stab):.6f} - PASS")
    
    # 5. Monte Carlo 100,000 randomized state draws on POL-05
    np.random.seed(42)
    s_rand = np.random.uniform(0.0, 5.0, size=(100000, 4))
    for i in range(100000):
        w = pol05_stabilized(s_rand[i], W, b)
        if not np.isclose(np.sum(w), 1.0) or np.any(w < 0):
            raise AssertionError(f"Simplex violation on iteration {i}: {w}")
    print("POL-05 Monte Carlo 100,000 Random Draws: 100% INVARIANT CONSERVATION PASSED.")
    
    # 6. Integer routing zero-leakage test (EVM precision)
    test_yields = [0, 1, 2, 3, 7, 10, 1000, 10**18, 333333333333333333, 10**24]
    for y in test_yields:
        routed = integer_routing(y, w5_norm)
        assert np.sum(routed) == y, f"Integer leakage for Y={y}: sum={np.sum(routed)}"
        assert np.all(routed >= 0), f"Negative token integer for Y={y}: {routed}"
    print("Integer Precision Smart Contract Routing: 100% ZERO TOKEN LEAKAGE PASSED.")

if __name__ == "__main__":
    run_tests()
