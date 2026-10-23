# Fábrica de software con agentes · M3B · Sesión 2

**El agente 3 (desarrollador) y el orquestador: la fábrica completa como un skill de Claude Code.**

| # | Agente | Entrada | Salida | Sesión |
| --- | --- | --- | --- | --- |
| 1 | Analista | Historia de usuario | `salida/HU-xx/criterios.feature` | 1 |
| 2 | Diseñador de pruebas | Criterios | `salida/HU-xx/casos_prueba.json` | 1 |
| 3a | Arquitecto (plan) | Criterios, casos y `app/` | `salida/HU-xx/plan.md` | 2 |
| 3b | Desarrollador | Plan aprobado | `app/backend`, `app/frontend` | 2 |

## La idea de la sesión

En la sesión 1 cada agente trabajaba solo. Ahora se encadenan, con **estado** (la carpeta `salida/HU-xx/`),
**compuertas deterministas** entre pasos y **una persona** en los puntos irreversibles.

Hay dos formas de orquestar, y en esta sesión ves las dos:

| | Workflow (el código decide el orden) | Agente orquestador (el modelo sigue un guion) |
| --- | --- | --- |
| Dónde | `ejemplos/s2_flujos/*.py` | `.claude/skills/fabrica/SKILL.md` |
| Quién decide el siguiente paso | un `if` / un `for` en Python | el agente principal, leyendo el guion |
| Qué lo mantiene en el carril | el propio código | compuertas: comandos de `validadores/` y `verificacion/`, hooks y permisos |
| Cuándo conviene | pasos fijos, máxima predictibilidad | pasos con conversación (aclarar, aprobar, corregir) |

| Concepto del curso | En M3 (API + LangGraph) | En M3B (Claude Code) |
| --- | --- | --- |
| Encadenamiento | `add_edge` en `flujos/flujo_s2.py` | pasos 1 → 8 de `/fabrica` |
| Estado | `Estado(TypedDict)` + `InMemorySaver` | la conversación del orquestador + `salida/HU-xx/` (pizarra en disco) |
| Enrutamiento | `despues_de_analizar()` | paso 3: ¿hay preguntas abiertas? (`validadores/preguntas.py`) |
| Humano en el flujo | `interrupt()` + `Command(resume=...)` | el orquestador te pregunta (AskUserQuestion) antes del paso irreversible |
| Plan-and-Execute | `desarrollador.planificar()` y `construir()` | subagentes `arquitecto` (solo lectura, escribe `plan.md`) y `desarrollador` |
| Evaluador-optimizador | `construir → verificar → construir` | `hooks/compuerta.py` corre `verificacion app` al terminar el desarrollador |
| Verificación determinista | `flujos/verificacion.py` | `python -m verificacion app` (backend en 8010 + `npm run build`) |
| Permisos de Claude Code | `ClaudeAgentOptions(allowed_tools=..., hooks=...)` | `tools:` del subagente + `hooks/roles.py` + `permissions.allow` |

## Cómo fluye `/fabrica`

```
/fabrica historias/HU-01-registrar-empleado.md
  1 analista ─► 2 validar criterios ─► 3 ¿preguntas? ──persona──► 4 diseñador ─► validar casos
  ─► 5 arquitecto ─► plan.md ──persona: ¿apruebas? (o comentarios → arquitecto otra vez, máx. 2)
  ─► 6 desarrollador ─► (compuerta: verificacion app, máx. 2) ─► 7 verificacion app ─► 8 bitacora.md
```

## Requisitos

Todo lo de la sesión 1, más **Node 20 o superior** (el frontend se compila con `npm run build`).

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
claude            # la primera vez: acepta el diálogo de confianza y sal con /exit
```

## Uso

```
/fabrica historias/HU-01-registrar-empleado.md          ← interactivo: te pregunta en los pasos 3 y 5
```

Paso a paso (cada uno es un skill):

```
/criterios historias/HU-01-registrar-empleado.md
/casos salida/HU-01/criterios.feature
/plan HU-01
/plan HU-01 agrega validación del correo en el frontend      ← rehacer con comentarios
/construir HU-01
```

Sin interacción (aprobación por adelantado):

```bash
claude -p "/fabrica historias/HU-01-registrar-empleado.md --aprobar" --permission-mode acceptEdits
python -m verificacion app          # el mismo juez que usa la fábrica
```

Ver la app a mano:

```bash
cd app/backend && ../../.venv/bin/python -m uvicorn main:app --port 8000   # http://localhost:8000/docs
cd app/frontend && npm run dev                                            # http://localhost:5173
```

Los patrones de flujo tienen su ejemplo en [`ejemplos/`](ejemplos/README.md).

## Labs

- **Lab 2A · El guion.** Abre `.claude/skills/fabrica/SKILL.md` y quita el paso 2 (validar criterios).
  Corre `/fabrica` con una historia ambigua del backlog. ¿Quién detecta ahora que los criterios están mal?
- **Lab 2B · El humano en el flujo.** Rechaza el plan con un comentario concreto. Compara el `plan.md` antes y
  después. ¿Qué parte del guion hace que se reescriba, y qué impide que se rechace infinitamente?
- **Lab 2C · El evaluador.** Rompe a propósito `app/backend/main.py` (por ejemplo, borra el endpoint de salud) y corre
  `/construir HU-01`. Observa cómo la compuerta devuelve el log al desarrollador. ¿Dónde está el tope?
- **Lab 2D · Workflow vs agente.** Escribe en Python (`ejemplos/s2_flujos/encadenamiento.py` como modelo) un workflow
  que llame `/criterios` y `/casos` con `claude -p` y valide entre ambos. ¿Qué ganas y qué pierdes frente a `/fabrica`?

## Preguntas de repaso

1. ¿Por qué el arquitecto no puede escribir en `app/` y el desarrollador no puede escribir `plan.md`?
2. Si el orquestador dice «la app está lista», ¿le crees? ¿Qué comando lo decide?
3. ¿Qué diferencia hay entre la compuerta del desarrollador (SubagentStop) y el paso 7 del guion?
4. ¿Qué pasaría si `/fabrica` no tuviera `disable-model-invocation: true`?
5. ¿En qué casos preferirías un workflow en código en lugar de un orquestador con guion?
