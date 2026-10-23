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

## Cómo correr los agentes

1. Activa el entorno (`source .venv/bin/activate`) y revisa que `.env` tenga `ANTHROPIC_API_KEY` y `MODEL`.
2. Corre **primero el analista y después el diseñador**: el segundo trabaja con lo que deja el primero.
   - El **analista** lee la historia y `contexto/`, y escribe `salida/HU-01/criterios.feature`.
   - El **diseñador** lee esos criterios y escribe `salida/HU-01/casos_prueba.json`.
3. Cada uno imprime cuántos escenarios o casos escribió. Revisa el resultado con
   `cat salida/HU-01/criterios.feature` y `cat salida/HU-01/casos_prueba.json`.
4. Repite con `HU-02` y `HU-03`.

En esta carpeta el bucle de `agentes/base.py` está **sin terminar a propósito** (Lab 1A): hasta que lo completes,
el analista falla con `NotImplementedError`. La carpeta de la sesión 2 ya lo trae resuelto.

**En macOS: `zsh: command not found: python`.** macOS solo trae `python3`; el comando `python` aparece al activar el
entorno virtual con `source .venv/bin/activate`, y hay que activarlo **en cada terminal nueva**. Si el entorno no
existe, créalo con `uv venv` y `uv pip install -r requirements.txt`. También puedes llamar al Python del entorno
directamente: `.venv/bin/python -m ...`. No uses `python3` a secas: es el del sistema y no tiene las dependencias del
curso, así que falla con `ModuleNotFoundError`.

## Uso

```bash
# Agentes 1 y 2 por separado
python -m agentes.analista historias/HU-01-registrar-empleado.md
python -m agentes.disenador_pruebas salida/HU-01/criterios.feature
```

Los patrones de cada sesión tienen un ejemplo corto en [`ejemplos/`](ejemplos/README.md), por ejemplo `python -m ejemplos.s1_razonamiento.react`.
