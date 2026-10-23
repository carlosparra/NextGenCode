"""La tabla de permisos de cada subagente: mínima agencia escrita como código.

En M3 cada agente recibía herramientas con permisos (`herramientas_archivos(lectura, escritura)`).
En M3B el agente es un subagente de Claude Code, y estos permisos los aplica el hook
`hooks/rol.py` ANTES de cada herramienta: si la ruta o el programa no están aquí, se bloquea.

- lee:          patrones de rutas (relativas a la raíz) que el agente puede leer o buscar
- escribe:      patrones de rutas que el agente puede crear o editar
- programas:    primera palabra permitida en cada tramo de un comando Bash
- entrega:      el archivo de salida/HU-xx/ que el agente DEBE dejar válido para terminar (hooks/compuerta.py)
- verifica:     la verificación de verificacion/ que debe pasar para terminar (sesión 2 en adelante)
- max_intentos: cuántas veces la compuerta lo devuelve a corregir antes de escalar a una persona
"""
from dataclasses import dataclass, field


@dataclass
class Rol:
    lee: list[str]
    escribe: list[str]
    programas: set[str] = field(default_factory=set)
    entrega: str | None = None
    verifica: str | None = None
    max_intentos: int = 3


ROLES = {
    # Sesión 1 · agentes 1 y 2: solo tocan texto, nunca la terminal
    "analista": Rol(lee=["historias/*", "contexto/*", "salida/*"],
                    escribe=["salida/*/criterios.feature"],
                    entrega="criterios.feature"),
    "disenador-pruebas": Rol(lee=["contexto/*", "salida/*"],
                             escribe=["salida/*/casos_prueba.json"],
                             entrega="casos_prueba.json"),
    # Sesión 2 · agente 3 en dos fases (Plan-and-Execute): el arquitecto planea sin tocar código,
    # el desarrollador ejecuta el plan aprobado y no termina hasta que la app verifica
    "arquitecto": Rol(lee=["contexto/*", "salida/*", "app/*"],
                      escribe=["salida/*/plan.md"],
                      entrega="plan.md"),
    "desarrollador": Rol(lee=["contexto/*", "salida/*", "app/*"],
                         escribe=["app/backend/*", "app/frontend/*"],
                         programas={"cd", "ls", "cat", "mkdir", "npm", "npx", "node", ".venv/bin/python"},
                         verifica="app", max_intentos=2),
}
