# 🦁 CL-RiskEngine: High-Performance Monte Carlo Simulator

![Status](https://img.shields.io/badge/STATUS-ACTIVE-success?style=for-the-badge)
![Python](https://img.shields.io/badge/PYTHON-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)

> **Motor de Riesgo Financiero Vectorizado** para el mercado chileno y global. Implementa simulación estocástica avanzada con detección de "Colas Gordas" (Fat Tails) y optimización de portafolios (Markowitz).

---

## 📋 Table of Contents
1. [About the Project](#-about-the-project)
2. [Tech Stack](#-tech-stack)
3. [Quant Methodology](#-quant-methodology)
4. [Project Structure](#-project-structure)
5. [Getting Started](#-getting-started)
6. [Visual Results](#-visual-results)

---

## 🚀 About The Project

**CL-RiskEngine** nace de la necesidad de modelar riesgos en mercados emergentes donde la "Normalidad Gaussiana" no existe. A diferencia de los simuladores académicos básicos, este motor integra ingeniería de datos real y matemáticas robustas.

### Key Features
* ✅ **Fat-Tail Awareness:** Detecta automáticamente la *Leptocurtosis* y cambia de Gaussiana a **t-Student Multivariada** ($\nu \approx 2.8$ para S&P500).
* ✅ **High-Performance Computing:** Núcleo escrito con `numpy.einsum` para álgebra lineal vectorizada (10k escenarios en <1s).
* ✅ **Correlation Healing:** Inducción de correlaciones vía **Cholesky** con reparación espectral para matrices no definidas positivas.
* ✅ **Architecture Hexagonal:** Separación limpia entre Ingesta (ELT), Calibración (JSON) y Simulación (Monte Carlo).

---

## 🛠 Tech Stack

El proyecto utiliza un stack científico de última generación. Haz clic en los badges para ver la documentación:

### Core & Math
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-654FF0?style=for-the-badge&logo=scipy&logoColor=white)](https://scipy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

### Data Engineering & APIs
[![Yahoo Finance](https://img.shields.io/badge/Yahoo_Finance-6001D2?style=for-the-badge&logo=yahoo&logoColor=white)](https://pypi.org/project/yfinance/)
[![BCCH API](https://img.shields.io/badge/Banco_Central_Chile-002D56?style=for-the-badge)](https://github.com/Titogjs/bcchapi)
[![Parquet](https://img.shields.io/badge/Apache_Parquet-C92919?style=for-the-badge&logo=apache&logoColor=white)](https://parquet.apache.org/)

### Visualization & Analysis
[![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)](https://matplotlib.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white)](https://jupyter.org/)

---

## 🧮 Quant Methodology

El motor se basa en la Ecuación Diferencial Estocástica (SDE) del Movimiento Browniano Geométrico modificado:

$$dS_t = (r - 0.5\sigma^2)S_t dt + \sigma S_t dZ_t$$

Donde la innovación estocástica $dZ_t$ se modela mediante **t-Student normalizada** para capturar eventos extremos:

1.  **Calibración MLE:** Se obtienen los grados de libertad $\nu$ históricos para cada activo.
2.  **Normalización:** $Z = t_\nu \cdot \sqrt{\frac{\nu-2}{\nu}}$ (para preservar la varianza unitaria).
3.  **Correlación:** $Z_{corr} = Z \cdot L^T$ (donde $L$ es la matriz de Cholesky).

---

## 📂 Project Structure

```bash
CL-RiskEngine/
├── data/
│   ├── 01_bronze/          # Raw Parquet files (BCCH + Yahoo)
│   └── 02_silver/          # Log-Returns & Clean Data
├── notebooks/
│   ├── 01_eda_market_data.ipynb       # Ingesta, Cleaning & Jarque-Bera Tests
│   └── 02_monte_carlo_simulation.ipynb # Simulación Vectorizada & Markowitz
├── risk_engine_config.json # 🧠 The Brain: Matriz Sigma, Mu & Nu parameters
├── requirements.txt        # Dependencias
└── README.md               # You are here

```

---

## 🏁 Getting Started

### Prerrequisitos

* Python 3.10 o superior
* Claves de API del Banco Central (opcional, si usas datos cacheados)

### Instalación

1. **Clonar el repositorio**
```bash
git clone [https://github.com/tu-usuario/CL-RiskEngine.git](https://github.com/tu-usuario/CL-RiskEngine.git)

```

2. **Activar entorno virtual**
```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

```

3. **Instalar librerías**
```bash
pip install -r requirements.txt

```

---

## 📉 Visual Results

### 1. Simulación de Escenarios (t-Student)

*Proyección de 1,000 caminos posibles para SQM-B considerando colas pesadas.*

### 2. Frontera Eficiente (Markowitz Bullet)

*Optimización dinámica de portafolio Riesgo vs Retorno.*

---

## ⚠️ Disclaimer

This project is for **educational and research purposes**. It is not financial advice. The models assume historical parameters which may not predict future performance.

---

<div align="center">
<p>Developed with ❤️ by <strong> Canis chilensis</strong></p>
<p>
<a href="https://www.google.com/search?q=https://linkedin.com/in/gvidalastudillo">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/LinkedIn-blue%3Fstyle%3Dflat%26logo%3Dlinkedin%26logoColor%3Dwhite" alt="LinkedIn" />
</a>
<a href="https://www.google.com/search?q=https://github.com/canischilensis">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/GitHub-black%3Fstyle%3Dflat%26logo%3Dgithub%26logoColor%3Dwhite" alt="GitHub" />
</a>
</p>
</div>

```

```