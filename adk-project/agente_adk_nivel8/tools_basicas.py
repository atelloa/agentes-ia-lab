from datetime import datetime
from typing import Union

def obtener_hora() -> str:
    """Devuelve la hora local actual."""
    ahora = datetime.now()
    return ahora.strftime("Son las %H:%M:%S")

def sumar(a: int, b: int) -> Union[int, str]:
    """Suma dos números enteros entre 0 y 100.
    
    Args:
        a: Número entero entre 0-100.
        b: Número entero entre 0-100.
    
    Returns:
        La suma de a + b, o un mensaje de error si la validación falla.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        return "Error: La tool sumar solo acepta enteros."
    if not (0 <= a <= 100) or not (0 <= b <= 100):
        return "Error: La tool sumar solo acepta números entre 0 y 100."
    return a + b