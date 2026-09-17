import random
import time

from AP_03_ordenacao import selection_sort, divide_and_conquer_sort, quick_sort


TAMANHOS = [100, 300, 500, 700]
REPETICOES = 50


def caso_medio(n):
    return [random.randint(0, 10 * n) for _ in range(n)]


def pior_caso(n):
    return list(range(n, 0, -1))


def medir_tempo(algoritmo, dados, repeticoes):
    total = 0.0

    for _ in range(repeticoes):
        copia = dados.copy()
        inicio = time.perf_counter()
        algoritmo(copia)
        fim = time.perf_counter()
        total += fim - inicio

    return total / repeticoes


def main():
    algoritmos = [
        ("Selection Sort", selection_sort),
        ("Merge Sort", divide_and_conquer_sort),
        ("Quick Sort", quick_sort),
    ]

    print(f"{'Algoritmo':<18} {'N':>6} {'Cenario':<12} {'Tempo medio (s)':>18}")
    print("-" * 58)

    for n in TAMANHOS:
        dados_medios = caso_medio(n)
        dados_piores = pior_caso(n)

        for nome, algoritmo in algoritmos:
            tempo = medir_tempo(algoritmo, dados_medios, REPETICOES)
            print(f"{nome:<18} {n:>6} {'medio':<12} {tempo:>18.8f}")

            tempo = medir_tempo(algoritmo, dados_piores, REPETICOES)
            print(f"{nome:<18} {n:>6} {'pior':<12} {tempo:>18.8f}")


if __name__ == "__main__":
    main()
