"""
Punto de entrada principal del agente con sesiones persistentes configuradas.
Uso: python -m agente_adk_nivel8
"""
import asyncio
import sys
from google.adk.sessions import DatabaseSessionService
from google.adk import Context
from google.adk.agents.invocation_context import InvocationContext
from .agent import root_agent


async def main():
    """Ejecuta el agente con sesiones persistentes."""
    
    # Configurar parámetros
    db_url = "sqlite+aiosqlite:///./agent_data.db"
    app_name = "agente_adk_nivel8"
    user_id = "default_user"
    
    # Leer input del usuario
    print("🤖 Agente ADK Nivel 8 - Con sesiones persistentes")
    print(f"📦 BD: {db_url}\n")
    
    try:
        user_input = sys.argv[1] if len(sys.argv) > 1 else input("Escribe tu mensaje: ")
    except EOFError:
        user_input = "Hola, ¿cuántas horas son?"
    
    # Inicializar el servicio de sesión
    session_service = DatabaseSessionService(db_url=db_url)
    
    async with session_service:
        # Crear una sesión persistente
        session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
        )
        
        print(f"✅ Sesión creada: {session.session_id}")
        
        # Crear el contexto de invocación con la sesión
        invocation_context = InvocationContext(
            session_service=session_service,
            session=session,
        )
        
        # Crear el contexto del agente
        context = Context(invocation_context=invocation_context)
        
        # Ejecutar el agente
        print(f"🚀 Ejecutando...\n")
        async for event in root_agent.run(ctx=context, node_input=user_input):
            if event.output:
                print(f"{event.output}")
        
        print(f"\n✅ Sesión guardada: {session.session_id}")


if __name__ == "__main__":
    asyncio.run(main())
