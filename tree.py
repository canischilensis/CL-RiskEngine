import os

def crear_estructura():
    # definir la jerarquia de carpetas pa que esto no sea un chiquero
    estructura = [
        "CL-RiskEngine/src/data",       # pa bajr y limpir precios
        "CL-RiskEngine/src/models",     # aqui vive la logica monte carlo t-student
        "CL-RiskEngine/src/utils",      # herramientas varias, validaciones matematicas
        "CL-RiskEngine/tests",          # pa ver si el codigo aguanta o revienta
        "CL-RiskEngine/config",         # variables de entorno, pa no quemar credenciales
        "CL-RiskEngine/notebooks",      # pa hacer pruebas locas antes de pasarl a produccion
        "CL-RiskEngine/output",         # aqui caen los reportes txt que generamos
    ]

    # recorrer la lista y crear directo, sin miedo al exito
    for carpeta in estructura:
        os.makedirs(carpeta, exist_ok=True)
        # crear un __init__.py pa que python reconozca esto como paquete
        with open(os.path.join(carpeta, "__init__.py"), "w") as f:
            pass 
            
    print("✅ Estructura de carpetas lista. Ahora a mover el codigo pa dond corresponde.")

if __name__ == "__main__":
    crear_estructura()