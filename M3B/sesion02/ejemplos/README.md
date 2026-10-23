# Ejemplos de patrones para clase (sin API key)

Programas cortos, uno por patrón, sobre el mismo dominio (empleados) y las mismas historias, para que lo
único que cambie de un archivo a otro sea **la estructura**. Todos llaman al modelo con `claude -p`
(ver `ejemplos/comun.py`), así que usan tu sesión de `claude auth login`.

Se ejecutan desde la raíz de la sesión, con el entorno activado:

```bash
python -m ejemplos.s1_razonamiento.react
```

Cada ejecución hace entre 1 y 6 llamadas cortas; cada llamada tarda unos segundos porque arranca Claude Code.

## Sesión 1 · Patrones de razonamiento

| Archivo | Patrón | Lo que lo distingue en el código | En tu fábrica |
| --- | --- | --- | --- |
| `s1_razonamiento/react.py` | ReAct | No hay `for`: **observamos** el bucle de Claude Code con `stream-json` (razona → actúa → observa) | Cada subagente de `.claude/agents/` |
| `s1_razonamiento/plan_ejecucion.py` | Plan-and-Execute | Dos fases: `planificar()` devuelve un `Plan` (Pydantic, `--json-schema`), una persona aprueba, `ejecutar()` lo recorre | Arquitecto y desarrollador (sesión 2); `claude --permission-mode plan` |
| `s1_razonamiento/salidas_estructuradas.py` | Salidas estructuradas | Contrato Pydantic → `--json-schema` → validación en dos niveles (esquema y reglas) → si no, decide una persona | `validadores/contratos.py` → `PlanPruebas` |
| `s1_razonamiento/reflexion.py` | Reflexión | `for intento`: el revisor (código) devuelve problemas y se agregan al prompt | `hooks/compuerta.py` (el mismo ciclo, sin escribir el `for`) |

## Sesión 2 · Patrones de flujo (Python puro: el patrón es la estructura, no la librería)

| Archivo | Patrón | Lo que lo distingue en el código | En tu fábrica |
| --- | --- | --- | --- |
| `s2_flujos/encadenamiento.py` | Encadenamiento | Llamadas en línea recta con un `if` de compuerta entre pasos | Pasos 1 → 8 de `/fabrica` |
| `s2_flujos/enrutamiento.py` | Enrutamiento | Clasificador con `Literal` + tabla `RUTAS = {valor: función}`; una sola rama por entrada | Paso 3 de `/fabrica`; filtro de la sesión 4 |
| `s2_flujos/paralelizacion.py` | Paralelización | `ThreadPoolExecutor`: abanico (`submit`) y unión (`result`); mide el tiempo | Paso 8 de `/fabrica` (sesión 3) |
| `s2_flujos/orquestador.py` | Orquestador y trabajadores | El número de trabajadores sale de la respuesta del modelo, no del código | El agente principal lanzando subagentes |
| `s2_flujos/humano.py` | El humano en el flujo | El modelo propone; el código clasifica el riesgo; `input()` antes de lo irreversible | Aprobación del plan en `/fabrica` |
| `s2_flujos/evaluador.py` | Evaluador-optimizador | Ciclo generar → pytest → generar, con tope; el juez no es el mismo agente | `hooks/compuerta.py` + `verificacion app` |
