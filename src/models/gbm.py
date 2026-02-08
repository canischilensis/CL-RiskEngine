import numpy as np
import pandas as pd
from src.models.base import StochasticModel

class GeometricBrownianMotionStrategy(StochasticModel):
    """
    Estrategia Clásica: Movimiento Browniano Geométrico (GBM).
    Asume que los retornos siguen una Distribución Normal Multivariada.
    """
    def __init__(self):
        self.mu = None
        self.chol_matrix = None
        self.n_assets = None

    def train(self, log_returns: pd.DataFrame):
        """
        Calibra mu (drift) y Sigma (covarianza) bajo supuestos normales.
        """
        self.n_assets = log_returns.shape[1]
        
        # 1. Vector de Medias (Drift Anualizado no necesario para paso diario, pero guardamos diario)
        self.mu = log_returns.mean().values
        
        # 2. Matriz de Covarianza
        cov_matrix = log_returns.cov().values
        
        # 3. Descomposición de Cholesky para correlaciones
        try:
            self.chol_matrix = np.linalg.cholesky(cov_matrix)
        except np.linalg.LinAlgError:
            # Regularización en caso de matriz no definida positiva
            cov_matrix += np.eye(self.n_assets) * 1e-6
            self.chol_matrix = np.linalg.cholesky(cov_matrix)
            
        print(f"🧠 [GBM] Modelo Normal calibrado (Sin colas pesadas).")

    def simulate(self, initial_prices: np.ndarray, horizon: int, n_sims: int) -> np.ndarray:
        if self.chol_matrix is None:
            raise ValueError("Modelo no entrenado.")

        # 1. Generar Shocks Normales Estándar Z ~ N(0, I)
        Z = np.random.normal(0, 1, size=(horizon, n_sims, self.n_assets))
        
        # 2. Inducir Correlación: X = Z * L^T
        correlated_shocks = np.einsum('tsa,ba->tsb', Z, self.chol_matrix)
        
        # 3. Trayectorias de Precio (Solución exacta de la EDO de Black-Scholes)
        # S_t = S_{t-1} * exp( (mu - 0.5*sigma^2)dt + sigma*dW )
        
        sigma_sq = np.diag(self.chol_matrix @ self.chol_matrix.T)
        drift = self.mu - 0.5 * sigma_sq
        
        # Difusión
        log_returns = (drift * 1) + correlated_shocks
        cumulative_returns = np.cumsum(log_returns, axis=0)
        
        # Construir matriz final
        simulations = np.zeros((horizon + 1, n_sims, self.n_assets))
        simulations[0] = initial_prices
        simulations[1:] = initial_prices * np.exp(cumulative_returns)
        
        return np.transpose(simulations[1:], (1, 0, 2))