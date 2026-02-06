# Entry Point
import sys
import os
from datetime import datetime, timedelta

# Truco pa que Python encuentre nuestros modulos en la carpeta src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data.loader import MarketDataLoader
from src.models.monte_carlo import MonteCarloEngine
from src.utils.reporter import RiskReporter

# --- CONFIGURACIÓN GLOBAL ---
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN'] # Portafolio Tech
YEARS_BACK = 2
N_SIMS = 5000       # Universos paralelos
HORIZON = 252       # 1 año bursátil
INITIAL_CAP = 100   # Base 100 pa indexar

def main():
    print("🚀 Iniciando CL-RiskEngine v1.0...")
    print("=" * 40)

    # 1. DEFINIR FECHAS
    end_date = datetime.now()
    start_date = end_date - timedelta(days=YEARS_BACK*365)
    
    # 2. INGESTA DE DATOS (El 'Loader')
    print("\n[PASO 1] Ingesta de Datos")
    loader = MarketDataLoader(TICKERS, start_date, end_date)
    loader.download_data()
    log_returns = loader.calculate_returns()
    last_prices = loader.get_last_prices() # S0

    if log_returns is None or last_prices is None:
        print("❌ Abortando misión: Falló la descarga de datos.")
        return

    # 3. MOTOR DE SIMULACIÓN (El 'Engine')
    print("\n[PASO 2] Simulación Monte Carlo t-Student")
    engine = MonteCarloEngine(N_SIMS, HORIZON)
    
    # Entrenar con la historia
    engine.train(log_returns)
    
    # Simular el futuro
    simulated_paths = engine.simulate(last_prices.values)

    # 4. REPORTING (El 'Reporter')
    print("\n[PASO 3] Generación de Reporte")
    reporter = RiskReporter(output_dir="output")
    
    # Calcular PnL (Ganancias/Pérdidas) de cada escenario
    # Ojo: Aquí simplificamos asumiendo que el portafolio se mueve igual que la suma de precios
    # En una versión v2, deberíamos meter 'pesos' (weights)
    
    # Hack rápido pa calcular retorno del portafolio total:
    # Asumimos equiponderado (equal weight) implícito en la suma de precios
    pnl_scenarios = reporter.compute_pnl(simulated_paths)
    
    # Calcular métricas de riesgo
    metrics = reporter.calculate_metrics(pnl_scenarios)
    
    # Empaquetar params pa ponerlos en el txt
    params = {
        'tickers': TICKERS,
        'horizon': HORIZON,
        'n_sims': N_SIMS,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
    
    # Guardar el txt
    reporter.generate_report(metrics, params)

    print("\n" + "=" * 40)
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("   Revisa la carpeta 'output/' para analizar el reporte.")
    print("=" * 40)

if __name__ == "__main__":
    main()