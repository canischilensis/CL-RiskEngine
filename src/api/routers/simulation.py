from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import numpy as np

# Importamos tus esquemas (Contratos de datos)
from src.api.schemas.risk import RiskRequest, RiskResponse

# Importamos EL NÚCLEO (Tu lógica de negocio existente)
from src.data.loader import MarketDataLoader
from src.models.monte_carlo import MonteCarloEngine
from src.utils.reporter import RiskReporter

router = APIRouter()

@router.post("/simulate", response_model=RiskResponse)
def run_simulation(payload: RiskRequest):
    """
    Endpoint principal: Recibe un portafolio y devuelve métricas de riesgo.
    """
    try:
        # 1. Configuración de Fechas (Dinámica)
        end_date = datetime.now()
        # Usamos 2 años de historia para entrenar, como en tu script original
        start_date = end_date - timedelta(days=365 * 2) 

        # 2. Ingesta de Datos (Reutilizando tu Loader)
        print(f"📡 API Request: Descargando datos para {payload.tickers}")
        loader = MarketDataLoader(payload.tickers, start_date, end_date)
        loader.download_data()
        log_returns = loader.calculate_returns()
        last_prices = loader.get_last_prices()

        if log_returns is None or log_returns.empty:
            raise HTTPException(status_code=400, detail="No se pudieron descargar datos para los tickers proporcionados.")

        # 3. Motor de Simulación (Reutilizando tu Engine)
        print(f"🎲 API Request: Iniciando Monte Carlo ({payload.n_sims} sims)")
        engine = MonteCarloEngine(payload.n_sims, payload.horizon)
        engine.train(log_returns)
        simulated_paths = engine.simulate(last_prices.values)

        # 4. Cálculo de Métricas (Reutilizando tu Reporter)
        # OJO: Instanciamos el reporter solo para usar sus fórmulas, no para escribir TXT
        reporter = RiskReporter(output_dir="output") # El directorio no importa aquí
        pnl_scenarios = reporter.compute_pnl(simulated_paths)
        metrics = reporter.calculate_metrics(pnl_scenarios)

        # 5. Formatear la Respuesta JSON (Adaptar al Schema)
        response_metrics = {}
        
        # Mapeo manual para asegurar que coincida con lo que el frontend espera
        metric_descriptions = {
            "VaR 95%": "Pérdida máxima esperada con 95% de confianza",
            "CVaR 95%": "Pérdida promedio en el peor 5% de los casos",
            "VaR 99%": "Pérdida máxima esperada con 99% de confianza (Estrés)",
            "CVaR 99%": "Pérdida promedio en el peor 1% de los casos (Colapso)"
        }

        for key, value in metrics.items():
            if key in metric_descriptions:
                response_metrics[key] = {
                    "value": round(float(value), 4), # Redondear a 4 decimales
                    "description": metric_descriptions[key]
                }

        return {
            "status": "success",
            "metadata": {
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d'),
                "execution_time": 0.0 # TODO: Medir tiempo real si se desea
            },
            "metrics": response_metrics
        }

    except Exception as e:
        print(f"❌ Error Interno: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en el motor de cálculo: {str(e)}")