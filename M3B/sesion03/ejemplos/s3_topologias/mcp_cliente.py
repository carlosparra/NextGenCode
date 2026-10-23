"""MCP · cliente: Claude Code DESCUBRE las herramientas de un servidor y las usa en su bucle ReAct.

Lo que distingue a MCP en el código: aquí no hay ningún esquema de herramienta escrito a mano.
Le pasamos a Claude Code el archivo .mcp.json; al arrancar, se conecta al servidor, pide la lista de
herramientas (list_tools) y las ofrece al modelo como `mcp__directorio__<herramienta>`.
Compáralo con react.py: es el mismo bucle, pero la herramienta vive en otro proceso.

Uso:  python -m ejemplos.s3_topologias.mcp_cliente
En tu fábrica:  .mcp.json en la raíz: cualquier subagente con `mcp__directorio__*` en tools puede usarlo.
"""
import json

from ejemplos.comun import eventos, paso, titulo

HERRAMIENTAS = "mcp__directorio__buscar_empleados,mcp__directorio__consultar_empleado"


def preguntar(pregunta: str) -> str:
    respuesta = ""
    for e in eventos(pregunta, herramientas="",                       # sin herramientas integradas: solo MCP
                     extra=["--mcp-config", ".mcp.json", "--strict-mcp-config", "--allowedTools", HERRAMIENTAS]):
        if e["type"] == "system" and e.get("subtype") == "init":
            servidores = [f"{s['name']} ({s['status']})" for s in e.get("mcp_servers", [])]
            paso("descubre", f"servidores: {servidores} · herramientas: "
                             f"{[t for t in e.get('tools', []) if t.startswith('mcp__')]}")
        elif e["type"] == "assistant":
            for b in e["message"]["content"]:
                if b["type"] == "text" and b["text"].strip():
                    paso("razona", b["text"])
                elif b["type"] == "tool_use":
                    paso("actúa (vía MCP)", f"{b['name']}({b['input']})")
        elif e["type"] == "user":
            for b in e["message"]["content"]:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    contenido = b["content"] if isinstance(b["content"], str) else json.dumps(b["content"])
                    paso("observa", contenido, 160)
        elif e["type"] == "result":
            respuesta = e.get("result", "")
    return respuesta


if __name__ == "__main__":
    titulo("MCP · Claude Code como cliente")
    print(preguntar("¿Quién es el empleado activo más antiguo de Tecnología? Y ¿existe el EMP-0099?"))
