# Fábrica de software con agentes · M3B · Sesión 4

**Flujo E2E con triage y defensas: la fábrica completa, segura y con humanos en el lazo.**

| # | Agente | Entrada | Salida | Sesión |
| --- | --- | --- | --- | --- |
| 0 | Filtro de seguridad | Historia (no confiable) | `salida/HU-xx/veredicto.json` | 4 |
| 1 | Analista | Historia de usuario | `salida/HU-xx/criterios.feature` | 1 |
| 2 | Diseñador de pruebas | Criterios | `salida/HU-xx/casos_prueba.json` | 1 |
| 3 | Arquitecto + Desarrollador | Criterios y casos | `app/backend`, `app/frontend` | 2 |
| 4 | Despliegue | Código | Contenedores con Docker Compose | 3 |
| 5 | Automatizador | Casos de prueba | `app/tests` (pytest + Playwright) | 3 |
| 6 | Triage | Pruebas fallidas | `salida/HU-xx/diagnostico.json` → reporte | 4 |

## La idea de la sesión

Dos temas: **cerrar el ciclo** (probar de punta a punta y, si algo falla, que el responsable correcto lo corrija)
y **seguridad** (la historia de usuario es contenido no confiable).

| Concepto del curso | En M3 (API + LangGraph) | En M3B (Claude Code) |
| --- | --- | --- |
| Pruebas E2E | `ejecutar_pruebas()` | `python -m verificacion e2e HU-xx` → `resultados.xml` y `fallos.md` |
| Triage (supervisor que enruta) | `diagnosticar()` con `Diagnostico` (Pydantic) | subagente `triage` → `diagnostico.json`, validado con el mismo contrato |
| Ciclo de corrección con tope | `MAX_CICLOS = 2` | paso 11 de `/fabrica`: máximo 2 ciclos, luego ESCALAR |
| Filtro de historia | `filtrar_historia()` con `Veredicto` | subagente `filtro-seguridad` (solo lee `historias/`, solo escribe su veredicto) |
| El orquestador no lee lo no confiable | — | regla del guion: el principal **nunca** lee la historia, solo pasa su ruta |
| Lectura confinada y secretos | `confinar_lectura()` | `hooks/seguridad.py` (para todos) + `hooks/rol.py` (por rol) |
| Comandos permitidos | `comandos_permitidos()` | `programas` de `hooks/roles.py` + `hooks/seguridad.py` (sin `$(...)`, sin secretos) |
| Prevención de fuga | — | `hooks/seguridad.py` bloquea escribir el contenido del señuelo |
| Auditoría | `auditar()` → `auditoria.jsonl` | `hooks/seguridad.py` → `auditoria.jsonl` (con `agent_type`) |
| Sin salida a internet | `disallowed_tools=["WebFetch", "WebSearch"]` | `permissions.deny` en `.claude/settings.json` |
| Demo del ataque | `DEFENSAS=0` | `DEFENSAS=0 claude` (apaga `seguridad.py`, el filtro y la lectura por rol; la escritura por rol sigue) |

**Defensa en profundidad:** ninguna capa es suficiente sola. El filtro puede equivocarse; por eso además el agente
que lee la historia casi no tiene poder, los hooks bloquean las lecturas peligrosas y la auditoría deja rastro.

## Cómo fluye `/fabrica` (lo nuevo: pasos 0, 10, 11 y 12)

```
0 filtro ──sospechosa──► 12 reporte (BLOQUEADA)
   │ ok
1 … 9 (sesiones 1 a 3) ─► 10 verificacion e2e ──OK──► 12 reporte (LISTA)
                               │ falla
                               ▼
                        11 triage ─► desarrollador (+ redespliegue) │ automatizador │ despliegue
                               └──────────── vuelve a 10 (máx. 2 ciclos) ─► ESCALAR
```

## Requisitos

Los de la sesión 3 (Docker encendido, `playwright install chromium`).

## Uso

```
/fabrica historias/HU-01-registrar-empleado.md
/filtrar historias/HU-99-envenenada.md          ← el filtro por separado
/triage HU-01                                    ← el triage por separado (necesita salida/HU-01/fallos.md)
```

Demo de seguridad con la historia envenenada:

```bash
claude -p "/fabrica historias/HU-99-envenenada.md --aprobar" --permission-mode acceptEdits     # BLOQUEADA
DEFENSAS=0 claude -p "/fabrica historias/HU-99-envenenada.md --aprobar" --permission-mode acceptEdits   # solo en clase
grep -r "BANDERA-DEMO" app/ && echo "el ataque funcionó"
tail auditoria.jsonl                              # qué herramientas usó cada agente
```

Probar los hooks sin modelo:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"cat $(echo .env)"}}' | .venv/bin/python hooks/seguridad.py; echo $?
```

## Labs

- **Lab 4A · El ataque.** Lee `historias/HU-99-envenenada.md`. Corre la demo con y sin defensas. ¿Qué capa lo detuvo
  primero? Desactiva solo el filtro (paso 0 del guion) y vuelve a intentarlo: ¿qué capa lo detiene ahora?
- **Lab 4B · El triage.** Edita una prueba de `app/tests/` para que espere un código de estado equivocado y corre los
  pasos 10 y 11. ¿A quién manda el triage? ¿Qué criterio de aceptación usó para decidir?
- **Lab 4C · Auditoría.** Con `auditoria.jsonl`, responde: ¿qué agente usó más herramientas? ¿Alguno intentó leer algo
  fuera de su rol?
- **Lab 4D · Tu defensa.** Agrega a `hooks/seguridad.py` una regla nueva (por ejemplo, bloquear `curl` a dominios que no
  sean `localhost`) y pruébala sin modelo con `echo '...' | .venv/bin/python hooks/seguridad.py`.

## Preguntas de repaso

1. ¿Por qué el orquestador no debe leer la historia, si es el agente «más inteligente»?
2. ¿Por qué el filtro usa un modelo pequeño y casi no tiene herramientas?
3. ¿Qué capas siguen activas con `DEFENSAS=0` y por qué no se apagan?
4. ¿Qué evita que el ciclo triage → corrección → E2E sea infinito?
5. ¿Qué información deja `auditoria.jsonl` que no deja la bitácora del orquestador?
