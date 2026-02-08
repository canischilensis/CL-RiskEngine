import os

class Settings:
    """
    Patrón Singleton para gestión de configuración.
    Centraliza parámetros del negocio y evita 'números mágicos' en el código.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # --- Parámetros de Mercado ---
        self.TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
        self.YEARS_BACK = 2
        
        # --- Parámetros de Simulación ---
        self.N_SIMS = 5000       # Universos paralelos
        self.HORIZON = 252       # 1 año bursátil
        self.INITIAL_CAP = 100   # Base 100
        self.CONFIDENCE_LEVEL = 0.95
        
        # --- Rutas de Infraestructura ---
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.DATA_DIR = os.path.join(self.BASE_DIR, "data")
        self.OUTPUT_DIR = os.path.join(self.BASE_DIR, "output")
        
        # Garantizar existencia de carpetas clave
        os.makedirs(os.path.join(self.DATA_DIR, "gold"), exist_ok=True)
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)

# Instancia global lista para importar
settings = Settings()