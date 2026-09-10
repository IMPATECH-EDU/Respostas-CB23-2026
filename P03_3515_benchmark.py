import time
import random
import sys
from AP_03_ordenacao import (selection_sort, divide_and_conquer_sort, quick_sort)
sys.setrecursionlimit(10000)

TAMANHOS = [100, 500, 1000, 5000]
K = 50

def gerar_caso_medio(n):
    return [ random.randint(0, 100000) for _ in range(n) ]


def gerar_pior_caso(n):
    return list(range(n, 0, -1))


def medir_tempo(algoritmo, lista):
    inicio = time.perf_counter()

    algoritmo(lista)

    fim = time.perf_counter()

    return fim - inicio


def executar_benchmark(algoritmo, gerador, n):
    tempos = []
    for _ in range(K):
        lista = gerador(n)
        lista_teste = lista.copy()
        tempo = medir_tempo(algoritmo, lista_teste)
        tempos.append(tempo)

    media = sum(tempos) / K
    return media


def imprimir_resultado(nome_algoritmo, n, caso, tempo_medio):
    print(
        f"{nome_algoritmo:<20}"
        f"{n:<10}"
        f"{caso:<15}"
        f"{tempo_medio:.6f} s")


def main():
    algoritmos = [("Selection Sort", selection_sort), ("Merge Sort", divide_and_conquer_sort), ("Quick Sort", quick_sort)]

    print("=" * 70)
    print("BENCHMARK DE ALGORITMOS DE ORDENACAO")
    print("=" * 70)

    print(
        f"{'Algoritmo':<20}"
        f"{'N':<10}"
        f"{'Cenario':<15}"
        f"{'Tempo medio'}"
    )

    print("-" * 70)

    for nome_algoritmo, algoritmo in algoritmos:
        for n in TAMANHOS:
            tempo_medio = executar_benchmark(algoritmo, gerar_caso_medio, n)

            imprimir_resultado(nome_algoritmo, n, "Caso Medio", tempo_medio)

            tempo_medio = executar_benchmark(algoritmo, gerar_pior_caso, n)

            imprimir_resultado(nome_algoritmo, n, "Pior Caso", tempo_medio)

    print("=" * 70)
    print("Benchmark finalizado com sucesso!")
    print("=" * 70)


if __name__ == "__main__":
    main()