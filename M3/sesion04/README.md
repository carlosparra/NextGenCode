# Fábrica de software con agentes · Módulo 3 · Sesión 4

Estado del proyecto al terminar la sesión 4.

| # | Agente | Entrada | Salida | Sesión |
| --- | --- | --- | --- | --- |
| 1 | Analista | Historia de usuario | `salida/HU-xx/criterios.feature` | 1 |
| 2 | Diseñador de pruebas | Criterios | `salida/HU-xx/casos_prueba.json` | 1 |
| 3 | Desarrollador (Claude Code) | Criterios y casos | `app/backend`, `app/frontend` | 2 |
| 4 | Despliegue (Claude Code) | Código | Contenedores con Docker Compose | 3 |
| 5 | Automatizador (Claude Code) | Casos de prueba | `app/tests` (pytest + Playwright) | 3 |
| 6 | Flujo E2E con triage | Pruebas y app desplegada | `salida/HU-xx/reporte.md` | 4 |

## Requisitos

Python 3.12, Node 20 o superior, Docker Desktop, Claude Code y una clave de API de Anthropic con créditos.

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
playwright install chromium
cp .env.example .env        # escribe ANTHROPIC_API_KEY y MODEL
```

## Cómo correr los agentes

1. Activa el entorno, revisa `.env`, enciende Docker y ten instalado el navegador de Playwright (`playwright install chromium`).
2. `flujos.flujo_s4` empieza con el **filtro de seguridad**: si la historia es sospechosa, se detiene (BLOQUEADA POR SEGURIDAD)
   sin gastar en los demás agentes.
3. Después hace lo de la sesión 3 y corre las **pruebas E2E** contra la app desplegada. Si fallan, el **triage** manda
   corregir al responsable y vuelve a probar (máximo 2 ciclos).
4. El resultado queda en `salida/HU-01/reporte.md`: LISTA, ESCALAR A UNA PERSONA o BLOQUEADA POR SEGURIDAD.
5. La demostración con `historias/HU-99-envenenada.md` y `DEFENSAS=0` se hace **solo en una copia** de la carpeta.

## Uso

```bash
# Agentes 1 y 2 por separado
python -m agentes.analista historias/HU-01-registrar-empleado.md
python -m agentes.disenador_pruebas salida/HU-01/criterios.feature

# Fábrica con estado: analista -> diseñador -> plan aprobado -> desarrollador
python -m flujos.flujo_s2 historias/HU-01-registrar-empleado.md

# Se suman despliegue y automatización
python -m flujos.flujo_s3 historias/HU-01-registrar-empleado.md

# Flujo completo con pruebas E2E, triage y defensas
python -m flujos.flujo_s4 historias/HU-01-registrar-empleado.md
```

Los patrones de cada sesión tienen un ejemplo corto en [`ejemplos/`](ejemplos/README.md), por ejemplo `python -m ejemplos.s3_topologias.supervisor`.

La aplicación queda en http://localhost:8080 y la documentación de la API en http://localhost:8000/docs.
