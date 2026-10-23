# Fábrica de software con agentes · Módulo 3 · Sesión 3

Estado del proyecto al terminar la sesión 3.

| # | Agente | Entrada | Salida | Sesión |
| --- | --- | --- | --- | --- |
| 1 | Analista | Historia de usuario | `salida/HU-xx/criterios.feature` | 1 |
| 2 | Diseñador de pruebas | Criterios | `salida/HU-xx/casos_prueba.json` | 1 |
| 3 | Desarrollador (Claude Code) | Criterios y casos | `app/backend`, `app/frontend` | 2 |
| 4 | Despliegue (Claude Code) | Código | Contenedores con Docker Compose | 3 |
| 5 | Automatizador (Claude Code) | Casos de prueba | `app/tests` (pytest + Playwright) | 3 |

## Requisitos

Python 3.12, Node 20 o superior, Docker Desktop, Claude Code y una clave de API de Anthropic con créditos.

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
playwright install chromium
cp .env.example .env        # escribe ANTHROPIC_API_KEY y MODEL
```

## Cómo correr los agentes

1. Activa el entorno, revisa `.env` y **enciende Docker Desktop** (`docker info` debe responder).
2. `flujos.flujo_s3` hace lo mismo que el de la sesión 2 y, si la app verifica, lanza **en paralelo** al agente de
   despliegue (Docker Compose) y al automatizador (pruebas pytest + Playwright).
3. Responde las mismas pausas de la sesión 2: preguntas abiertas y aprobación del plan.
4. El flujo dice **LISTA** solo si pasan la app, el despliegue **y** las pruebas; si no, `ESCALAR A UNA PERSONA`.
5. La app queda en http://localhost:8080 y la API en http://localhost:8000/docs. Apágala con `cd app && docker compose down`.

## Uso

```bash
# Agentes 1 y 2 por separado
python -m agentes.analista historias/HU-01-registrar-empleado.md
python -m agentes.disenador_pruebas salida/HU-01/criterios.feature

# Fábrica con estado: analista -> diseñador -> plan aprobado -> desarrollador
python -m flujos.flujo_s2 historias/HU-01-registrar-empleado.md

# Se suman despliegue y automatización
python -m flujos.flujo_s3 historias/HU-01-registrar-empleado.md
```

Los patrones de cada sesión tienen un ejemplo corto en [`ejemplos/`](ejemplos/README.md), por ejemplo `python -m ejemplos.s3_topologias.supervisor`.

La aplicación queda en http://localhost:8080 y la documentación de la API en http://localhost:8000/docs.
