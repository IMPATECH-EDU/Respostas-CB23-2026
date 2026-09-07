# Nicael Lima Coelho matricula: 3513

import random
import sys
import time
import AP_03_ordenacao as ordena

sys.setrecursionlimit(10000) #tava dando erro e precisou disso aq

def caso_medio(n):
    return [random.randint(1, 10000) for _ in range(n)]

def pior_caso(n):
    return list(range(n, 0, -1))

def timer_medio(funcao_algoritmo, gerador_casos, n, k=30):
    tempo_total = 0.0

    for _ in range(k):
        dados_originais = gerador_casos(n)
        dados_teste = (dados_originais.copy())  # Copia para não reordenar lista já ordenada
        inicio = time.perf_counter()
        funcao_algoritmo(dados_teste)
        fim = time.perf_counter()
        tempo_total += fim - inicio

    tempo_medio = tempo_total / k
    return tempo_medio * 1000


def desempenho():
    tamanhos_n = [100, 500, 1000, 2000]
    k_repeticoes = 30

    algoritmos = {
        "Selection Sort": ordena.selection_sort,
        "Merge Sort": ordena.divide_and_conquer_sort,
        "Quick Sort": ordena.quick_sort,
    }

    casos = {"Caso Médio": caso_medio, "Pior Caso": pior_caso}

    print("-" * 65)
    print(
        f"{'Algoritmo':<18} | {'Casos':<12} | {'N':<6} | {'Tempo Médio (ms)':<15}"
    )
    print("-" * 65)

    for nome_algo, func_algo in algoritmos.items():
        for nome_casos, func_casos in casos.items():
            for n in tamanhos_n:
                tempo_ms = timer_medio(
                    func_algo, func_casos, n, k_repeticoes
                )
                print(
                    f"{nome_algo:<18} | {nome_casos:<12} | {n:<6} | {tempo_ms:<15.4f}"
                )
            print("-" * 65)


if __name__ == "__main__":
    desempenho()
