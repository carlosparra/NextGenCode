"""Patrón de flujo: Orquestador y trabajadores. Un modelo decide en el momento cuántas subtareas hay.

Lo que distingue al patrón en el código: el número de trabajadores NO está escrito en el código;
sale de la respuesta del orquestador (una lista) y se lanza un trabajador por elemento.
Compáralo con paralelizacion.py: allí las ramas están escritas; aquí no se conocen de antemano.

Uso:  python -m ejemplos.s2_flujos.orquestador
En tu fábrica:  Claude Code hace esto con subagentes: el agente principal decide cuántos lanzar (herramienta Agent)
"""
from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel

from ejemplos.comun import claude, historia, paso, titulo


class Subtareas(BaseModel):
    subtareas: list[str]  # entre 2 y 5, independientes entre sí (así se pueden hacer en paralelo)


def orquestador(hu: str) -> list[str]:
    plan = Subtareas.model_validate(claude(
        "Divide la implementación de esta historia en 2 a 5 subtareas independientes "
        "(por ejemplo: modelo de datos, endpoint, pantalla, pruebas). Decide tú cuántas:\n" + hu, esquema=Subtareas))
    paso("orquestador", f"decidió {len(plan.subtareas)} subtareas: {plan.subtareas}")
    return plan.subtareas


def trabajador(hu: str, subtarea: str) -> str:
    texto = claude(f"Historia:\n{hu}\n\nResuelve SOLO esta subtarea, en 5 líneas como máximo: {subtarea}")
    paso(f"trabajador · {subtarea[:40]}", texto, 160)
    return f"### {subtarea}\n{texto}"


if __name__ == "__main__":
    titulo("Orquestador y trabajadores")
    hu = historia("HU-03")
    subtareas = orquestador(hu)
    with ThreadPoolExecutor() as pool:                               # ← un trabajador por subtarea
        resultados = list(pool.map(lambda t: trabajador(hu, t), subtareas))
    paso("síntesis", claude("Une estos resultados en un plan de implementación coherente y breve:\n\n"
                            + "\n\n".join(resultados)), 600)
