from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

# --- INPUT MODEL (Lo que nos envían) ---
class RiskRequest(BaseModel):
    tickers: List[str] = Field(
        ..., 
        min_length=1, 
        description="Lista de símbolos bursátiles (ej. ['AAPL', 'MSFT'])",
        example=["AAPL", "MSFT", "GOOGL"]
    )
    horizon: int = Field(
        252, 
        ge=1, 
        le=1260, 
        description="Horizonte de proyección en días (1 año bursátil = 252)"
    )
    n_sims: int = Field(
        5000, 
        ge=1000, 
        le=50000, 
        description="Número de simulaciones Monte Carlo"
    )
    confidence_level: float = Field(
        0.95, 
        gt=0, 
        lt=1, 
        description="Nivel de confianza para el VaR (ej. 0.95 o 0.99)"
    )

    @field_validator('tickers')
    def validate_tickers(cls, v):
        # Convertir a mayúsculas para estandarizar
        return [t.upper() for t in v]

# --- OUTPUT MODEL (Lo que respondemos) ---
class RiskMetric(BaseModel):
    value: float
    description: str

class SimulationMetadata(BaseModel):
    start_date: str
    end_date: str
    execution_time: float

class RiskResponse(BaseModel):
    status: str
    metadata: SimulationMetadata
    metrics: dict[str, RiskMetric]