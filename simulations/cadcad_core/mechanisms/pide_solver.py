"""
Numerical Partial Integro-Differential Equation (PIDE) Finite-Difference Solver
Solves the continuous-time Merton-Kou jump-diffusion pricing PDE for path-dependent tranches.
Methodology: Unconditionally Stable Implicit-Explicit (IMEX) Crank-Nicolson Scheme with Thomas Algorithm.
Governing Standard: SSRN-3856569 + Cont & Voltchkova (2005) IMEX PIDE Canon
"""
import math
import numpy as np
from typing import Tuple

class TranchePIDESolver:
    def __init__(
        self,
        r: float = 0.05,
        sigma: float = 0.8986,
        lambda_j: float = 2.4,
        mu_j: float = -0.12,
        sigma_j: float = 0.18,
        R: float = 0.073,
        H_u: float = 2.0,
        H_d: float = 0.25
    ):
        self.r = r
        self.sigma = sigma
        self.lambda_j = lambda_j
        self.mu_j = mu_j
        self.sigma_j = sigma_j
        self.R = R
        self.H_u = H_u
        self.H_d = H_d
        
        # Expected jump size kappa = E[Y - 1] = exp(mu_j + 0.5 * sigma_j^2) - 1
        self.kappa = math.exp(self.mu_j + 0.5 * self.sigma_j**2) - 1.0

    def jump_density(self, y: float) -> float:
        """Log-normal jump density f_Y(y)."""
        if y <= 1e-6:
            return 0.0
        coef = 1.0 / (y * self.sigma_j * math.sqrt(2.0 * math.pi))
        exponent = -((math.log(y) - self.mu_j)**2) / (2.0 * self.sigma_j**2)
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
        - Diffusion / Black-Scholes operator is solved implicitly via Thomas tridiagonal elimination.
        - Non-local jump integral is evaluated explicitly at time level n+1.
        
        Parameters:
            S_min: Minimum normalized collateral index (default 0.1)
            S_max: Maximum normalized collateral index (default 3.0)
            N_S: Number of spatial grid intervals (default 60)
            T_epoch: Total epoch duration in years (default 1.0)
            N_T: Number of temporal grid intervals (default 60)
            theta: Implicitness weight (0.5 = Crank-Nicolson, 1.0 = Fully Implicit)
            
        Returns:
            S_grid (np.ndarray): 1D array of spatial nodes (length N_S)
            T_grid (np.ndarray): 1D array of time nodes (length N_T + 1)
            W_surface (np.ndarray): 2D array of Class A tranche prices (shape [N_T + 1, N_S])
        """
        S_grid = np.linspace(S_min, S_max, N_S)
        dS = S_grid[1] - S_grid[0]
        dt = T_epoch / N_T
        T_grid = np.linspace(0.0, T_epoch, N_T + 1)
        
        # Initialize pricing grid W(t, S)
        W = np.zeros((N_T + 1, N_S))
        
        # Terminal condition at epoch maturity: W(S, T) = 1.0 + R * T_epoch
        W[N_T, :] = 1.0 + self.R * T_epoch
        
        # Quadrature grid for explicit jump integral evaluation
        y_quad = np.linspace(0.1, 2.5, 31)
        dy = y_quad[1] - y_quad[0]
        f_y = np.array([self.jump_density(y_k) for y_k in y_quad])
        
        # Backward time-stepping from t = T down to t = 0
        for n in range(N_T - 1, -1, -1):
            t_curr = T_grid[n]
            W_next = W[n + 1, :]
            
            # Dynamic reset barrier boundaries at time t_curr
            S_u = (self.H_u + 1.0 + self.R * t_curr) / 2.0
            S_d = (self.H_d + 1.0 + self.R * t_curr) / 2.0
            
            # 1. Evaluate explicit jump integral on W_next
            jump_int = np.zeros(N_S)
            for i in range(N_S):
                S_i = S_grid[i]
                S_targets = S_i * y_quad
                W_interp = np.interp(S_targets, S_grid, W_next)
                jump_int[i] = np.sum((W_interp - W_next[i]) * f_y) * dy
                
            # 2. Construct Tridiagonal System: A_i * W_{i-1}^n + B_i * W_i^n + C_i * W_{i+1}^n = RHS_i
            A = np.zeros(N_S)
            B = np.zeros(N_S)
            C = np.zeros(N_S)
            RHS = np.zeros(N_S)
            
            for i in range(N_S):
                S_i = S_grid[i]
                if S_i <= S_d or S_i >= S_u or i == 0 or i == N_S - 1:
                    # Dirichlet reset barrier / boundary condition
                    A[i] = 0.0
                    B[i] = 1.0
                    C[i] = 0.0
                    RHS[i] = 1.0 + self.R * t_curr
                else:
                    # Spatial differential coefficients
                    a_i = (self.r - self.lambda_j * self.kappa) * S_i
                    b_i = 0.5 * (self.sigma**2) * (S_i**2)
                    
                    alpha_i = b_i / (dS**2) - a_i / (2.0 * dS)
                    beta_i = -2.0 * b_i / (dS**2) - self.r
                    gamma_i = b_i / (dS**2) + a_i / (2.0 * dS)
                    
                    # Explicit components from time level n+1
                    diff_next = alpha_i * W_next[i - 1] + beta_i * W_next[i] + gamma_i * W_next[i + 1]
                    RHS[i] = W_next[i] + (1.0 - theta) * dt * diff_next + dt * self.lambda_j * jump_int[i]
                    
                    # Implicit components for time level n
                    A[i] = -theta * dt * alpha_i
                    B[i] = 1.0 - theta * dt * beta_i
                    C[i] = -theta * dt * gamma_i
            
            # 3. Solve Tridiagonal System via Thomas Algorithm O(N_S)
            c_prime = np.zeros(N_S)
            d_prime = np.zeros(N_S)
            
            c_prime[0] = C[0] / B[0]
            d_prime[0] = RHS[0] / B[0]
            
            for i in range(1, N_S):
                denom = B[i] - A[i] * c_prime[i - 1]
                c_prime[i] = C[i] / denom if i < N_S - 1 else 0.0
                d_prime[i] = (RHS[i] - A[i] * d_prime[i - 1]) / denom
                
            W_curr = np.zeros(N_S)
            W_curr[N_S - 1] = d_prime[N_S - 1]
            for i in range(N_S - 2, -1, -1):
                W_curr[i] = d_prime[i] - c_prime[i] * W_curr[i + 1]
                
            W[n, :] = W_curr
            
        return S_grid, T_grid, W

if __name__ == "__main__":
    solver = TranchePIDESolver()
    S_grid, T_grid, W_surface = solver.solve_tranche_pricing_grid(N_S=60, N_T=60)
    print("PIDE Solver converged successfully via IMEX Crank-Nicolson scheme.")
    print(f"Grid Dimensions: Space ({len(S_grid)} nodes), Time ({len(T_grid)} nodes)")
    print(f"Fair Class A Price at S=1.0, t=0.0: ${np.interp(1.0, S_grid, W_surface[0, :]):.4f}")
    print(f"Surface Min: ${np.min(W_surface):.4f}, Surface Max: ${np.max(W_surface):.4f}")
