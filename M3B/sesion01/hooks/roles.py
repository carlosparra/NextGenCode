"""La tabla de permisos de cada subagente: mínima agencia escrita como código.

En M3 cada agente recibía herramientas con permisos (`herramientas_archivos(lectura, escritura)`).
En M3B el agente es un subagente de Claude Code, y estos permisos los aplica el hook
`hooks/rol.py` ANTES de cada herramienta: si la ruta o el programa no están aquí, se bloquea.

- lee:       patrones de rutas (relativas a la raíz) que el agente puede leer o buscar
- escribe:   patrones de rutas que el agente puede crear o editar
- programas: primer palabra permitida en cada tramo de un comando Bash
- entrega:   el archivo que el agente DEBE dejar válido para poder terminar (hooks/compuerta.py)
"""
from dataclasses import dataclass, field


@dataclass
class Rol:
    lee: list[str]
    escribe: list[str]
    programas: set[str] = field(default_factory=set)
    entrega: str | None = None


ROLES = {
    # Sesión 1 · agentes 1 y 2: solo tocan texto, nunca la terminal
    "analista": Rol(lee=["historias/*", "contexto/*", "salida/*"],
                    escribe=["salida/*/criterios.feature"],
                    entrega="criterios.feature"),
    "disenador-pruebas": Rol(lee=["contexto/*", "salida/*"],
                             escribe=["salida/*/casos_prueba.json"],
                             entrega="casos_prueba.json"),
}
