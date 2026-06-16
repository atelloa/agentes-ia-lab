import json
from pathlib import Path
import re


MEMORIA_PATH = Path(__file__).parent / "memoria_adk.json"


def cargar_memoria() -> dict:
    if MEMORIA_PATH.exists():
        with open(MEMORIA_PATH, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return {}


def guardar_memoria(memoria: dict) -> None:
    with open(MEMORIA_PATH, "w", encoding="utf-8") as archivo:
        json.dump(memoria, archivo, ensure_ascii=False, indent=4)

def guardar_nombre(nombre: str) -> str:
    """Guarda el nombre del usuario en memoria persistente.
    
    Validaciones de negocio:
    - No puede estar vacío
    - Solo letras, números y espacios
    - Máximo 50 caracteres
    
    Args:
        nombre: Nombre a guardar.
    
    Returns:
        Mensaje de confirmación o error.
    """
    # Validación 1: No vacío
    if not nombre or nombre.strip() == "":
        return "Error: El nombre no puede estar vacío."
    
    # Validación 2: Solo letras, números y espacios
    if not re.match(r"^[a-záéíóúñA-ZÁÉÍÓÚÑ0-9\s]+$", nombre):
        return "Error: El nombre solo puede contener letras, números y espacios."
    
    # Validación 3: Máximo 50 caracteres
    if len(nombre) > 50:
        return "Error: El nombre no puede exceder 50 caracteres."
    
    # Si pasa todas las validaciones → guardar
    memoria = cargar_memoria()
    memoria["nombre"] = nombre.strip()
    guardar_memoria(memoria)
    return f"Guardé en memoria persistente que te llamas {nombre.strip()}."


def consultar_nombre() -> str:
    """Consulta el nombre del usuario guardado en memoria persistente."""
    memoria = cargar_memoria()

    if "nombre" in memoria:
        return f"Te llamas {memoria['nombre']}."

    return "Todavía no sé cómo te llamas."