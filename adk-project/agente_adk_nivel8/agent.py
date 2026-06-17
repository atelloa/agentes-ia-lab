from google.adk.agents.llm_agent import Agent
from .tools_basicas import obtener_hora, sumar
from .memory_tools import guardar_nombre, consultar_nombre
from .estado_tools import guardar_nombre_sesion, consultar_nombre_sesion, activar_modo_debug, consultar_modo_debug, consultar_ultima_tool
from google.adk.tools import ToolContext

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
    tool_response: dict,
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
    model='gemini-3.1-flash-lite',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    before_tool_callback=log_antes_de_tool,
    after_tool_callback=log_despues_de_tool,
    tools=[obtener_hora, sumar, guardar_nombre, consultar_nombre, guardar_nombre_sesion, consultar_nombre_sesion, activar_modo_debug, consultar_modo_debug, consultar_ultima_tool],
)
