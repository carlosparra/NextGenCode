"""Patrón de flujo: Evaluador-optimizador. Un generador produce y un juez independiente decide.

Lo que distingue al patrón en el código: un CICLO (generar → evaluar → generar) con un tope, y un
evaluador que no es el mismo agente. Aquí el juez es pytest: pruebas escritas a partir de las reglas de
negocio. El código generado nunca se ejecuta con exec(): solo pytest, en un subproceso con tiempo límite.

Uso:  python -m ejemplos.s2_flujos.evaluador
En tu fábrica:  hooks/compuerta.py con el desarrollador: no termina hasta que `verificacion app` pasa
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from ejemplos.comun import claude, paso, titulo

MAX_INTENTOS = 3

PRUEBAS = '''
import pytest
from correo import validar_correo

def test_acepta_y_normaliza():
    assert validar_correo("  Ana.Lopez@Empresa.com ") == "ana.lopez@empresa.com"

def test_rechaza_otro_dominio():
    with pytest.raises(ValueError, match="Usa el correo corporativo @empresa.com"):
        validar_correo("ana@gmail.com")

def test_rechaza_dominio_parecido():
    with pytest.raises(ValueError):
        validar_correo("ana@empresa.com.mx")
'''


def generar(error: str) -> str:
    prompt = ("Escribe en Python la función validar_correo(correo: str) -> str para el correo corporativo "
              "de un empleado. Responde solo con un bloque ```python```.")
    if error:                                                  # la crítica del juez vuelve como contexto
        prompt += f"\n\nTu versión anterior falló estas pruebas; corrígela:\n{error[-2500:]}"
    texto = claude(prompt)
    codigo = re.search(r"```python\n(.*?)```", texto, re.S)
    return codigo.group(1) if codigo else texto


def evaluar(codigo: str) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as carpeta:
        Path(carpeta, "correo.py").write_text(codigo, encoding="utf-8")
        Path(carpeta, "test_correo.py").write_text(PRUEBAS, encoding="utf-8")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", carpeta],
                           capture_output=True, text=True, timeout=60)
    resumen = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]
    paso("evaluador · pytest", ("✓ " if r.returncode == 0 else "✗ ") + resumen)
    return r.returncode == 0, r.stdout


if __name__ == "__main__":
    titulo("Evaluador-optimizador")
    error, aprobado, codigo = "", False, ""
    for intento in range(1, MAX_INTENTOS + 1):                 # ← el ciclo, con su tope
        codigo = generar(error)
        paso(f"generador · intento {intento}/{MAX_INTENTOS}", "escribió una nueva versión")
        aprobado, error = evaluar(codigo)
        if aprobado:
            break
    print("\nAprobado" if aprobado else "\nSin aprobar: lo decide una persona")
    print(codigo)
