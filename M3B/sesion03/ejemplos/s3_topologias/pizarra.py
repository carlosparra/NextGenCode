"""Topología: Pizarra (blackboard). Los agentes no se hablan: leen y escriben en un estado compartido.

Lo que distingue a la topología en el código:
  - cada agente declara QUÉ necesita leer y QUÉ campo escribe (tabla AGENTES),
  - un controlador en código mira la pizarra y activa al primer agente que ya puede trabajar,
  - nadie llama a nadie: agregar un agente nuevo es agregar una línea a la tabla.

Uso:  python -m ejemplos.s3_topologias.pizarra
En tu fábrica:  la carpeta salida/HU-xx/ es una pizarra en disco: cada subagente lee lo que dejó el anterior.
"""
from ejemplos.comun import claude, historia, paso, titulo

#           agente:     (lee,                       escribe,     tarea)
AGENTES = {
    "pantalla": (["criterios", "endpoint"], "pantalla", "Describe el formulario React en 6 líneas."),
    "disenador": (["criterios"], "casos", "Escribe un caso de prueba por criterio."),
    "analista": (["historia"], "criterios", "Escribe 3 criterios Gherkin breves."),
    "backend": (["criterios"], "endpoint", "Propón el endpoint FastAPI en 6 líneas."),
}


def listo_para(pizarra: dict) -> list[str]:
    """Agentes cuyos insumos ya están en la pizarra y cuyo campo sigue vacío."""
    return [a for a, (lee, escribe, _) in AGENTES.items()
            if all(pizarra.get(c) for c in lee) and not pizarra.get(escribe)]


if __name__ == "__main__":
    titulo("Pizarra")
    pizarra = {"historia": historia("HU-01")}
    while candidatos := listo_para(pizarra):                       # ← el controlador mira la pizarra
        paso("pizarra", f"tiene {list(pizarra)} · pueden trabajar: {candidatos}")
        nombre = candidatos[0]
        lee, escribe, tarea = AGENTES[nombre]
        insumos = "\n\n".join(f"## {c}\n{pizarra[c]}" for c in lee)
        pizarra[escribe] = claude(f"{tarea}\n\n{insumos}")         # ← cada agente escribe SOLO su campo
        paso(f"{nombre} escribe '{escribe}'", pizarra[escribe], 140)
    paso("pizarra", f"completa: {list(pizarra)}")
