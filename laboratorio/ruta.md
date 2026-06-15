# Laboratorio: arquitectura de agentes IA desde cero

**Versión:** v1.0  
**Fecha de corte:** 2026-06-14  
**Propósito:** llevar el contexto completo del laboratorio a otro chat u otra IA sin repetir todo desde cero.

---

## 1. Objetivo del laboratorio

Entender la arquitectura de agentes IA paso a paso, empezando desde Python básico y avanzando hacia frameworks como ADK y, más adelante, LangGraph.

El foco no es construir rápido, sino entender la diferencia entre:

- agentes con reglas
- agentes con loop conversacional
- agentes con tools
- agentes con router
- agentes con memoria / estado
- agentes con LLM
- agentes con contrato de tools
- frameworks de agentes como ADK o LangGraph
- callbacks / hooks
- session/state
- guardrails
- subagentes

---

## 2. Dinámica obligatoria del laboratorio

La dinámica debe mantenerse así:

1. Avanzar en bloques pequeños.
2. Dar solo un paso por vez.
3. Cada paso debe incluir:
   - qué hacer
   - por qué se hace
   - cómo validar que funcionó
4. No avanzar hasta que el usuario diga: `siguiente`.
5. Priorizar claridad sobre completitud.
6. No repetir lo anterior salvo que sea necesario para ubicar el contexto.
7. Si aparece un concepto técnico nuevo, explicarlo antes de seguir con código.
8. Separar arquitectura de implementación.
9. Señalar errores, supuestos débiles y limitaciones.
10. En laboratorios técnicos, mantener estrictamente un paso por vez.

---

## 3. Ruta arquitectónica acordada

```text
Nivel 1: reglas
Nivel 2: loop conversacional
Nivel 3: tools simples
Nivel 4: router manual
Nivel 5: memoria / estado persistente
Nivel 6: LLM como detector semántico de intención
Nivel 7: LLM con salida estructurada: intención + parámetros
Nivel 8: framework tipo ADK
  ├─ 8D: Separación por capas
  ├─ 8E: Session/State/ToolContext
  ├─ 8F: Callbacks/hooks
  └─ 8G: Validaciones y guardrails
Nivel 8.5: Conceptos complementarios ADK
  ├─ Memoria persistente con ADK (vs manual)
  ├─ Manejo de errores y recuperación
  ├─ Flujos condicionales basados en estado
  ├─ Tool composition
  └─ Límites de seguridad/ejecución
Nivel 9: comparación opcional ADK vs LangGraph
```

---

# Parte A: laboratorio manual previo

## Nivel 1: reglas

Se construyó un agente básico con `if/elif`.

Concepto aprendido:

```text
entrada del usuario → reglas manuales → respuesta
```

---

## Nivel 2: loop conversacional

Se agregó un `while True` para mantener viva la conversación.

Concepto aprendido:

```text
entrada → procesamiento → respuesta → vuelve a esperar entrada
```

---

## Nivel 3: tools simples

Se agregaron funciones ejecutables como:

- `obtener_hora()`
- `sumar()`

Concepto aprendido:

```text
agente → decide usar función → ejecuta función → responde
```

---

## Nivel 4: router manual

Se separó la arquitectura en:

- `detectar_intencion()`
- `ejecutar_intencion()`

Concepto aprendido:

```text
usuario → detectar intención → router → acción
```

El router manual era `ejecutar_intencion(...)`, porque decidía qué acción ejecutar según la intención detectada.

---

## Nivel 5: memoria / estado persistente

Se agregó memoria con:

- diccionario Python
- archivo `memoria.json`

Concepto aprendido:

```text
usuario → intención → router → memoria / tool / respuesta
```

La memoria permitía guardar datos entre ejecuciones del programa.

---

## Nivel 6: LLM como detector semántico de intención

El LLM no reemplazó todo el agente. Reemplazó solo la parte de detección de intención.

Flujo:

```text
usuario
  ↓
LLM detecta intención
  ↓
router Python ejecuta acción
  ↓
tool / memoria / respuesta
```

Concepto aprendido:

```text
Nivel 5: reglas detectan intención.
Nivel 6: LLM detecta intención semánticamente.
```

---

## Nivel 7: LLM con contrato de acción

El LLM pasó de devolver solo una intención a devolver JSON estructurado con:

- `intencion`
- `parametros`

Flujo:

```text
usuario
  ↓
LLM genera JSON
  ↓
json.loads()
  ↓
router manual
  ↓
tool / memoria
  ↓
respuesta final
```

Concepto aprendido:

```text
El LLM no debe responder cualquier cosa.
Debe cumplir un contrato estructurado.
```

Archivo manual relevante:

```text
agent_nivel7.py
```

Estado alcanzado en Nivel 7:

- OpenAI SDK real.
- `analizar_solicitud_llm()`.
- El LLM devuelve JSON con `intencion` + `parametros`.
- Se usa `json.loads()`.
- Se usa router manual `ejecutar_intencion(intencion, pregunta, memoria, parametros)`.
- Existe memoria persistente `memoria.json`.
- Arquitectura manual monolítica procedural por capas.

---

# Parte B: salto a ADK / Nivel 8

## Entorno usado

- Sistema: Windows.
- Editor: VS Code.
- Terminal: Git Bash dentro de VS Code.
- Python: Anaconda base.
- ADK instalado: `google-adk 2.2.0`.
- Se decidió seguir en Anaconda base por ahora, aunque se reconoció el riesgo de entorno “sucio”.

Validaciones de entorno realizadas:

```text
which python → /c/Users/Alvaro/anaconda3/python
which pip    → /c/Users/Alvaro/anaconda3/Scripts/pip
which adk    → /c/Users/Alvaro/anaconda3/Scripts/adk
adk --version → 2.2
```

Hubo un warning de dependencia con `watchdog`, pero ADK funcionó.

---

## Proyecto ADK creado

Estructura actual:

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

`.env` contiene `GOOGLE_API_KEY`, pero **no debe compartirse con otra IA ni subirse a ningún lado**.

Validaciones realizadas:

```text
adk run agente_adk_nivel8
adk web
```

ADK web permitió ver trazas de tool calls.

---

## Nivel 8D: separación por capas

Se dejó `agent.py` como archivo de composición.

Responsabilidad de `agent.py`:

- importar `Agent`
- importar tools
- registrar tools
- definir instrucciones
- definir callbacks
- construir `root_agent`

Responsabilidad de `tools_basicas.py`:

- `obtener_hora()`
- `sumar()`

Responsabilidad de `memoria_tools.py`:

- cargar/guardar `memoria_adk.json`
- `guardar_nombre()`
- `consultar_nombre()`

Responsabilidad de `estado_tools.py`:

- tools que usan `ToolContext`
- lectura/escritura de `session.state`

Concepto aprendido:

```text
ADK reduce pegamento, pero no elimina la lógica de aplicación.
```

ADK ayuda con:

- loop conversacional
- exposición de tools
- extracción de parámetros
- llamadas estructuradas a funciones
- trazabilidad básica
- callbacks
- session/state

ADK no reemplaza:

- diseño de memoria persistente
- reglas de negocio
- validaciones de dominio
- seguridad
- diseño de arquitectura

---

# Parte C: Nivel 8E — Session / State / ToolContext

## Conceptos aprendidos

Mapa mental:

```text
Session
  ├─ events
  └─ state
```

### Session

Una `Session` representa una conversación o hilo conversacional gestionado por ADK.

No es solo “el historial”. Es el contenedor de la conversación.

### Events

`events` representa el historial cronológico de lo que pasó:

- usuario dijo algo
- agente respondió
- tool fue llamada
- tool devolvió algo
- errores
- cambios de ejecución

### State

`state` es un diccionario de datos vivos asociado a la sesión.

Sirve para datos temporales de ejecución:

- flags
- paso actual de un flujo
- resultado intermedio
- preferencias temporales
- trazabilidad temporal

### ToolContext

`ToolContext` es el objeto que ADK puede pasar a una tool para que la tool acceda al contexto de ejecución, incluyendo `tool_context.state`.

Conclusión:

```text
ToolContext = puente entre una tool y el contexto de sesión ADK.
```

---

## Diferencia validada: memoria_adk.json vs session.state

| Pieza | Quién la gestiona | Persistencia observada | Uso correcto |
|---|---|---:|---|
| `memoria_adk.json` | Código propio | Sobrevive reinicio | memoria persistente manual |
| `session.state` | ADK + tools | Se perdió al reiniciar en el laboratorio | estado temporal de sesión |
| `events` | ADK | depende del SessionService | historial de ejecución |

Conclusión validada:

```text
session.state ≠ memoria_adk.json
```

---

## Tools creadas con ToolContext

Se crearon tools para:

- guardar nombre temporal en `session.state`
- consultar nombre temporal desde `session.state`
- activar modo debug temporal
- consultar modo debug temporal
- consultar última tool ejecutada

El código exacto está separado en:

```text
laboratorio_agentes_ia_codigo_v1.0.md
```

---

## Validaciones de Nivel 8E

### Prueba 1: nombre temporal en session.state

Se probó:

```text
guarda en session state que mi nombre temporal es Álvaro
consulta mi nombre temporal de session state
```

Resultado:

```text
La tool pudo escribir y leer desde session.state.
No grabó en memoria_adk.json.
```

### Prueba 2: reinicio de adk run

Se reinició `adk run` y se consultó de nuevo el nombre temporal.

Resultado:

```text
session.state perdió el dato temporal.
memoria_adk.json mantuvo el nombre persistente.
```

### Prueba 3: modo debug temporal

Se activó `modo_debug` en `session.state`, se consultó y luego se reinició `adk run`.

Resultado:

```text
modo_debug funcionó durante la sesión.
Se perdió al reiniciar.
```

Conclusión:

```text
session.state sirve para estado temporal de ejecución, no para memoria permanente por defecto.
```

---

# Parte D: Nivel 8F — Callbacks / hooks

## Conceptos aprendidos

Callback:

```text
función que ADK ejecuta automáticamente en un punto específico del flujo.
```

Hook:

```text
punto de enganche dentro del flujo.
```

Diferencia clave:

```text
tool = acción que el agente puede elegir.
callback = código que se engancha al flujo del agente.
```

Flujo conceptual:

```text
usuario
  ↓
LLM decide tool
  ↓
before_tool_callback
  ↓
tool
  ↓
after_tool_callback
  ↓
respuesta
```

---

## before_tool_callback implementado

Se implementó un callback antes de ejecutar tools.

Responsabilidades actuales:

- imprimir logs antes de la tool
- validar argumentos de `sumar`
- bloquear la ejecución si `sumar` recibe argumentos no enteros

Concepto aprendido:

```text
return None → ADK deja ejecutar la tool.
return dict → ADK bloquea/reemplaza la ejecución de la tool con ese resultado.
```

Validado:

```text
suma 8 y 15 → ejecutó normal.
suma hola y quince → callback bloqueó y el agente respondió que sumar solo acepta enteros.
```

Limitación aprendida:

```text
La validación en callback solo protege llamadas vía ADK.
Si alguien llama sumar() directamente desde Python, el callback no se ejecuta.
```

---

## after_tool_callback implementado

Se implementó un callback después de ejecutar tools.

Responsabilidades actuales:

- imprimir logs después de la tool
- guardar en `session.state`:
  - última tool ejecutada
  - últimos argumentos
  - última respuesta de tool
- excluir tools de diagnóstico del tracking funcional

Validado:

```text
qué hora es → before y after callback se imprimieron.
suma 4 y 6 → before y after callback se imprimieron; respuesta de tool fue 10.
```

---

## Problema detectado: la tool de diagnóstico contaminaba la trazabilidad

Al preguntar:

```text
cuál fue la última tool ejecutada
```

ADK ejecutaba `consultar_ultima_tool`, y esa misma tool sobrescribía `ultima_tool`.

Problema conceptual:

```text
observar el estado modificaba el estado observado.
```

Corrección aplicada:

```text
consultar_ultima_tool fue excluida del tracking en after_tool_callback.
```

Validación:

```text
Después de ejecutar sumar, consultar dos veces la última tool mantiene sumar como última tool funcional.
```

Concepto aprendido:

```text
No todo evento técnico debe contarse como evento funcional/de negocio.
```

---

# Parte E: cuotas, tokens y modelos

## Error encontrado

Se recibió:

```text
google.genai.errors.ClientError: 429 RESOURCE_EXHAUSTED
```

Causa:

```text
Se excedió la cuota gratuita de requests para el modelo usado.
```

El log mostró que `sumar` sí se ejecutó y que el error ocurrió después, cuando ADK volvió a llamar al modelo para redactar la respuesta final.

Concepto aprendido:

```text
Una interacción con tool puede consumir más de una llamada al modelo.
```

Flujo:

```text
Request 1 → modelo decide tool
Tool → se ejecuta en Python
Request 2 → modelo redacta respuesta final
```

---

## RPM, TPM y RPD

### RPM

```text
Requests Per Minute = solicitudes por minuto.
```

Una interacción ADK con tools puede consumir más de una request.

### TPM

```text
Tokens Per Minute = tokens por minuto.
```

Mide volumen de texto procesado por minuto:

- instrucciones
- tools
- historial
- mensaje del usuario
- resultado de tools
- respuesta generada

### RPD

```text
Requests Per Day = solicitudes por día.
```

Fue el límite principal que se agotó.

---

## Token

Un token es una unidad de texto que el modelo procesa.

No equivale exactamente a una palabra.

Puede ser:

- una palabra
- parte de una palabra
- un signo
- un número
- un espacio
- fragmento de código

Idea:

```text
texto → tokens → números → modelo
```

En ADK, aunque el usuario escriba poco, también consumen tokens:

- instruction del agente
- metadata de tools
- docstrings
- schemas
- historial
- resultado de tools

---

## Diseño y consumo

Pregunta analizada:

```text
¿Hacer que el modelo decida la tool consume más tokens que usar un condicional en código?
```

Respuesta:

```text
Sí. Puede cambiar drásticamente el consumo.
```

Comparación:

```text
routing con LLM → más tokens, más requests, más latencia, más costo, más flexibilidad.
condicional en código → 0 tokens, más rápido, más determinístico, menos flexible.
```

Regla arquitectónica:

```text
si es predecible → código.
si es lenguaje natural variable → LLM.
si es crítico → código valida aunque el LLM decida.
```

---

## Modelo cambiado

El modelo anterior chocó con cuota.

Se cambió a:

```text
gemini-3.1-flash-lite
```

Motivo:

```text
El usuario vio en su tabla que tenía mayor RPD/RPM para laboratorio.
```

Nota:

```text
Si otra IA/entorno no reconoce ese modelo, usar un modelo disponible con mayor RPD/RPM.
```

---

# Parte F: Nivel 8G — Validaciones y guardrails

## Paso 0 conceptual completado

Se explicó la diferencia entre validación y guardrail.

### Validación

Revisa si una entrada cumple una condición esperada.

Ejemplo:

```text
a debe ser int
b debe ser int
```

### Guardrail

Es una barrera de seguridad o control alrededor del agente.

Ejemplos:

- no permitir montos negativos
- no ejecutar tools peligrosas
- no consultar datos fuera del usuario actual
- no guardar secretos
- no permitir operaciones sin confirmación
- no llamar una API si falta autorización

Diferencia:

```text
validación = este dato tiene formato correcto.
guardrail = esta acción está permitida en este contexto.
```

---

## Dónde poner validaciones / guardrails

Posibles ubicaciones:

1. dentro de la tool
2. en callbacks
3. en capa de dominio externa

Regla crítica:

```text
No pongas reglas fuertes solo en prompts.
```

Uso sano:

```text
validación esencial de dominio → dentro de la tool o capa de dominio.
validación transversal/observabilidad → callback.
prompt → ayuda, pero no garantiza seguridad.
```

---

# Parte G: punto exacto para continuar

El laboratorio quedó aquí:

```text
Nivel 8G — Validaciones y guardrails simples
Paso 0 conceptual completado.
Siguiente paso: Nivel 8G — Paso 1.
```

## Siguiente acción técnica

Mover una validación esencial dentro de la tool `sumar`.

Regla didáctica propuesta:

```text
sumar solo acepta enteros entre 0 y 100.
```

Motivo:

```text
La validación en before_tool_callback solo protege llamadas vía ADK.
La validación dentro de sumar protege también llamadas directas desde Python.
```

La otra IA debe continuar desde este punto, manteniendo la dinámica de un paso por vez.

---

## Nivel 8.5: Conceptos complementarios en ADK
   
   Después de dominar callbacks y validaciones, exploramos:
   
   - Memoria persistente CON ADK: cómo ADK maneja persistencia vs manual JSON
   - Manejo de errores: recuperación, fallbacks, reintentos
   - Flujos condicionales: control basado en estado
   - Tool composition: herramientas que llaman otras herramientas
   - Límites de seguridad: timeouts, rate limiting, iteración máxima

# Parte H: archivo de código asociado

El código actual reconstruido está separado en:

```text
laboratorio_agentes_ia_codigo_v1.0.md
```

No enviar `.env` con la API key real.

# Parte I: Estado del laboratorio (hoy)
   
   - Versión actual: v1.1
   - Último chat: [fecha]
   - Nivel alcanzado: 8G Paso 1 ✅
   - Próximo paso: 8G Paso 2
   - Archivos en proyecto: ruta.md, codigo.md, checkpoint.md, código Python

## 4. Estructura de archivos y propósito

### En `/laboratorio/`

**`ruta.md`** (este archivo)
- Conceptual: niveles, decisiones arquitectónicas, aprendizajes
- Se actualiza cuando hay cambios conceptuales grandes
- El nuevo chat LEE ESTO primero para entender la estrategia

**`codigo.md`**
- Código Python actual (archivos espejo de `/adk-project/`)
- Referencia: qué cambios se hicieron en cada paso
- NO es la fuente de verdad (la fuente es `/adk-project/` directamente)

**`checkpoint.md`**
- **CRÍTICO: Indica EXACTAMENTE dónde estamos parados**
- Qué paso se completó
- Qué está en progreso
- Qué falta
- El nuevo chat LEE ESTO segundo para continuar sin repetir

### En `/adk-project/`

Código Python real (la fuente de verdad)
- El nuevo chat examina estos archivos
- Cualquier cambio debe hacerse aquí y reflejarse en `codigo.md`

---

## 5. Cómo cambiar de chat

Cuando cambies:
1. Actualiza `checkpoint.md` (qué completaste, qué sigue)
2. Commit y push a GitHub
3. En el nuevo chat, adjunta o dile: "Hice commit. Lee `checkpoint.md`"

# Fin de laboratorio_agentes_ia_ruta_v1.0.md
