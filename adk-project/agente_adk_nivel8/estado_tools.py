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