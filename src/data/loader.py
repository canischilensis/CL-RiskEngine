import yfinance as yf
import pandas as pd
import numpy as np

class MarketDataLoader:
    def __init__(self, tickers, start_date, end_date):
        """
        Configuracion inicial.
        """
        self.tickers = tickers
        self.start = start_date
        self.end = end_date
        self.data = None
        self.log_returns = None

    def download_data(self):
        """
        Bajr precios de manera robusta.
        Fix: Separar la descarga del filtro de columnas pa no crashear.
        """
        print(f"📡 Conectando a API pa descargr: {self.tickers}...")
        try:
            # 1. Descargr data cruda sin filtrar todavía
            # group_by='column' ayuda a que la estructura sea predecible
            df = yf.download(self.tickers, start=self.start, end=self.end, group_by='column', progress=False)
            
            # 2. Validar si bajó algo
            if df.empty:
                raise ValueError("⚠️ La API devolvió un DataFrame vacío.")

            # 3. Intentar sacar 'Adj Close', si no ta, usar 'Close'
            # A veces yfinance cambia los nombres segun la version
            if 'Adj Close' in df.columns:
                self.data = df['Adj Close']
            elif 'Close' in df.columns:
                print("⚠️ 'Adj Close' no encontrao, usando 'Close' regular...")
                self.data = df['Close']
            else:
                # Caso raro: Estructura MultiIndex compleja
                # Intentamos acceder nivel por nivel si es necesario
                try:
                    self.data = df.xs('Adj Close', level=0, axis=1)
                except:
                    raise KeyError(f"No pillé ni 'Adj Close' ni 'Close'. Columnas disponibles: {df.columns}")
            
            # Limpir filas vacías (días feriados)
            self.data = self.data.dropna()
            
            print(f"✅ Data descargada: {self.data.shape[0]} días de historia.")
            return self.data
            
        except Exception as e:
            print(f"❌ Error al bajr data: {e}")
            # Importante: Retornar None pa que el main sepa que falló
            return None

    def calculate_returns(self):
        """
        Calculr retornos logaritmicos.
        """
        if self.data is None:
            print("⚠️ Primero tienes que corrér download_data().")
            return None
        
        # ln(Pt / Pt-1)
        self.log_returns = np.log(self.data / self.data.shift(1)).dropna()
        
        print("✅ Retornos logarítmicos calculaos.")
        return self.log_returns

    def get_last_prices(self):
        """
        Sacr el último precio conocido (S0).
        """
        if self.data is None:
            return None
        return self.data.iloc[-1]