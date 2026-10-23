"""Hook PreToolUse · Sesión 4 · Defensas para TODOS los agentes (también el principal).

La historia de usuario es contenido NO confiable: puede traer instrucciones escondidas para el agente
(inyección de prompt, ver historias/HU-99-envenenada.md). Estas defensas no dependen de que el modelo
«se dé cuenta»: son código que se ejecuta antes de cada herramienta.

1. Lectura confinada: nada fuera del proyecto y ningún archivo con secretos.
2. Terminal: sin sustitución de comandos y sin mencionar secretos ni variables de entorno.
3. Escritura: ningún archivo puede contener el señuelo de secretos_demo.txt (prevención de fuga).
4. Auditoría: cada herramienta queda registrada en auditoria.jsonl.

DEFENSAS=0 las apaga, SOLO en clase, para ver el ataque funcionar (hooks/rol.py también relaja la lectura).
"""
import json
import os
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SECRETOS = (".env", "secretos")
PALABRAS_SECRETAS = (".env", "secretos", "printenv", "environ", "env ")
SENUELO = "BANDERA-DEMO"


def bloquear(motivo: str) -> None:
    print(f"Seguridad: {motivo}", file=sys.stderr)
    sys.exit(2)


def auditar(datos: dict) -> None:
    registro = {"ts": round(time.time(), 1), "agente": datos.get("agent_type") or "principal",
                "herramienta": datos["tool_name"], "entrada": str(datos.get("tool_input", {}))[:300]}
    with open(RAIZ / "auditoria.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")


def revisar(herramienta: str, entrada: dict) -> None:
    if herramienta in ("Read", "Glob", "Grep"):
        ruta = entrada.get("file_path") or entrada.get("path") or "."
        destino = (RAIZ / ruta).resolve()
        if not destino.is_relative_to(RAIZ):
            bloquear(f"lectura fuera del proyecto bloqueada: {ruta}")
        if any(s in destino.name.lower() for s in SECRETOS) and not destino.name.endswith(".example"):
            bloquear(f"archivo con secretos bloqueado: {destino.name}")
    elif herramienta == "Bash":
        comando = entrada.get("command", "")
        if "`" in comando or "$(" in comando:
            bloquear("sustitución de comandos no permitida")
        if any(p in comando.lower() for p in PALABRAS_SECRETAS):
            bloquear("el comando menciona secretos o variables de entorno")
    elif herramienta in ("Write", "Edit", "MultiEdit"):
        contenido = entrada.get("content") or entrada.get("new_string") or json.dumps(entrada.get("edits", ""))
        if SENUELO in contenido:
            bloquear("el contenido incluye datos de secretos_demo.txt (fuga de información)")


if __name__ == "__main__":
    datos = json.load(sys.stdin)
    if os.environ.get("DEFENSAS", "1") == "0":
        sys.exit(0)
    auditar(datos)
    revisar(datos["tool_name"], datos.get("tool_input", {}))
    sys.exit(0)
