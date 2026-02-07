from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import simulation

# Metadatos para la documentación automática (Swagger UI)
app = FastAPI(
    title="CL-RiskEngine API",
    description="Microservicio de Riesgo Financiero con Monte Carlo t-Student",
    version="2.0.0",
    contact={
        "name": "Equipo de Ingeniería Financiera",
        "email": "engineering@cl-risk.com",
    },
)

app.include_router(simulation.router, prefix="/v1/risk", tags=["Risk Engine"])

# Configuración CORS (Permitir que cualquier frontend nos llame por ahora)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint raíz para verificar que la API respira."""
    return {"message": "🦁 CL-RiskEngine API is online and roaring."}

@app.get("/health")
async def health_check():
    """Usado por Docker/Kubernetes para saber si el servicio está vivo."""
    return {"status": "healthy", "service": "risk-engine"}