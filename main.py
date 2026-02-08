# Entry Point
import sys
import os
import multiprocessing
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# IMPORTS ACTUALIZADOS
from src.config.settings import settings  # Singleton
from src.data.loader import MarketDataLoader
from src.models.distributed import DistributedMonteCarlo
from src.utils.reporter import RiskReporter
from src.models.student_t import StudentTStrategy
from src.models.gbm import GeometricBrownianMotionStrategy # Nuevo Modelo

def main():
    print("🚀 Iniciando CL-RiskEngine v4.0 (Enterprise Compliance)...")
    print("=" * 40)

    # 1. FECHAS (Desde Settings)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=settings.YEARS_BACK*365)
    
    # 2. INGESTA
    print("\n[PASO 1] Pipeline de Datos (ELT)")
    loader = MarketDataLoader(settings.TICKERS, start_date, end_date)
    loader.ingest_data()
    loader.transform_to_silver()
    log_returns, last_prices = loader.load_for_simulation()

    if log_returns is None:
        return

    # 3. SELECCIÓN DE ESTRATEGIA (Polimorfismo en acción)
    # Aquí podríamos poner un input del usuario o flag. Por defecto usaremos t-Student.
    # Para probar GBM, cambie a: strategy = GeometricBrownianMotionStrategy()
    
    print("\n[PASO 2] Selección de Modelo")
    # strategy = GeometricBrownianMotionStrategy() # Descomentar para probar GBM
    strategy = StudentTStrategy()
    model_name = strategy.__class__.__name__
    print(f"🧠 Estrategia Activa: {model_name}")

    # 4. SIMULACIÓN DISTRIBUIDA
    n_cores = multiprocessing.cpu_count()
    engine = DistributedMonteCarlo(strategy, n_workers=n_cores)
    
    engine.train(log_returns)
    simulated_paths = engine.simulate(
        last_prices.values, 
        horizon=settings.HORIZON, 
        total_sims=settings.N_SIMS
    )
    
    # 5. REPORTING (Capa Oro)
    print("\n[PASO 3] Reporting & Gold Layer")
    reporter = RiskReporter(output_dir=settings.OUTPUT_DIR, gold_dir=os.path.join(settings.DATA_DIR, "gold"))
    
    pnl_scenarios = reporter.compute_pnl(simulated_paths)
    metrics = reporter.calculate_metrics(pnl_scenarios, confidence=settings.CONFIDENCE_LEVEL)
    
    params = {
        'tickers': settings.TICKERS,
        'horizon': settings.HORIZON,
        'n_sims': settings.N_SIMS,
        'model_name': model_name
    }
    
    reporter.generate_report(metrics, params)

    print("\n✅ PROCESO COMPLETADO EXITOSAMENTE")

if __name__ == "__main__":
    main()