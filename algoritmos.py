
def particionar(arr, izquierda, derecha):
    """Toma como pivote el primer elemento y devuelve la posición final del pivote."""
    pivote = arr[izquierda]
    i = izquierda + 1
    j = derecha
    while True:
        while i <= j and arr[i] <= pivote:
            i += 1
        while j >= i and arr[j] > pivote:
            j -= 1
        if i >= j:
            break
        # Intercambio de arr[i] y arr[j]
        arr[i], arr[j] = arr[j], arr[i]
    # Intercambio de arr[izquierda] y arr[j] (posicionar el pivote)
    arr[izquierda], arr[j] = arr[j], arr[izquierda]
    return j


def quick_sort(arr, izquierda, derecha):
    """Ordena arr[izquierda..derecha] de forma recursiva."""
    if izquierda < derecha:
        pivote = particionar(arr, izquierda, derecha)
        quick_sort(arr, izquierda, pivote - 1)
        quick_sort(arr, pivote + 1, derecha)


def merge_sort(arr):
    """Divide el arreglo a la mitad, ordena cada mitad recursivamente y las combina."""
    if len(arr) > 1:
        # Encontrar el punto medio del arreglo
        mid = len(arr) // 2
        # Dividir el arreglo en dos mitades
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Llamar recursivamente a merge_sort para ambas mitades
        merge_sort(left_half)
        merge_sort(right_half)

        # Inicializar índices para las dos mitades
        i = j = k = 0

        # Combinar las dos mitades en un arreglo ordenado
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Verificar si quedan elementos en el lado izquierdo
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        # Verificar si quedan elementos en el lado derecho
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def mezclar(arr, izq, medio, der):
    """Mezcla dos sublistas ordenadas: arr[izq..medio] y arr[medio+1..der]."""
    numElementosIzq = medio - izq + 1
    numElementosDer = der - medio

    arregloIzq = arr[izq:izq + numElementosIzq]
    arregloDer = arr[medio + 1:medio + 1 + numElementosDer]

    i = 0
    j = 0
    k = izq

    while i < numElementosIzq and j < numElementosDer:
        if arregloIzq[i] <= arregloDer[j]:
            arr[k] = arregloIzq[i]
            i += 1
        else:
            arr[k] = arregloDer[j]
            j += 1
        k += 1

    while i < numElementosIzq:
        arr[k] = arregloIzq[i]
        i += 1
        k += 1

    while j < numElementosDer:
        arr[k] = arregloDer[j]
        j += 1
        k += 1


def mezcla_natural(arr):
    """Busca las corridas (tramos ya ordenados) y las mezcla de dos en dos
    hasta que solo quede una corrida, es decir, todo el arreglo ordenado."""
    n = len(arr)
    if n < 2:
        return
    while True:
        # 1) Identificar las corridas naturales como pares (inicio, fin)
        corridas = []
        inicio = 0
        for i in range(1, n):
            if arr[i] < arr[i - 1]:
                corridas.append((inicio, i - 1))
                inicio = i
        corridas.append((inicio, n - 1))

        # 2) Si solo hay una corrida, el arreglo ya está ordenado
        if len(corridas) == 1:
            break

        # 3) Mezclar las corridas de dos en dos (si sobra una, se queda igual)
        for c in range(0, len(corridas) - 1, 2):
            izq = corridas[c][0]
            medio = corridas[c][1]
            der = corridas[c + 1][1]
            mezclar(arr, izq, medio, der)
