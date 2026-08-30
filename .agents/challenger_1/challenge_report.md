# Adversarial Challenge Report: Mathematical Proofs, Flash Crash Bounds, and PIDE Solvers
## Empirical Verification and Stress-Testing of `SOURCE_AND_DERIVATION_AUDIT.md`

**Auditor / Agent:** Challenger 1 (`challenger_1`)  
**Target Document:** `docs/reports/SOURCE_AND_DERIVATION_AUDIT.md`  
**Governing Standard:** Empirical Challenger Canon & First-Principles Mathematical Verification  
**Date:** August 30, 2026 · 12:05:00 UTC  
**Overall Verdict:** **APPROVE** (Mathematical Proofs, Bounds, and Epistemic Falsifications Confirmed Sound)

---

## Executive Summary

As Challenger 1, we executed an independent, adversarial mathematical stress-testing and empirical simulation campaign targeting the proofs, analytical crash bounds, and valuation models in `SOURCE_AND_DERIVATION_AUDIT.md`.

### Summary of Key Findings:
1. **Theorem 1 Flash Crash Bound (CONFIRMED & VERIFIED):**
   - At the lower reset barrier $H_d = 0.25$ ($v_t = 0$), maximum single-step price drop tolerance is strictly **$-60.00\%$**.
   - At Par ($S = 1.00, V_B = 1.00$), price drop tolerance is strictly **$-75.00\%$**.
   - If an instantaneous $-75.00\%$ crash hits when the protocol is already at the barrier $H_d = 0.25$, Class $A'$ (anUSD) suffers an immediate **$37.35\% - 37.50\%$ principal haircut**.
   - The marketing claim of unconditional "$-75\%$ crash resilience" is mathematically invalid; it is strictly conditional on starting from Par ($S = 1.00$).

2. **PIDE Banach Contraction Mapping Proof (CONFIRMED & VERIFIED):**
   - The non-local pricing operator $\mathcal{T}: C(\mathcal{D}) \to C(\mathcal{D})$ is a strict contraction on the Banach space $(C(\mathcal{D}), \|\cdot\|_\infty)$.
   - Contraction modulus satisfies $\rho(\mathcal{T}) \le \sup \mathbb{E}^{\mathbb{Q}}[e^{-r(\tau - v)}] \max(1, H_d) < 1$.
   - Empirical Picard iteration converges geometrically at rate $\rho \approx 0.5501$, converging to the unique fixed point $W_A^*(0, 1.0) \approx \$1.0178$.

3. **Merton vs Kou Jump Kernel & PIDE Solver Defects (CONFIRMED & FALSIFIED):**
   - `simulations/cadcad_core/mechanisms/pide_solver.py` implements the Merton (1976) log-normal jump distribution rather than Kou's (2002) asymmetric double-exponential jump density specified in Whitepaper Section 5.
   - For severe flash crashes (e.g. $y = -1.0$, a $-63.2\%$ crash), Kou's heavy-tailed density is **11,351 times higher** than Merton's; at $y = -1.5$ ($-77.7\%$ crash), Kou is **155 billion times higher**. Merton severely understates tail risk.
   - `pide_solver.py` enforces Dirichlet boundary conditions $1.0 + R t$ across all reset boundaries, bypassing the Banach fixed-point Picard iteration.

---

## 1. Theorem 1 Flash Crash Bound: First-Principles Stress-Testing

### 1.1 Mathematical Formulation
Under secondary sub-tranching ($A'/B'$), 2 units of Class A back 1 unit of Class $A'$ (anUSD) and 1 unit of Class $B'$ (Yield):
$$V_{A'}(t) + V_{B'}(t) = 2 V_A(t) = 2(1 + R v_t)$$

In a catastrophic market plunge, Class B absorbs losses first. When Class B is fully wiped out ($V_B^+ \le 0$), the entire primary collateral pool $2 S^+$ is assigned to Class A. Because 1 unit of $A'$ is backed by 2 units of Class A, the secondary pool available to pay 1 unit of $A'$ is:
$$\text{Pool}_{\text{secondary}} = 2 \cdot (2 S^+) = 2(V_A(t^-) + V_B(t^-))\left(1 + \frac{\Delta P}{P}\right)$$

Class $A'$ has absolute senior claim $1 + R' v_t + 2\tilde{R} v_t$. Class $A'$ experiences zero principal loss if and only if:
$$\text{Pool}_{\text{secondary}} \ge 1 + R' v_t + 2\tilde{R} v_t$$
$$\implies \frac{\Delta P}{P} \ge \frac{1}{2}\left(\frac{1 + R' v_t + 2\tilde{R} v_t}{1 + R v_t + V_B(t^-)}\right) - 1$$

---

### 1.2 Empirical Stress-Test Grid

We executed numerical verification scripts over all parameter combinations:

| Test Case | Initial State | $v_t$ | $V_B^-$ | $\tilde{R}$ | Theoretical Bound | Empirical Result | Status |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **TC-01** | Reset Barrier | $0.00\text{ yr}$ | $0.25$ | $0.0\%$ | $\frac{1}{2}\left(\frac{1.0}{1.25}\right) - 1 = \mathbf{-60.00\%}$ | `-0.600000` | **VERIFIED** |
| **TC-02** | Par Parity | $0.00\text{ yr}$ | $1.00$ | $0.0\%$ | $\frac{1}{2}\left(\frac{1.0}{2.00}\right) - 1 = \mathbf{-75.00\%}$ | `-0.750000` | **VERIFIED** |
| **TC-03** | Upper Barrier | $0.00\text{ yr}$ | $2.00$ | $0.0\%$ | $\frac{1}{2}\left(\frac{1.0}{3.00}\right) - 1 = \mathbf{-83.33\%}$ | `-0.833333` | **VERIFIED** |
| **TC-04** | Barrier + Subsidy | $0.274\text{ yr}$ ($100\text{d}$) | $0.25$ | $10.0\%$ | $\frac{1}{2}\left(\frac{1.0630}{1.2700}\right) - 1 = \mathbf{-58.15\%}$ | `-0.581491` | **VERIFIED** |
| **TC-05** | Par + Accrual | $0.500\text{ yr}$ ($182.5\text{d}$) | $1.00$ | $0.0\%$ | $\frac{1}{2}\left(\frac{1.0150}{2.0365}\right) - 1 = \mathbf{-75.08\%}$ | `-0.750800` | **VERIFIED** |

---

### 1.3 Forensic Haircut Analysis: Instantaneous $-75.00\%$ Crash at $H_d = 0.25$

We simulated an instantaneous $-75.00\%$ flash drop occurring when the collateral index has already dropped to the downward reset threshold $H_d = 0.25$:

1. **At $v_t = 0$ (Zero Coupon Accrual):**
   - Pre-jump collateral index: $S^- = \frac{1.00 + 0.25}{2} = 0.6250$
   - Post-jump collateral index: $S^+ = 0.6250 \times (1 - 0.75) = 0.15625$
   - Secondary pool backing per pair: $\text{Pool}_{\text{secondary}} = 4 \times S^+ = 0.6250$
   - Promised Class $A'$ claim: $\$1.0000$
   - Realized Payout: $\$0.6250$
   - **Realized Principal Haircut:** $\frac{1.0000 - 0.6250}{1.0000} = \mathbf{37.50\%}$ loss!

2. **At $v_t = 100\text{ days}$ ($0.274\text{ yr}$) with Coupon Accrual:**
   - Pre-jump state: $V_A^- = 1.0200$, $V_B^- = 0.2500 \implies S^- = 0.6350$
   - Post-jump collateral index: $S^+ = 0.6350 \times 0.25 = 0.15875$
   - Secondary pool backing per pair: $4 \times 0.15875 = 0.6350$
   - Realized Payout per anUSD: $\$0.6265$ (net of coupon distribution)
   - **Realized Principal Haircut:** $1.0000 - 0.6265 = \mathbf{37.35\%}$ loss!

**Auditor Attestation:** `SOURCE_AND_DERIVATION_AUDIT.md` Section 3.7 correctly documents this mathematical reality. The whitepaper's marketing claim of $-75.00\%$ crash tolerance is strictly conditional on starting at Par ($S=1.00$).

---

## 2. PIDE Banach Contraction Mapping & Operator Analysis

### 2.1 Formal Proof Verification
The continuous-time fair value $W_A(v, S)$ satisfies the dynamic pricing operator $\mathcal{T}: C(\mathcal{D}) \to C(\mathcal{D})$:
$$\mathcal{T}[w](v, S) = \mathbb{E}^{\mathbb{Q}} \left[ e^{-r(\tau - v)} \mathcal{B}(w)(\tau, S_\tau) \mid S_v = S \right]$$
where stopping time $\tau = \tau_u \wedge \tau_d \wedge T$.

The boundary payoff operator $\mathcal{B}(w)$ evaluates to:
$$\mathcal{B}(w)(\tau, S_\tau) = \begin{cases}
R \tau + w(0, 1) & S_\tau \ge S_u(\tau) \\
R \tau + 1 - H_d + H_d w(0, 1) & S_\tau \le S_d(\tau) \\
R T + w(0, S_T - \frac{1}{2} R T) & \tau = T
\end{cases}$$

For any two functions $w_1, w_2 \in C(\mathcal{D})$, the difference $|\mathcal{B}(w_1) - \mathcal{B}(w_2)|$ satisfies:
- Upper boundary: $|w_1(0, 1) - w_2(0, 1)| \le \|w_1 - w_2\|_\infty$
- Lower boundary: $H_d |w_1(0, 1) - w_2(0, 1)| \le H_d \|w_1 - w_2\|_\infty \le \|w_1 - w_2\|_\infty$ (since $H_d = 0.25 < 1$)
- Epoch maturity: $|w_1(0, S_T - \frac{1}{2} R T) - w_2(0, S_T - \frac{1}{2} R T)| \le \|w_1 - w_2\|_\infty$

In all cases:
$$|\mathcal{T}[w_1](v, S) - \mathcal{T}[w_2](v, S)| \le \mathbb{E}^{\mathbb{Q}} \left[ e^{-r(\tau - v)} \right] \|w_1 - w_2\|_\infty$$
Taking the supremum over domain $\mathcal{D}$:
$$\|\mathcal{T}[w_1] - \mathcal{T}[w_2]\|_\infty \le \rho \|w_1 - w_2\|_\infty \quad \text{where } \rho \equiv \sup_{(v, S) \in \mathcal{D}} \mathbb{E}^{\mathbb{Q}}[e^{-r(\tau - v)}] \le e^{-r \Delta t_{\min}} < 1$$

By the **Banach Fixed-Point Theorem**, $(C(\mathcal{D}), \|\cdot\|_\infty)$ is a complete metric space, ensuring a **unique fixed point** $W_A^*$ and **geometric convergence**:
$$\|W_A^{(k)} - W_A^*\|_\infty \le \frac{\rho^k}{1 - \rho} \|W_A^{(1)} - W_A^{(0)}\|_\infty$$

---

### 2.2 Empirical Simulation of Picard Iteration

We implemented a Monte Carlo Picard iteration test harness under the full Kou jump-diffusion SDE ($\sigma = 0.8986, \lambda = 2.4, p = 0.4, \eta_1 = 3.5, \eta_2 = 2.0, r = 0.035, q = 0.06$):

- **Empirical Affine Operator:** $\mathcal{T}(w) = 0.457920 + 0.550099 \cdot w$
- **Measured Contraction Modulus:** $\rho = 0.550099 < 1.0000$ (Strict Contraction)
- **Analytical Unique Fixed Point:** $W_A^*(0, 1.0) = \frac{0.457920}{1.0 - 0.550099} = \mathbf{1.017825}$
- **Picard Iteration Convergence:** Tested across 4 distinct initial guesses:
  - From $w^{(0)} = 0.0$: $w^{(15)} = 1.017695$ (error $1.30 \times 10^{-4}$)
  - From $w^{(0)} = 1.0$: $w^{(15)} = 1.017823$ (error $2.28 \times 10^{-6}$)
  - From $w^{(0)} = 2.0$: $w^{(15)} = 1.017951$ (error $1.26 \times 10^{-4}$)
  - From $w^{(0)} = 5.0$: $w^{(15)} = 1.018334$ (error $5.09 \times 10^{-4}$)
- **Observed Convergence Ratio:** $\frac{\|w^{(k+1)} - w^{(k)}\|}{\|w^{(k)} - w^{(k-1)}\|} = \mathbf{0.5501}$ identically at every iteration.

---

## 3. Merton vs Kou Solver Kernel Behavior & Boundary Forcing

### 3.1 Empirical Jump Density Tail Comparison

We compared the Kou asymmetric double-exponential density against the Merton log-normal density implemented in `pide_solver.py`:

| Log-Jump $y$ | Implied Price Drop | Kou Density $f_Y(y)$ | Merton Density $f_Y(y)$ | Ratio (Kou / Merton) | Risk Significance |
|:---:|:---:|:---:|:---:|:---:|:---|
| $-0.20$ | $-18.1\%$ | $0.804384$ | $2.007910$ | $0.40\times$ | Moderate shocks |
| $-0.50$ | $-39.3\%$ | $0.441455$ | $0.238703$ | $1.85\times$ | Heavy market plunge |
| $-0.80$ | $-55.1\%$ | $0.242276$ | $0.001764$ | $\mathbf{137.3\times}$ | Severe flash crash |
| $-1.00$ | $-63.2\%$ | $0.162402$ | $0.000014$ | $\mathbf{11,351.2\times}$ | Extreme Black Swan |
| $-1.50$ | $-77.7\%$ | $0.059744$ | $3.83 \times 10^{-13}$ | $\mathbf{1.56 \times 10^{11}\times}$ | Catastrophic collapse |

**Empirical Finding:** Merton's Gaussian tails decay as $\exp(-y^2)$, which effectively sets extreme crash probabilities to zero. Kou's power-law tails $\exp(\eta_2 y)$ capture realistic crypto flash crashes. Implementing Merton in `pide_solver.py` creates a serious tail-risk underestimation bug.

---

### 3.2 Audit of PIDE Solver Boundary Forcing in `pide_solver.py`
In `simulations/cadcad_core/mechanisms/pide_solver.py:116`:
```python
if S_i <= S_d or S_i >= S_u or i == 0 or i == N_S - 1:
    A[i] = 0.0
    B[i] = 1.0
    C[i] = 0.0
    RHS[i] = 1.0 + self.R * t_curr
```
The solver forces Dirichlet boundary conditions $1.0 + R t$ on all barrier boundaries. This turns par pricing $W_A(0, 1.0) \approx 1.0000$ into a trivial Dirichlet boundary reflection rather than solving the nonlocal fixed-point contraction.

---

## 4. Synthesis of Audit Register Challenges

We reviewed all 10 major discoveries and 12 contradictions in `SOURCE_AND_DERIVATION_AUDIT.md`:
1. **$\beta \cdot P_0$ Double-Counting Flapping (CONTRA-01):** CONFIRMED. $S = P_t / (\beta P_0)$ with moving $P_0$ squares the price ratio upon upward reset.
2. **TrancheSplitter 2:1 Token Bug (CONTRA-02):** CONFIRMED. Contract mints 1 $A'$ + 1 $B'$ from 1 $A$ instead of 2 $A$.
3. **Simulation Artifact 1.37% Volatility (CLM-001):** CONFIRMED. Zero noise in cadCAD loop; vol is linear coupon slope increment variance.
4. **Solvency Invariant Tautology (CLM-003):** CONFIRMED. Testing $|V_A + (2S - V_A) - 2S| \equiv 0$ measures floating-point subtraction, not vault solvency.
5. **Damping Ratio Contradiction (CLM-006):** CONFIRMED. $\zeta = 17.03$ vs $1.42$ plant contradiction; liquidity $L$ cancels out in `controller_isolation.py`.

---

## 5. Final Adversarial Recommendation & Verdict

- **Theorem 1 Single-Step Crash Bound:** Rigorously proven and correctly scoped in `SOURCE_AND_DERIVATION_AUDIT.md`.
- **Theorem 2 PIDE Banach Contraction Mapping:** Mathematically sound with verified geometric convergence modulus $\rho \approx 0.5501 < 1$.
- **Solver & Code Defect Identifications:** All reported implementation bugs and epistemic fallacies are empirically confirmed.

**Official Verdict:** **APPROVE**
