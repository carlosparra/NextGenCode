# Fábrica de software con agentes · Módulo 3 · Sesión 2

Estado del proyecto al terminar la sesión 2.

| # | Agente | Entrada | Salida | Sesión |
| --- | --- | --- | --- | --- |
| 1 | Analista | Historia de usuario | `salida/HU-xx/criterios.feature` | 1 |
| 2 | Diseñador de pruebas | Criterios | `salida/HU-xx/casos_prueba.json` | 1 |
| 3 | Desarrollador (Claude Code) | Criterios y casos | `app/backend`, `app/frontend` | 2 |

## Requisitos

Python 3.12, Node 20 o superior, Docker Desktop, Claude Code y una clave de API de Anthropic con créditos.

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env        # escribe ANTHROPIC_API_KEY y MODEL
```

## Cómo correr los agentes

1. Activa el entorno y revisa `.env` (`ANTHROPIC_API_KEY`, `MODEL` y `PRESUPUESTO_USD`). Necesitas Node para el frontend.
2. Los agentes 1 y 2 se siguen corriendo por separado, como en la sesión 1. La **fábrica completa** es `flujos.flujo_s2`:
   analista → diseñador → plan → **tu aprobación** → desarrollador → verificación.
3. El flujo **se detiene a preguntarte** en la terminal:
   - si el analista dejó preguntas abiertas: `si` para seguir; cualquier otra respuesta detiene el flujo;
   - al mostrarte el plan: `si` lo aprueba; si escribes comentarios, el agente planifica de nuevo (máximo 3 rechazos).
4. Al terminar imprime `=== HU-01 · app LISTA · … USD ===` (o `ESCALAR A UNA PERSONA`) y la bitácora.
5. El código queda en `app/backend` y `app/frontend`. Compruébalo con
   `python -c "from flujos.verificacion import verificar_app; print(verificar_app()[0])"` (debe imprimir `True`).

## Uso

```bash
# Agentes 1 y 2 por separado
python -m agentes.analista historias/HU-01-registrar-empleado.md
python -m agentes.disenador_pruebas salida/HU-01/criterios.feature

# Fábrica con estado: analista -> diseñador -> plan aprobado -> desarrollador
python -m flujos.flujo_s2 historias/HU-01-registrar-empleado.md
```

Los patrones de cada sesión tienen un ejemplo corto en [`ejemplos/`](ejemplos/README.md), por ejemplo `python -m ejemplos.s2_flujos.enrutamiento`.

La aplicación queda en http://localhost:8080 y la documentación de la API en http://localhost:8000/docs.
