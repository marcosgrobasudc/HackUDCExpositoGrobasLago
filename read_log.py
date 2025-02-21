import json
from datetime import datetime

def guardar_interaccion(usuario, mensaje, emociones, archivo="registros.json"):
    """
    Guarda las consultas del usuario junto con las emociones detectadas y sus scores.
    """
    try:
        # Cargar datos previos si el archivo existe
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            datos = {}

        # Crear estructura del usuario si no existe
        if usuario not in datos:
            datos[usuario] = {"interacciones": [], "registros_diarios": {}}

        # Agregar la interacción
        datos[usuario]["interacciones"].append({
            "mensaje": mensaje,
            "emociones": emociones,
            "timestamp": datetime.now().isoformat()
        })

        # Guardar cambios en el archivo
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error guardando la interacción: {e}")

def guardar_registro_diario(usuario, registro, archivo="registros.json"):
    """
    Guarda un registro diario del usuario con la fecha actual.
    """
    try:
        # Cargar datos previos si el archivo existe
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            datos = {}

        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        # Crear estructura del usuario si no existe
        if usuario not in datos:
            datos[usuario] = {"interacciones": [], "registros_diarios": {}}
        
        # Guardar el registro diario
        datos[usuario]["registros_diarios"][fecha_actual] = registro
        
        # Guardar cambios en el archivo
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error guardando el registro diario: {e}")


if __name__ == "__main__":
    # Simulación de interacciones
    guardar_interaccion("Juan", "Hoy me siento increíble", {"feliz": 0.9, "emocionado": 0.7})
    guardar_interaccion("Ana", "Estoy un poco cansada", {"cansado": 0.8, "estresado": 0.6})
    
    # Simulación de registro diario
    guardar_registro_diario("Juan", "Hoy tuve un gran día en el trabajo.")
    guardar_registro_diario("Ana", "El día fue agotador, pero productivo.")
    
    # Mostrar el contenido del archivo
    with open("registros.json", "r", encoding="utf-8") as f:
        print(json.load(f))