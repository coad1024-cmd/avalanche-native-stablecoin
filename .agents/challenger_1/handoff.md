# Empirical Challenger Handoff Report: Open-Source Tooling Audit & Simulation Verification

**Document Identifier:** `BCRG-CHALLENGER-AUDIT-01`  
**Agent:** `challenger_1` (Empirical Challenger & Adversarial Reviewer)  
**Date:** August 30, 2026  
**Verdict:** **REQUEST_CHANGES**  

---

## 1. Observation

Direct empirical observations, tool commands, line numbers, and verbatim outputs obtained during execution:

### 1.1 Scientific Libraries Verification
Executed toolchain inspection:
```bash
python3 -c "
import numpy as np, scipy, control, pandas as pd, matplotlib
print(np.__version__, scipy.__version__, control.__version__, pd.__version__, matplotlib.__version__)
"
```
**Observed Output:**
- `NumPy Version`: `2.4.4`
- `SciPy Version`: `1.17.1`
- `Control Version`: `0.10.2`
- `Pandas Version`: `3.0.2`
- `Matplotlib Version`: `3.10.8`
- `SALib Version`: `Not installed` (Attempting `import SALib` raises `ModuleNotFoundError: No module named 'SALib'`)

### 1.2 Foundry Smart Contract Test Suite
Command: `cd contracts && forge test -vvv`
**Observed Output:**
```
Ran 3 tests for test/unit/YieldRecycler.t.sol:YieldRecyclerUnitTest [PASS] (3/3)
Ran 2 tests for test/invariant/SolvencyInvariant.t.sol:SolvencyInvariantTest [PASS] (2/2)
Ran 3 tests for test/unit/CustodianVault.t.sol:CustodianVaultUnitTest [PASS] (3/3)
Ran 3 test suites in 12.44ms (3.84ms CPU time): 8 tests passed, 0 failed, 0 skipped (8 total tests)
```

### 1.3 Tranche Mathematical Solvency & Invariants
Executed 100,000 random floating-point state perturbations ($P \in [0.001, 10000], \beta \in [0.0001, 1000], P_0 \in [0.001, 10000], v \in [0, 5], R \in [0, 0.50]$) and a 5,000-step dynamic reset trajectory with 4,855 upward and 3 downward resets:
- Primary Solvency Invariant: $\max |V_A + V_B - 2S| = 3.5527 \times 10^{-15} \le 10^{-12}$ (**PASSED**)
- Secondary Parity Invariant: $\max |V_{A'} + V_{B'} - 2V_A| = 8.8818 \times 10^{-16} \le 10^{-12}$ (**PASSED**)
- Theorem 1 Single-Step Crash Tolerance: Model-free bound $\Delta P_{\max} = -60.0000\%$. Class $A'$ (`anUSD`) suffered $0.00\%$ haircut for single-step drops of $-10\%, -20\%, -30\%, -40\%, -50\%, -60\%$ from $H_d = \$0.25$ ($S=0.625$). Haircuts initiated at $-65\%$ ($12.50\%$ haircut) and $-75\%$ ($37.50\%$ haircut) exactly as predicted by Theorem 1 (**PASSED**).

### 1.4 Control Damping Ratio & Stability
- Analytical Closed-Loop Damping Ratio: $\zeta = \frac{1 + K_{\text{amm}} K_p}{2 \sqrt{K_{\text{amm}} K_i \tau_{\text{arb}}}} = 17.0318 \gg 1.00$ ($K_p=0.150, K_i=0.020, K_{\text{amm}}=1.20, \tau_{\text{arb}}=0.05$).
- Transfer Function Poles (`control.feedback`): $s_1 = -23.58, s_2 = -0.02036$ (strictly real, negative poles $\implies$ strictly overdamped, zero oscillatory resonance).
- Non-linear AMM simulation (`controller_isolation.py`) confirmed stability across $\$30\text{M}, \$10\text{M}, \$1.5\text{M}$ liquidity tiers.

### 1.5 PIDE Numerical Solver Instability & Explosion
File: `simulations/cadcad_core/mechanisms/pide_solver.py` (lines 81-84):
```python
diffusion_term = (self.r - self.lambda_j * self.kappa) * S_i * dW_dS + 0.5 * (self.sigma**2) * (S_i**2) * d2W_dS2 - self.r * W_next[i]
integral_term = self.lambda_j * jump_int
W_curr[i] = W_next[i] + dt * (diffusion_term + integral_term)
```
File: `simulations/cadcad_core/experiments/run_pide_surface.py` (lines 32-34):
Executed with $N_S = 60, N_T = 60$.
**Observed Numerical Results on Grid:**
- `Max |W_surface|`: $5.0767 \times 10^{71}$
- `Min W_surface`: $-5.0767 \times 10^{71}$
- `Max W_surface`: $4.2306 \times 10^{71}$
- `W_surface at S=1.0, t=0.0`: $1.0000$ (center point was masked, but outer spatial grid exploded by 71 orders of magnitude).
- When tested across grid dimensions:
  - $N_S=50, N_T=50$: `Max |W|` = $1.2214 \times 10^{54}$
  - $N_S=100, N_T=100$: `Max |W|` = $8.0427 \times 10^{148}$
  - $N_S=50, N_T=500$: `Max |W|` = $1.0730$ (stable)
  - $N_S=100, N_T=10000$: `Max |W|` = $1.0730$ (stable)

### 1.6 Simulation Pipeline Import & Execution Failures
Command 1: `python3 simulations/cadcad_core/experiments/run_monte_carlo.py`
**Verbatim Error:**
```
Traceback (most recent call last):
  File "/home/hash/Hub/Projects/avalanche-native-stablecoin/simulations/cadcad_core/experiments/run_monte_carlo.py", line 14, in <module>
    from params import DEFAULT_PARAMS
ImportError: cannot import name 'DEFAULT_PARAMS' from 'params' (/home/hash/Hub/Projects/avalanche-native-stablecoin/simulations/cadcad_core/params.py). Did you mean: 'DEFAULT_ENV_PARAMS'?
```

Command 2: `python3 simulations/cadcad_core/experiments/run_black_swan_replays.py`
**Verbatim Error:**
```
Traceback (most recent call last):
  File "/home/hash/Hub/Projects/avalanche-native-stablecoin/simulations/cadcad_core/experiments/run_black_swan_replays.py", line 20, in <module>
    from params import DEFAULT_PARAMS
ImportError: cannot import name 'DEFAULT_PARAMS' from 'params' (/home/hash/Hub/Projects/avalanche-native-stablecoin/simulations/cadcad_core/params.py). Did you mean: 'DEFAULT_ENV_PARAMS'?
```

Command 3: In `simulations/cadcad_core/psubs.py`:
- Line 12: `from mechanisms.tranche_math import verify_solvency_invariant` $\implies$ `ImportError: cannot import name 'verify_solvency_invariant' from 'mechanisms.tranche_math'`.
- Line 149: `params["bear_subsidy_R_tilde"]` vs `params.py` line 20 `"bear_subsidy_R"`.
- Lines 172-174: `params["acp67_burn_share"]`, `params["acp67_val_share"]`, `params["acp67_l1_share"]` vs `params.py` lines 45-47 `"acp67_burn_pct"`, etc.

---

## 2. Logic Chain

1. **PIDE Numerical Scheme Defect (Obs 1.5)**:
   - The report and source code describe the PIDE solver as an "Implicit-Explicit (IMEX) finite difference scheme".
   - Inspection of `pide_solver.py:84` reveals an explicit Euler forward-step in backward time ($W_{n} = W_{n+1} + \Delta t \cdot \mathcal{L}W_{n+1}$).
   - For an explicit parabolic operator with diffusion $\frac{1}{2} \sigma^2 S^2 \frac{\partial^2 W}{\partial S^2}$, stability requires the CFL condition $\Delta t \le \frac{(\Delta S)^2}{\sigma^2 S_{\max}^2}$.
   - For $S_{\max} = 3.0$ and $\sigma = 0.8986$, $\sigma^2 S_{\max}^2 \approx 7.27$. With $N_S=60$ ($\Delta S \approx 0.0492$), $\Delta t_{\max} \approx 0.000332 \implies N_T \ge 3,010$.
   - Because `run_pide_surface.py` and `pide_solver.py` run with $N_T=60$ ($\Delta t \approx 0.0167$, $50\times$ above CFL limit), numerical truncation errors amplify exponentially backward in time to $10^{71}$.
   - While $W(1.0, 0.0) = 1.0000$ happened to remain bounded at the center point, the outer spatial grid is corrupted, rendering the pricing surface in Figure 10 invalid.

2. **Pipeline Integration Defect (Obs 1.6)**:
   - `cadcad_core/params.py` defines `DEFAULT_GOVERNANCE_LEVERS` and `DEFAULT_ENV_PARAMS` but omits `DEFAULT_PARAMS`.
   - `run_monte_carlo.py` and `run_black_swan_replays.py` directly attempt `from params import DEFAULT_PARAMS`, failing immediately with `ImportError`.
   - `psubs.py` attempts to import `verify_solvency_invariant` from `tranche_math.py`, where it is undefined.
   - Parameter dictionary key mismatches (`bear_subsidy_R_tilde` vs `bear_subsidy_R`, `acp67_burn_share` vs `acp67_burn_pct`) prevent end-to-end execution of the cadCAD simulation pipeline without patching.

3. **Core Economic & Smart Contract Integrity (Obs 1.2, 1.3, 1.4)**:
   - The underlying mathematical mechanisms (`tranche_math.py`, `dynamic_resets.py`, `acp67_waterfall.py`, `feedback_controller.py`) and Solidity smart contracts (`contracts/src/`) are mathematically rigorous and empirically sound.
   - Solvency conservation $|V_A + V_B - 2S| \le 3.55 \times 10^{-15}$ exceeds the required $10^{-12}$ tolerance by three orders of magnitude.
   - Theorem 1 single-step crash invariance ($0.00\%$ haircut up to $-60.00\%$) holds strictly.
   - All 8 Foundry unit, invariant, and integration tests pass in $12.44\text{ ms}$.
   - Control damping ratio $\zeta = 17.0318$ is mathematically proven and confirmed via `python-control`.

---

## 3. Caveats

1. **SALib Package Availability**: SALib is not installed in the standard CLI environment. While the repository provides a clean native SciPy QMC Sobol implementation in `sobol_sensitivity.py`, the audit report claims dual-validation against SALib. This dual validation cannot be executed in the current environment without installing SALib.
2. **Computational Load of High-Resolution PIDE**: Resolving the PIDE explicit CFL limit by setting $N_T=10,000$ in pure Python requires $\sim 20$ seconds due to non-vectorized nested quadrature loops. Implementing an implicit tridiagonal solver (e.g. via `scipy.linalg.solve_banded`) will solve the PIDE unconditionally in $<50\text{ ms}$.

---

## 4. Conclusion

**Verdict: REQUEST_CHANGES**

The architectural design, mathematical derivations (SSRN-3856569 + ACP-67), control-theoretic proofs ($\zeta = 17.03$), and Foundry smart contracts are exemplary and pass all empirical verification gates. However, publication of the tooling audit report and simulation package must be gated on fixing two technical defects:

1. **Fix PIDE Solver Numerical Scheme (`simulations/cadcad_core/mechanisms/pide_solver.py`)**:
   - Upgrade the spatial diffusion discretization from explicit forward Euler to an actual **IMEX scheme** (Implicit diffusion via tridiagonal matrix inversion `scipy.linalg.solve_banded` + Explicit jump quadrature), or enforce adaptive $\Delta t \le \frac{(\Delta S)^2}{\sigma^2 S^2}$ sub-stepping ($N_T \ge 3,500$) to eliminate numerical explosion ($10^{71}$).
   - Re-generate `docs/figures/fig10_pide_pricing_surface.png` with the stable surface.

2. **Fix cadCAD Simulation Imports and Parameter Registry (`simulations/cadcad_core/`)**:
   - In `params.py`: Export unified `DEFAULT_PARAMS = {**DEFAULT_GOVERNANCE_LEVERS, **DEFAULT_ENV_PARAMS, "dt_years": 1.0/365.0, "bear_subsidy_R_tilde": 0.10, "acp67_burn_share": 0.65, "acp67_val_share": 0.20, "acp67_l1_share": 0.15}`.
   - In `tranche_math.py`: Define `verify_solvency_invariant(V_A, V_B, S_index, tolerance=1e-12)`.
   - Ensure `run_monte_carlo.py` and `run_black_swan_replays.py` execute cleanly out-of-the-box.

---

## 5. Verification Method

To independently verify these findings:

1. **Verify PIDE Explosion with Default Grid**:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, '/home/hash/Hub/Projects/avalanche-native-stablecoin/simulations/cadcad_core')
   from mechanisms.pide_solver import TranchePIDESolver
   import numpy as np
   solver = TranchePIDESolver()
   _, _, W = solver.solve_tranche_pricing_grid(N_S=60, N_T=60)
   print('Max |W| with N_S=60, N_T=60:', np.max(np.abs(W)))
   "
   ```
   *Expected Outcome:* Prints `Max |W|: 5.0767e+71`, proving numerical instability.

2. **Verify Monte Carlo Import Failure**:
   ```bash
   python3 /home/hash/Hub/Projects/avalanche-native-stablecoin/simulations/cadcad_core/experiments/run_monte_carlo.py
   ```
   *Expected Outcome:* Fails with `ImportError: cannot import name 'DEFAULT_PARAMS' from 'params'`.

3. **Verify Solvency Invariants**:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, '/home/hash/Hub/Projects/avalanche-native-stablecoin/simulations/cadcad_core')
   from mechanisms.tranche_math import compute_normalized_pool_index, evaluate_primary_navs
   S = compute_normalized_pool_index(25.0, 1.0, 25.0)
   v_a, v_b = evaluate_primary_navs(S, 0.0, 0.073)
   assert abs((v_a + v_b) - 2.0 * S) < 1e-12
   print('Solvency Invariant OK')
   "
   ```
   *Expected Outcome:* Prints `Solvency Invariant OK`.
