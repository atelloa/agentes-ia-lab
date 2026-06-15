import json
from pathlib import Path


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
    """Guarda el nombre del usuario en memoria persistente."""
    memoria = cargar_memoria()
    memoria["nombre"] = nombre
    guardar_memoria(memoria)
    return f"Recordaré que te llamas {nombre}."


def consultar_nombre() -> str:
    """Consulta el nombre del usuario guardado en memoria persistente."""
    memoria = cargar_memoria()

    if "nombre" in memoria:
        return f"Te llamas {memoria['nombre']}."

    return "Todavía no sé cómo te llamas."