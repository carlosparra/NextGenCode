"""El humano en el flujo: el agente propone, el código clasifica el riesgo y una persona aprueba lo irreversible.

Lo que distingue al patrón en el código: el modelo solo PROPONE acciones estructuradas; nada se ejecuta
todavía. El código decide qué es de bajo riesgo (se ejecuta solo) y qué es irreversible (espera a una
persona, que ve EXACTAMENTE qué se va a hacer y a quién). Lo que no se puede clasificar, se escala.
(En M3 la pausa era `interrupt()` de LangGraph; aquí es `input()`. En Claude Code es el diálogo de permisos
y, en un skill, la pregunta que el agente te hace antes de seguir.)

Uso:  python -m ejemplos.s2_flujos.humano
En tu fábrica:  /fabrica → aprobación del plan del arquitecto y de las preguntas abiertas
"""
from typing import Literal

from pydantic import BaseModel

from ejemplos.comun import EMPLEADOS, claude, paso, titulo


class Accion(BaseModel):
    tipo: Literal["cambiar_puesto", "dar_de_baja", "otra"]   # "otra": una forma honesta de decir «no sé qué es»
    numero_empleado: str
    detalle: str


class Acciones(BaseModel):
    acciones: list[Accion]


def interpretar(solicitud: str) -> tuple[list[Accion], list[Accion]]:
    """El agente propone; el CÓDIGO clasifica el riesgo, no el modelo."""
    a = Acciones.model_validate(claude(f"Directorio: {EMPLEADOS}\n\nConvierte esta solicitud de RR. HH. en "
                                       f"acciones:\n{solicitud}", esquema=Acciones))
    auto = [x for x in a.acciones if x.tipo == "cambiar_puesto"]
    riesgo = [x for x in a.acciones if x.tipo != "cambiar_puesto"]
    paso("agente propone", f"{len(auto)} automáticas · {len(riesgo)} requieren a una persona")
    return auto, riesgo


if __name__ == "__main__":
    titulo("El humano en el flujo")
    auto, riesgo = interpretar("Jorge Díaz (EMP-0004) pasa a ser Líder técnico. "
                               "Además, da de baja a Luis Pérez (EMP-0002) a partir de hoy.")
    bitacora = [f"AUTO · {x.tipo} {x.numero_empleado}: {x.detalle}" for x in auto]
    for linea in bitacora:
        paso("ejecuta sin pedir permiso", linea)
    for x in riesgo:                                             # ← la pausa: nada irreversible antes de esto
        empleado = next((e for e in EMPLEADOS if e["numero"] == x.numero_empleado), "NO ENCONTRADO")
        print(f"\n⏸  {x.tipo} · {empleado}\n   {x.detalle}")
        decision = input("   ¿Apruebas? (si / no) ").strip().lower()
        bitacora.append(f"{'APROBADA' if decision == 'si' else 'RECHAZADA'} por una persona · "
                        f"{x.tipo} {x.numero_empleado}: {x.detalle}")
    print("\nBitácora:", *bitacora, sep="\n  ")
