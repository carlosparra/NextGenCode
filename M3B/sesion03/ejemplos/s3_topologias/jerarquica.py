"""Topología: Jerárquica. Supervisores de supervisores: cada equipo tiene su líder.

Lo que distingue a la topología en el código: el director no habla con los miembros, solo con los
líderes, y cada líder le sube un RESUMEN corto, no los mensajes internos: así cada nivel mantiene su
contexto pequeño.

Uso:  python -m ejemplos.s3_topologias.jerarquica
En tu fábrica:  el agente principal lanza subagentes, y un subagente con la herramienta Agent puede lanzar
los suyos (hasta 3 niveles por defecto). Cada uno regresa solo su mensaje final, como estos líderes.
"""
from typing import Literal

from pydantic import BaseModel

from ejemplos.comun import claude, historia, paso, titulo

EQUIPOS = {
    "calidad": [("analista", "Escribe 3 criterios Gherkin breves."),
                ("tester", "Escribe un caso de prueba por criterio.")],
    "desarrollo": [("backend", "Propón el endpoint FastAPI en 8 líneas."),
                   ("frontend", "Propón el formulario React en 8 líneas.")],
}


class Orden(BaseModel):
    siguiente: Literal["calidad", "desarrollo", "FIN"]


def equipo(nombre: str, hu: str) -> str:
    """Un equipo completo: miembros en cadena y su líder al final, que resume para el director."""
    detalle = ""
    for miembro, tarea in EQUIPOS[nombre]:
        texto = claude(f"{tarea}\n\nHistoria:\n{hu}\n\n{detalle}")
        paso(f"  {miembro}", texto, 120)
        detalle += f"\n## {miembro}\n{texto}"
    resumen = claude(f"Resume en 3 viñetas para el director:\n{detalle}")   # ← lo que sube de nivel es corto
    paso(f" líder de {nombre}", resumen, 160)
    return resumen


if __name__ == "__main__":
    titulo("Jerárquica")
    hu, informes = historia("HU-01"), {}
    while len(informes) < len(EQUIPOS):
        o = Orden.model_validate(claude(
            f"Diriges los equipos 'calidad' y 'desarrollo'. Ya informaron: {list(informes) or 'ninguno'}. "
            "¿Qué equipo trabaja ahora? (calidad define qué se espera antes de que desarrollo construya)",
            esquema=Orden))
        paso("director", f"→ equipo {o.siguiente}")
        if o.siguiente == "FIN" or o.siguiente in informes:
            break
        informes[o.siguiente] = equipo(o.siguiente, hu)              # ← un equipo dentro del flujo del director
    for nombre, informe in informes.items():
        print(f"\nInforme de {nombre}:\n{informe}")
