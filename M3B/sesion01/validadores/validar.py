"""Valida un artefacto de salida/ desde la terminal (lo usan los hooks y lo puedes usar tú).

Uso:  python -m validadores.validar salida/HU-01/criterios.feature
      python -m validadores.validar salida/HU-01/casos_prueba.json
Código de salida 0 = válido; 1 = hay problemas (se imprimen).
"""
import sys
from pathlib import Path

from validadores.contratos import validar_gherkin, validar_plan


def problemas_de(ruta: Path) -> list[str] | None:
    """Problemas del archivo, o None si no es un artefacto que sepamos validar."""
    if ruta.name == "criterios.feature":
        return validar_gherkin(ruta.read_text(encoding="utf-8"))
    if ruta.name == "casos_prueba.json":
        criterios = ruta.parent / "criterios.feature"
        if not criterios.exists():
            return [f"Falta {criterios}: primero el analista escribe los criterios."]
        return validar_plan(ruta.read_text(encoding="utf-8"), criterios.read_text(encoding="utf-8"))
    return None


if __name__ == "__main__":
    ruta = Path(sys.argv[1])
    problemas = problemas_de(ruta)
    if problemas is None:
        sys.exit(f"No sé validar {ruta.name}")
    for p in problemas:
        print("-", p)
    print("válido" if not problemas else f"{len(problemas)} problema(s)")
    sys.exit(1 if problemas else 0)
