# Checkpoint: Nivel 8G Paso 1

**Fecha:** 2026-06-14  
**Paso completado:** Nivel 8G Paso 1

## Qué hicimos
- Movimos validación esencial dentro de `sumar()`
- Cambiamos de lanzar excepciones a retornar errores (Union[int, str])
- Validamos con 4 casos: normal, fuera de rango, negativo, string

## Resultado
✅ Todas las validaciones funcionan correctamente
✅ Defensa en capas: LLM + validación en código + callbacks

## Código cambiado
- `tools_basicas.py`: función `sumar()` con validación interna

## Próximo paso
Nivel 8G Paso 2: Guardrails en memoria persistente