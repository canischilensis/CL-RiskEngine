# Usamos una imagen oficial de Python ligera pero compatible con compilación
FROM python:3.10-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias para compilar librerías científicas
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# 1. Copiar primero los requirements (Estrategia de Caché de Docker)
COPY requirements.txt .

# 2. Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiar todo el código fuente (respetando el .dockerignore)
COPY . .

# Crear carpetas necesarias para datos y logs
RUN mkdir -p data/bronze data/silver data/gold output

# Comando por defecto al iniciar el contenedor
# Ejecuta el orquestador principal
CMD ["python", "main.py"]