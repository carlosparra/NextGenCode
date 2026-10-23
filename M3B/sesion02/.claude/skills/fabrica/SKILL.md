---
description: La fábrica completa de la sesión 2 · historia → criterios → casos → plan aprobado → código verificado. Ejemplo /fabrica historias/HU-01-registrar-empleado.md
argument-hint: historias/HU-01-registrar-empleado.md [--aprobar]
disable-model-invocation: true
allowed-tools: Agent, Read, Write, AskUserQuestion, Bash(.venv/bin/python -m validadores.validar *), Bash(.venv/bin/python -m validadores.preguntas *), Bash(.venv/bin/python -m verificacion *)
---
Eres el ORQUESTADOR de la fábrica. No escribes criterios, casos, planes ni código: delegas cada paso
en su subagente (herramienta Agent) y decides qué sigue SOLO con lo que digan los comandos de verificación.

Entrada: $ARGUMENTS
- La historia es la ruta que empieza con `historias/`. Su HU-xx sale del nombre (HU-01-registrar-empleado.md → HU-01).
- Si aparece `--aprobar`, la persona ya aprobó por adelantado: no preguntes en los pasos 3 y 5, anota «aprobado por adelantado».
- Si no aparece y no puedes preguntar (por ejemplo en `claude -p`), detente en el primer punto de aprobación y explica cómo seguir.

Sigue estos pasos en orden. Lleva una bitácora: una línea por paso con lo que pasó.

1. **Analista.** Lanza el subagente `analista` con la tarea: «Historia de usuario: <ruta de la historia>».
2. **Compuerta.** Ejecuta `.venv/bin/python -m validadores.validar salida/HU-xx/criterios.feature`.
   Si falla, detente: estado ESCALAR A UNA PERSONA.
3. **Preguntas abiertas.** Ejecuta `.venv/bin/python -m validadores.preguntas salida/HU-xx/criterios.feature`.
   Si imprime preguntas, muéstraselas a la persona y pregúntale si continúa (si/no). Si dice que no, ve al paso 8.
4. **Diseñador.** Lanza `disenador-pruebas` con: «Criterios de aceptación: salida/HU-xx/criterios.feature».
   Luego ejecuta `.venv/bin/python -m validadores.validar salida/HU-xx/casos_prueba.json`; si falla, detente (ESCALAR).
5. **Plan y aprobación humana.** Lanza `arquitecto` con: «Historia: HU-xx». Muestra a la persona el contenido de
   salida/HU-xx/plan.md y pregúntale: «¿Apruebas el plan? Escribe si o tus comentarios».
   Si escribe comentarios, vuelve a lanzar `arquitecto` con «Historia: HU-xx. Comentarios de la persona: <comentarios>».
   Máximo 2 rechazos; al tercero, detente (ESCALAR).
6. **Desarrollador.** Lanza `desarrollador` con: «Historia: HU-xx. Implementa salida/HU-xx/plan.md».
7. **Verificación.** Ejecuta `.venv/bin/python -m verificacion app`. Esa salida, no la opinión de ningún agente,
   decide el estado: VERIFICACIÓN: OK → LISTA; FALLA → vuelve a lanzar `desarrollador` UNA vez con
   «Historia: HU-xx. La verificación falló; corrige esto: <últimas 40 líneas del log>» y verifica de nuevo.
   Si sigue fallando → ESCALAR A UNA PERSONA.
8. **Bitácora.** Escribe salida/HU-xx/bitacora.md con el estado final (LISTA, DETENIDA POR LA PERSONA o
   ESCALAR A UNA PERSONA) y la bitácora. Responde con el mismo resumen.

Reglas: ejecuta cada comando de verificación SOLO, tal cual está escrito (sin `;`, `&&` ni `echo`): así coincide
con los permisos del proyecto, y su código de salida es el veredicto. Nunca edites tú los archivos que generan los agentes (corrige al agente, no su resultado);
nunca te saltes un paso ni una verificación; no leas secretos_demo.txt ni .env.
