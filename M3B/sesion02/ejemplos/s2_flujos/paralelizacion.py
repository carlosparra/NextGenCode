"""Patrón de flujo: Paralelización. Ramas independientes corren a la vez y se unen al final.

Lo que distingue al patrón en el código:
  1. abanico: dos tareas que se lanzan al mismo tiempo (`submit`),
  2. unión: esperar a ambas (`result()`) antes de seguir.
Mide el tiempo: debería tardar casi lo mismo que la rama más lenta, no la suma de las dos.

Uso:  python -m ejemplos.s2_flujos.paralelizacion
En tu fábrica:  sesión 3 → /fabrica lanza los subagentes despliegue y automatizador en el mismo turno
"""
import time
from concurrent.futures import ThreadPoolExecutor

from ejemplos.comun import claude, historia, paso, titulo


def rama(nombre: str, pedido: str, hu: str) -> str:
    inicio = time.perf_counter()
    texto = claude(f"{pedido}\n{hu}")
    paso(f"rama {nombre} · {time.perf_counter() - inicio:.1f} s", texto)
    return f"{nombre}:\n{texto}"


if __name__ == "__main__":
    titulo("Paralelización")
    hu, inicio = historia("HU-01"), time.perf_counter()
    with ThreadPoolExecutor() as pool:                                         # ← abanico
        api = pool.submit(rama, "API", "Escribe 3 casos de prueba de la API (método, ruta, código esperado) para:", hu)
        ui = pool.submit(rama, "UI", "Escribe 3 casos de prueba de la pantalla (qué hace la persona, qué ve) para:", hu)
        casos = [api.result(), ui.result()]                                    # ← unión: espera a las dos
    paso("unir", f"llegaron {len(casos)} bloques de casos")
    print(f"\nTiempo total: {time.perf_counter() - inicio:.1f} s")
