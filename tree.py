import os

def crear_estructura_api():
    rutas = [
        "src/api",          # Aquí vivirá la aplicación FastAPI
        "src/api/routers",  # Para separar endpoints (ej. /risk, /backtest)
        "src/api/schemas",  # Modelos Pydantic (Validación de datos de entrada/salida)
    ]

    for ruta in rutas:
        os.makedirs(ruta, exist_ok=True)
        # Crear __init__.py para que sea un paquete importable
        with open(os.path.join(ruta, "__init__.py"), "w") as f:
            pass

    print("✅ Estructura de API creada en 'src/api/'.")

if __name__ == "__main__":
    crear_estructura_api()