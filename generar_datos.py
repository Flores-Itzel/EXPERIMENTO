# generar_datos.py
# Crea los 15 archivos de texto del experimento (A1..A5, B1..B5, C1..C5).
# Cada línea es una cadena alfanumérica aleatoria de 10 caracteres.
#   python generar_datos.py           -> archivos reales en la carpeta "datos"
#   python generar_datos.py prueba    -> archivos pequeños en "datos_prueba" (para probar)
import os
import random
import string
import sys
import time

PRUEBA = "prueba" in sys.argv
CARPETA = "datos_prueba" if PRUEBA else "datos"
TAMANOS = {"A": 1_000_000, "B": 5_000_000, "C": 10_000_000}
if PRUEBA:
    TAMANOS = {k: v // 1000 for k, v in TAMANOS.items()}   # 1,000 / 5,000 / 10,000
CARACTERES = string.ascii_letters + string.digits
LARGO = 10
BLOQUE = 100_000

os.makedirs(CARPETA, exist_ok=True)
inicio = time.time()
for letra, n in TAMANOS.items():
    for num in range(1, 6):
        nombre = f"{letra}{num}"
        ruta = os.path.join(CARPETA, nombre + ".txt")
        if os.path.exists(ruta):
            print(f"{nombre}.txt ya existe, se omite")
            continue
        random.seed(nombre)          # misma semilla = mismos datos si se vuelve a generar
        with open(ruta, "w") as f:
            for desde in range(0, n, BLOQUE):
                m = min(BLOQUE, n - desde)
                texto = "".join(random.choices(CARACTERES, k=LARGO * m))
                f.write("\n".join(texto[j:j + LARGO] for j in range(0, LARGO * m, LARGO)))
                f.write("\n")
        print(f"{nombre}.txt creado con {n:,} cadenas")
print(f"Listo en {time.time() - inicio:.1f} s")
