# Laboratorio: Arquitectura de Agentes IA desde Cero

**Estado:** Nivel 8G Paso 1 ✅ completado  
**Próximo:** Nivel 8G Paso 2  
**Última actualización:** 2026-06-14

---

## 🚀 Para el siguiente chat

Lee en este orden:
1. `checkpoint.md` (dónde estamos exactamente)
2. Este archivo (conceptos y ruta)
3. Código en `/adk-project/` (es la fuente de verdad)

---

## 📍 Ruta arquitectónica

```text
Nivel 1: reglas
Nivel 2: loop conversacional
Nivel 3: tools simples
Nivel 4: router manual
Nivel 5: memoria / estado persistente
Nivel 6: LLM como detector semántico
Nivel 7: LLM con JSON estructurado
Nivel 8: Framework ADK
  ├─ 8D: Separación por capas
  ├─ 8E: Session/State/ToolContext
  ├─ 8F: Callbacks/hooks
  └─ 8G: Validaciones y guardrails
Nivel 8.5: Conceptos complementarios ADK
  ├─ Memoria persistente con ADK
  ├─ Manejo de errores y recuperación
  ├─ Flujos condicionales basados en estado
  ├─ Tool composition
  └─ Límites de seguridad/ejecución
Nivel 9: Comparación opcional ADK vs LangGraph
```

---

## 🎓 Nivel 8G: Validaciones y Guardrails

### Paso 1 ✅ Completado
Validación esencial dentro de tool `sumar()`
- Archivo modificado: `tools_basicas.py`
- Concepto: Defensa en capas (validación en código + callback + LLM)
- Resultado: sumar rechaza números fuera de rango (0-100), no enteros, strings

### Paso 2 (Siguiente)
Guardrails de negocio en memoria persistente
- Archivo a modificar: `memoria_tools.py`
- Concepto: Separar validación (formato) de guardrails (reglas negocio)
- Ejemplo: No permitir guardar nombre vacío, con caracteres inválidos

### Paso 3-7
[Descritos brevemente si es necesario]

---

## 📚 Estructura de archivos

**`checkpoint.md`**  
Indica exactamente dónde estamos parados. Lee primero en cada nuevo chat.

**`/adk-project/`**  
Código Python real. Esta es la fuente de verdad.

**`codigo.md`**  
Referencia: espejo del código para revisar cambios. NO editar directamente.

---

# Fin