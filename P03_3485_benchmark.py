import time
import random
import AP_03_ordenacao as algoritmos
import sys

sys.setrecursionlimit(20000)

def caso_medio(n):
    return [random.randint(0, 1000) for _ in range(n)]


def pior_caso(n):
    return list(range(n, 0, -1))

tamanhos = [10, 50, 100, 500, 1000]
k = 50

for algo in [algoritmos.selection_sort, algoritmos.divide_and_conquer_sort, algoritmos.quick_sort]:
    for i in tamanhos:
        for cenario in [caso_medio, pior_caso]:
            tempos = []
            for vezes in range(k):
                dados = cenario(i)
                inicio = time.perf_counter()
                algo(dados.copy())
                fim = time.perf_counter()
                tempos.append(fim - inicio)
            media = sum(tempos)/k
            print(f" algoritmo:{algo.__name__} | tamanho: {i} | cenário: {cenario.__name__} | tempo médio de execução: {media:.6f} ")
            print("|", end="")
            print("-" * 120, end="")
            print("|")
            print("|", end="")




