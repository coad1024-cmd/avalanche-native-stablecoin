"""
Global Sensitivity Analysis (GSA) Engine: Sobol Variance Decomposition & Morris Screening
Governing Standard: BCRG Mathematical Canon & Saltelli (2002/2008) Sampling Method
"""
from typing import Dict, Any, List, Tuple, Callable
import numpy as np
import pandas as pd
from scipy.stats import qmc

def generate_saltelli_samples(
    param_bounds: Dict[str, Tuple[float, float]],
    N_base: int = 512,
    seed: int = 42
) -> Tuple[np.ndarray, List[str]]:
    """
    Generates Saltelli sampling matrix for N_params parameters.
    Total sample size = N_base * (2 * D + 2) where D = num_params.
    """
    param_names = list(param_bounds.keys())
    D = len(param_names)
    
    # Generate two independent Sobol sequences of size (N_base, D)
    sampler = qmc.Sobol(d=2*D, seed=seed)
    sobol_raw = sampler.random(n=N_base)
    
    A = sobol_raw[:, :D]
    B = sobol_raw[:, D:]
    
    # Scale to physical parameter bounds
    lower_bounds = np.array([param_bounds[p][0] for p in param_names])
    upper_bounds = np.array([param_bounds[p][1] for p in param_names])
    
    A_scaled = lower_bounds + A * (upper_bounds - lower_bounds)
    B_scaled = lower_bounds + B * (upper_bounds - lower_bounds)
    
    # Construct Saltelli matrix: A, B, and A_B^(i) matrices
    all_samples = [A_scaled, B_scaled]
    
    for i in range(D):
        AB_i = np.copy(A_scaled)
        AB_i[:, i] = B_scaled[:, i]
        all_samples.append(AB_i)
        
    for i in range(D):
        BA_i = np.copy(B_scaled)
        BA_i[:, i] = A_scaled[:, i]
        all_samples.append(BA_i)
        
    sample_matrix = np.vstack(all_samples)
    return sample_matrix, param_names

def compute_sobol_indices(
    Y_evals: np.ndarray,
    N_base: int,
    D: int,
    param_names: List[str]
) -> pd.DataFrame:
    """
    Computes First-Order (S_i) and Total-Order (S_Ti) Sobol Sensitivity Indices.
    """
    # Split evaluations into A, B, AB_i, BA_i
    y_A = Y_evals[:N_base]
    y_B = Y_evals[N_base:2*N_base]
    
    var_total = np.var(np.concatenate([y_A, y_B]))
    if var_total < 1e-12:
        # Zero variance -> all indices zero
        return pd.DataFrame({
            "parameter": param_names,
            "first_order_Si": np.zeros(D),
            "total_order_STi": np.zeros(D),
            "interaction_effect": np.zeros(D)
        })
        
    S_i = np.zeros(D)
    S_Ti = np.zeros(D)
    
    for i in range(D):
        y_AB_i = Y_evals[(2 + i)*N_base : (3 + i)*N_base]
        
        # First-order index formula: S_i = ( (1/N) sum(y_A * y_AB_i) - (E[y])^2 ) / Var(y)
        f_0_sq = np.mean(y_A) * np.mean(y_B)
        v_i = np.mean(y_B * (y_AB_i - y_A))
        S_i[i] = max(0.0, min(1.0, (np.mean(y_A * y_AB_i) - f_0_sq) / var_total))
        
        # Total-order index formula: S_Ti = ( (1/(2N)) sum( (y_A - y_AB_i)^2 ) ) / Var(y)
        S_Ti[i] = max(S_i[i], min(1.5, np.mean((y_A - y_AB_i)**2) / (2.0 * var_total)))
        
    df_sobol = pd.DataFrame({
        "parameter": param_names,
        "first_order_Si": S_i,
        "total_order_STi": S_Ti,
        "interaction_effect": np.maximum(0.0, S_Ti - S_i)
    })
    
    df_sobol = df_sobol.sort_values(by="total_order_STi", ascending=False).reset_index(drop=True)
    return df_sobol
