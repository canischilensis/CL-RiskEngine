# Informe Técnico de Justificación de Infraestructura: Modernización de la Plataforma de Datos para Riesgo de Mercado

### 1\. Resumen Ejecutivo

Este informe técnico detalla la arquitectura propuesta para el nuevo sistema de riesgo de mercado. La estrategia se aleja de los enfoques monolíticos tradicionales para adoptar un paradigma **Data Lakehouse** moderno. Esta decisión no es una concesión a las tendencias, sino una respuesta de ingeniería necesaria ante la alta dimensionalidad, volatilidad y requisitos de cumplimiento regulatorio inherentes a los datos financieros actuales. La propuesta integra patrones **ELT (Extract-Load-Transform)** y almacenamiento columnar **Parquet**, respaldada por literatura técnica autorizada en ingeniería de datos, arquitecturas financieras y sistemas de Machine Learning. El objetivo es garantizar una ventaja competitiva sostenible mediante la reducción del *Time-to-Insight* y la optimización del Costo Total de Propiedad (TCO).

### 2\. Fundamentos de la Arquitectura: Convergencia hacia el Data Lakehouse

El ecosistema de datos financieros se caracteriza por su "alta dimensionalidad" y "múltiples jerarquías", como las estructuras de subsidiarias o los desgloses de balances complejos, que requieren una gestión flexible pero rigurosa (Khraisha, 2027). Los enfoques tradicionales de Data Warehouse (DWH) y Data Lake aislados resultan insuficientes para un sistema de riesgo que debe procesar tanto la agilidad de datos no estructurados (noticias, sentimiento) como la precisión transaccional (precios, operaciones).  
Proponemos una arquitectura unificada **Lakehouse**. Este enfoque desacopla el almacenamiento del cómputo, permitiendo escalar los recursos de procesamiento bajo demanda durante los picos de volatilidad del mercado, un principio clave de la arquitectura moderna de datos (Reis & Housley, 2022). Además, el Lakehouse combina la flexibilidad económica del almacenamiento de objetos del Data Lake con las capacidades de gestión y transacciones ACID del Data Warehouse (Tranquillin et al., 2024).

### 3\. Estrategia de Gestión de Esquemas: Agilidad frente a Volatilidad

La elección entre *Schema-on-Read* y *Schema-on-Write* define la capacidad de reacción del negocio ante nuevos instrumentos financieros.

#### 3.1. El Costo de la Rigidez (Schema-on-Write)

En el modelo tradicional de DWH, el esquema se define estrictamente antes de la ingesta. Si bien esto garantiza consistencia, introduce una rigidez peligrosa. Cada vez que una fuente de datos cambia (ej. un nuevo *feed* de derivados con campos exóticos), se requiere una reingeniería costosa de los procesos de carga, ralentizando la innovación (Reis & Housley, 2022).

#### 3.2. La Ventaja Competitiva (Schema-on-Read)

Recomendamos un enfoque híbrido que priorice **Schema-on-Read** para las capas de ingesta (Bronze Layer). Esto permite aterrizar datos crudos, como feeds en tiempo real o archivos JSON complejos, sin una validación estructural bloqueante inmediata.

* **Justificación de Negocio:** Imaginemos la integración de un nuevo *feed* de precios de derivados complejo y semi-estructurado. Con *Schema-on-Read*, podemos ingerir estos datos inmediatamente para que los *quants* exploren patrones, evitando cuellos de botella de ingeniería.  
* **Mitigación de Riesgos:** Para evitar que el lago se convierta en un "Data Swamp" (pantano de datos), aplicamos esquemas estrictos y gobernanza solo en las capas curadas (Gold Layer) destinadas al cálculo del VaR (Value at Risk) y reporte regulatorio (Reis & Housley, 2022).

### 4\. Almacenamiento y Formato: La Decisión por Apache Parquet

El almacenamiento eficiente es crítico para el rendimiento de las consultas analíticas (OLAP). Desaconsejamos el uso de formatos orientados a filas como CSV o JSON para la capa analítica en favor de **Apache Parquet**.

#### 4.1. Eficiencia en E/S y Consultas Analíticas

Los modelos de riesgo requieren escanear millones de registros históricos, pero a menudo solo unas pocas columnas específicas (ej. precio\_cierre, volatilidad\_implícita). Los formatos *row-major* son ineficientes aquí, ya que obligan a leer la fila completa, desperdiciando ancho de banda y E/S. Parquet, al ser un formato **columnar**, permite a los motores de consulta leer solo los atributos necesarios (proyección de columnas) y saltar bloques de datos irrelevantes (predicados *pushdown*). Esto optimiza drásticamente la velocidad de consulta y es el estándar para sistemas analíticos modernos (Reis & Housley, 2022).

#### 4.2. Compresión y Costos

Dado que los datos financieros históricos crecen exponencialmente, la eficiencia del almacenamiento es vital. Parquet ofrece esquemas de compresión superiores al agrupar tipos de datos homogéneos en cada columna. Esto reduce significativamente los costos de almacenamiento en la nube y la latencia de red durante la transferencia de datos, un factor crítico en arquitecturas distribuidas (Tranquillin et al., 2024).

### 5\. Estrategia de Procesamiento: Transición de ETL a ELT

La arquitectura propuesta abandona los pipelines ETL (Extract-Transform-Load) tradicionales en favor de un enfoque **ELT (Extract-Load-Transform)**.

#### 5.1. Preservación del Dato Crudo y Auditoría

En finanzas, la trazabilidad es obligatoria. En un ETL tradicional, las transformaciones ocurren antes de la carga; si la lógica de negocio tiene un error, los datos originales pueden perderse irrecuperablemente. Con ELT, cargamos los datos tal cual llegan al Lakehouse. Esto garantiza que siempre podamos "reproducir" la historia y auditar la transformación desde la fuente hasta el reporte final, un requisito esencial para la integridad del dato financiero (Khraisha, 2027).

#### 5.2. Escalabilidad y FinOps

El modelo ELT aprovecha la potencia de cómputo masiva y elástica de la nube moderna para realizar transformaciones. En lugar de mantener servidores de transformación dedicados que están inactivos gran parte del tiempo, utilizamos recursos bajo demanda. Esto alinea el gasto tecnológico con el valor generado, pagando por la transformación solo cuando se ejecuta, lo cual es un principio fundamental de las operaciones financieras en la nube (FinOps) (Reis & Housley, 2022).

### 6\. Calidad del Dato y Machine Learning en Series de Tiempo

El pipeline no solo alimenta reportes, sino también modelos predictivos de riesgo. Aquí, la calidad del dato es sinónimo de estabilidad financiera.

#### 6.1. Prevención de Data Leakage (Fuga de Datos)

Los datos financieros están altamente correlacionados en el tiempo. Huyen (2022) advierte sobre el peligro crítico del *data leakage* al entrenar modelos; dividir datos aleatoriamente en lugar de cronológicamente puede filtrar información futura al modelo, creando resultados artificialmente buenos que fallan en producción. Nuestra infraestructura debe imponer particionamiento estricto por tiempo (ej. /año/mes/día/) para garantizar simulaciones de *backtesting* honestas y robustas.

#### 6.2. Semántica y Linaje

La infraestructura debe incluir un catálogo de datos robusto que gestione metadatos y linaje. Los campos financieros tienen "semánticas de dominio" complejas (ej. diferenciación entre normas IFRS vs. GAAP o precios *real-time* vs. *end-of-day*). Sin un gobierno de datos claro que defina estas semánticas en el Lakehouse, el riesgo de interpretaciones erróneas en los modelos se dispara (Khraisha, 2027).

### 7\. Conclusión y Recomendación

La adopción de una arquitectura **Data Lakehouse** con pipelines **ELT** y almacenamiento **Parquet** no es una opción tecnológica más, sino una necesidad estratégica para la gestión de riesgos moderna.

1. **Agilidad:** El enfoque *Schema-on-Read* nos permite integrar nuevas fuentes de datos financieros complejos en horas, no semanas.  
2. **Rendimiento:** El formato columnar Parquet asegura que las consultas analíticas masivas sean rápidas y eficientes en costos.  
3. **Robustez:** El diseño ELT asegura la preservación de los datos crudos para auditoría y re-procesamiento, mitigando riesgos operativos.  
4. **Inteligencia:** La infraestructura está preparada para soportar flujos de trabajo de ML avanzados, evitando errores comunes como la fuga de datos temporales.

Esta arquitectura posiciona a nuestra organización para escalar sus capacidades analíticas de manera segura, cumpliendo con los estándares más exigentes de la ingeniería de datos actual (Reis & Housley, 2022; Tranquillin et al., 2024).

### 8\. Referencias Bibliográficas

* Huyen, C. (2022). *Designing Machine Learning Systems: An Iterative Process for Production-Ready Applications*. O'Reilly Media.  
* Khraisha, T. (2027). *Designing Financial Data Architectures: Patterns and Principles for AI, Analytics, and Operational Efficiency*. O'Reilly Media. \\\[Early Release\\\]  
* Reis, J., & Housley, M. (2022). *Fundamentals of Data Engineering: Plan and Build Robust Data Systems*. O'Reilly Media.  
* Tranquillin, M., Lakshmanan, V., & Tekiner, F. (2024). *Architecting Data and Machine Learning Platforms: Enable Analytics and AI-Driven Innovation in the Cloud*. O'Reilly Media.
