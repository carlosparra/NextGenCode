"""Hook SubagentStop · El código decide cuándo terminó un agente (reflexión con tope).

Claude Code llama a este script cuando un subagente quiere terminar. Si su entrega no pasa
el validador determinista, respondemos {"decision": "block", "reason": ...}: el subagente
NO termina, recibe los problemas como instrucción y vuelve a intentarlo.

Es el mismo patrón que `generar_criterios()` en M3 (intentar → validar → corregir), pero
aquí el bucle lo pone Claude Code y nosotros solo ponemos la compuerta y el tope.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from hooks.roles import ROLES  # noqa: E402
from validadores.validar import problemas_de  # noqa: E402

MAX_INTENTOS = 3                                  # todo bucle tiene un límite
ESTADO = RAIZ / "salida" / ".compuerta"           # cuántas veces hemos bloqueado a cada subagente


def tarea_del_subagente(transcripcion: str | None) -> str:
    """El primer mensaje de la transcripción del subagente es la tarea que recibió."""
    try:
        with open(transcripcion, encoding="utf-8") as f:
            for linea in f:
                d = json.loads(linea)
                if d.get("type") == "user":
                    contenido = d["message"]["content"]
                    return contenido if isinstance(contenido, str) else json.dumps(contenido)
    except (OSError, TypeError, ValueError, KeyError):
        pass
    return ""


if __name__ == "__main__":
    datos = json.load(sys.stdin)
    agente = datos.get("agent_type")
    rol = ROLES.get(agente)
    hu = re.search(r"HU-\d+", tarea_del_subagente(datos.get("agent_transcript_path")))
    if not rol or not rol.entrega or not hu:      # sin entrega asignada no hay nada que validar
        sys.exit(0)

    ruta = RAIZ / "salida" / hu.group() / rol.entrega
    problemas = problemas_de(ruta) if ruta.exists() else [f"No escribiste {ruta.relative_to(RAIZ)}."]
    if problemas is None:                         # falla cerrado: una entrega sin validador nunca pasa sola
        problemas = [f"La compuerta no sabe validar {rol.entrega}; agrega su validador en validadores/validar.py."]
    if not problemas:
        sys.exit(0)                               # entrega válida: puede terminar

    ESTADO.mkdir(parents=True, exist_ok=True)
    contador = ESTADO / f"{datos.get('agent_id', agente)}.txt"
    intentos = int(contador.read_text()) if contador.exists() else 0
    if intentos >= MAX_INTENTOS:                  # tope: dejamos terminar y avisamos a la persona
        print(json.dumps({"systemMessage": f"{agente}: {ruta.relative_to(RAIZ)} sigue inválido tras "
                                           f"{MAX_INTENTOS} correcciones; revísalo a mano:\n- "
                                           + "\n- ".join(problemas)}, ensure_ascii=False))
        sys.exit(0)
    contador.write_text(str(intentos + 1))
    print(json.dumps({"decision": "block", "reason":
                      f"El validador rechazó {ruta.relative_to(RAIZ)} (corrección {intentos + 1} de "
                      f"{MAX_INTENTOS}). Corrige y vuelve a guardarlo completo:\n- " + "\n- ".join(problemas)},
                     ensure_ascii=False))
