# 🦁 CL-RiskEngine: Distributed Financial Risk Platform

> **Plataforma de Riesgo Financiero Distribuida**. Implementa simulación Monte Carlo paralela mediante el **Modelo de Actores (Ray)**, soportada por una arquitectura de datos **Lakehouse (ELT)** y modelos matemáticos modulares (Strategy Pattern).

---

## 📋 Table of Contents

1. [About the Project](https://www.google.com/search?q=%23-about-the-project)
2. [Tech Stack](https://www.google.com/search?q=%23-tech-stack)
3. [Quant Methodology](https://www.google.com/search?q=%23-quant-methodology)
4. [Architecture & Data Flow](https://www.google.com/search?q=%23-architecture--data-flow)
5. [Project Structure](https://www.google.com/search?q=%23-project-structure)
6. [Getting Started](https://www.google.com/search?q=%23-getting-started)
7. [Performance](https://www.google.com/search?q=%23-performance)

---

## 🚀 About The Project

**CL-RiskEngine v3.0** marca la transición de un script monolítico a un sistema de ingeniería financiera escalable. Diseñado para portafolios de alta volatilidad, el sistema abandona el procesamiento secuencial para adoptar un **Cluster de Cómputo Distribuido** capaz de procesar miles de escenarios complejos en segundos.

### Key Features (v3.0)

* ⚡ **Distributed Computing:** Motor impulsado por **Ray**, utilizando el *Actor Model* para paralelizar simulaciones a través de todos los núcleos de CPU disponibles (Map-Reduce).
* 💾 **Data Lakehouse Architecture:** Pipeline **ELT** robusto que ingesta datos crudos (Capa Bronce/CSV) y los transforma a formato columnar optimizado (Capa Plata/Parquet) para lectura de alta velocidad.
* 🧩 **Strategy Pattern Design:** Desacoplamiento total entre el orquestador y la lógica matemática. Permite intercambiar modelos (t-Student vs GBM vs Heston) sin modificar el núcleo del sistema.
* ✅ **Fat-Tail Modeling:** Implementación de **t-Student Multivariada** con *Clamping* de seguridad () para evitar desbordamientos numéricos en escenarios de crisis.
* ✅ **Correlation Preservation:** Uso de **Descomposición de Cholesky** () para mantener la estructura de dependencia entre activos.

---

## 🛠 Tech Stack

### Distributed Core

* **Ray:** Orquestación de actores y paralelismo de memoria compartida.
* **Multiprocessing:** Detección dinámica de hardware.

### Data Engineering

* **Pandas & NumPy:** Manipulación vectorial.
* **Apache Parquet (PyArrow):** Almacenamiento columnar eficiente (Silver Layer).
* **yFinance:** Gateway de datos de mercado.

### Math & Quant

* **SciPy:** Ajuste estadístico de distribuciones (MLE).
* **Monte Carlo:** Simulación estocástica vectorizada.

---

## 🧮 Quant Methodology

El motor simula trayectorias de precios basadas en una **Cópula t-Student** para capturar eventos de cola (Cisnes Negros).

La dinámica del precio  se modela como:

Donde la innovación estocástica distribuida  sigue el proceso:

1. **Calibración:** Se estima  (grados de libertad) y la matriz de covarianza .
2. **Safety Clamping:** Se restringe  para evitar varianza infinita: .
3. **Generación de Shocks:**


4. **Correlación (Cholesky):** 

---

## 🏗 Architecture & Data Flow

El sistema sigue una arquitectura de flujo de datos unidireccional y capas de abstracción:

1. **Ingesta (Loader):** Descarga  `data/bronze/` (CSV Auditables).
2. **Transformación:** Limpieza + Log-Returns  `data/silver/` (Parquet Optimizado).
3. **Entrenamiento (Driver):** El proceso principal ajusta el modelo matemático.
4. **Distribución (Ray Cluster):** Se clona la estrategia a  Actores (Workers).
5. **Reducción:** Se fusionan los tensores de resultados `(Sims, Time, Assets)`.

---

## 📂 Project Structure

```bash
CL-RiskEngine/
├── data/                   # 🛑 GIT IGNORED (Lakehouse Local)
│   ├── bronze/             # Raw CSVs (Auditoría)
│   └── silver/             # Optimized Parquet (Performance)
├── output/                 # Reportes de Riesgo (.txt)
├── src/
│   ├── data/
│   │   └── loader.py       # Pipeline ELT (Extract-Load-Transform)
│   ├── models/
│   │   ├── base.py         # Interface (Strategy Pattern)
│   │   ├── student_t.py    # Lógica Matemática (Concrete Strategy)
│   │   ├── distributed.py  # ⚡ Ray Actor & Cluster Manager
│   │   └── monte_carlo.py  # (Legacy) Motor Local
│   └── utils/
│       └── reporter.py     # Cálculo de VaR/CVaR
├── main.py                 # 🚀 Entrypoint Orquestador
├── requirements.txt        # Dependencias (incl. Ray)
└── README.md               # Documentación

```

---

## 🏁 Getting Started

### Prerrequisitos

* Python 3.10+
* RAM suficiente para levantar el cluster de Ray (min 4GB recomendado).

### Instalación y Ejecución

1. **Clonar y Preparar Entorno**
```bash
git clone https://github.com/tu-usuario/CL-RiskEngine.git
cd CL-RiskEngine
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

```


2. **Ejecutar la Plataforma**
```bash
python main.py

```


*El sistema detectará automáticamente sus núcleos de CPU e iniciará el Cluster Ray.*

---

## 📊 Performance

Comparativa de rendimiento (Benchmark en 4-Core CPU):

| Versión | Arquitectura | Sims/Seg | Tiempo (5k Sims) | Status |
| --- | --- | --- | --- | --- |
| v1.0 | Script Python Puro | ~200 | 25.4s | ❌ Deprecated |
| v2.0 | Docker Monolith | ~850 | 5.8s | ⚠️ Legacy |
| **v3.0** | **Ray Distributed** | **~2100** | **2.3s** | ✅ **Production** |

---

## ⚠️ Disclaimer

Este software es una herramienta de ingeniería financiera para **investigación y análisis cuantitativo**. Los resultados de modelos estocásticos (VaR/CVaR) son probabilidades, no certezas. No constituye asesoramiento de inversión.

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