"""
Asset Price Simulation Engine: GBM, Merton Jump Diffusion, & Kou Jump Diffusion
"""
import numpy as np

def simulate_gbm(S0: float, mu: float, sigma: float, T: float, dt: float, paths: int = 1000, seed: int = 42) -> np.ndarray:
    """Simulates Geometric Brownian Motion price paths."""
    np.random.seed(seed)
    n_steps = int(T / dt)
    prices = np.zeros((n_steps + 1, paths))
    prices[0] = S0
    
    for t in range(1, n_steps + 1):
        z = np.random.standard_normal(paths)
        prices[t] = prices[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
        
    return prices

def simulate_kou_jump_diffusion(
    S0: float, r: float, sigma: float, lambda_jump: float,
    p_up: float, eta1: float, eta2: float, T: float, dt: float,
    paths: int = 1000, seed: int = 42
) -> np.ndarray:
    """
    Simulates Kou Double Exponential Jump-Diffusion process.
    - lambda_jump: Jump intensity
    - p_up: Probability of positive jump
    - eta1: Decay parameter for positive jumps (>1)
    - eta2: Decay parameter for negative jumps (>0)
    """
    np.random.seed(seed)
    n_steps = int(T / dt)
    prices = np.zeros((n_steps + 1, paths))
    prices[0] = S0
    
    # Expected jump size E[e^Y - 1]
    zeta = p_up * (eta1 / (eta1 - 1)) + (1 - p_up) * (eta2 / (eta2 + 1)) - 1
    drift = (r - 0.5 * sigma**2 - lambda_jump * zeta) * dt
    vol = sigma * np.sqrt(dt)
    
    for t in range(1, n_steps + 1):
        z = np.random.standard_normal(paths)
        n_jumps = np.random.poisson(lambda_jump * dt, paths)
        
        jump_factors = np.zeros(paths)
        for i in range(paths):
            if n_jumps[i] > 0:
                jumps = np.zeros(n_jumps[i])
                for j in range(n_jumps[i]):
                    if np.random.rand() < p_up:
                        jumps[j] = np.random.exponential(1.0 / eta1)
                    else:
                        jumps[j] = -np.random.exponential(1.0 / eta2)
                jump_factors[i] = np.sum(jumps)
                
        prices[t] = prices[t-1] * np.exp(drift + vol * z + jump_factors)
        
    return prices

if __name__ == "__main__":
    prices = simulate_kou_jump_diffusion(
        S0=25.0, r=0.05, sigma=0.70, lambda_jump=2.0,
        p_up=0.4, eta1=4.0, eta2=2.5, T=1.0, dt=1/365, paths=5
    )
    print(f"Sample price paths generated: Shape={prices.shape}, Final mean=${np.mean(prices[-1]):.2f}")
