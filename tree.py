import os
import sys

def create_project_structure():
    # Definimos el nombre del proyecto
    base_path = "CL-RiskEngine"
    
    # 1. VALIDACIÓN DE SEGURIDAD: Verificar si el proyecto ya existe
    if os.path.exists(base_path):
        print(f"❌ ERROR: El directorio '{base_path}' ya existe.")
        print("Abortando para evitar conflictos con archivos existentes.")
        sys.exit(1) # Salida con código de error

    # Definición de la estructura basada en el Informe Platinum
    folders = [
        "config",
        "data/01_bronze",
        "data/02_silver",
        "data/03_gold",
        "notebooks",
        "src/core/domain",
        "src/core/interfaces",
        "src/core/strategy",
        "src/adapters/market_data",
        "src/adapters/repositories",
        "src/orchestration",
        "tests/unit",
        "tests/integration"
    ]
    
    files = {
        "config/settings.py": "# Global Settings - Singleton Pattern\n",
        "src/core/interfaces/market_data.py": "# Market Data Port (Hexagonal Architecture)\n",
        "src/core/strategy/base_model.py": "# Strategy Interface (Strategy Pattern)\n",
        "src/orchestration/ray_cluster.py": "# Ray Initialization (Distributed Computing)\n",
        "main.py": "# Entry Point\n",
        "README.md": "# CL-RiskEngine\n\nProyecto de simulación de riesgo financiero de alto rendimiento."
    }

    try:
        print(f"🏗️ Iniciando creación de estructura para: {base_path}...")
        
        for folder in folders:
            path = os.path.join(base_path, folder)
            os.makedirs(path, exist_ok=False) # 'exist_ok=False' lanza FileExistsError si ya existe
            
            # Crear __init__.py para que Python reconozca los paquetes
            with open(os.path.join(path, "__init__.py"), "w") as f:
                pass

        for file_path, content in files.items():
            full_path = os.path.join(base_path, file_path)
            with open(full_path, "w") as f:
                f.write(content)

        print(f"✅ ÉXITO: Estructura de CL-RiskEngine creada y blindada.")
        
    except FileExistsError as e:
        print(f"❌ ERROR DE ARCHIVO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_project_structure()