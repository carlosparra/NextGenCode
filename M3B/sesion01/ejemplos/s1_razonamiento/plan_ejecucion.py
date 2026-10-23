"""Patrón Plan-and-Execute: primero un plan completo y revisable; después se ejecuta paso a paso.

Lo que distingue al patrón: DOS fases separadas. La primera devuelve una estructura (Plan, con
Pydantic) que una persona puede aprobar; la segunda recorre esa lista con un `for`.
En M3 el plan salía de una herramienta forzada (tool_choice); en M3B, de `--json-schema`.

Uso:  python -m ejemplos.s1_razonamiento.plan_ejecucion
En tu fábrica:  el subagente arquitecto (plan, solo lectura) y el desarrollador (lo ejecuta), sesión 2.
Claude Code trae este patrón integrado: `claude --permission-mode plan` (o Shift+Tab dos veces).
"""
from pydantic import BaseModel

from ejemplos.comun import claude, historia, paso, titulo


class Plan(BaseModel):
    pasos: list[str]  # cada paso es una instrucción concreta y ejecutable


def planificar(tarea: str) -> Plan:
    """Fase 1. La salida estructurada garantiza la forma; Pydantic la valida otra vez en nuestro lado."""
    return Plan.model_validate(claude(f"Haz un plan breve, de 3 a 5 pasos, para: {tarea}", esquema=Plan))


def ejecutar(tarea: str, plan: Plan) -> str:
    """Fase 2. Cada paso recibe lo que produjeron los anteriores."""
    avance = ""
    for i, instruccion in enumerate(plan.pasos, 1):
        resultado = claude(f"Tarea general: {tarea}\nAvance hasta ahora:\n{avance or '(nada)'}\n\n"
                           f"Haz SOLO este paso y responde en pocas líneas: {instruccion}")
        paso(f"ejecuta {i}/{len(plan.pasos)}", resultado)
        avance += f"\n## Paso {i}: {instruccion}\n{resultado}"
    return avance


if __name__ == "__main__":
    tarea = "Definir qué construir para esta historia (modelo de datos, endpoint y pantalla):\n" + historia("HU-01")
    titulo("Fase 1 · Planificar")
    plan = planificar(tarea)
    for i, p in enumerate(plan.pasos, 1):
        print(f"  {i}. {p}")
    if input("\n¿Aprobar el plan? (si/no) ").strip().lower() != "si":   # punto de control humano
        raise SystemExit("Plan rechazado: no se gastó nada en ejecutarlo.")
    titulo("Fase 2 · Ejecutar")
    ejecutar(tarea, plan)
