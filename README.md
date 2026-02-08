Aquí tienes el **README.md** actualizado a la versión **v4.0.0 (Enterprise Edition)**.

Este documento refleja todos los hitos de ingeniería que hemos completado: **Dockerización**, **Capa Oro (Persistencia)**, **Tests Unitarios**, **Singleton** y el soporte polimórfico (**GBM + Student-t**).

---

# 🦁 CL-RiskEngine: Enterprise Financial Risk Platform

> **Plataforma de Riesgo Financiero "Production Ready"**. Sistema distribuido y containerizado que implementa simulación Monte Carlo (GBM & t-Student) sobre una arquitectura **Data Lakehouse Completa (Medallion)**, cumpliendo estándares de auditoría y portabilidad.

---

## 📋 Table of Contents

1. [About the Project](#-about-the-project)
2. [Tech Stack](#-tech-stack)
3. [Features & Architecture](#-features--architecture)
4. [Project Structure](#-project-structure)
5. [Getting Started (Docker)](#-getting-started-docker)
6. [Quant Methodology](#-quant-methodology)
7. [Performance](#-performance--evolution)

---

## 🚀 About The Project

**CL-RiskEngine v4.0** representa la madurez arquitectónica del sistema. Más allá del cálculo bruto, esta versión se enfoca en la **Ingeniería de Software Robusta (Compliance)**. Incorpora persistencia histórica para auditoría ("Time Travel"), configuración centralizada y despliegue agnóstico mediante contenedores, eliminando el problema de "funciona en mi máquina".

### Key Features (v4.0)

* 🐳 **Portable Deployment:** Empaquetado completo en **Docker** (Python Slim + Ray Cluster), garantizando reproducibilidad exacta del entorno de ejecución en cualquier infraestructura.
* 🏆 **Gold Layer Persistence:** Implementación de la Capa Oro del Data Lakehouse. Los resultados de riesgo (VaR/CVaR) se persisten incrementalmente en formato **Parquet**, permitiendo análisis históricos y auditoría de evolución del riesgo.
* ⚡ **Distributed Computing:** Motor impulsado por **Ray**, utilizando el *Actor Model* para paralelizar simulaciones a través de todos los núcleos de CPU disponibles (Map-Reduce).
* 🧩 **Polymorphic Models:** Arquitectura flexible (Strategy Pattern) que soporta múltiples motores matemáticos:
* **t-Student:** Para colas pesadas y cisnes negros (con *Safety Clamping*).
* **GBM (Geometric Brownian Motion):** Estándar de industria para benchmarking.


* 🧪 **Quality Assurance:** Suite de **Tests Unitarios** y validación de arquitectura (Singleton, Rutas, Lógica Matemática) integrada.

---

## 🛠 Tech Stack

### Infrastructure & DevOps

* **Docker & Docker Compose:** Orquestación de contenedores y volúmenes.
* **Ray:** Cómputo distribuido.
* **Git:** Control de versiones semántico.

### Data Engineering (Medallion Architecture)

* **Bronze:** CSV Crudos (Auditables).
* **Silver:** Parquet columnar (Optimizado para lectura).
* **Gold:** Parquet agregado (Métricas de Negocio Históricas).

### Core & Math

* **Python 3.10+:** Lenguaje base.
* **NumPy/Pandas:** Álgebra lineal y manipulación de datos.
* **SciPy:** Inferencia estadística (MLE).

---

## 🏗 Features & Architecture

El sistema implementa una arquitectura hexagonal estricta con flujo de datos unidireccional:

1. **Configuración (Singleton):** Carga centralizada de parámetros desde `src/config/settings.py`.
2. **Ingesta (Loader):** Descarga  `data/bronze/`  Limpieza  `data/silver/`.
3. **Distribución (Ray Cluster):** El `DistributedMonteCarlo` clona la estrategia matemática (GBM o t-Student) a  Actores.
4. **Reducción:** Fusión de tensores de resultados.
5. **Persistencia (Reporter):**
* Genera reporte ejecutivo `.txt` en `output/`.
* Escribe registro histórico en `data/gold/risk_metrics_history.parquet`.



---

## 📂 Project Structure

Estructura final aprobada para producción:

```bash
CL-RiskEngine/
├── Dockerfile                  # 🐳 Receta de la Imagen
├── docker-compose.yml          # 🐙 Orquestador y Volúmenes
├── requirements.txt            # Dependencias
├── main.py                     # 🚀 Entrypoint
├── tests/                      # 🧪 Suite de Pruebas
│   └── unit/
│       └── test_architecture.py
├── data/                       # 💾 Data Lakehouse (Montado en Volumen)
│   ├── bronze/                 # Raw Audit
│   ├── silver/                 # Clean Processing
│   └── gold/                   # 🏆 Historical Business Metrics
├── output/                     # Reportes Legibles (.txt)
└── src/
    ├── config/
    │   └── settings.py         # Singleton Configuration
    ├── data/
    │   └── loader.py           # ETL Pipeline
    ├── models/
    │   ├── base.py             # Interface Strategy
    │   ├── gbm.py              # Modelo Normal (Nuevo v4)
    │   ├── student_t.py        # Modelo Colas Pesadas
    │   └── distributed.py      # Ray Actor Manager
    └── utils/
        └── reporter.py         # Reporting & Gold Layer Logic

```

---

## 🏁 Getting Started (Docker)

La forma recomendada de ejecutar **CL-RiskEngine v4.0** es mediante Docker Compose. No requiere instalación de Python ni librerías en su máquina.

### 1. Clonar y Construir

```bash
git clone https://github.com/tu-usuario/CL-RiskEngine.git
cd CL-RiskEngine

# Levantar el entorno (Construye la imagen y ejecuta)
docker-compose up --build

```

### 2. Resultados

Gracias a los volúmenes de Docker, los resultados aparecerán mágicamente en su carpeta local:

* **Reporte:** `./output/risk_report_YYYY-MM-DD.txt`
* **Histórico:** `./data/gold/risk_metrics_history.parquet`

*Nota: Para verificar el historial acumulado, puede ejecutar:*

```bash
python -c "import pandas as pd; print(pd.read_parquet('data/gold/risk_metrics_history.parquet'))"

```

---

## 🧮 Quant Methodology

El motor soporta dos dinámicas estocásticas intercambiables:

### A. Modelo t-Student (Colas Pesadas)

Diseñado para estrés y cisnes negros.


* **Calibración:**  (grados de libertad) ajustado con *Safety Clamping* ().

### B. Modelo GBM (Geometric Brownian Motion)

Estándar de la industria (Black-Scholes assumptions).


* Utilizado para benchmarking y condiciones de mercado normales.

---

## 📊 Performance & Evolution

Evolución del rendimiento y capacidad del sistema:

| Versión | Arquitectura | Sims/Seg | Características Clave | Status |
| --- | --- | --- | --- | --- |
| v1.0 | Script Python | ~200 | Lógica básica | ❌ Deprecated |
| v2.0 | Docker API | ~850 | Microservicio Web | ⚠️ Legacy |
| v3.0 | Ray Distributed | ~2100 | Cómputo Paralelo | ✅ Stable |
| **v4.0** | **Enterprise** | **~2100** | **Docker + Gold Layer + Tests** | 🚀 **Production** |

---

## ⚠️ Disclaimer

Este software es una herramienta de ingeniería financiera para **investigación y análisis cuantitativo**. Los resultados de modelos estocásticos (VaR/CVaR) son probabilidades basadas en datos históricos, no garantías de rendimiento futuro.

---

<div align="center">
<p>Developed with 💻 & ☕ by <strong>Canis chilensis</strong></p>
<p>
<a href="#">
<img src="[https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&logoColor=white](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&logoColor=white)" alt="LinkedIn" />
</a>
<a href="#">
<img src="[https://img.shields.io/badge/GitHub-black?style=flat&logo=github&logoColor=white](https://img.shields.io/badge/GitHub-black?style=flat&logo=github&logoColor=white)" alt="GitHub" />
</a>
</p>
</div>