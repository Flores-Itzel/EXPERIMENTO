# analisis.py
# Lee resultados.csv y calcula, para cada uno de los 9 renglones (3 tamaños x 3 algoritmos):
# promedio, varianza y desviación estándar (fórmula del profesor, dividiendo entre N).
# Genera: tabla_resultados.csv, calculo_desviacion.txt (evidencia paso a paso) y grafica.png
#   python analisis.py          -> con resultados.csv
#   python analisis.py prueba   -> con resultados_prueba.csv
import csv
import math
import sys

PRUEBA = "prueba" in sys.argv
ARCHIVO = "resultados_prueba.csv" if PRUEBA else "resultados.csv"
TAMANOS = ["1 millón", "5 millones", "10 millones"]
ALGORITMOS = ["MD", "MN", "QS"]
NOMBRES = {"MD": "MergeSort-Directa", "MN": "MergeSort-Mezcla natural", "QS": "QuickSort"}

# 1) leer tiempos (si un conjunto se corrió dos veces, se usa la última corrida)
tiempos = {}
with open(ARCHIVO, newline="", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        if fila["ms"] != "ERROR":
            tiempos[(fila["tamano"], fila["algoritmo"], fila["conjunto"])] = float(fila["ms"])

# 2) cálculos
filas = []
evidencia = ["EVIDENCIA DEL CÁLCULO DE LA DESVIACIÓN ESTÁNDAR",
             "Fórmula: σ = raíz( Σ (xi − X̄)² / N )   (X̄ = media, N = número de observaciones)", ""]
for tam in TAMANOS:
    for alg in ALGORITMOS:
        xs = [tiempos[k] for k in sorted(tiempos) if k[0] == tam and k[1] == alg]
        if not xs:
            continue
        n = len(xs)
        media = sum(xs) / n
        desv = [x - media for x in xs]
        cuad = [d * d for d in desv]
        varianza = sum(cuad) / n
        sigma = math.sqrt(varianza)
        filas.append([tam, alg] + xs + [""] * (5 - n) + [media, varianza, sigma])
        evidencia += [
            f"{tam} - {alg} ({NOMBRES[alg]})  N = {n}",
            "  tiempos xi (ms):   " + ", ".join(f"{x:,.2f}" for x in xs),
            f"  media X̄ = {sum(xs):,.2f} / {n} = {media:,.2f} ms",
            "  (xi − X̄):          " + ", ".join(f"{d:,.2f}" for d in desv),
            "  (xi − X̄)²:         " + ", ".join(f"{c:,.2f}" for c in cuad),
            f"  Σ (xi − X̄)² = {sum(cuad):,.2f}",
            f"  varianza σ² = {sum(cuad):,.2f} / {n} = {varianza:,.2f} ms²",
            f"  desviación σ = raíz({varianza:,.2f}) = {sigma:,.2f} ms",
            "",
        ]

# 3) tabla en pantalla y en CSV
encabezado = ["Tamaño", "Alg.", "Ej.1", "Ej.2", "Ej.3", "Ej.4", "Ej.5", "Promedio", "Varianza", "Desv. est."]
print(" | ".join(f"{h:>11}" for h in encabezado))
for fila in filas:
    celdas = [f"{fila[0]:>11}", f"{fila[1]:>11}"]
    celdas += [f"{v:>11,.2f}" if v != "" else f"{'':>11}" for v in fila[2:]]
    print(" | ".join(celdas))
with open("tabla_resultados.csv" if not PRUEBA else "tabla_resultados_prueba.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Tamaño del conjunto", "Algoritmo", "Ejecución 1 (ms)", "Ejecución 2 (ms)", "Ejecución 3 (ms)",
                "Ejecución 4 (ms)", "Ejecución 5 (ms)", "Promedio (ms)", "Varianza (ms²)", "Desviación estándar (ms)"])
    for fila in filas:
        w.writerow([fila[0], fila[1]] + [f"{v:.2f}" if v != "" else "" for v in fila[2:]])
with open("calculo_desviacion.txt" if not PRUEBA else "calculo_desviacion_prueba.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(evidencia))
print("\nGuardados: tabla_resultados.csv y calculo_desviacion.txt")

# 4) gráfica de líneas multiserie (promedio vs tamaño)
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    print("Para la gráfica instala matplotlib:  pip install matplotlib")
    sys.exit()

x = [1, 5, 10]
estilos = {"MD": ("o", "-"), "MN": ("s", "--"), "QS": ("^", "-.")}
desplazamientos = {"MD": (0, 12), "MN": (30, 6), "QS": (0, -16)}
plt.figure(figsize=(9, 5.5))
for alg in ALGORITMOS:
    prom = [f[-3] for f in filas if f[1] == alg]
    if len(prom) == 3:
        plt.plot(x, prom, marker=estilos[alg][0], linestyle=estilos[alg][1], linewidth=2, label=NOMBRES[alg])
        for xi, yi in zip(x, prom):
            plt.annotate(f"{yi:,.0f}", (xi, yi), textcoords="offset points", xytext=desplazamientos[alg], ha="center", fontsize=8)
plt.title("Tiempo promedio de ordenamiento según el tamaño del conjunto")
plt.xlabel("Tamaño del conjunto de datos (millones de cadenas)")
plt.ylabel("Tiempo promedio (ms)")
plt.xticks(x)
plt.grid(True, alpha=0.3)
plt.legend()
plt.ylim(-8000, 156000)
plt.xlim(0.5, 11.5)
plt.tight_layout()
plt.savefig("grafica.png" if not PRUEBA else "grafica_prueba.png", dpi=150)
print("Gráfica guardada: grafica.png")
