from datetime import datetime

def obtener_hora() -> str:
    """Devuelve la hora local actual."""
    ahora = datetime.now()
    return ahora.strftime("Son las %H:%M:%S")


def sumar(a: int, b: int) -> int:
    """Suma dos números enteros y devuelve el resultado."""
    return a + b