import os
import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime

class MarketDataLoader:
    def __init__(self, tickers, start_date, end_date, data_dir="data"):
        """
        Inicializa el gestor de datos siguiendo la arquitectura Lakehouse.
        
        Directorios:
        - data/bronze: Datos crudos (csv/json) - Auditoría
        - data/silver: Datos procesados (parquet) - Rendimiento
        """
        self.tickers = tickers
        self.start = start_date
        self.end = end_date
        self.base_dir = data_dir
        
        # Definición de capas del Lakehouse
        self.bronze_dir = os.path.join(self.base_dir, "bronze")
        self.silver_dir = os.path.join(self.base_dir, "silver")
        
        # Garantizar que existan las carpetas
        os.makedirs(self.bronze_dir, exist_ok=True)
        os.makedirs(self.silver_dir, exist_ok=True)

    def _get_bronze_path(self, ticker):
        """Genera ruta particionada por fecha de ingestión."""
        today = datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(self.bronze_dir, today)
        os.makedirs(path, exist_ok=True)
        return os.path.join(path, f"{ticker}.csv")

    def _get_silver_path(self, ticker):
        """Ruta al archivo Parquet optimizado."""
        return os.path.join(self.silver_dir, f"{ticker}.parquet")

    def ingest_data(self):
        """
        Paso 1 (EL): Extracción y Carga a Capa Bronce.
        Descarga datos de Yahoo y los guarda CRUDOS sin tocar.
        """
        print(f"📡 INGESTA: Iniciando descarga para {len(self.tickers)} activos...")
        
        for ticker in self.tickers:
            try:
                # Descarga individual para evitar problemas de MultiIndex de Yahoo
                df = yf.download(ticker, start=self.start, end=self.end, progress=False)
                
                if df.empty:
                    print(f"⚠️ Advertencia: No hay datos para {ticker}")
                    continue
                
                # PERSISTENCIA BRONCE (Schema-on-Read)
                # Guardamos CSV crudo para auditoría
                raw_path = self._get_bronze_path(ticker)
                df.to_csv(raw_path)
                print(f"✅ [Bronce] Guardado: {ticker} -> {raw_path}")
                
            except Exception as e:
                print(f"❌ Error descargando {ticker}: {str(e)}")

    def transform_to_silver(self):
        """
        Paso 2 (T): Transformación y Carga a Capa Plata.
        Lee de Bronce, fuerza tipos numéricos, limpia y guarda en Parquet.
        """
        print(f"⚙️ TRANSFORMACIÓN: Generando capa Plata (Parquet)...")
        
        for ticker in self.tickers:
            try:
                raw_path = self._get_bronze_path(ticker)
                if not os.path.exists(raw_path):
                    print(f"⚠️ No se encontró raw data para {ticker}, saltando...")
                    continue
                
                # Cargar CSV crudo (puede contener basura en los headers)
                df = pd.read_csv(raw_path, index_col=0, parse_dates=[0])
                
                # Selección de Columna
                if 'Adj Close' in df.columns:
                    series = df['Adj Close']
                elif 'Close' in df.columns:
                    series = df['Close']
                else:
                    # Intento de fallback: si la columna se llama diferente (ej. ticker)
                    # Esto pasa a veces con yfinance multi-index
                    series = df.iloc[:, 0] 

                # === 🛡️ CORRECCIÓN DE INGENIERÍA DE DATOS 🛡️ ===
                # 1. Forzar conversión a NUMÉRICO.
                # 'errors=coerce' convierte cualquier texto (como headers repetidos) en NaN
                series = pd.to_numeric(series, errors='coerce')

                # 2. Limpieza de NaNs (incluyendo los generados por la conversión)
                series = series.ffill().dropna()

                # Verificar si quedó vacío después de limpiar
                if series.empty:
                    print(f"⚠️ {ticker}: Datos vacíos tras limpieza. Revisar CSV Bronce.")
                    continue
                
                # Crear DataFrame limpio para Silver
                df_silver = pd.DataFrame(series)
                df_silver.columns = ['price']
                
                # Calcular Retornos Logarítmicos
                df_silver['log_return'] = np.log(df_silver['price'] / df_silver['price'].shift(1))
                df_silver = df_silver.dropna()

                # PERSISTENCIA PLATA
                silver_path = self._get_silver_path(ticker)
                df_silver.to_parquet(silver_path, engine='pyarrow', compression='snappy')
                
                print(f"💎 [Plata] Optimizado: {ticker} -> {silver_path}")
                
            except Exception as e:
                print(f"❌ Error transformando {ticker}: {str(e)}")

    def load_for_simulation(self):
        """
        Paso 3: Lectura para el Motor.
        Lee exclusivamente desde la Capa Plata (Parquet).
        Retorna: (DataFrame retornos, Series últimos precios)
        """
        returns_list = []
        last_prices = {}
        
        print(f"🚀 LEER: Cargando datos desde Data Lake (Silver Layer)...")
        
        for ticker in self.tickers:
            silver_path = self._get_silver_path(ticker)
            if not os.path.exists(silver_path):
                print(f"❌ Error Crítico: No existe capa plata para {ticker}. Ejecute ingest primero.")
                continue
            
            # Lectura ultra-rápida con Parquet
            df = pd.read_parquet(silver_path, engine='pyarrow')
            
            # Validar integridad
            if 'log_return' not in df.columns or 'price' not in df.columns:
                 print(f"❌ Integridad de datos fallida en {ticker}")
                 continue

            # Agregar al dataset final
            returns_list.append(df['log_return'].rename(ticker))
            last_prices[ticker] = df['price'].iloc[-1]
            
        if not returns_list:
            return None, None
            
        # Consolidar matriz de retornos (Inner Join por fecha)
        all_returns = pd.concat(returns_list, axis=1).dropna()
        last_prices_series = pd.Series(last_prices)
        
        return all_returns, last_prices_series