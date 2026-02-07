# Entry Point
import sys
import os
import multiprocessing # Necesario para contar núcleos de CPU
from datetime import datetime, timedelta

# Truco pa que Python encuentre nuestros modulos en la carpeta src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data.loader import MarketDataLoader
# from src.models.monte_carlo import MonteCarloEngine # YA NO se usa
from src.models.distributed import DistributedMonteCarlo # s eusa EL MOTOR RAY
from src.utils.reporter import RiskReporter
from src.models.student_t import StudentTStrategy

# --- CONFIGURACIÓN GLOBAL ---
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN'] # Portafolio Tech
YEARS_BACK = 2
N_SIMS = 5000       # Universos paralelos
HORIZON = 252       # 1 año bursátil
INITIAL_CAP = 100   # Base 100 pa indexar

def main():
    print("🚀 Iniciando CL-RiskEngine v3.0 (Distributed)...")
    print("=" * 40)

    # 1. DEFINIR FECHAS
    end_date = datetime.now()
    start_date = end_date - timedelta(days=YEARS_BACK*365)
    
    # 2. INGESTA DE DATOS (Arquitectura Lakehouse)
    print("\n[PASO 1] Pipeline de Datos (ELT)")
    loader = MarketDataLoader(TICKERS, start_date, end_date)
    
    # a) Extract & Load (Bronce)
    loader.ingest_data()
    
    # b) Transform (Plata)
    loader.transform_to_silver()
    
    # c) Read (Para el motor)
    log_returns, last_prices = loader.load_for_simulation()

    if log_returns is None or last_prices is None:
        print("❌ Abortando misión: Falló la carga de datos del Lakehouse.")
        return

    # 3. MOTOR DE SIMULACIÓN DISTRIBUIDO (Ray)
    print("\n[PASO 2] Simulación Monte Carlo Distribuida (Ray Cluster)")
    
    # 1. Instanciar la estrategia (El "Cartucho" matemático)
    strategy = StudentTStrategy()
    
    # 2. Detectar recursos y lanzamos el Cluster
    n_cores = multiprocessing.cpu_count()
    print(f"⚡ Detectados {n_cores} núcleos de CPU. Iniciando clúster Ray...")
    
    # Inyectar la estrategia en el motor distribuido
    engine = DistributedMonteCarlo(strategy, n_workers=n_cores)
    
    # 3. Ejecutar
    # Entrenar (Se hace en el driver localmente porque es rápido)
    engine.train(log_returns)
    
    # Simular (Se distribuye a los workers)
    # Nota: Usamos 'total_sims' conforme a la clase DistributedMonteCarlo
    simulated_paths = engine.simulate(last_prices.values, horizon=HORIZON, total_sims=N_SIMS)
    
    # 4. REPORTING (El 'Reporter')
    print("\n[PASO 3] Generación de Reporte")
    reporter = RiskReporter(output_dir="output")
    
    # Calcular PnL (Ganancias/Pérdidas) de cada escenario
    pnl_scenarios = reporter.compute_pnl(simulated_paths)
    
    # Calcular métricas de riesgo
    metrics = reporter.calculate_metrics(pnl_scenarios)
    
    # Empaquetar params pa ponerlos en el txt
    params = {
        'tickers': TICKERS,
        'horizon': HORIZON,
        'n_sims': N_SIMS,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'engine_type': 'Ray Distributed Cluster'
    }
    
    # Guardar el txt
    reporter.generate_report(metrics, params)

    print("\n" + "=" * 40)
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("   Revisa la carpeta 'output/' para analizar el reporte.")
    print("=" * 40)

if __name__ == "__main__":
    main()