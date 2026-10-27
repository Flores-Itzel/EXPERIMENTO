# experimento.py
# Ejecuta MD, MN y QS en cada conjunto de datos y guarda los tiempos en resultados.csv
#   python experimento.py            -> corre los 15 conjuntos (A1..C5)
#   python experimento.py A          -> solo los conjuntos A1..A5
#   python experimento.py B3 C1      -> solo B3 y C1
#   python experimento.py prueba     -> usa la carpeta "datos_prueba" (para probar)
import csv
import gc
import os
import sys
import time

from algoritmos import merge_sort_directa, mezcla_natural, quicksort

PRUEBA = "prueba" in sys.argv
CARPETA = "datos_prueba" if PRUEBA else "datos"
ARCHIVO = "resultados_prueba.csv" if PRUEBA else "resultados.csv"
ALGORITMOS = [("MD", merge_sort_directa), ("MN", mezcla_natural), ("QS", quicksort)]
TAMANO = {"A": "1 millón", "B": "5 millones", "C": "10 millones"}

pedidos = [a.upper() for a in sys.argv[1:] if a != "prueba"]
conjuntos = [f"{l}{n}" for l in "ABC" for n in range(1, 6)]
if pedidos:
    conjuntos = [c for c in conjuntos if c in pedidos or c[0] in pedidos]


def leer(ruta):
    with open(ruta) as f:
        return f.read().split()


def esta_ordenada(lista):
    for i in range(1, len(lista)):
        if lista[i] < lista[i - 1]:
            return False
    return True


if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["tamano", "conjunto", "algoritmo", "ms"])

inicio_total = time.time()
for conj in conjuntos:
    ruta = os.path.join(CARPETA, conj + ".txt")
    if not os.path.exists(ruta):
        print(f"No existe {ruta}. Primero corre generar_datos.py")
        continue
    datos = leer(ruta)
    print("=" * 60)
    print(f"Conjunto {conj}: {len(datos):,} cadenas")
    for nombre, funcion in ALGORITMOS:
        copia = datos.copy()               # cada algoritmo ordena los mismos datos
        gc.collect()
        gc.disable()
        try:
            t0 = time.perf_counter()
            funcion(copia)
            ms = (time.perf_counter() - t0) * 1000
            ok = esta_ordenada(copia)
            print(f"{nombre}({conj}): {ms:,.2f} ms   ordenado correctamente: {'Sí' if ok else 'NO'}")
            valor = f"{ms:.2f}"
        except (MemoryError, RecursionError) as e:
            print(f"{nombre}({conj}): ERROR {type(e).__name__}")
            valor = "ERROR"
        finally:
            gc.enable()
            del copia
        with open(ARCHIVO, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([TAMANO[conj[0]], conj, nombre, valor])
print("=" * 60)
print(f"Terminado en {(time.time() - inicio_total) / 60:.1f} minutos. Tiempos guardados en {ARCHIVO}")
