"""Patrón Reflexión: generar → revisar contra criterios → corregir, con un límite de intentos.

Lo que distingue al patrón en el código: un `for intento` donde la crítica del revisor se AGREGA
al siguiente prompt. Aquí el revisor es código (reglas verificables), igual que en la fábrica.

Uso:  python -m ejemplos.s1_razonamiento.reflexion
En tu fábrica:  hooks/compuerta.py hace lo mismo SIN que escribas el for: cuando el subagente
quiere terminar, el validador revisa su entrega y, si falla, le devuelve la crítica (decision: block).
"""
import re

from ejemplos.comun import claude, historia, paso, titulo

MAX_INTENTOS = 3


def revisar(gherkin: str) -> list[str]:
    """El revisor: reglas que se comprueban sin modelo. Devuelve la lista de problemas."""
    problemas = []
    escenarios = re.split(r"\n\s*Escenario:", gherkin)[1:]
    if len(escenarios) < 3:
        problemas.append(f"Hay {len(escenarios)} escenarios; se necesitan al menos 3 (éxito y dos errores).")
    for i, esc in enumerate(escenarios, 1):
        for palabra in ("Dado", "Cuando", "Entonces"):
            if not re.search(rf"^\s*{palabra}\b", esc, re.M):
                problemas.append(f"El escenario {i} no tiene '{palabra}'.")
    if "Usa el correo corporativo @empresa.com" not in gherkin:
        problemas.append("Falta el escenario del correo no corporativo con el mensaje exacto "
                         "«Usa el correo corporativo @empresa.com».")
    return problemas


def generar_con_reflexion(hu: str) -> str:
    tarea = (f"Escribe criterios de aceptación en Gherkin (# language: es) para esta historia. "
             f"Responde solo con el Gherkin, sin explicaciones:\n{hu}")
    for intento in range(1, MAX_INTENTOS + 1):
        gherkin = claude(tarea)                                   # GENERAR
        problemas = revisar(gherkin)                              # REVISAR (código, no modelo)
        paso(f"intento {intento}", f"{len(problemas)} problema(s): {problemas}" if problemas else "sin problemas")
        if not problemas:
            return gherkin
        tarea += ("\n\nTu versión anterior tiene estos problemas; corrígelos y devuelve el Gherkin completo:\n- "
                  + "\n- ".join(problemas))                       # CORREGIR: la crítica vuelve como contexto
    raise RuntimeError(f"Tras {MAX_INTENTOS} intentos sigue habiendo problemas: {problemas}")


if __name__ == "__main__":
    titulo("Reflexión")
    print(generar_con_reflexion(historia("HU-01")))
