# Curso: Construcción de Sistemas Agénticos (Módulo 3 · versión B, sin API key)

Repositorio de la «fábrica de software»: una cadena de agentes que, a partir de una historia de usuario,
escribe criterios de aceptación, casos de prueba, el código de una aplicación de gestión de empleados
(base de datos, API y front-end), la despliega y la prueba de punta a punta. En esta versión **cada agente
es un subagente de Claude Code** y se usa con `claude login` (sin ANTHROPIC_API_KEY).

## Estructura

- `.claude/agents/` — los subagentes: su prompt de sistema y sus herramientas
- `.claude/skills/` — los comandos de la fábrica (`/criterios`, `/casos`, ...)
- `.claude/settings.json` — permisos del proyecto y registro de hooks
- `hooks/roles.py` — qué puede leer, escribir y ejecutar cada subagente
- `hooks/rol.py` — hook PreToolUse que aplica `roles.py` (mínima agencia)
- `hooks/compuerta.py` — hook SubagentStop: un subagente no termina hasta que su entrega es válida
- `validadores/` — contratos Pydantic y validadores deterministas (sin modelo)
- `historias/`, `contexto/` — entradas; `salida/HU-xx/` — artefactos por historia
- `ejemplos/` — un programa corto por patrón, con `claude -p`

## Reglas

- Comentarios, nombres de dominio y mensajes en español
- El código decide si un paso terminó bien, no el agente: cada entrega pasa por `validadores/`
- Todo bucle tiene un límite (intentos de la compuerta, ciclos de corrección)
- Nunca leas `.env` ni `secretos_demo.txt`; los ataques de clase apuntan solo al señuelo
- No edites a mano lo que generan los agentes en `salida/`: corrige al agente, no su resultado
- Antes de cambiar más de un archivo, muestra un plan y espera aprobación; explica el porqué de cada cambio
