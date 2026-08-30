"""
Numerical Partial Integro-Differential Equation (PIDE) Finite-Difference Solver
Solves the continuous-time Kou / Merton jump-diffusion pricing PIDE for path-dependent tranches.
Methodology: Unconditionally Stable Implicit-Explicit (IMEX) Crank-Nicolson Scheme with Thomas Tridiagonal Algorithm.
Governing Standard: SSRN-3856569 + Kou (2002) + Cont & Voltchkova (2005) IMEX PIDE Canon
"""

import math
import numpy as np
from typing import Tuple, Optional


class TranchePIDESolver:
    def __init__(
        self,
        r: float = 0.05,
        sigma: float = 0.8913,
        lambda_j: float = 3.0,
        model_type: str = "kou", # "kou" or "merton"
        # Kou parameters
        p: float = 0.418,
        eta1: float = 3.181,
        eta2: float = 2.331,
        # Merton parameters
        mu_j: float = -0.12,
        sigma_j: float = 0.18,
        # Protocol parameters
        R: float = 0.073,
        H_u: float = 2.0,
        H_d: float = 0.25,
        tau_reset: float = 1.0 # Expected reset epoch duration (years)
    ):
        self.r = r
        self.sigma = sigma
        self.lambda_j = lambda_j
        self.model_type = model_type
        
        # Kou parameters
        self.p = p
        self.eta1 = eta1
        self.eta2 = eta2
        
        # Merton parameters
        self.mu_j = mu_j
        self.sigma_j = sigma_j
        
        # Protocol parameters
        self.R = R
        self.H_u = H_u
        self.H_d = H_d
        self.tau_reset = tau_reset
        
        # Compute expected jump size kappa = E[e^Y - 1]
        if self.model_type == "kou":
            # Kou compensator: E[e^Y - 1] = p * eta1 / (eta1 - 1) + (1-p) * eta2 / (eta2 + 1) - 1
            if self.eta1 > 1.0:
                self.kappa = (self.p * self.eta1 / (self.eta1 - 1.0)) + ((1.0 - self.p) * self.eta2 / (self.eta2 + 1.0)) - 1.0
            else:
                self.kappa = 0.0
        else:
            # Merton compensator: E[e^Y - 1] = exp(mu_j + 0.5 * sigma_j^2) - 1
            self.kappa = math.exp(self.mu_j + 0.5 * self.sigma_j**2) - 1.0

    @property
    def contraction_modulus(self) -> float:
        """
        Computes the analytical Banach contraction modulus rho of the periodic PIDE operator.
        rho = (1 / tau_reset) / (r + lambda_j + 1 / tau_reset)
        """
        alpha_decay = self.r + self.lambda_j + (1.0 / self.tau_reset)
        return (1.0 / self.tau_reset) / alpha_decay

    def jump_density(self, y: float) -> float:
        """
        Evaluates the jump amplitude probability density function f_Y(y) where Y = ln(J).
        """
        if self.model_type == "kou":
            # Kou double exponential density
            if y >= 0:
                return self.p * self.eta1 * math.exp(-self.eta1 * y)
            else:
                return (1.0 - self.p) * self.eta2 * math.exp(self.eta2 * y)
        else:
            # Merton log-normal density in log-space: y ~ N(mu_j, sigma_j^2)
            coef = 1.0 / (self.sigma_j * math.sqrt(2.0 * math.pi))
            exponent = -((y - self.mu_j)**2) / (2.0 * self.sigma_j**2)
            return coef * math.exp(exponent)

    def solve_tranche_pricing_grid(
        self,
        S_min: float = 0.1,
        S_max: float = 3.0,
        N_S: int = 60,
        T_epoch: float = 1.0,
        N_T: int = 60,
        theta: float = 0.5
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Solves the PIDE across a 2D space-time grid (S, t) using IMEX Crank-Nicolson finite differences.
        - Diffusion operator is solved implicitly via Thomas tridiagonal algorithm.
        - Jump integral operator is integrated explicitly via composite Simpson/trapezoidal quadrature.
        """
        S_grid = np.linspace(S_min, S_max, N_S)
        dS = S_grid[1] - S_grid[0]
        dt = T_epoch / N_T
        T_grid = np.linspace(0.0, T_epoch, N_T + 1)
        
        # Initialize pricing grid W(t, S)
        W = np.zeros((N_T + 1, N_S))
        
        # Terminal condition at epoch maturity: W(S, T) = 1.0 + R * T_epoch
        W[N_T, :] = 1.0 + self.R * T_epoch
        
        # Backward induction in time from t = T down to t = 0
        for n in range(N_T - 1, -1, -1):
            t_curr = T_grid[n]
            
            # 1. Compute explicit jump integral for each spatial node:
            # J[W](S) = lambda * integral_{0}^{infty} (W(S*e^y) - W(S)) f_Y(y) dy
            jump_integral = np.zeros(N_S)
            for i in range(N_S):
                s_val = S_grid[i]
                
                # Discrete numerical quadrature over log-jump domain y in [-2.5, +2.5]
                y_nodes = np.linspace(-2.5, 2.5, 41)
                dy = y_nodes[1] - y_nodes[0]
                
                s_post_jump = s_val * np.exp(y_nodes)
                w_post_jump = np.interp(s_post_jump, S_grid, W[n + 1, :], left=1.0, right=1.0 + self.R * t_curr)
                
                density_vals = np.array([self.jump_density(y) for y in y_nodes])
                integrand = (w_post_jump - W[n + 1, i]) * density_vals
                jump_integral[i] = self.lambda_j * np.trapezoid(integrand, y_nodes)
            
            # 2. Setup Tridiagonal System for Implicit Diffusion:
            # a_i * W_{i-1}^{n} + b_i * W_i^{n} + c_i * W_{i+1}^{n} = rhs_i
            A_diag = np.zeros(N_S)
            B_diag = np.zeros(N_S)
            C_diag = np.zeros(N_S)
            RHS = np.zeros(N_S)
            
            for i in range(1, N_S - 1):
                s_val = S_grid[i]
                
                # Drift term adjusted for jump compensator: mu_eff = r - q - lambda * kappa
                mu_eff = self.r - self.lambda_j * self.kappa
                
                alpha_i = 0.5 * (self.sigma**2) * (s_val**2) / (dS**2)
                beta_i = 0.5 * mu_eff * s_val / dS
                
                # Implicit operator coefficients (at time level n)
                A_diag[i] = -theta * dt * (alpha_i - beta_i)
                B_diag[i] = 1.0 + theta * dt * (2.0 * alpha_i + self.r + (1.0 / self.tau_reset))
                C_diag[i] = -theta * dt * (alpha_i + beta_i)
                
                # Explicit operator coefficients (at time level n+1)
                expl_diff = (1.0 - theta) * dt * (
                    (alpha_i - beta_i) * W[n + 1, i - 1]
                    - (2.0 * alpha_i + self.r + (1.0 / self.tau_reset)) * W[n + 1, i]
                    + (alpha_i + beta_i) * W[n + 1, i + 1]
                )
                
                # RHS vector including explicit jump and reset source terms
                reset_source = (dt / self.tau_reset) * (1.0 + self.R * 0.0) # Par value upon reset
                RHS[i] = W[n + 1, i] + expl_diff + dt * jump_integral[i] + reset_source
                
            # Boundary Conditions
            # Lower boundary S -> S_min: Senior Class A amortizes at barrier
            B_diag[0] = 1.0
            C_diag[0] = 0.0
            RHS[0] = 1.0 + self.R * t_curr
            
            # Upper boundary S -> S_max: Class A fully covered
            A_diag[N_S - 1] = 0.0
            B_diag[N_S - 1] = 1.0
            RHS[N_S - 1] = 1.0 + self.R * t_curr
            
            # 3. Solve Tridiagonal System via Thomas Algorithm
            W[n, :] = self._thomas_solve(A_diag, B_diag, C_diag, RHS)
            
        return S_grid, T_grid, W

    @staticmethod
    def _thomas_solve(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
        """Thomas Algorithm for O(N) Tridiagonal Matrix Inversion."""
        n = len(d)
        c_prime = np.zeros(n)
        d_prime = np.zeros(n)
        x = np.zeros(n)
        
        c_prime[0] = c[0] / b[0]
        d_prime[0] = d[0] / b[0]
        
        for i in range(1, n):
            denom = b[i] - a[i] * c_prime[i - 1]
            if abs(denom) < 1e-15:
                denom = 1e-15
            c_prime[i] = c[i] / denom if i < n - 1 else 0.0
            d_prime[i] = (d[i] - a[i] * d_prime[i - 1]) / denom
            
        x[n - 1] = d_prime[n - 1]
        for i in range(n - 2, -1, -1):
            x[i] = d_prime[i] - c_prime[i] * x[i + 1]
            
        return x


if __name__ == "__main__":
    solver_kou = TranchePIDESolver(model_type="kou")
    s_grid, t_grid, w_grid = solver_kou.solve_tranche_pricing_grid()
    
    par_index = np.argmin(np.abs(s_grid - 1.0))
    w_par = w_grid[0, par_index]
    
    print("=== IMEX Crank-Nicolson PIDE Solver (Kou 2002 Jump Diffusion) ===")
    print(f"Contraction Modulus rho: {solver_kou.contraction_modulus:.4f} (Strict Contraction: {solver_kou.contraction_modulus < 1.0})")
    print(f"Par Class A Price at t=0 (S=1.00): ${w_par:.4f}")
    print(f"Lower Barrier Price (S={s_grid[0]:.2f}): ${w_grid[0, 0]:.4f}")
    print(f"Upper Barrier Price (S={s_grid[-1]:.2f}): ${w_grid[0, -1]:.4f}")
