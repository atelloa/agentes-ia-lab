# Checkpoint: Nivel 8G - Estado actual

**Fecha:** 2026-06-15  
**Versión de ruta:** v1.1  
**Versión de código:** v1.1

## Dónde estamos exactamente

- **Nivel:** 8G - Validaciones y guardrails
- **Pasos completados:** 1, 2, 3
- **Pasos saltados:** 4 (manejo de errores - lógica app, no arquitectura)
- **Próximo paso:** Paso 5 (Flujos condicionales) o Paso 6 (Tool composition)

## Qué completamos hoy

✅ **Paso 1:** Validación esencial dentro de tool `sumar()`
- Código: `tools_basicas.py` con Union[int, str]
- Patrón: Defensa en capas

✅ **Paso 2:** Guardrails de negocio en `guardar_nombre()`
- Código: `memoria_tools.py` con validaciones (vacío, caracteres, longitud)
- Patrón: Separar validación (formato) de guardrails (negocio)

✅ **Paso 3:** Persistencia nativa con DatabaseSessionService
- Comando: `adk web --session_service_uri="sqlite:///./agent_data.db" agente_adk_nivel8`
- Patrón: ADK maneja persistencia automáticamente
- Validación: Sesiones anteriores recuperables en combo

## Archivos modificados

- `tools_basicas.py` - con validación interna
- `memoria_tools.py` - con guardrails de negocio
- `agent.py` - removido import innecesario de DatabaseSessionService
- `agent_data.db` - creado automáticamente por adk web

## Decisiones arquitectónicas tomadas

1. **Defensa en capas:** LLM + validación código + callbacks
2. **Guardrails vs Validación:** Separar formato de reglas negocio
3. **Persistencia:** Usar DatabaseSessionService en lugar de InMemorySessionService
4. **Low-code alternativas:** Decidimos seguir con ADK para entender arquitectura profunda

## Próximos pasos

### Paso 6 - Tool composition (PRÓXIMO)
- Concepto: Una tool que orquesta otras tools
- Ejemplo: `procesar_compra()` → `validar_pago()` + `guardar_orden()` + `enviar_confirmacion()`
- Patrón arquitectónico real

### Paso 7 - Límites de seguridad
- Max iteraciones, timeouts, rate limiting
- Patrón arquitectónico real

### Paso 5 - SALTADO
- Razón: Flujos condicionales es lógica de app, no arquitectura de agentes

## Estado del código

Todo limpio. Sin líneas innecesarias.
- `tools_basicas.py` ✅
- `memoria_tools.py` ✅
- `estado_tools.py` ✅
- `agent.py` ✅

## Cómo continuar en próximo chat

1. Lee este checkpoint.md primero
2. Código real está en `/adk-project/`
3. Próximo paso recomendado: Paso 6 (Tool composition)
4. Comando para testear: `adk web --session_service_uri="sqlite:///./agent_data.db" agente_adk_nivel8`