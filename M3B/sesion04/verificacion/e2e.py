"""Sesión 4 · Corre TODAS las pruebas (API y E2E) contra la app desplegada y resume los fallos.

Deja dos archivos para el triage: salida/HU-xx/resultados.xml (JUnit) y salida/HU-xx/fallos.md (resumen).
"""
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

from verificacion.comun import APP, SALIDA


def verificar(hu: str | None = None) -> tuple[bool, str]:
    if not hu:
        return False, "Indica la historia: python -m verificacion e2e HU-01"
    carpeta = SALIDA / hu
    carpeta.mkdir(parents=True, exist_ok=True)
    reporte = carpeta / "resultados.xml"
    entorno = {**os.environ, "URL_API": "http://localhost:8000", "URL_WEB": "http://localhost:8080"}
    r = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q", "--tb=short", f"--junitxml={reporte}"],
                       cwd=APP, capture_output=True, text=True, timeout=900, env=entorno)
    fallos = []
    if reporte.exists():
        for caso in ET.parse(reporte).getroot().iter("testcase"):
            for problema in list(caso.findall("failure")) + list(caso.findall("error")):
                fallos.append(f"- {caso.get('classname')}::{caso.get('name')}\n  {(problema.get('message') or '')[:400]}")
    resumen = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "sin salida"
    log = f"{resumen}\n" + "\n".join(fallos)
    (carpeta / "fallos.md").write_text(f"# Pruebas de {hu}\n\n{log}\n", encoding="utf-8")
    return r.returncode == 0, log
