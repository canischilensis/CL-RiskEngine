import numpy as np
import pandas as pd
from scipy.stats import t
from src.models.base import StochasticModel

class StudentTStrategy(StochasticModel):
    """
    Estrategia Concreta: Monte Carlo con Cópula t-Student.
    """
    def __init__(self):
        self.mu = None
        self.chol_matrix = None
        self.nu = None
        self.n_assets = None

    def train(self, log_returns: pd.DataFrame):
        self.n_assets = log_returns.shape[1]
        nus = []
        for col in log_returns.columns:
            try:
                params = t.fit(log_returns[col])
                nus.append(params[2])
            except:
                nus.append(4.0) # Fallback conservador
        raw_nu = np.mean(nus)

        # === 🛡️ FIX DE SEGURIDAD (CLAMPING) 🛡️ ===
        # Limitamos Nu entre 2.5 (Colas muy gordas) y 30 (Casi normal)
        # Esto evita explosiones numéricas e infinitos.
        self.nu = np.clip(raw_nu, 2.5, 30.0)
        self.mu = log_returns.mean().values
        cov_matrix = log_returns.cov().values
        try:
            self.chol_matrix = np.linalg.cholesky(cov_matrix)
        except np.linalg.LinAlgError:
            print("⚠️ Advertencia: Regularizando matriz de covarianza.")
            cov_matrix += np.eye(self.n_assets) * 1e-6
            self.chol_matrix = np.linalg.cholesky(cov_matrix)
        print(f"🧠 [Strategy] Modelo t-Student calibrado. Nu promedio: {self.nu:.2f}")

    def simulate(self, initial_prices: np.ndarray, horizon: int, n_sims: int) -> np.ndarray:
        if self.chol_matrix is None:
            raise ValueError("El modelo no ha sido entrenado. Ejecute .train() primero.")
            
        # 1. Shocks
        Z = np.random.normal(0, 1, size=(horizon, n_sims, self.n_assets))
        W = np.random.chisquare(self.nu, size=(horizon, n_sims, 1)) / self.nu
        T_shocks = Z / np.sqrt(W)
        
        # 2. Correlación
        correlated_shocks = np.einsum('tsa,ba->tsb', T_shocks, self.chol_matrix)

        # 3. Trayectorias
        simulations = np.zeros((horizon + 1, n_sims, self.n_assets))
        simulations[0] = initial_prices
        
        sigma_sq = np.diag(self.chol_matrix @ self.chol_matrix.T)
        drift = self.mu - 0.5 * sigma_sq
        
        log_returns = (drift * 1) + correlated_shocks
        cumulative_returns = np.cumsum(log_returns, axis=0)
        simulations[1:] = initial_prices * np.exp(cumulative_returns)
        
        return np.transpose(simulations[1:], (1, 0, 2))