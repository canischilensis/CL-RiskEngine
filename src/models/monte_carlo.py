import numpy as np
import pandas as pd
from scipy import stats

class MonteCarloEngine:
    def __init__(self, n_sims, horizon, seed=42):
        """
        Configurar el motor.
        n_sims: Cuántos universos paralelos vamos a crear (ej. 10,000).
        horizon: Cuántos días al futuro vamos a ver (ej. 252).
        seed: Pa que los resultados sean reproducibles si corremos de nuevo.
        """
        self.n_sims = n_sims
        self.horizon = horizon
        self.seed = seed
        self.mu = None      # Promedio de retornos
        self.cov = None     # Matriz de covarianza
        self.nu = None      # Grados de libertad (t-Student)
        self.dt = 1         # Paso de tiempo (1 día)

    def train(self, log_returns):
        """
        Aprender del pasao.
        Calculamos la media, la covarianza y estimamos qué tan 'gordas' son las colas.
        """
        print("🧠 Entrenando modelo estadístico...")
        
        # 1. Calcular media y covarianza de los retornos logarítmicos
        self.mu = log_returns.mean().values
        self.cov = log_returns.cov().values
        
        # 2. Estimar parámetros de t-Student (Nu)
        # Pa simplificar, sacamos un promedio de los Nu de cada activo
        nus = []
        for col in log_returns.columns:
            # Ajustamos una t-student a cada serie
            params = stats.t.fit(log_returns[col])
            nus.append(params[0]) # El primer param es Nu (df)
        
        self.nu = np.mean(nus)
        print(f"✅ Modelo entrenao. Nu promedio (grosor de colas): {self.nu:.2f}")

    def simulate(self, S0):
        """
        Correr la simulación Monte Carlo Estructurada.
        S0: Precios iniciales (los de hoy).
        """
        if self.mu is None:
            raise ValueError("⚠️ Entrena el modelo primero con .train()")
        
        np.random.seed(self.seed)
        n_assets = len(S0)
        
        print(f"🎲 Simulando {self.n_sims} escenarios a {self.horizon} días...")

        # 1. Descomposición de Cholesky
        # Esto es clave pa mantener la correlación entre activos
        # L * L.T = Covarianza
        try:
            L = np.linalg.cholesky(self.cov)
        except np.linalg.LinAlgError:
            # Si la matriz no es definida positiva (pasa a veces), forzamos un fix
            print("🔧 Ajustando matriz de covarianza (no era positiva definida)...")
            eigenvals, eigenvecs = np.linalg.eigh(self.cov)
            eigenvals = np.maximum(eigenvals, 1e-8) # Poner piso mínimo
            self.cov = eigenvecs @ np.diag(eigenvals) @ eigenvecs.T
            L = np.linalg.cholesky(self.cov)

        # 2. Generar Shocks Aleatorios (El núcleo del caos)
        # Z ~ Normal(0, 1)
        Z = np.random.standard_normal((self.n_sims, self.horizon, n_assets))
        
        # 3. Ajuste t-Student (El factor miedo)
        # W ~ Chi-Cuadrado / nu
        # X = Z * sqrt((nu-2)/W)  <-- Esto infla las colas
        if self.nu > 2:
            chi2_vars = np.random.chisquare(df=self.nu, size=(self.n_sims, self.horizon, 1))
            factor_t = np.sqrt(self.nu / chi2_vars)
            # Aplicamos el factor a los shocks normales
            Z_student = Z * factor_t
        else:
            # Si nu es muy chico o hay error, usamos normal (fallback)
            Z_student = Z

        # 4. Construir Caminatas Aleatorias (Geometric Brownian Motion con Drift)
        # Drift = mu - 0.5 * varianza (ajuste de Ito)
        drift = self.mu - 0.5 * np.diag(self.cov)
        
        # Correlacionar los shocks: Z_corr = Z_student @ L.T
        # shape: (n_sims, horizon, n_assets)
        shocks_correlated = np.einsum('ijk,lk->ijl', Z_student, L)
        
        # Retornos diarios simulados
        sim_log_returns = drift + shocks_correlated
        
        # 5. Acumular y convertir a precios
        # Suma acumulada en el eje del tiempo (horizonte)
        cumulative_returns = np.cumsum(sim_log_returns, axis=1)
        
        # S_t = S_0 * exp(suma_retornos)
        # Necesitamos expandir S0 pa que tenga la misma forma que la matriz
        S0_matrix = np.array(S0).reshape(1, 1, n_assets)
        simulated_prices = S0_matrix * np.exp(cumulative_returns)
        
        # Agregamos el precio inicial al principio (t=0)
        # Esto es pa que graficar empiece desde hoy
        initial_prices = np.tile(S0_matrix, (self.n_sims, 1, 1))
        full_paths = np.concatenate([initial_prices, simulated_prices], axis=1)
        
        print("✅ Simulación completada.")
        return full_paths