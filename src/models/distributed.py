import ray
import numpy as np
from src.models.base import StochasticModel

@ray.remote
class RiskWorker:
    """
    ACTOR DISTRIBUIDO (Ray)
    Este componente vive en un proceso separado (Quantum Arquitectónico).
    Mantiene su propia copia de la estrategia y estado.
    """
    def __init__(self, strategy: StochasticModel):
        self.strategy = strategy

    def run_simulation_chunk(self, current_prices: np.ndarray, horizon: int, n_sims: int):
        """
        Ejecuta una fracción del total de simulaciones.
        """
        # Delega a la estrategia (que ya contiene la lógica matemática)
        return self.strategy.simulate(current_prices, horizon, n_sims)

class DistributedMonteCarlo:
    """
    Orquestador del Clúster (Driver).
    Divide el trabajo y recolecta resultados (Map-Reduce).
    """
    def __init__(self, strategy: StochasticModel, n_workers: int = 4):
        self.strategy = strategy
        self.n_workers = n_workers
        
        # Inicializar Ray (si no está corriendo ya)
        if not ray.is_initialized():
            ray.init(ignore_reinit_error=True)

    def train(self, log_returns):
        # El entrenamiento es rápido, se hace en el Driver (centralizado)
        # y luego se envia la estrategia entrenada a los workers.
        self.strategy.train(log_returns)

    def simulate(self, current_prices: np.ndarray, horizon: int, total_sims: int):
        print(f"⚡ [Ray] Distribuyendo {total_sims} sims entre {self.n_workers} workers...")
        
        # 1. Instanciar Actores (Workers)
        # copia la estrategia YA ENTRENADA a cada worker
        workers = [RiskWorker.remote(self.strategy) for _ in range(self.n_workers)]
        
        # 2. Dividir trabajo (Sharding)
        sims_per_worker = total_sims // self.n_workers
        remainder = total_sims % self.n_workers
        
        # 3. Lanzar tareas asíncronas (Non-blocking)
        futures = []
        for i, worker in enumerate(workers):
            # El último worker se lleva el resto si la división no es exacta
            count = sims_per_worker + (remainder if i == self.n_workers - 1 else 0)
            
            # .remote() devuelve un Future (ObjectID) inmediatamente
            future = worker.run_simulation_chunk.remote(current_prices, horizon, count)
            futures.append(future)

        # 4. Barrier Synchronization (Esperar a todos)
        # ray.get() bloquea hasta que los resultados estén listos
        results_list = ray.get(futures)
        
        # 5. Reducción (Merge de resultados)
        # Concatena los arrays (n_sims, horizon, assets) a lo largo del eje 0
        final_simulation = np.concatenate(results_list, axis=0)
        
        print(f"✅ [Ray] Fusión completada. Tensor final: {final_simulation.shape}")
        return final_simulation