# python 3

import random
import time

def selection_sort(nums):
    """Ordena a lista usando Selection Sort."""

    def argmin(NX):
        min_index = 0
        min_x = NX[0]

        for count, x in enumerate(NX):
            if x < min_x:
                min_index = count
                min_x = x

        return min_index, min_x

    for i in range(len(nums) - 1):
        idx, _ = argmin(nums[i:])
        nums[i], nums[idx + i] = nums[idx + i], nums[i]

    return nums

def divide_and_conquer_sort(nums):
    """Ordena a lista usando Merge Sort."""

    if len(nums) <= 1:
        return nums.copy()

    meio = len(nums) // 2

    n1 = divide_and_conquer_sort(nums[:meio])
    n2 = divide_and_conquer_sort(nums[meio:])

    ordenado = []
    i = 0
    j = 0

    while i < len(n1) and j < len(n2):
        if n1[i] <= n2[j]:
            ordenado.append(n1[i])
            i += 1
        else:
            ordenado.append(n2[j])
            j += 1

    ordenado.extend(n1[i:])
    ordenado.extend(n2[j:])

    return ordenado

def quick_sort(nums, b=0, u=None):
    """Ordena a lista usando Quick Sort."""

    if u is None:
        u = len(nums) - 1

    if b >= u:
        return nums

    pb = b
    pivot = nums[u]

    for i in range(b, u):
        if nums[i] < pivot:
            nums[pb], nums[i] = nums[i], nums[pb]
            pb += 1

    nums[pb], nums[u] = nums[u], nums[pb]

    quick_sort(nums, b, pb - 1)
    quick_sort(nums, pb + 1, u)

    return nums

def gerar_caso_medio(n):
    """Gera uma lista aleatória."""

    return [random.randint(-100000, 100000) for _ in range(n)]


def gerar_pior_caso_selection(n):
    """
    Para Selection Sort, listas aleatórias, ordenadas ou
    invertidas continuam tendo comportamento O(n²).
    """

    return list(range(n, 0, -1))

def gerar_pior_caso_merge(n):
    """
    Merge Sort possui O(n log n) mesmo no pior caso.
    Uma lista invertida é usada como cenário desfavorável.
    """

    return list(range(n, 0, -1))


def gerar_pior_caso_quick(n):
    """
    Como o Quick Sort utiliza o último elemento como pivô,
    uma lista já ordenada produz partições extremamente
    desequilibradas e leva ao pior caso O(n²).
    """

    return list(range(n))

def medir_tempo(algoritmo, dados):
    inicio = time.perf_counter()

    resultado = algoritmo(dados)

    fim = time.perf_counter()

    # Verifica se realmente foi ordenado
    if resultado != sorted(dados):
        raise ValueError("O algoritmo não ordenou corretamente os dados.")

    return fim - inicio


def executar_experimento(n, repeticoes=5):

    print("=" * 70)
    print(f"TAMANHO DA LISTA: {n}")
    print("=" * 70)

    algoritmos = {
        "Selection Sort": selection_sort,
        "Merge Sort": divide_and_conquer_sort,
        "Quick Sort": quick_sort
    }

    print("\nCASO MÉDIO")
    print("-" * 70)

    dados_medio = gerar_caso_medio(n)

    for nome, algoritmo in algoritmos.items():

        tempos = []

        for _ in range(repeticoes):
            dados = dados_medio.copy()

            tempo = medir_tempo(algoritmo, dados)
            tempos.append(tempo)

        media = sum(tempos) / len(tempos)

        print(f"{nome:<20} | Tempo médio: {media:.8f} segundos")

    print("\nPIOR CASO")
    print("-" * 70)

    casos_piores = {
        "Selection Sort": gerar_pior_caso_selection(n),
        "Merge Sort": gerar_pior_caso_merge(n),
        "Quick Sort": gerar_pior_caso_quick(n)
    }

    for nome, algoritmo in algoritmos.items():

        tempos = []

        for _ in range(repeticoes):
            dados = casos_piores[nome].copy()

            tempo = medir_tempo(algoritmo, dados)
            tempos.append(tempo)

        media = sum(tempos) / len(tempos)

        print(f"{nome:<20} | Tempo médio: {media:.8f} segundos")

if __name__ == "__main__":

    print("=" * 70)
    print("COMPARAÇÃO DE ALGORITMOS DE ORDENAÇÃO")
    print("=" * 70)

    # Teste de funcionamento
    X = [
        5, 6, 2, 4, 6, 1, 2, 9,
        -1, -2, -3, 10, 3, 4, 5,
        0, 28, -10
    ]

    print("\nTESTE DE FUNCIONAMENTO")
    print("-" * 70)

    print("Original:")
    print(X)

    print("\nSelection Sort:")
    print(selection_sort(X.copy()))

    print("\nMerge Sort:")
    print(divide_and_conquer_sort(X.copy()))

    print("\nQuick Sort:")
    print(quick_sort(X.copy()))

    tamanhos = [100, 500, 1000, 5000]

    