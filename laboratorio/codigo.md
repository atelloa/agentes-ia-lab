# Código del laboratorio de agentes IA

**Versión:** v1.0  
**Fecha de corte:** 2026-06-14  
**Propósito:** entregar a otra IA los archivos clave del proyecto ADK para continuar sin adivinar el estado del código.

---

## Nota crítica

Este archivo contiene el código reconstruido del estado actual del laboratorio.

El contexto conceptual está separado en:

```text
laboratorio_agentes_ia_ruta_v1.0.md
```

No compartir el archivo `.env` real ni la API key.

---

## Estructura actual del proyecto ADK

```text
agente_adk_nivel8/
  ├─ __init__.py
  ├─ .env
  ├─ agent.py
  ├─ tools_basicas.py
  ├─ memoria_tools.py
  ├─ estado_tools.py
  └─ memoria_adk.json
```

---

## Archivo: `tools_basicas.py`

```python
from datetime import datetime


def obtener_hora() -> str:
    """Devuelve la hora local actual.

    Returns:
        Hora local actual en formato HH:MM:SS.
    """
    ahora = datetime.now()
    return ahora.strftime("Son las %H:%M:%S")


def sumar(a: int, b: int) -> int:
    """Suma dos números enteros.

    Args:
        a: Primer número entero.
        b: Segundo número entero.

    Returns:
        Resultado de sumar a + b.
    """
    return a + b
```

Estado antes de continuar con Nivel 8G:

- `sumar()` todavía no tiene validación interna fuerte.
- La validación de tipos se hizo en `before_tool_callback`.
- El siguiente paso será mover una validación esencial dentro de `sumar()`.

---

## Archivo: `memoria_tools.py`

```python
import json
from pathlib import Path

MEMORIA_PATH = Path(__file__).parent / "memoria_adk.json"


def cargar_memoria() -> dict:
    """Carga la memoria persistente desde memoria_adk.json."""
    if MEMORIA_PATH.exists():
        with open(MEMORIA_PATH, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return {}


def guardar_memoria(memoria: dict) -> None:
    """Guarda la memoria persistente en memoria_adk.json."""
    with open(MEMORIA_PATH, "w", encoding="utf-8") as archivo:
        json.dump(memoria, archivo, ensure_ascii=False, indent=4)


def guardar_nombre(nombre: str) -> str:
    """Guarda el nombre del usuario en memoria persistente.

    Args:
        nombre: Nombre que se guardará de forma persistente.

    Returns:
        Mensaje de confirmación.
    """
    memoria = cargar_memoria()
    memoria["nombre"] = nombre
    guardar_memoria(memoria)
    return f"Recordaré de forma persistente que te llamas {nombre}."


def consultar_nombre() -> str:
    """Consulta el nombre guardado en memoria persistente.

    Returns:
        Nombre guardado o mensaje indicando que no existe.
    """
    memoria = cargar_memoria()
    nombre = memoria.get("nombre")

    if nombre is None:
        return "Todavía no sé cómo te llamas en memoria persistente."

    return f"En memoria persistente te llamas {nombre}."
```

---

## Archivo: `estado_tools.py`

```python
from google.adk.tools import ToolContext


def guardar_nombre_sesion(nombre: str, tool_context: ToolContext) -> str:
    """Guarda un nombre temporal en el estado de sesión ADK.

    Args:
        nombre: Nombre que se guardará en la sesión actual.

    Returns:
        Mensaje de confirmación.
    """
    tool_context.state["nombre_sesion"] = nombre
    return f"Guardé en session.state que tu nombre temporal es {nombre}."


def consultar_nombre_sesion(tool_context: ToolContext) -> str:
    """Consulta el nombre temporal guardado en el estado de sesión ADK.

    Returns:
        Nombre temporal guardado en la sesión actual.
    """
    nombre = tool_context.state.get("nombre_sesion")

    if nombre is None:
        return "No hay ningún nombre guardado en session.state."

    return f"En session.state tu nombre temporal es {nombre}."


def activar_modo_debug(tool_context: ToolContext) -> str:
    """Activa el modo debug temporal para la sesión actual.

    Returns:
        Mensaje de confirmación.
    """
    tool_context.state["modo_debug"] = True
    return "Modo debug activado para esta sesión."


def consultar_modo_debug(tool_context: ToolContext) -> str:
    """Consulta si el modo debug está activo en la sesión actual.

    Returns:
        Estado actual del modo debug.
    """
    modo_debug = tool_context.state.get("modo_debug", False)

    if modo_debug:
        return "El modo debug está activo en esta sesión."

    return "El modo debug no está activo en esta sesión."


def consultar_ultima_tool(tool_context: ToolContext) -> str:
    """Consulta la última tool registrada en el estado de sesión.

    Returns:
        Información de la última tool ejecutada durante la sesión actual.
    """
    ultima_tool = tool_context.state.get("ultima_tool")
    ultimos_args = tool_context.state.get("ultimos_args")
    ultima_respuesta = tool_context.state.get("ultima_respuesta_tool")

    if ultima_tool is None:
        return "Todavía no hay una última tool registrada en session.state."

    return (
        f"Última tool ejecutada: {ultima_tool}\n"
        f"Argumentos: {ultimos_args}\n"
        f"Respuesta: {ultima_respuesta}"
    )
```

---

## Archivo: `agent.py`

```python
from google.adk.agents.llm_agent import Agent
from google.adk.tools import ToolContext

from .tools_basicas import obtener_hora, sumar
from .memoria_tools import guardar_nombre, consultar_nombre
from .estado_tools import (
    guardar_nombre_sesion,
    consultar_nombre_sesion,
    activar_modo_debug,
    consultar_modo_debug,
    consultar_ultima_tool,
)


def log_antes_de_tool(
    tool,
    args: dict,
    tool_context: ToolContext,
):
    print(f"[CALLBACK before_tool] Tool solicitada: {tool.name}")
    print(f"[CALLBACK before_tool] Args: {args}")

    if tool.name == "sumar":
        a = args.get("a")
        b = args.get("b")

        if not isinstance(a, int) or not isinstance(b, int):
            return {
                "error": "La tool sumar solo acepta enteros.",
                "args_recibidos": args,
            }

    return None


def log_despues_de_tool(
    tool,
    args: dict,
    tool_context: ToolContext,
    tool_response,
):
    print(f"[CALLBACK after_tool] Tool ejecutada: {tool.name}")
    print(f"[CALLBACK after_tool] Args: {args}")
    print(f"[CALLBACK after_tool] Respuesta: {tool_response}")

    tools_no_trackear = {
        "consultar_ultima_tool",
    }

    if tool.name not in tools_no_trackear:
        tool_context.state["ultima_tool"] = tool.name
        tool_context.state["ultimos_args"] = args
        tool_context.state["ultima_respuesta_tool"] = str(tool_response)

    return None


root_agent = Agent(
    name="agente_adk_nivel8",
    model="gemini-3.1-flash-lite",
    description="Agente de laboratorio para aprender arquitectura de agentes IA.",
    instruction="""
Eres un agente de laboratorio para aprender arquitectura de agentes IA.

Usa las tools cuando el usuario pida acciones concretas.

Diferencia de memoria:
- Usa guardar_nombre y consultar_nombre cuando el usuario quiera memoria persistente.
- Usa guardar_nombre_sesion y consultar_nombre_sesion cuando el usuario mencione session.state, sesión, temporal o contexto actual.

Diferencia de diagnóstico:
- Usa consultar_ultima_tool cuando el usuario pregunte por la última tool ejecutada.
- Usa activar_modo_debug y consultar_modo_debug para modo debug temporal de sesión.
""",
    tools=[
        obtener_hora,
        sumar,
        guardar_nombre,
        consultar_nombre,
        guardar_nombre_sesion,
        consultar_nombre_sesion,
        activar_modo_debug,
        consultar_modo_debug,
        consultar_ultima_tool,
    ],
    before_tool_callback=log_antes_de_tool,
    after_tool_callback=log_despues_de_tool,
)
```

Notas:

- Si el entorno tiene otro `model` funcionando, mantenerlo.
- En la sesión se cambió de `gemini-2.5-flash` a `gemini-3.1-flash-lite` por límites de cuota.
- Si ADK no reconoce ese modelo en otro entorno, usar un modelo disponible con mayor RPD/RPM.

---

## Archivo: `.env`

No compartir la API key real.

Formato esperado:

```env
GOOGLE_API_KEY=pegar_aqui_la_key_real
```

---

## Archivo: `memoria_adk.json`

Ejemplo de contenido posible:

```json
{
  "nombre": "Álvaro"
}
```

Este archivo sí persiste después de reiniciar `adk run`.

---

## Comandos de validación usados

Desde la carpeta padre del paquete:

```bash
adk --version
adk run agente_adk_nivel8
adk web
```

Validaciones funcionales:

```text
qué hora es
suma 4 y 6
mi nombre es Álvaro
cómo me llamo
guarda en session state que mi nombre temporal es Álvaro
consulta mi nombre temporal de session state
activa el modo debug para esta sesión
consulta si el modo debug está activo
cuál fue la última tool ejecutada
```

---

## Estado exacto para continuar

```text
Nivel 8G — Validaciones y guardrails simples
Paso 0 conceptual completado.
Siguiente paso: Nivel 8G — Paso 1.
```

Siguiente acción técnica:

```text
Mover una validación esencial dentro de la tool sumar.
Regla didáctica: sumar solo acepta enteros entre 0 y 100.
```

Motivo:

```text
La validación en before_tool_callback solo protege llamadas vía ADK.
La validación dentro de sumar protege también llamadas directas desde Python.
```

# Fin de laboratorio_agentes_ia_codigo_v1.0.md
