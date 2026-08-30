"""
Reflexer RAI-Inspired Control-Theoretic Dynamic Interest Rate Feedback Controller
Methodology: BlockScience "Summoning the Money God" & Classical Feedback Control Theory

Purpose:
Dynamically adjusts the anUSD benchmark coupon rate R'(t) based on secondary AMM peg error:
e(t) = P_DEX(t) - V_A'(t)

Control Law:
Delta_R'(t) = - ( K_p * e(t) + K_i * Integral(e(tau) dtau) + K_d * de/dt )
"""
from typing import Dict, Any, Tuple

class ReflexerPIDController:
    def __init__(self, K_p: float = 0.150, K_i: float = 0.020, K_d: float = 0.005, max_rate_adjustment: float = 0.050):
        self.K_p = K_p
        self.K_i = K_i
        self.K_d = K_d
        self.max_adj = max_rate_adjustment
        
        # State memory
        self.integral_error = 0.0
        self.prev_error = 0.0

    def reset(self):
        self.integral_error = 0.0
        self.prev_error = 0.0

    def compute_rate_modulation(self, P_DEX: float, V_A_prime: float, dt_years: float) -> Tuple[float, float, float]:
        """
        Calculates dynamic rate adjustment Delta_R'(t):
        Returns:
            modulated_R_prime: base_R_prime + Delta_R'
            Delta_R_prime: raw adjustment
            error: P_DEX - V_A_prime
        """
        error = P_DEX - V_A_prime
        
        # Integrate error with anti-windup clamping
        self.integral_error += error * dt_years
        self.integral_error = max(-0.10, min(0.10, self.integral_error))
        
        # Derivative error
        d_error = (error - self.prev_error) / max(1e-6, dt_years)
        self.prev_error = error
        
        # Proportional-Integral-Derivative Control Signal
        # If P_DEX < V_A_prime (error < 0), signal is POSITIVE => Increases anUSD yield R'
        # If P_DEX > V_A_prime (error > 0), signal is NEGATIVE => Decreases anUSD yield R'
        raw_control_signal = - (self.K_p * error + self.K_i * self.integral_error + self.K_d * d_error)
        
        # Clamp to max adjustment bounds
        clamped_adj = max(-self.max_adj, min(self.max_adj, raw_control_signal))
        
        return clamped_adj, error, self.integral_error

    def compute_system_damping_ratio(self, plant_gain_K: float = 1.20, plant_time_constant_tau: float = 0.05) -> float:
        """
        Calculates theoretical closed-loop damping ratio zeta:
        Characteristic polynomial: s^2 + (1/tau + K*Kp/tau) s + (K*Ki/tau) = 0
        2 * zeta * omega_n = (1 + K*Kp) / tau
        omega_n^2 = (K*Ki) / tau
        => zeta = (1 + K*Kp) / (2 * sqrt(K * Ki * tau))
        """
        omega_n = (plant_gain_K * self.K_i / plant_time_constant_tau) ** 0.5
        if omega_n <= 1e-6:
            return 1.0
        zeta = (1.0 + plant_gain_K * self.K_p) / (2.0 * (plant_gain_K * self.K_i * plant_time_constant_tau) ** 0.5)
        return zeta
