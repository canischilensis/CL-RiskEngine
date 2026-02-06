import numpy as np
import pandas as pd
import os
import datetime

class RiskReporter:
    def __init__(self, output_dir="output"):
        """
        Configurar dónde guardar los reportes.
        Nota: Ya no forzamos el 'initial_capital' aquí, lo calculamos dinámico.
        """
        self.output_dir = output_dir
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def compute_pnl(self, simulated_paths):
        """
        Calculr retornos comparando el valor FINAL contra el valor INICIAL real.
        simulated_paths: Array (n_sims, horizon + 1, n_assets)
        """
        # 1. Obtener el valor del portafolio en t=0 (Inicio)
        # Tomamos la primera fila de precios (todos los escenarios empiezan igual)
        initial_prices = simulated_paths[0, 0, :]
        portfolio_initial_value = np.sum(initial_prices)
        
        # 2. Obtener el valor del portafolio en t=Final
        final_prices = simulated_paths[:, -1, :]
        portfolio_final_values = np.sum(final_prices, axis=1)
        
        # 3. Calculr Retorno Real
        # PnL = (Valor Final / Valor Inicial Real) - 1
        portfolio_returns = (portfolio_final_values / portfolio_initial_value) - 1
        
        return portfolio_returns

    def calculate_metrics(self, portfolio_returns):
        """
        Calculr VaR y CVaR. 
        OJO: En finanzas, el VaR suele reportarse como pérdida (negativo).
        Aquí lo dejamos tal cual sale del percentil.
        """
        metrics = {}
        alphas = [0.95, 0.99]
        
        for alpha in alphas:
            # VaR: El percentil q (cola izquierda)
            q = 1.0 - alpha
            var_value = np.percentile(portfolio_returns, q * 100)
            
            # CVaR: Promedio de la cola
            cvar_value = portfolio_returns[portfolio_returns <= var_value].mean()
            
            metrics[f'VaR {alpha:.0%}'] = var_value
            metrics[f'CVaR {alpha:.0%}'] = cvar_value
            
        return metrics

    def generate_report(self, metrics, params):
        """
        Escribir el reporte txt.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"risk_report_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        # Datframe pa la tabla
        report_data = {
            "Métrica": [
                "Horizonte Temporal", 
                "Simulaciones",
                "VaR 95% (Confianza)", 
                "CVaR 95% (Déficit Esp.)", 
                "VaR 99% (Estrés)", 
                "CVaR 99% (Colapso)"
            ],
            "Valor": [
                f"{params.get('horizon')} días",
                f"{params.get('n_sims')}",
                f"{metrics['VaR 95%']:.2%}",
                f"{metrics['CVaR 95%']:.2%}",
                f"{metrics['VaR 99%']:.2%}",
                f"{metrics['CVaR 99%']:.2%}"
            ]
        }
        df = pd.DataFrame(report_data)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("==================================================\n")
                f.write(f"🛡️ CL-RISKENGINE | REPORTE EJECUTIVO\n")
                f.write(f"Fecha: {timestamp}\n")
                f.write("==================================================\n\n")
                
                f.write(f"ACTIVOS: {params.get('tickers')}\n")
                f.write(f"MODELO: Monte Carlo Estructurado (t-Student)\n")
                f.write("-" * 50 + "\n\n")
                
                f.write(df.to_string(index=False, justify="left"))
                
                f.write("\n\n" + "-" * 50 + "\n")
                f.write("INTERPRETACIÓN:\n")
                f.write(f"* VaR 95%: El límite inferior esperado con 95% de confianza es {metrics['VaR 95%']:.2%}.\n")
                f.write(f"* Si el número es NEGATIVO, es pérdida. Si es POSITIVO, es la ganancia mínima.\n")
                
            print(f"✅ Reporte generado en: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error escribiendo reporte: {e}")
            return None