"""
Ejecutor del agente con sesiones persistentes configuradas explícitamente.
Usa DatabaseSessionService para almacenar sesiones en una base de datos.
"""
import asyncio
from google.adk.sessions import DatabaseSessionService
from google.adk import Context
from google.adk.agents.invocation_context import InvocationContext
from .agent import root_agent


async def run_agent_with_persistent_sessions(
    user_input: str,
    db_url: str = "sqlite+aiosqlite:///./agent_data.db",
    app_name: str = "agente_adk_nivel8",
    user_id: str = "default_user",
):
    """
    Ejecuta el agente con sesiones persistentes usando DatabaseSessionService.
    
    Args:
        user_input: El input del usuario para el agente
        db_url: URL de la base de datos (por defecto SQLite)
        app_name: Nombre de la aplicación para agrupar sesiones
        user_id: ID del usuario
    """
    # Inicializar el servicio de sesión
    session_service = DatabaseSessionService(db_url=db_url)
    
    async with session_service:
        # Crear una sesión persistente
        session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
        )
        
        print(f"✅ Sesión creada: {session.session_id}")
        print(f"📦 Estado inicial: {session.state}")
        
        # Crear el contexto de invocación con la sesión
        invocation_context = InvocationContext(
            session_service=session_service,
            session=session,
        )
        
        # Crear el contexto del agente
        context = Context(invocation_context=invocation_context)
        
        # Ejecutar el agente
        print(f"\n🚀 Ejecutando agente con input: {user_input}\n")
        async for event in root_agent.run(ctx=context, node_input=user_input):
            if event.output:
                print(f"📤 Salida: {event.output}")
        
        print(f"\n✅ Ejecución completada")
        print(f"📦 Estado final: {session.state}")
        
        return session


if __name__ == "__main__":
    # Ejemplo de uso
    asyncio.run(
        run_agent_with_persistent_sessions(
            user_input="Hola, ¿cuántas horas son?",
        )
    )
