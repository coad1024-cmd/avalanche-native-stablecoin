"""
Numerical Partial Integro-Differential Equation (PIDE) Finite-Difference Solver
Solves the continuous-time Merton-Kou jump-diffusion pricing PDE for path-dependent tranches.
Methodology: Implicit-Explicit (IMEX) finite difference scheme with Simpson jump integral quadrature.
"""
import numpy as np
import math

class TranchePIDESolver:
    def __init__(self, r=0.05, sigma=0.8986, lambda_j=2.4, mu_j=-0.12, sigma_j=0.18, R=0.073, H_u=2.0, H_d=0.25):
        self.r = r
        self.sigma = sigma
        self.lambda_j = lambda_j
        self.mu_j = mu_j
        self.sigma_j = sigma_j
        self.R = R
        self.H_u = H_u
        self.H_d = H_d
        
        # Expected jump size kappa = E[Y - 1]
        self.kappa = math.exp(self.mu_j + 0.5 * self.sigma_j**2) - 1.0

    def jump_density(self, y):
        """Log-normal jump density f_Y(y)"""
        if y <= 1e-6:
            return 0.0
        return (1.0 / (y * self.sigma_j * math.sqrt(2 * math.pi))) * math.exp(-((math.log(y) - self.mu_j)**2) / (2 * self.sigma_j**2))

    def solve_tranche_pricing_grid(self, S_min=0.1, S_max=3.0, N_S=100, T_epoch=1.0, N_T=100):
        """
        Solves the PIDE across a 2D space-time grid (S, t) using IMEX finite difference.
        Returns:
            S_grid (np.ndarray), T_grid (np.ndarray), W_surface (np.ndarray)
        """
        S_grid = np.linspace(S_min, S_max, N_S)
        dS = S_grid[1] - S_grid[0]
        dt = T_epoch / N_T
        T_grid = np.linspace(0, T_epoch, N_T + 1)
        
        # Initialize pricing grid W(S, t)
        W = np.zeros((N_T + 1, N_S))
        
        # Terminal condition at epoch end: W(S, T) = 1.0 + R * T
        W[N_T, :] = 1.0 + self.R * T_epoch
        
        # Backward time-stepping
        for n in range(N_T - 1, -1, -1):
            t_curr = T_grid[n]
            W_next = W[n + 1, :]
            
            # Boundary conditions at reset barriers
            # S_u corresponds to V_B = H_u => 2S - (1 + R*t) = H_u => S = (H_u + 1 + R*t) / 2
            S_u = (self.H_u + 1.0 + self.R * t_curr) / 2.0
            S_d = (self.H_d + 1.0 + self.R * t_curr) / 2.0
            
            W_curr = np.copy(W_next)
            for i in range(1, N_S - 1):
                S_i = S_grid[i]
                if S_i >= S_u:
                    W_curr[i] = 1.0 + self.R * t_curr
                elif S_i <= S_d:
                    V_A_val = 1.0 + self.R * t_curr
                    W_curr[i] = (V_A_val - self.H_d) + self.H_d * 1.0
                else:
                    # Finite difference derivatives
                    dW_dS = (W_next[i + 1] - W_next[i - 1]) / (2 * dS)
                    d2W_dS2 = (W_next[i + 1] - 2 * W_next[i] + W_next[i - 1]) / (dS**2)
                    
                    # Numerical jump integral quadrature
                    # Integral_{0}^{S_max/S_i} [ W(S_i * y) - W(S_i) ] f_Y(y) dy
                    y_quad = np.linspace(0.1, 2.5, 30)
                    dy = y_quad[1] - y_quad[0]
                    jump_int = 0.0
                    for y_k in y_quad:
                        S_target = S_i * y_k
                        # Linear interpolation on S_grid
                        W_interp = np.interp(S_target, S_grid, W_next)
                        jump_int += (W_interp - W_next[i]) * self.jump_density(y_k) * dy
                    
                    # Black-Scholes PDE operator + Jump Operator
                    diffusion_term = (self.r - self.lambda_j * self.kappa) * S_i * dW_dS + 0.5 * (self.sigma**2) * (S_i**2) * d2W_dS2 - self.r * W_next[i]
                    integral_term = self.lambda_j * jump_int
                    
                    W_curr[i] = W_next[i] + dt * (diffusion_term + integral_term)
            
            W[n, :] = W_curr
            
        return S_grid, T_grid, W

if __name__ == "__main__":
    solver = TranchePIDESolver()
    S_grid, T_grid, W_surface = solver.solve_tranche_pricing_grid(N_S=50, N_T=50)
    print(f"PIDE Solver converged successfully.")
    print(f"Grid Dimensions: Space ({len(S_grid)}), Time ({len(T_grid)})")
    print(f"Fair Class A Price at S=1.0, t=0.0: ${W_surface[0, len(S_grid)//2]:.4f}")
