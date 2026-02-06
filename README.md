# 🦁 CL-RiskEngine: Stochastic Financial Risk Simulator

> **Motor de Riesgo de Mercado Modular** diseñado para portafolios de alta volatilidad. Implementa simulación Monte Carlo Estructurada con ajuste de **Colas Pesadas (t-Student)** y cálculo automatizado de métricas VaR/CVaR.

---

## 📋 Table of Contents

1. [About the Project](https://www.google.com/search?q=%23-about-the-project)
2. [Tech Stack](https://www.google.com/search?q=%23-tech-stack)
3. [Quant Methodology](https://www.google.com/search?q=%23-quant-methodology)
4. [Project Structure](https://www.google.com/search?q=%23-project-structure)
5. [Getting Started](https://www.google.com/search?q=%23-getting-started)
6. [Visual Results](https://www.google.com/search?q=%23-visual-results)

---

## 🚀 About The Project

**CL-RiskEngine** es una solución de ingeniería financiera desarrollada para superar las limitaciones de los modelos de riesgo tradicionales que asumen normalidad en los retornos. Este software está diseñado para operar bajo la premisa de que los eventos extremos ("Cisnes Negros") son más frecuentes de lo que predice la teoría Gaussiana.

### Key Features

* ✅ **Fat-Tail Modeling:** Sustitución de la distribución Normal por **t-Student** calibrada dinámicamente ( degrees of freedom) para capturar leptocurtosis.
* ✅ **Vectorized Simulation:** Núcleo matemático optimizado con `numpy` para proyectar miles de escenarios correlacionados sin bucles explícitos.
* ✅ **Correlation Preservation:** Uso de **Descomposición de Cholesky** () para mantener la estructura de dependencia entre activos (e.g., Tech Stocks).
* ✅ **Robust ETL:** Módulo de ingesta resiliente (`MarketDataLoader`) capaz de manejar inconsistencias en APIs financieras (Yahoo Finance) y limpiar datos faltantes.
* ✅ **Automated Reporting:** Generación de Fichas Técnicas de Riesgo (`.txt`) con interpretación de negocio para VaR y CVaR (Expected Shortfall).

---

## 🛠 Tech Stack

El proyecto implementa un stack científico enfocado en performance y reproducibilidad:

### Core & Math

### Data Engineering & Ingestion

---

## 🧮 Quant Methodology

El motor simula trayectorias de precios basadas en el **Movimiento Browniano Geométrico (GBM)** adaptado para colas pesadas.

La dinámica del precio  se modela como:

Donde el término de innovación estocástica  se construye mediante:

1. **Ajuste de Distribución:** Se estima el parámetro  (grados de libertad) de los retornos históricos logarítmicos.
2. **Generación de Shocks:** Se generan variables aleatorias  y .
3. **Transformación t-Student:**


4. **Inducción de Correlación:** Se aplica la matriz de Cholesky  para correlacionar los shocks independientes:



---

## 📂 Project Structure

La arquitectura sigue el patrón de separación de responsabilidades (SoC) para facilitar el mantenimiento y escalabilidad:

```bash
CL-RiskEngine/
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   └── loader.py       # Ingesta, limpieza y cálculo de Log-Returns
│   ├── models/
│   │   ├── __init__.py
│   │   └── monte_carlo.py  # Motor matemático (Cholesky + t-Student)
│   └── utils/
│       ├── __init__.py
│       └── reporter.py     # Cálculo de PnL y Generación de Reportes TXT
├── output/                 # Carpeta destino para los reportes generados
├── main.py                 # Orquestador del flujo de ejecución
├── requirements.txt        # Dependencias del entorno
└── README.md               # Documentación Técnica

```

---

## 🏁 Getting Started

### Prerrequisitos

* Python 3.8 o superior.
* Conexión a internet (para descarga de datos de mercado).

### Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/CL-RiskEngine.git
cd CL-RiskEngine

```

2. **Crear entorno virtual**

```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

```

3. **Instalar dependencias**

```bash
pip install yfinance pandas numpy scipy

```

4. **Ejecutar el Motor**

```bash
python main.py

```

---

## 📉 Visual Results

El sistema genera automáticamente un reporte ejecutivo en la carpeta `output/`.

**Ejemplo de Salida (Risk Report):**

```text
==================================================
🛡️ CL-RISKENGINE | REPORTE EJECUTIVO
Fecha: 2026-02-06_18-07
==================================================

ACTIVOS: ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
MODELO: Monte Carlo Estructurado (t-Student)
--------------------------------------------------
Métrica                      Valor    
Horizonte Temporal           252 días
Simulaciones                 5000
VaR 95% (Confianza)          -29.89%
CVaR 95% (Déficit Esp.)      -38.53%
VaR 99% (Estrés)             -44.56%
CVaR 99% (Colapso)           -50.51%
--------------------------------------------------

```

---

## ⚠️ Disclaimer

Este software es una prueba de concepto (PoC) para **investigación académica y desarrollo de portafolio**. No constituye asesoramiento financiero. Los modelos estocásticos se basan en parámetros históricos que no garantizan rendimientos futuros.

---

<div align="center">
<p>Developed with 💻 & ☕ by <strong>Canis chilensis</strong></p>
<p>
<a href="#">
<img src="[https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&logoColor=white](https://www.google.com/search?q=https://img.shields.io/badge/LinkedIn-blue%3Fstyle%3Dflat%26logo%3Dlinkedin%26logoColor%3Dwhite)" alt="LinkedIn" />
</a>
<a href="#">
<img src="[https://img.shields.io/badge/GitHub-black?style=flat&logo=github&logoColor=white](https://www.google.com/search?q=https://img.shields.io/badge/GitHub-black%3Fstyle%3Dflat%26logo%3Dgithub%26logoColor%3Dwhite)" alt="GitHub" />
</a>
</p>
</div>