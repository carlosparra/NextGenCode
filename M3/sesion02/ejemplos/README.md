# Ejemplos de patrones para clase

Diecisiete programas cortos: uno por patrón, más dos para los conceptos de salidas estructuradas y del humano en el flujo, y una pareja servidor-cliente para MCP. Todos trabajan sobre el mismo dominio (empleados de la empresa) y las mismas historias, para que lo único que cambie de un archivo a otro sea **la estructura**. Cada archivo empieza con un comentario que dice qué línea distingue al patrón y dónde aparece en tu fábrica.

Se ejecutan con Claude real (usan `ANTHROPIC_API_KEY` y `MODEL` de tu `.env`), siempre desde la raíz del repo:

```bash
python -m ejemplos.s1_razonamiento.react
python -m ejemplos.s2_flujos.enrutamiento
python -m ejemplos.s3_topologias.supervisor
```

Cada ejecución hace entre 1 y 10 llamadas cortas al modelo; ejecutar todos cuesta del orden de centavos de dólar.

## Sesión 1 · Patrones de razonamiento (Python y `anthropic`, sin frameworks)

| Archivo | Patrón | Lo que lo distingue en el código | En tu fábrica |
| --- | --- | --- | --- |
| `s1_razonamiento/react.py` | ReAct | `for` que sigue mientras `stop_reason == "tool_use"`; la observación vuelve como `tool_result` | `agentes/base.py` → `ejecutar_agente()` |
| `s1_razonamiento/plan_ejecucion.py` | Plan-and-Execute | Dos fases: `planificar()` devuelve un `Plan` (Pydantic), una persona aprueba, `ejecutar()` lo recorre | `agentes/desarrollador.py` → `planificar()` y `construir()` |
| `s1_razonamiento/salidas_estructuradas.py` | Salidas estructuradas y validación | Un contrato Pydantic, la herramienta forzada con `tool_choice` y dos niveles de validación en código (esquema y reglas); si no se puede corregir, decide una persona | `agentes/disenador_pruebas.py` → `PlanPruebas` y `validar_plan()` |
| `s1_razonamiento/reflexion.py` | Reflexión | `for intento`: el revisor (código) devuelve problemas y se agregan al prompt | `agentes/analista.py` → `validar_gherkin()` |

## Sesión 2 · Patrones de flujo (LangGraph)

| Archivo | Patrón | Lo que lo distingue en el código | En tu fábrica |
| --- | --- | --- | --- |
| `s2_flujos/encadenamiento.py` | Encadenamiento | Solo `add_edge` en línea recta y una compuerta con `add_conditional_edges` | `flujos/flujo_s2.py`: analizar → diseñar → planificar → construir |
| `s2_flujos/enrutamiento.py` | Enrutamiento | `add_conditional_edges(nodo, función, {valor: destino})`; clasificador con `Literal` | `despues_de_analizar()`; `filtrar_historia` en `flujo_s4.py` |
| `s2_flujos/paralelizacion.py` | Paralelización | Dos aristas desde el mismo nodo, unión con `add_edge([a, b], "unir")` y un reductor | `flujos/flujo_s3.py`: desplegar ∥ automatizar |
| `s2_flujos/orquestador.py` | Orquestador y trabajadores | `Send("trabajador", datos)` en una lista: el número de trabajadores lo decide el modelo | `agentes/triage.py`; subagentes de Claude Code |
| `s2_flujos/humano.py` | El humano en el flujo | `interrupt()` muestra qué se hará, `InMemorySaver` guarda el estado y `Command(resume=…)` reanuda; el código decide qué requiere aprobación | `flujo_s2.py` → `aprobar_plan` y `pedir_aclaracion` |
| `s2_flujos/evaluador.py` | Evaluador-optimizador | Un ciclo evaluar → generar con tope; el juez es pytest en un subproceso | `construir` → `verificar` → `construir` |
