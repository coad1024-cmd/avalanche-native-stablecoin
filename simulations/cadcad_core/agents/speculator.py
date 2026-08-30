"""
Behavioral Agent Archetype: Leveraged Class B Speculator
Role: Adjusts demand for subordinated Class B equity based on real-time leverage Lambda_B and price momentum.
"""

class SpeculatorAgent:
    def __init__(self, eta_L: float = 0.40, eta_P: float = 0.25):
        self.eta_L = eta_L
        self.eta_P = eta_P

    def evaluate_speculator_demand_factor(
        self,
        current_leverage: float,
        spot_momentum: float,
        V_B: float
    ) -> float:
        """
        Calculates demand scaling factor for Class B tokens:
        - Higher leverage (Lambda_B > 2.0) increases demand if market momentum is positive
        - If V_B approaches downward barrier (H_d), speculators scale down exposure due to reverse split fear
        """
        if V_B <= 0.30:
            # Downward barrier fear discount
            fear_penalty = max(0.20, (V_B - 0.25) / 0.05)
        else:
            fear_penalty = 1.0
            
        leverage_signal = 1.0 + self.eta_L * (current_leverage - 2.0)
        momentum_signal = 1.0 + self.eta_P * spot_momentum
        
        demand_factor = leverage_signal * momentum_signal * fear_penalty
        return max(0.10, min(demand_factor, 3.0))
