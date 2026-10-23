# M3B · La fábrica de software con agentes de Claude Code (sin API key)

La misma fábrica de M3 —historia de usuario → criterios → casos → código → despliegue → pruebas E2E—,
pero **cada agente es un subagente de Claude Code** y todo corre con tu sesión de `claude auth login`
(plan Pro o Max). No se usa `ANTHROPIC_API_KEY` en ningún momento.

| | M3 | M3B |
| --- | --- | --- |
| Modelo | API de Anthropic (`ANTHROPIC_API_KEY`) | Claude Code (`claude auth login`) |
| Un agente es… | un `.py` con `SISTEMA`, herramientas y el bucle | un `.claude/agents/<nombre>.md` |
| El bucle ReAct | lo escribes (`ejecutar_agente`, Lab 1A) | lo corre Claude Code; lo observas con `stream-json` |
| Orquestación | LangGraph (`flujos/flujo_s*.py`) | un skill (`/fabrica`) con un guion y compuertas |
| Mínima agencia | herramientas con permisos + hooks del Agent SDK | `hooks/roles.py` + hook PreToolUse `hooks/rol.py` |
| Reflexión / evaluador | `for intento` en Python | hook SubagentStop `hooks/compuerta.py` (`decision: block`) |
| Contratos | Pydantic | los mismos modelos Pydantic (`validadores/contratos.py`) |
| Patrones de ejemplo | `ejemplos/` con la API y LangGraph | `ejemplos/` con `claude -p` y Python puro |

Las reglas del curso no cambian: **el modelo propone y el código decide**, **cada agente solo toca lo de su rol**,
**todo bucle tiene un límite** y **una persona aprueba lo irreversible**.

## Las cuatro sesiones

Cada carpeta es un proyecto independiente y contiene todo lo de la anterior más lo nuevo.

| Carpeta | Qué agrega | Comando principal |
| --- | --- | --- |
| `sesion01/` | analista y diseñador; hooks de rol y compuerta; patrones de razonamiento | `/criterios`, `/casos` |
| `sesion02/` | arquitecto y desarrollador; `/fabrica`; verificación de la app; patrones de flujo | `/fabrica historias/HU-01-registrar-empleado.md` |
| `sesion03/` | despliegue y automatizador en paralelo; topologías; MCP (`.mcp.json`) | `/fabrica ...` (con Docker) |
| `sesion04/` | filtro de seguridad, E2E, triage, hook de seguridad y auditoría; demo HU-99 | `/fabrica ...`, `DEFENSAS=0 ...` |

## Cómo correr una sesión

```bash
cd M3B/sesion0N
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
playwright install chromium          # solo sesiones 3 y 4
unset ANTHROPIC_API_KEY              # para que Claude Code use tu suscripción
claude auth login                    # solo la primera vez: inicia sesión con tu plan Pro o Max
claude                               # 1.ª vez: acepta «¿confías en esta carpeta?»; luego usa los /comandos
```

Requisitos: Claude Code con sesión iniciada, Python 3.12 y `uv`; Node 20+ desde la sesión 2; Docker Desktop desde la 3.
El `README.md` de cada sesión explica los conceptos, el mapa M3 → M3B, los comandos, los labs y las preguntas de repaso.

**Sobre el diálogo de confianza:** Claude Code solo aplica los permisos `allow` de `.claude/settings.json` en carpetas
que marcaste como confiables. Ábrela una vez con `claude` y acepta. Los hooks y las reglas `deny` sí se aplican siempre.

**Sobre el consumo:** cada llamada usa la cuota de tu suscripción. Como referencia, `/criterios` + `/casos` de una
historia consumen del orden de 0.5 USD equivalentes (Claude Code muestra el costo estimado al final de `claude -p`).
