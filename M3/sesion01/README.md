# Fábrica de software con agentes · Módulo 3 · Sesión 1

Punto de partida de la sesión 1: el bucle de `agentes/base.py` lo completas en el Lab 1A.

| # | Agente | Entrada | Salida | Sesión |
| --- | --- | --- | --- | --- |
| 1 | Analista | Historia de usuario | `salida/HU-xx/criterios.feature` | 1 |
| 2 | Diseñador de pruebas | Criterios | `salida/HU-xx/casos_prueba.json` | 1 |

## Requisitos

Python 3.12 y una clave de API de Anthropic con créditos.

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env        # escribe ANTHROPIC_API_KEY y MODEL
```

## Uso

```bash
# Agentes 1 y 2 por separado
python -m agentes.analista historias/HU-01-registrar-empleado.md
python -m agentes.disenador_pruebas salida/HU-01/criterios.feature
```

Los patrones de cada sesión tienen un ejemplo corto en [`ejemplos/`](ejemplos/README.md), por ejemplo `python -m ejemplos.s1_razonamiento.react`.
