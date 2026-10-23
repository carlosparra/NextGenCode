"""Salidas estructuradas y validación con código: el modelo propone, el código decide.

Tres piezas que se repiten en toda la fábrica:
  1. Un CONTRATO: un modelo Pydantic con tipos, campos obligatorios y valores permitidos (Literal).
  2. Obtenerlo del modelo con `claude -p --json-schema` (en M3: una herramienta forzada con tool_choice).
  3. Validar en dos niveles con código: el esquema (Pydantic) y las reglas de negocio (una función).
     Si falla, el error regresa al modelo; si después de N intentos sigue fallando, decide una persona.

Uso:  python -m ejemplos.s1_razonamiento.salidas_estructuradas
En tu fábrica:  validadores/contratos.py → PlanPruebas, que hooks/compuerta.py aplica al diseñador.
"""
from datetime import date
from typing import Literal

from pydantic import BaseModel, ValidationError

from ejemplos.comun import claude, paso, titulo

MAX_INTENTOS = 2


class AltaEmpleado(BaseModel):     # 1 · EL CONTRATO
    nombre: str
    correo: str
    puesto: str
    departamento: Literal["Tecnología", "Ventas", "Finanzas", "Recursos Humanos", "Operaciones"]
    fecha_ingreso: date
    dudas: list[str]               # un lugar legítimo para decir «no lo sé» en vez de inventar


def reglas_de_negocio(a: AltaEmpleado) -> list[str]:  # 3b · REGLAS que el esquema no expresa
    problemas = []
    if not a.correo.lower().endswith("@empresa.com"):
        problemas.append("Usa el correo corporativo @empresa.com")
    if a.fecha_ingreso > date.today():
        problemas.append("La fecha de ingreso no puede ser futura")
    if a.dudas:
        problemas.append(f"El modelo tiene dudas: {a.dudas}")
    return problemas


def extraer(correo_rh: str) -> AltaEmpleado | list[str]:
    tarea = (f"Hoy es {date.today()}. Extrae los datos del alta. No inventes: si un dato falta o es "
             f"ambiguo, anótalo en 'dudas'.\n\nCorreo de Recursos Humanos:\n{correo_rh}")
    problemas: list[str] = []
    for intento in range(1, MAX_INTENTOS + 1):
        datos = claude(tarea, esquema=AltaEmpleado)                      # 2 · FORZAR LA FORMA
        try:
            alta = AltaEmpleado.model_validate(datos)                    # 3a · ESQUEMA (otra vez, en nuestro lado)
            problemas = reglas_de_negocio(alta)                          # 3b · REGLAS
        except ValidationError as e:
            problemas = [f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in e.errors()]
        paso(f"intento {intento}", "válido" if not problemas else f"problemas: {problemas}")
        if not problemas:
            return alta                                                  # quien decide que terminó es el if
        tarea += "\n\nTu respuesta anterior tiene estos problemas; corrígelos SOLO si el correo lo permite:\n- " \
                 + "\n- ".join(problemas)
    return problemas          # no se pudo: esto lo decide una persona, no el modelo


if __name__ == "__main__":
    correos = [
        "Hola, por favor da de alta a Ana López (ana.lopez@empresa.com), Analista de datos en el área "
        "de Tecnología. Entró el 06 de octubre de 2026.",
        "Porfa registra a Luis, su correo es luis.perez@gmail.com, va a ventas o finanzas, aún no sé, "
        "y empieza la próxima semana.",
    ]
    for texto in correos:
        titulo("Salidas estructuradas")
        print(texto)
        resultado = extraer(texto)
        if isinstance(resultado, AltaEmpleado):
            print("\n✓ Alta lista para la API:", resultado.model_dump_json(indent=2))
        else:
            print("\n✗ No se registra. Se envía a una persona de RH con estos problemas:", *resultado, sep="\n  - ")
