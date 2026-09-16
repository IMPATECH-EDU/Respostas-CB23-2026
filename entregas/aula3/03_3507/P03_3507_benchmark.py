import sys
sys.setrecursionlimit(10000)

import time
import random
from AP_03_ordenacao import *


N_VALORES = [100, 500, 1000, 5000]
REPETICOES = 50


def caso_medio(n):
    return [random.randint(1, n) for _ in range(n)]


def pior_caso_selection(n):
    return list(range(n, 0, -1))


def pior_caso_merge(n):
    return list(range(n, 0, -1))


def pior_caso_quick(n):
    return list(range(n))


def mede_tempo(algoritmo, lista):
    copia = lista.copy()

    inicio = time.perf_counter()

    algoritmo(copia)

    fim = time.perf_counter()

    return fim - inicio


def teste(algoritmo, lista_media, lista_pior):
    tempo_medio = 0

    for _ in range(REPETICOES):
        tempo_medio += mede_tempo(algoritmo, lista_media)

    tempo_medio /= REPETICOES


    tempo_pior = mede_tempo(algoritmo, lista_pior)

    return tempo_medio, tempo_pior


def main():

    print("BENCHMARK DE ALGORITMOS DE ORDENAÇÃO")
    print()

    print("Selection Sort")
    print(
        f"{'N':>8} | "
        f"{'Caso médio (s)':>18} | "
        f"{'Pior caso (s)':>18}"
    )


    for n in N_VALORES:

        lista_media = caso_medio(n)
        lista_pior = pior_caso_selection(n)

        media, pior = teste(
            selection_sort,
            lista_media,
            lista_pior
        )

        print(
            f"{n:>8} | "
            f"{media:>18.8f} | "
            f"{pior:>18.8f}"
        )


    print("\nMerge Sort")
    print(
        f"{'N':>8} | "
        f"{'Caso médio (s)':>18} | "
        f"{'Pior caso (s)':>18}"
    )

    for n in N_VALORES:

        lista_media = caso_medio(n)
        lista_pior = pior_caso_merge(n)

        media, pior = teste(
            divide_and_conquer_sort,
            lista_media,
            lista_pior
        )

        print(
            f"{n:>8} | "
            f"{media:>18.8f} | "
            f"{pior:>18.8f}"
        )



    print("\nQuick Sort")

    print(
        f"{'N':>8} | "
        f"{'Caso médio (s)':>18} | "
        f"{'Pior caso (s)':>18}"
    )


    for n in N_VALORES:

        lista_media = caso_medio(n)
        lista_pior = pior_caso_quick(n)

        media, pior = teste(
            quick_sort,
            lista_media,
            lista_pior
        )

        print(
            f"{n:>8} | "
            f"{media:>18.8f} | "
            f"{pior:>18.8f}"
        )


if __name__ == "__main__":
    main()