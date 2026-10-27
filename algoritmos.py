# algoritmos.py
# Los tres algoritmos del experimento. Todos ordenan la lista "a" en su lugar
# (de menor a mayor) y no usan recursión profunda, así que aguantan millones de datos.
#   MD = MergeSort-Directa
#   MN = MergeSort-Mezcla natural
#   QS = QuickSort


def mezclar(a, aux, lo, mid, hi):
    """Mezcla las dos mitades ordenadas a[lo:mid] y a[mid:hi]."""
    aux[lo:hi] = a[lo:hi]
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if aux[j] < aux[i]:
            a[k] = aux[j]
            j += 1
        else:
            a[k] = aux[i]
            i += 1
        k += 1
    while i < mid:
        a[k] = aux[i]
        i += 1
        k += 1
    while j < hi:
        a[k] = aux[j]
        j += 1
        k += 1


def merge_sort_directa(a):
    """MD: mezcla directa. Mezcla bloques de tamaño 1, 2, 4, 8, ... hasta ordenar todo."""
    n = len(a)
    aux = a[:]
    ancho = 1
    while ancho < n:
        for lo in range(0, n, 2 * ancho):
            mid = min(lo + ancho, n)
            hi = min(lo + 2 * ancho, n)
            if mid < hi:
                mezclar(a, aux, lo, mid, hi)
        ancho *= 2


def mezcla_natural(a):
    """MN: mezcla natural. Detecta las corridas (tramos ya ordenados) y las va mezclando de dos en dos."""
    n = len(a)
    if n < 2:
        return
    aux = a[:]
    # inicios de cada corrida natural; el último valor es n
    inicios = [0]
    for i in range(1, n):
        if a[i] < a[i - 1]:
            inicios.append(i)
    inicios.append(n)
    while len(inicios) > 2:                      # mientras haya más de una corrida
        corridas = len(inicios) - 1
        nuevos = [0]
        for p in range(0, corridas - 1, 2):
            mezclar(a, aux, inicios[p], inicios[p + 1], inicios[p + 2])
            nuevos.append(inicios[p + 2])
        if corridas % 2 == 1:                    # la última corrida se queda sola
            nuevos.append(n)
        inicios = nuevos


def quicksort(a):
    """QS: QuickSort con pivote de mediana de tres y pila propia (sin recursión)."""
    n = len(a)
    if n < 2:
        return
    pila = [(0, n - 1)]
    while pila:
        lo, hi = pila.pop()
        while lo < hi:
            mid = (lo + hi) // 2
            x, y, z = a[lo], a[mid], a[hi]
            if x < y:
                pivote = y if y < z else (z if x < z else x)
            else:
                pivote = x if x < z else (z if y < z else y)
            i, j = lo, hi
            while i <= j:
                while a[i] < pivote:
                    i += 1
                while a[j] > pivote:
                    j -= 1
                if i <= j:
                    a[i], a[j] = a[j], a[i]
                    i += 1
                    j -= 1
            # se sigue con la parte más chica y la otra se guarda en la pila
            if j - lo < hi - i:
                pila.append((i, hi))
                hi = j
            else:
                pila.append((lo, j))
                lo = i
