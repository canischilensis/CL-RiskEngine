# ==========================================
# 🐍 ETAPA 1: BASE IMAGE
# ==========================================
# Usamos una imagen oficial de Python 3.10 versión "slim" (Debian)
# Esto reduce el tamaño final de la imagen drásticamente (de ~1GB a ~200MB)
FROM python:3.10-slim

# ==========================================
# ⚙️ VARIABLES DE ENTORNO
# ==========================================
# Evita la creación de archivos .pyc (innecesarios en contenedores)
ENV PYTHONDONTWRITEBYTECODE=1
# Asegura que los logs de Python se envíen directamente a la terminal (sin buffer)
ENV PYTHONUNBUFFERED=1
# Agrega el directorio actual al PYTHONPATH para evitar errores de importación
ENV PYTHONPATH=/app

# ==========================================
# 🛠 SISTEMA OPERATIVO Y DEPENDENCIAS
# ==========================================
WORKDIR /app

# Instalamos gcc (compilador C) por si alguna librería matemática lo requiere
# Limpiamos caché de apt para reducir tamaño
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ==========================================
# 📦 INSTALACIÓN DE LIBRERÍAS
# ==========================================
# Copiamos solo el requirements.txt primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos dependencias de Python (FastAPI, NumPy, etc.)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# 📂 CÓDIGO FUENTE
# ==========================================
# Copiamos el resto del código
COPY src/ ./src/
# Copiamos el script main (aunque usaremos la API, es bueno tenerlo)
COPY main.py .

# Creamos el directorio para los reportes TXT
RUN mkdir -p output

# ==========================================
# 🔐 SEGURIDAD (BEST PRACTICES)
# ==========================================
# Creamos un usuario sin privilegios root para ejecutar la app
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

# Cambiamos al usuario seguro
USER appuser

# ==========================================
# 🚀 PUNTO DE ENTRADA
# ==========================================
# Exponemos el puerto 8000 (estándar de FastAPI/Uvicorn)
EXPOSE 8000

# Comando por defecto al levantar el contenedor:
# Inicia el servidor Uvicorn apuntando a la API, escuchando en todas las interfaces (0.0.0.0)
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]