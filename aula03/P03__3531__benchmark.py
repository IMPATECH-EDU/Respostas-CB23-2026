from AP_03_ordenacao import selection_sort, divide_and_conquer_sort, quick_sort

import random
import time
import sys

sys.setrecursionlimit(10**6)

def gerar_caso_medio(n):

    return [random.randint(0, 10**6) for _ in range(n)]

def gerar_pior_caso(n):

    return list(range(n, 0, -1))

def Tempo_medio(algoritimo, gerador, N, K=100):

    tempos = []

    for _ in range(K):

        list_test = gerador(N)

        start_time = time.perf_counter()

        algoritimo(list_test)

        end_time = time.perf_counter()

        tempos.append(end_time - start_time)

    return sum(tempos) / K

if __name__ == "__main__":

    casos = [5, 10, 50, 100, 500, 1000, 5000, 10000]

    algoritmos = [("Selection Sort",selection_sort), ("Merge Sort",divide_and_conquer_sort), ("Quick Sort",quick_sort)]

    cenarios = [( "Caso Médio", gerar_caso_medio ), ( "Pior Caso", gerar_pior_caso )]

    print("-" * 65)
    print(f"{'Algoritmo':<18} | {'N':<6} | {'Cenário':<12} | {'Tempo Médio (s)':<15}")
    print("-" * 65)

    for n in casos:
        for nome_cenario, gerador_lista in cenarios:
            for nome_algoritmo, algoritimo in algoritmos:

                tempo = Tempo_medio(algoritimo, gerador_lista, n)

                print(f"{nome_algoritmo:<18} | {n:<6} | {nome_cenario:<12} | {tempo:<15.6f}")
    print("-" * 65)
