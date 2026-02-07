# 💸 CL-RiskEngine: Stochastic Financial Risk Microservice

> **Microservicio de Riesgo Financiero** containerizado. Implementa simulación Monte Carlo Estructurada con ajuste de **Colas Pesadas (t-Student)**, expuesto vía API REST para integración en sistemas de inversión.

---

## 📋 Table of Contents

1. [About the Project](https://www.google.com/search?q=%23-about-the-project)
2. [Tech Stack](https://www.google.com/search?q=%23-tech-stack)
3. [Quant Methodology](https://www.google.com/search?q=%23-quant-methodology)
4. [Project Structure](https://www.google.com/search?q=%23-project-structure)
5. [Getting Started (Docker)](https://www.google.com/search?q=%23-getting-started-docker)
6. [API Usage](https://www.google.com/search?q=%23-api-usage)

---

## 🚀 About The Project

**CL-RiskEngine v2.0** evoluciona el motor de riesgo original hacia una arquitectura orientada a servicios (**SOA**). Mantiene la robustez matemática del modelado de "Cisnes Negros", pero ahora permite su consumo agnóstico desde cualquier frontend o sistema externo mediante HTTP.

### Key Features

* ✅ **Fat-Tail Modeling:** Sustitución de la distribución Normal por **t-Student** ( degrees of freedom) calibrada dinámicamente para capturar leptocurtosis.
* ✅ **Microservice Architecture:** Motor expuesto vía **FastAPI** con documentación automática (Swagger UI/Redoc).
* ✅ **Containerization:** Empaquetado en **Docker** (Python Slim) para despliegue consistente en cualquier entorno (Local/AWS/Kubernetes).
* ✅ **Correlation Preservation:** Uso de **Descomposición de Cholesky** () para mantener la estructura de dependencia entre activos.
* ✅ **Robust ETL:** Sistema resiliente a fallos de API de terceros y limpieza de datos automatizada.

---

## 🛠 Tech Stack

El proyecto implementa un stack moderno de **MLOps** e Ingeniería Financiera:

### Core & Math

### API & Infrastructure

---

## 🧮 Quant Methodology

El motor simula trayectorias de precios basadas en el **Movimiento Browniano Geométrico (GBM)** adaptado para colas pesadas.

La dinámica del precio  se modela como:

Donde el término de innovación estocástica  se construye mediante:

1. **Ajuste de Distribución:** Se estima el parámetro  (grados de libertad) de los retornos históricos.
2. **Generación de Shocks:** Se generan variables aleatorias  y .
3. **Transformación t-Student:** 
4. **Inducción de Correlación:** Se aplica la matriz de Cholesky  para correlacionar los shocks: 

---

## 📂 Project Structure

Arquitectura modular preparada para producción:

```bash
CL-RiskEngine/
├── src/
│   ├── api/                # 🌐 Capa de Servicio (Nuevo v2.0)
│   │   ├── routers/        # Endpoints (e.g., /simulate)
│   │   ├── schemas/        # Contratos Pydantic (Request/Response)
│   │   └── main.py         # Entrypoint FastAPI
│   ├── data/               # 💾 Capa de Ingesta
│   ├── models/             # 🧠 Capa de Cálculo (Monte Carlo Core)
│   └── utils/              # 🛠 Helpers
├── output/                 # Persistencia de reportes
├── Dockerfile              # 🐳 Definición de Imagen
├── docker-compose.yml      # 🐙 Orquestador de Servicios
├── requirements.txt        # Dependencias
└── README.md               # Documentación

```

---

## 🏁 Getting Started (Docker)

La forma recomendada de ejecutar el motor es mediante contenedores. Esto garantiza que el entorno sea idéntico al de desarrollo.

### Prerrequisitos

* Docker & Docker Compose instalados.

### Despliegue en 1 Paso

1. **Clonar y Levantar:**

```bash
git clone https://github.com/tu-usuario/CL-RiskEngine.git
cd CL-RiskEngine

# Construir y levantar el servicio
docker-compose up --build

```

2. **Verificar:**
El servicio estará disponible en: `http://localhost:8000`

---

## 🔌 API Usage

Una vez levantado el servicio, puede interactuar con el motor a través de la documentación interactiva (Swagger UI) o mediante `curl`.

### 📖 Documentación Interactiva

Visite **[http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)** para probar los endpoints directamente desde el navegador.

### ⚡ Ejemplo de Request (cURL)

```bash
curl -X 'POST' \
  'http://localhost:8000/v1/risk/simulate' \
  -H 'Content-Type: application/json' \
  -d '{
  "tickers": ["AAPL", "GOOGL", "MSFT"],
  "horizon": 252,
  "n_sims": 5000,
  "confidence_level": 0.95
}'

```

### 📦 Ejemplo de Respuesta (JSON)

```json
{
  "status": "success",
  "metadata": {
    "start_date": "2024-02-08",
    "end_date": "2026-02-07",
    "execution_time": 0.45
  },
  "metrics": {
    "VaR 95%": {
      "value": -0.2811,
      "description": "Pérdida máxima esperada con 95% de confianza"
    },
    "CVaR 95%": {
      "value": -0.3839,
      "description": "Pérdida promedio en el peor 5% de los casos"
    }
  }
}

```

---

## ⚠️ Disclaimer

Este software es una prueba de concepto (PoC) para **investigación académica y desarrollo de portafolio**. No constituye asesoramiento financiero. Los modelos estocásticos se basan en parámetros históricos que no garantizan rendimientos futuros.

---

<div align="center">
<p>Developed with 💻 & ☕ by <strong>Canis chilensis</strong></p>
<p>
<a href="#">
<img src="[https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&logoColor=white](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&logoColor=white)" alt="LinkedIn" />
</a>
<a href="#">
<img src="[https://img.shields.io/badge/GitHub-black?style=flat&logo=github&logoColor=white](https://www.google.com/search?q=https://img.shields.io/badge/GitHub-black%3Fstyle%3Dflat%26logo%3Dgithub%26logoColor%3Dwhite)" alt="GitHub" />
</a>
</p>
</div>