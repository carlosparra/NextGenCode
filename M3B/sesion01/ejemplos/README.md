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
