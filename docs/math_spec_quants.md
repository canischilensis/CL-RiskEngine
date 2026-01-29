# Especificaciones Matemáticas y Computacionales de CL-RiskEngine

### 1\. Introducción

El presente documento consolida la especificación matemática definitiva para el núcleo de cálculo de CL-RiskEngine. Tras la revisión de los borradores anteriores y una reevaluación exhaustiva de la literatura de referencia —específicamente Hilpisch (2018)— se han subsanado las lagunas teóricas identificadas, particularmente en lo referente al modelado de dependencia entre activos.  
Esta especificación es normativa para la implementación del pipeline de producción.

### 2\. Definición del Modelo: Movimiento Browniano Geométrico (GBM)

Para la simulación de trayectorias de precios de activos en un entorno de riesgo de mercado, adoptamos el **Movimiento Browniano Geométrico (GBM)** como el modelo estocástico estándar. Este modelo asume que los rendimientos logarítmicos están distribuidos normalmente, lo cual es la base teórica del modelo Black-Scholes-Merton 1\.

#### 2.1. Ecuación Diferencial Estocástica (SDE)

La dinámica del precio del activo $S\_t$ se describe mediante la siguiente Ecuación Diferencial Estocástica (SDE):  
$$ dS_t = rS_t dt + \sigma S_t dZ_t $$

Donde:

* $r$ es la tasa libre de riesgo constante.  
* $\\sigma$ es la volatilidad constante del activo.  
* $Z\_t$ es un movimiento browniano estándar 2, 3\.

#### 2.2. Solución Discretizada (Esquema Exacto)

Aunque la SDE puede aproximarse mediante el esquema de Euler-Maruyama, el GBM posee una solución analítica exacta que evita el error de discretización en la variable de estado. Para el motor de simulación, utilizaremos la solución exacta en diferencias finitas sobre un intervalo de tiempo $\\Delta t$ (o $dt$).
La fórmula de transición para el precio del activo $S_t$ dado $S_{t-1}$ es: 

$$ S_t = S_{t-1} \exp\left(\left(r - \frac{1}{2}\sigma^2\right)dt + \sigma\sqrt{dt}z_t\right) $$  

Donde $z_t$ es una variable aleatoria extraída de una distribución normal estándar $\\mathcal{N}(0, 1)$ 4, 1\. Esta formulación garantiza la positividad de los precios y captura correctamente la propiedad log-normal del proceso 2\.

### 3\. Implementación Numérica: Vectorización

La viabilidad del CL-RiskEngine depende críticamente de la eficiencia computacional. Se prohíbe estrictamente el uso de bucles iterativos (for) nativos de Python para la generación de trayectorias.

#### 3.1. Justificación de Rendimiento

Las simulaciones de Monte Carlo requieren generar millones de números aleatorios y realizar operaciones algebraicas sobre ellos. Los bucles de Python introducen una sobrecarga significativa por iteración debido a la naturaleza interpretada del lenguaje.  
La **vectorización con NumPy** delega estas operaciones a código C precompilado y altamente optimizado. Según Hilpisch (2018), la diferencia de rendimiento es de varios órdenes de magnitud. Pruebas comparativas demuestran que operaciones matemáticas vectorizadas (como numpy.exp o numpy.sqrt) pueden reducir el tiempo de ejecución de \~1.6 segundos (en bucles puros) a \~88 milisegundos, una mejora de rendimiento crítica para sistemas de "Big Compute" 5, 6\.

#### 3.2. Especificación de Código

La implementación debe operar sobre matrices completas donde las filas representen pasos de tiempo y las columnas representen trayectorias simuladas simultáneas ($I$).  

```python
# Ejemplo conceptual basado en Hilpisch (2018) [7, 8]`  
S = np.zeros((M + 1, I))`  
S = S0  
rand = np.random.standard_normal((M, I))`

# El paso de tiempo t se calcula vectorizado para todas las I trayectorias`  
for t in range(1, M + 1):
    S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * rand[t - 1])
```

### 4\. Modelado de Dependencia: Matriz de Covarianza y Cholesky

En los informes preliminares se identificó una carencia respecto al modelado de portafolios multi-activo correlacionados 9\. Tras una revisión profunda de la obra de Hilpisch (2018), específicamente en la sección de modelos de volatilidad estocástica (Heston), se ha validado el método estándar para inducir correlación 10\.

#### 4.1. El Problema de la Independencia

La función np.random.standard\_normal genera variables aleatorias independientes. En un portafolio, los activos se mueven juntos (correlación). Simular activos independientemente subestimaría el riesgo sistémico del portafolio.

#### 4.2. Descomposición de Cholesky

Para inducir una estructura de correlación definida por una matriz de correlación $\\Sigma$ en una matriz de ruidos aleatorios no correlacionados $R$ (dimensiones: *factores x simulaciones*), utilizamos la Descomposición de Cholesky.  
Si $\sigma$ es una matriz definida positiva y simétrica, existe una matriz triangular inferior $L$ tal que:  
$$ \sigma = L L^T $$  
Esta matriz $L$ (matriz de Cholesky) se utiliza para transformar los aleatorios independientes.

#### 4.3. Algoritmo de Implementación

1. **Definir Matriz de Correlación:** Construir la matriz $\sigma$ de los activos 10\.  
2. **Calcular Cholesky:** Obtener $L$ usando numpy.linalg.cholesky(Sigma) 10\.  
3. **Generar Ruido Estándar:** Crear una matriz $Z$ de normales estándar independientes ($Z \sim \mathcal{N}(0, I)$) 11\.  
4. **Inducir Correlación:** Realizar el producto punto entre la matriz de Cholesky y la matriz de ruido aleatorio.

$$ Z_{corr} = L \cdot Z $$  
En la implementación de Hilpisch (2018), esto se visualiza explícitamente en la simulación de procesos correlacionados:  
```python
# Referencia: Hilpisch (2018), p. 365 [10, 11]`  
# corr_mat es la matriz de correlación definida`  
cho_mat = np.linalg.cholesky(corr_mat)` 

# ran_num son números aleatorios estándar independientes`  
# Se aplica el producto punto para correlacionarlos`  
ran = np.dot(cho_mat, ran_num[:, t, :])
```
Este procedimiento es matemáticamente obligatorio para cualquier simulación de portafolio dentro de CL-RiskEngine que involucre más de un factor de riesgo.


### 5\. Referencias Bibliográficas

* Dixon, M. F., Halperin, I., & Bilokon, P. (2020). *Machine Learning in Finance: From Theory to Practice*. Springer.  
* Hilpisch, Y. J. (2018). *Python for Finance: Mastering Data-Driven Finance* (2nd ed.). O'Reilly Media.