# Fábrica de software con agentes · M3B · Sesión 3

**Agentes 4 (despliegue) y 5 (automatizador) en paralelo, topologías multi-agente y MCP.**

| # | Agente | Entrada | Salida | Sesión |
| --- | --- | --- | --- | --- |
| 1 | Analista | Historia de usuario | `salida/HU-xx/criterios.feature` | 1 |
| 2 | Diseñador de pruebas | Criterios | `salida/HU-xx/casos_prueba.json` | 1 |
| 3 | Arquitecto + Desarrollador | Criterios y casos | `app/backend`, `app/frontend` | 2 |
| 4 | Despliegue | Código | Contenedores con Docker Compose | 3 |
| 5 | Automatizador | Casos de prueba | `app/tests` (pytest + Playwright) | 3 |

## La idea de la sesión

Con cinco agentes ya importa la **topología**: quién habla con quién y quién decide. La fábrica es un
**supervisor**: el agente principal (`/fabrica`) lanza a cada especialista y todos le reportan; los
especialistas nunca se hablan entre sí, solo dejan su trabajo en la pizarra (`salida/HU-xx/` y `app/`).

| Concepto del curso | En M3 (API + LangGraph) | En M3B (Claude Code) |
| --- | --- | --- |
| Paralelización | `despues_de_verificar()` devuelve `["desplegar", "automatizar"]` | paso 8: el orquestador lanza los dos subagentes **en el mismo mensaje** |
| Unión | `add_edge(["desplegar", "automatizar"], "listo")` | paso 9: espera a ambos y corre las dos verificaciones |
| Supervisor | `flujo_s4.py` (en código) | el agente principal con `/fabrica` |
| Jerárquica | Claude Code con sus subagentes | un subagente con la herramienta Agent puede lanzar los suyos (hasta 3 niveles) |
| Pizarra | el `Estado` de LangGraph | `salida/HU-xx/`: cada subagente lee lo que dejó el anterior |
| Mínima agencia por rol | `ESCRITURA` y `PROGRAMAS` de cada agente | `hooks/roles.py`: `despliegue` solo escribe Dockerfiles; `automatizador` solo `app/tests/` |
| Verificación de cada rama | `verificar_despliegue()` y `verificar_pruebas_escritas()` | `python -m verificacion despliegue` y `python -m verificacion pruebas HU-xx` |
| MCP | `claude mcp add directorio -- ...` | `.mcp.json` en la raíz: el servidor se comparte con el proyecto |

## Cómo fluye `/fabrica` (lo nuevo está en el paso 8)

```
… 7 verificacion app ─┬─► despliegue ─────(compuerta: verificacion despliegue)─┬─► 9 unión ─► 10 bitacora.md
                      └─► automatizador ─(compuerta: verificacion pruebas)─────┘
```

## Requisitos

Todo lo de la sesión 2, más **Docker Desktop encendido** y el navegador de Playwright:

```bash
uv pip install -r requirements.txt
playwright install chromium
docker info > /dev/null && echo "Docker OK"
claude            # acepta el diálogo de confianza y, si te lo pregunta, el servidor MCP «directorio»
```

## Cómo correr los agentes

1. Prepara la sesión como en la 2 y **enciende Docker Desktop** (`docker info` debe responder). La primera vez,
   aprueba el servidor MCP `directorio` cuando Claude Code te lo pregunte.
2. `/fabrica` hace lo de la sesión 2 y, en el **paso 8**, lanza a la vez al subagente de **despliegue** y al
   **automatizador**. Cada uno tiene su compuerta.
3. Comprueba cada rama con `python -m verificacion despliegue` y `python -m verificacion pruebas HU-01`.
4. La app queda en http://localhost:8080. Apágala con `cd app && docker compose down`.

## Uso

```
/fabrica historias/HU-01-registrar-empleado.md
/desplegar HU-01                 ← agentes por separado
/automatizar HU-01
```

```bash
python -m verificacion despliegue
python -m verificacion pruebas HU-01
cd app && docker compose down    # apagar
```

App en http://localhost:8080 · API en http://localhost:8000/docs

MCP: con `claude` abierto en la raíz, `/mcp` muestra el servidor `directorio`; pregunta «¿quién es el empleado activo más
antiguo de Tecnología?». O sin interacción: `python -m ejemplos.s3_topologias.mcp_cliente`.

## Labs

- **Lab 3A · Paralelo de verdad.** Corre `/fabrica` y observa el paso 8: ¿salen los dos subagentes en el mismo turno?
  Cambia el guion para lanzarlos uno después del otro y compara el tiempo total.
- **Lab 3B · Mínima agencia.** Pide al subagente `despliegue` que «arregle de paso» `app/backend/main.py`. ¿Quién lo
  impide? Encuentra la línea en `hooks/roles.py`.
- **Lab 3C · Topologías.** Corre `ejemplos/s3_topologias/supervisor.py` y `red.py` con la misma historia. ¿Cuántos turnos
  usa cada uno? ¿Cuál tiene tope y por qué es obligatorio?
- **Lab 3D · Tu servidor MCP.** Agrega a `mcp_directorio.py` una herramienta `contar_por_departamento()` y pregúntale a
  Claude Code por ella sin cambiar nada más. ¿Qué tuviste que escribir y qué descubrió solo?

## Preguntas de repaso

1. ¿Por qué despliegue y automatización pueden ir en paralelo, pero desarrollador y despliegue no?
2. ¿Qué topología es `/fabrica`? ¿Y la carpeta `salida/HU-xx/`?
3. ¿Qué cambia para un subagente si una herramienta viene de MCP en lugar de ser integrada?
4. Si el automatizador escribe pruebas que pasan la recolección pero no cubren todos los casos, ¿quién lo detecta?
