# Fábrica de software con agentes · M3B · Sesión 1

**Agentes 1 y 2 como subagentes de Claude Code, sin API key.**

| # | Agente | Entrada | Salida | Sesión |
| --- | --- | --- | --- | --- |
| 1 | Analista | Historia de usuario | `salida/HU-xx/criterios.feature` | 1 |
| 2 | Diseñador de pruebas | Criterios | `salida/HU-xx/casos_prueba.json` | 1 |

## La idea de la sesión

Un agente = **modelo + instrucciones + herramientas + bucle**. En M3 escribías el bucle en Python con la API.
En M3B el bucle ya lo trae Claude Code; tú defines las otras tres piezas y, sobre todo, **los límites**:

| Concepto del curso | En M3 (API) | En M3B (Claude Code) |
| --- | --- | --- |
| Modelo | `Anthropic()` + `ANTHROPIC_API_KEY` | `claude auth login` (tu suscripción) |
| Instrucciones | `SISTEMA = """..."""` en `agentes/analista.py` | el cuerpo de `.claude/agents/analista.md` |
| Herramientas | `herramientas_archivos(lectura, escritura)` | `tools: Read, Glob, Write` en el frontmatter |
| Bucle ReAct | `ejecutar_agente()` en `agentes/base.py` (Lab 1A) | lo corre Claude Code; lo observas en `ejemplos/s1_razonamiento/react.py` |
| Mínima agencia | `_dentro_de()` + `PermissionError` | `hooks/roles.py` + hook PreToolUse `hooks/rol.py` (salida 2 = bloqueado) |
| Errores al modelo | `tool_result` con `is_error: True` | el `stderr` del hook llega al agente como motivo |
| Contrato | `PlanPruebas` (Pydantic) + `guardar_casos` | el mismo `PlanPruebas`, en `validadores/contratos.py` |
| Reflexión con tope | `for intento in range(max_intentos)` | hook SubagentStop `hooks/compuerta.py` con `decision: block` y `MAX_INTENTOS` |
| Cómo se invoca | `python -m agentes.analista ...` | `/criterios ...` (skill en `.claude/skills/criterios/SKILL.md`) |

Las tres reglas no cambian: **el modelo propone y el código decide**, **cada agente solo toca lo de su rol**
y **todo bucle tiene un límite**.

## Cómo fluye una llamada

```
/criterios historias/HU-01-registrar-empleado.md
   │  .claude/skills/criterios/SKILL.md   (context: fork, agent: analista)
   ▼
subagente analista  ── Read / Glob / Write ──►  hooks/rol.py (PreToolUse)
   │                                             ¿está en roles.py? sí → sigue · no → salida 2 + motivo
   │  quiere terminar
   ▼
hooks/compuerta.py (SubagentStop)  →  validadores/  →  ¿válido?
   sí → termina y responde        no → decision: block + problemas → el analista corrige (máx. 3)
```

## Requisitos

- Claude Code con sesión iniciada: `claude auth login` (plan Pro o Max). **No necesitas ANTHROPIC_API_KEY**;
  si la tienes definida en la terminal, Claude Code la usaría: quítala con `unset ANTHROPIC_API_KEY`.
- Python 3.12 y `uv` (los hooks y validadores son Python).

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
claude            # la primera vez: acepta el diálogo «¿confías en esta carpeta?» y sal con /exit
```

El diálogo de confianza importa: sin él, Claude Code ignora los permisos `allow` del proyecto.
Los hooks se ejecutan con `.venv/bin/python`, así que el entorno debe existir en la raíz de la sesión.

## Cómo correr los agentes

1. Activa el entorno (`source .venv/bin/activate`) y quita la clave de API si la tienes: `unset ANTHROPIC_API_KEY`.
   Si nunca iniciaste sesión, corre `claude auth login` (plan Pro o Max).
2. Abre `claude` una vez en esta carpeta y acepta «¿confías en esta carpeta?».
3. Corre **primero `/criterios` y después `/casos`**: el diseñador trabaja con lo que deja el analista.
   - `/criterios` lanza al subagente **analista**, que escribe `salida/HU-01/criterios.feature`.
   - `/casos` lanza al **diseñador de pruebas**, que escribe `salida/HU-01/casos_prueba.json`.
4. Al terminar cada uno, la **compuerta** valida su entrega y, si tiene problemas, lo regresa a corregir (máximo 3 veces).
   Claude Code te puede pedir permiso para escribir el archivo: apruébalo o pulsa Shift+Tab para editar sin preguntar.
5. Comprueba el resultado con el mismo juez de la compuerta:
   `python -m validadores.validar salida/HU-01/criterios.feature` y `python -m validadores.validar salida/HU-01/casos_prueba.json`.
6. Repite con `HU-02` y `HU-03`.

**En macOS: `zsh: command not found: python`.** macOS solo trae `python3`; el comando `python` aparece al activar el
entorno virtual con `source .venv/bin/activate`, y hay que activarlo **en cada terminal nueva**. Si el entorno no
existe, créalo con `uv venv` y `uv pip install -r requirements.txt`. También puedes llamar al Python del entorno
directamente: `.venv/bin/python -m ...`. No uses `python3` a secas: es el del sistema y no tiene las dependencias del
curso, así que falla con `ModuleNotFoundError`.

## Uso

Dentro de Claude Code (interactivo):

```
/criterios historias/HU-01-registrar-empleado.md
/casos salida/HU-01/criterios.feature
/agents                      ← ver los subagentes del proyecto
/hooks                       ← ver los hooks registrados
```

Sin interacción (útil para scripts):

```bash
claude -p "/criterios historias/HU-01-registrar-empleado.md" --permission-mode acceptEdits
claude -p "/casos salida/HU-01/criterios.feature" --permission-mode acceptEdits
python -m validadores.validar salida/HU-01/casos_prueba.json      # el mismo juez, a mano
```

Repite con `HU-02` y `HU-03`. Los patrones de razonamiento tienen su ejemplo en [`ejemplos/`](ejemplos/README.md).

## Labs

- **Lab 1A · Tu primer subagente.** Borra `.claude/agents/analista.md` y escríbelo tú: frontmatter
  (`name`, `description`, `tools`) y prompt. Prueba con `/criterios`. ¿Qué pasa si quitas `Write` de `tools`?
- **Lab 1B · Mínima agencia.** Pide en Claude Code: «usa el subagente analista para leer
  `historias/../secretos_demo.txt`». Mira el motivo del bloqueo y encuentra la línea de `hooks/rol.py` que lo produce.
  Prueba el hook sin modelo:
  `echo '{"agent_type":"analista","tool_name":"Read","tool_input":{"file_path":".env"}}' | .venv/bin/python hooks/rol.py; echo $?`
- **Lab 1C · El contrato.** Cambia `MAX_INTENTOS` de `hooks/compuerta.py` a 0 y vuelve a correr `/casos`:
  ¿quién decide ahora si el JSON sirve? Agrega una regla a `validar_plan()` (por ejemplo, al menos un caso `e2e`)
  y observa cómo el diseñador se corrige solo.

## Preguntas de repaso

1. ¿Qué parte del agente escribe Claude Code y cuál escribes tú?
2. ¿Por qué el permiso se revisa en un hook y no solo en el prompt del agente?
3. ¿Qué diferencia hay entre una salida 2 de PreToolUse y un `decision: block` de SubagentStop?
4. ¿Qué pasaría sin `MAX_INTENTOS`?
5. ¿Por qué el diseñador no puede leer `historias/`?
