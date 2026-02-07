import numpy as np
import pandas as pd
from src.models.base import StochasticModel

class MonteCarloEngine:
    def __init__(self, strategy: StochasticModel):
        """
        Motor de Riesgo Agnóstico (Contexto del Patrón Strategy).
        No sabe matemáticas, solo sabe ejecutar estrategias.
        
        Args:
            strategy (StochasticModel): Una instancia de una estrategia (ej. StudentTStrategy)
        """
        self.strategy = strategy
        self.simulations = None

    def train(self, log_returns: pd.DataFrame):
        """Delega el entrenamiento a la estrategia."""
        self.strategy.train(log_returns)

    def simulate(self, current_prices: np.ndarray, horizon: int = 252, n_sims: int = 1000):        
        """
        Orquesta la simulación delegando en la estrategia.
        Ahora recibe horizon y n_sims aquí, no en el __init__.
        """
        print(f"🎲 [Engine] Iniciando simulación ({n_sims} sims, {horizon} días)...")
        
        # Dalega la matemática compleja a la estrategia
        self.simulations = self.strategy.simulate(current_prices, horizon, n_sims)
        
        print("✅ [Engine] Simulación finalizada.")
        return self.simulations