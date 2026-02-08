import os
import numpy as np
import pandas as pd
from datetime import datetime

class RiskReporter:
    def __init__(self, output_dir="output", gold_dir="data/gold"):
        self.output_dir = output_dir
        self.gold_dir = gold_dir
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.gold_dir, exist_ok=True)

    def compute_pnl(self, simulated_paths: np.ndarray) -> np.ndarray:
        """Calcula PnL del portafolio (Equiponderado)."""
        # Sumamos precios de todos los activos en cada día/simulación
        portfolio_paths = simulated_paths.sum(axis=2) # (n_sims, days)
        
        # Retorno Total al final del horizonte
        initial_value = portfolio_paths[:, 0]
        final_value = portfolio_paths[:, -1]
        
        # PnL %
        return (final_value / initial_value) - 1

    def calculate_metrics(self, pnl_array: np.ndarray, confidence=0.95):
        """Calcula VaR y CVaR."""
        var_percentile = (1 - confidence) * 100
        
        var_value = np.percentile(pnl_array, var_percentile)
        cvar_value = pnl_array[pnl_array <= var_value].mean()
        
        # Cálculo extremo (99%)
        var_99 = np.percentile(pnl_array, 1)
        cvar_99 = pnl_array[pnl_array <= var_99].mean()
        
        return {
            f"VaR {int(confidence*100)}%": var_value,
            f"CVaR {int(confidence*100)}%": cvar_value,
            "VaR 99%": var_99,
            "CVaR 99%": cvar_99
        }

    def generate_report(self, metrics, params):
        """Genera TXT y guarda en CAPA ORO."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        
        # 1. Reporte Humano (TXT)
        filename = f"risk_report_{timestamp}.txt"
        path = os.path.join(self.output_dir, filename)
        
        with open(path, 'w') as f:
            f.write("="*50 + "\n")
            f.write(f"🛡️ CL-RISKENGINE | REPORTE EJECUTIVO\n")
            f.write(f"Fecha: {timestamp}\n")
            f.write("="*50 + "\n\n")
            f.write(f"ACTIVOS: {params['tickers']}\n")
            f.write(f"MODELO: {params.get('model_name', 'Unknown')}\n")
            f.write("-" * 50 + "\n")
            for k, v in metrics.items():
                f.write(f"{k:<25} {v:.2%}\n")
            f.write("-" * 50 + "\n")
            
        print(f"✅ Reporte TXT generado: {path}")

        # 2. Capa Oro (Parquet - Time Travel)
        # Guardamos un registro histórico estructurado
        record = {
            'execution_date': datetime.now(),
            'model': params.get('model_name', 'Unknown'),
            'n_sims': params['n_sims'],
            'horizon': params['horizon'],
            'var_95': metrics[f"VaR 95%"],
            'cvar_95': metrics[f"CVaR 95%"],
            'var_99': metrics["VaR 99%"],
            'cvar_99': metrics["CVaR 99%"]
        }
        
        df_gold = pd.DataFrame([record])
        
        # Modo Append: Leemos existente o creamos nuevo
        gold_path = os.path.join(self.gold_dir, "risk_metrics_history.parquet")
        
        if os.path.exists(gold_path):
            df_old = pd.read_parquet(gold_path)
            df_final = pd.concat([df_old, df_gold], ignore_index=True)
        else:
            df_final = df_gold
            
        df_final.to_parquet(gold_path, index=False)
        print(f"🏆 [Capa Oro] Métricas persistidas en: {gold_path}")