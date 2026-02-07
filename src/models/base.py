from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class StochasticModel(ABC):
    """
    Interfaz Abstracta (Strategy Interface)
    Define el contrato que todos los modelos matemáticos deben cumplir.
    Cumple con el Principio de Inversión de Dependencias (DIP).
    """

    @abstractmethod
    def train(self, log_returns: pd.DataFrame):
        """
        Calibra el modelo usando datos históricos.
        Ej: Calcular matriz de covarianza, nu, mu, sigma.
        """
        pass

    @abstractmethod
    def simulate(self, initial_prices: np.ndarray, horizon: int, n_sims: int) -> np.ndarray:
        """
        Genera trayectorias de precios futuras.
        Debe retornar un array 3D: (n_sims, days, n_assets)
        """
        pass