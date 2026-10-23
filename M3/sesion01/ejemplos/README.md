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
