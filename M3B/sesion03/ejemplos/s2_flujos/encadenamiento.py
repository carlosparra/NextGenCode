"""Patrón de flujo: Encadenamiento. Pasos fijos; la salida de uno es la entrada del siguiente.

Lo que distingue al patrón en el código: llamadas en línea recta, más una compuerta (un `if`)
que impide avanzar si la validación falla. El orden lo decide el código, nunca el modelo.
(En M3 era un grafo de LangGraph con `add_edge`; aquí son tres líneas de Python: el patrón es el mismo.)

Uso:  python -m ejemplos.s2_flujos.encadenamiento
En tu fábrica:  .claude/skills/fabrica/SKILL.md → analista → validar → diseñador → arquitecto → desarrollador
"""
from ejemplos.comun import claude, historia, paso, titulo


def escribir_criterios(hu: str) -> str:
    texto = claude("Escribe 3 escenarios Gherkin (# language: es), breves, para esta historia. "
                   "Responde solo con el Gherkin:\n" + hu)
    paso("1 · criterios", texto)
    return texto


def compuerta(criterios: str) -> bool:
    """Validación determinista entre pasos: si falla, la cadena no avanza."""
    faltan = [p for p in ("Escenario", "Dado", "Cuando", "Entonces") if p not in criterios]
    paso("compuerta", f"✗ faltan {faltan}: se detiene" if faltan else "✓ criterios válidos")
    return not faltan


def escribir_casos(criterios: str) -> str:
    texto = claude("Convierte cada escenario en un caso de prueba (id, pasos, resultado esperado):\n" + criterios)
    paso("2 · casos", texto)
    return texto


if __name__ == "__main__":
    titulo("Encadenamiento")
    criterios = escribir_criterios(historia("HU-01"))     # paso 1
    if compuerta(criterios):                              # compuerta
        escribir_casos(criterios)                         # paso 2
