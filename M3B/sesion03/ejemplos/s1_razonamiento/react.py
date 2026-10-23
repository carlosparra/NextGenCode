"""Patrón ReAct: razonar → actuar (herramienta) → observar → repetir hasta poder responder.

En M3 escribías este bucle a mano (`for` mientras stop_reason == "tool_use").
En M3B el bucle YA EXISTE: Claude Code es un agente ReAct. Aquí no lo programamos, lo OBSERVAMOS:
con `--output-format stream-json` cada vuelta del bucle llega como un evento.

  assistant · text      → razona
  assistant · tool_use  → actúa   (Claude Code ejecuta la herramienta, no nosotros)
  user · tool_result    → observa (la observación vuelve al modelo)
  result                → terminó; trae turnos y costo

Uso:  python -m ejemplos.s1_razonamiento.react
En tu fábrica:  cada subagente de .claude/agents/ corre este mismo bucle.
"""
import json

from ejemplos.comun import EMPLEADOS, RAIZ, eventos, paso, titulo


def react(pregunta: str) -> str:
    # La "herramienta" es leer un archivo: le damos solo Read, nada más (mínima agencia)
    datos = RAIZ / "ejemplos" / "salidas" / "empleados.json"
    datos.parent.mkdir(exist_ok=True)
    datos.write_text(json.dumps(EMPLEADOS, ensure_ascii=False, indent=2), encoding="utf-8")
    prompt = f"{pregunta}\nLos datos están en {datos.relative_to(RAIZ)}; léelos con la herramienta Read."

    respuesta = ""
    for e in eventos(prompt, herramientas="Read"):
        if e["type"] == "assistant":
            for b in e["message"]["content"]:
                if b["type"] == "text" and b["text"].strip():
                    paso("razona", b["text"])
                elif b["type"] == "tool_use":
                    paso("actúa", f"{b['name']}({b['input']})")
        elif e["type"] == "user":
            for b in e["message"]["content"]:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    contenido = b["content"] if isinstance(b["content"], str) else json.dumps(b["content"])
                    paso("observa", contenido, limite=160)
        elif e["type"] == "result":
            paso("fin", f"{e.get('num_turns')} turnos · {e.get('total_cost_usd', 0):.4f} USD (cuota de tu suscripción)")
            respuesta = e.get("result", "")
    return respuesta


if __name__ == "__main__":
    titulo("ReAct (el bucle de Claude Code, visto desde fuera)")
    print(react("¿Cuántos empleados ACTIVOS hay en Tecnología y quién de ellos es el más antiguo?"))
