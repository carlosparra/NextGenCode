"""Topología: Traspasos (handoffs). No hay supervisor: el agente activo pasa el control.

Lo que distingue a la topología en el código:
  - cada agente responde O transfiere (`transferir_a`); transferir ES decidir quién sigue,
  - todos comparten UNA conversación, que viaja con el control,
  - cambia el prompt de sistema (el «quién soy»), no la conversación.

Uso:  python -m ejemplos.s3_topologias.traspasos
En tu fábrica:  analista → diseñador → desarrollador podrían ser traspasos; usamos un guion (/fabrica) para fijar el orden.
"""
from typing import Literal

from pydantic import BaseModel

from ejemplos.comun import EMPLEADOS, claude, paso, titulo

MAX_TRASPASOS = 4
AGENTES = {
    "recepcion": "Eres recepción de RR. HH. No resuelves nada: transfiere al agente correcto (altas o directorio).",
    "altas": "Atiendes altas y bajas. Explica qué datos se necesitan para registrar (reglas: correo "
             "@empresa.com, departamento válido, fecha no futura). Si piden otra cosa, transfiere.",
    "directorio": f"Consultas el directorio. Datos: {EMPLEADOS}. Responde la consulta; si piden otra cosa, transfiere.",
}


class Turno(BaseModel):
    transferir_a: Literal["recepcion", "altas", "directorio", "nadie"]   # "nadie" = respondo yo
    motivo: str
    respuesta: str                                                       # vacía si transfiere


def atender(pregunta: str) -> str:
    conversacion, agente = [f"Persona: {pregunta}"], "recepcion"
    for traspasos in range(MAX_TRASPASOS + 1):
        t = Turno.model_validate(claude("\n".join(conversacion), sistema=AGENTES[agente], esquema=Turno))
        if t.transferir_a in ("nadie", agente) or traspasos == MAX_TRASPASOS:
            paso(agente, t.respuesta)
            return t.respuesta                                           # responde y termina
        paso(agente, f"traspasa a {t.transferir_a}: {t.motivo}")         # ← el traspaso
        conversacion.append(f"[Traspaso: {agente} pasa la conversación a {t.transferir_a}. Motivo: {t.motivo}]")
        agente = t.transferir_a
    return ""


if __name__ == "__main__":
    for pregunta in ["Quiero dar de alta a una nueva analista en Finanzas, ¿qué necesito?",
                     "¿Quién es el empleado más antiguo de Tecnología que sigue activo?"]:
        titulo(f"Traspasos · «{pregunta}»")
        atender(pregunta)
