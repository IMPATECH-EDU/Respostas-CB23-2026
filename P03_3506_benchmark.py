import random
import time

from AP_03_ordenacao import (
    selection_sort,
    divide_and_conquer_sort,
    quick_sort
)


def gerar_caso_medio(n):
    return [random.randint(0, 100000) for _ in range(n)]


def gerar_pior_caso(n):
    return list(range(n, 0, -1))


def benchmark(algoritmo, gerador, n, repeticoes):
    tempo_total = 0

    for _ in range(repeticoes):
        lista = gerador(n)

        inicio = time.perf_counter()
        algoritmo(lista)
        fim = time.perf_counter()

        tempo_total += fim - inicio

    return tempo_total / repeticoes


def main():
    algoritmos = [
        ("Selection Sort", selection_sort),
        ("Merge Sort", divide_and_conquer_sort),
        ("Quick Sort", quick_sort)
    ]

    tamanhos = [100, 300, 500, 800]
    repeticoes = 50

    print(f"{'Algoritmo':<16} {'N':<8} {'Cenário':<12} {'Tempo médio (s)':<15}")
    print("-" * 55)

    for nome, algoritmo in algoritmos:
        for n in tamanhos:

            tempo_medio = benchmark(
                algoritmo,
                gerar_caso_medio,
                n,
                repeticoes
            )

            print(
                f"{nome:<16} "
                f"{n:<8} "
                f"{'Médio':<12} "
                f"{tempo_medio:<15.6f}"
            )

            tempo_pior = benchmark(
                algoritmo,
                gerar_pior_caso,
                n,
                repeticoes
            )

            print(
                f"{nome:<16} "
                f"{n:<8} "
                f"{'Pior':<12} "
                f"{tempo_pior:<15.6f}"
            )


if __name__ == "__main__":
    main()
