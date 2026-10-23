"""Topología: Red (swarm). Cualquier agente puede pasarle el trabajo a cualquier otro.

Lo que distingue a la topología en el código: no hay un orden ni un jefe; cada turno, el agente
que trabaja elige al siguiente. El flujo emerge de sus decisiones; por eso el tope de turnos es obligatorio.
Compáralo con supervisor.py: allí solo el supervisor decide; aquí decide cada uno.

Uso:  python -m ejemplos.s3_topologias.red
En tu fábrica:  no la usamos: con pasos conocidos, un guion fijo es más predecible y más barato.
"""
from typing import Literal

from pydantic import BaseModel

from ejemplos.comun import claude, historia, paso, titulo

MAX_TURNOS = 6
ROLES = {
    "analista": "aclaras la historia y escribes criterios de aceptación",
    "tester": "buscas huecos en los criterios y propones casos de prueba",
    "desarrollador": "propones cómo implementarlo (endpoint y modelo de datos)",
    "revisor": "revisas todo el trabajo y decides si está listo",
}


class Turno(BaseModel):
    aporte: str                                                             # máximo 4 líneas
    siguiente: Literal["analista", "tester", "desarrollador", "revisor", "FIN"]
    motivo: str


if __name__ == "__main__":
    titulo("Red")
    hu, notas, actual, turnos = historia("HU-03"), [], "analista", 0
    while actual != "FIN" and turnos < MAX_TURNOS:                          # ← tope obligatorio
        turnos += 1
        t = Turno.model_validate(claude(
            f"Eres el {actual}: {ROLES[actual]}. Equipo: {list(ROLES)}.\nHistoria:\n{hu}\n\n"
            "Notas del equipo hasta ahora:\n" + "\n".join(notas) +
            "\n\nAporta algo nuevo (máximo 4 líneas) y elige a quién pasar el trabajo, o FIN si está listo.",
            esquema=Turno))
        paso(f"{actual} · turno {turnos}", f"{t.aporte}  → {t.siguiente} ({t.motivo})", 220)
        notas.append(f"{actual}: {t.aporte}")
        actual = t.siguiente                                                # ← cualquiera → cualquiera
    print(f"\nTurnos usados: {turnos} de {MAX_TURNOS}")
