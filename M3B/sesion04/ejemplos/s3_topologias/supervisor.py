"""Topología: Supervisor. Un agente central decide quién trabaja; todos le reportan a él.

Lo que distingue a la topología en el código:
  - en cada vuelta el supervisor devuelve una Decision (Literal): él elige al siguiente especialista,
  - cada especialista entrega su trabajo y regresa al supervisor; los especialistas nunca se hablan.

Uso:  python -m ejemplos.s3_topologias.supervisor
En tu fábrica:  el agente principal que corre /fabrica ES un supervisor: lanza subagentes y todos le reportan.
"""
from typing import Literal

from pydantic import BaseModel

from ejemplos.comun import claude, historia, paso, titulo

MAX_VUELTAS = 6
AGENTES = {
    "analista": "Escribe 3 criterios de aceptación breves en Gherkin para la historia.",
    "tester": "Escribe un caso de prueba por criterio (id, pasos, resultado esperado).",
    "desarrollador": "Propón el endpoint FastAPI y el modelo de datos, en pseudocódigo de 10 líneas.",
}


class Decision(BaseModel):
    siguiente: Literal["analista", "tester", "desarrollador", "FIN"]
    motivo: str


def supervisor(hu: str, trabajo: dict[str, str]) -> Decision:
    d = Decision.model_validate(claude(
        f"Eres el supervisor de un equipo: {list(AGENTES)}.\nHistoria:\n{hu}\n\n"
        f"Ya entregaron: {list(trabajo) or 'nadie'}.\nDecide quién sigue (cada uno trabaja una vez, "
        "en un orden que tenga sentido) o FIN si ya está todo.", esquema=Decision))
    paso("supervisor", f"→ {d.siguiente} · {d.motivo}")
    return d


def especialista(nombre: str, hu: str, trabajo: dict[str, str]) -> str:
    previo = "\n\n".join(f"## {k}\n{v}" for k, v in trabajo.items())
    texto = claude(f"{AGENTES[nombre]}\n\nHistoria:\n{hu}\n\n{previo}")
    paso(nombre, texto, 160)
    return texto


if __name__ == "__main__":
    titulo("Supervisor")
    hu, trabajo = historia("HU-01"), {}
    for _ in range(MAX_VUELTAS):                                   # tope de vueltas
        d = supervisor(hu, trabajo)                                # ← el supervisor enruta
        if d.siguiente == "FIN":
            break
        trabajo[d.siguiente] = especialista(d.siguiente, hu, trabajo)   # ← y el especialista le reporta
