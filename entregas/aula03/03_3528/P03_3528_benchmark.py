import AP_03_ordenacao as ordenacao
import time
import random
import sys


random.seed(1001)
sys.setrecursionlimit(10000)


# Selection Sort
def tmcm_selection_sort(N, K):
    tempo_cmedio = 0
    for _ in range(K):
        caso_medio = random.sample(range(1, N+1), N)
        inicio = time.perf_counter()
        ordenacao.selection_sort(caso_medio)
        tempo_cmedio += time.perf_counter() - inicio
    return tempo_cmedio/K

def tmcp_selection_sort(N, K):
    tempo_cpior = 0
    for _ in range(K):
        caso_pior = list(range(N, 0, -1))
        inicio = time.perf_counter()
        ordenacao.selection_sort(caso_pior)
        tempo_cpior += time.perf_counter() - inicio
    return tempo_cpior/K


# Merge Sort
def tmcm_divide_and_conquer_sort(N, K):
    tempo_cmedio = 0
    for _ in range(K):
        caso_medio = random.sample(range(1, N+1), N)
        inicio = time.perf_counter()
        ordenacao.divide_and_conquer_sort(caso_medio)
        tempo_cmedio += time.perf_counter() - inicio
    return tempo_cmedio/K

def tmcp_divide_and_conquer_sort(N, K):
    tempo_cpior = 0
    for _ in range(K):
        caso_pior = list(range(N, 0, -1))
        inicio = time.perf_counter()
        ordenacao.divide_and_conquer_sort(caso_pior)
        tempo_cpior += time.perf_counter() - inicio
    return tempo_cpior/K


# Quick Sort
def tmcm_quick_sort(N, K):
    tempo_cmedio = 0
    for _ in range(K):
        caso_medio = random.sample(range(1, N+1), N)
        inicio = time.perf_counter()
        ordenacao.quick_sort(caso_medio)
        tempo_cmedio += time.perf_counter() - inicio
    return tempo_cmedio/K

def tmcp_quick_sort(N, K):
    tempo_cpior = 0
    for _ in range(K):
        caso_pior = list(range(N, 0, -1))
        inicio = time.perf_counter()
        ordenacao.quick_sort(caso_pior)
        tempo_cpior += time.perf_counter() - inicio
    return tempo_cpior/K


# Parametros
N = [100, 500, 1000, 5000]
K = 50

# Imprimir para o Terminal
print("----------------------------------------------------------------------------------------------------------------------------------------")

# Selection Sort
for i in N:
    print(f"Selection Sort | N = {i} | Tempo Medio Caso Medio: {tmcm_selection_sort(i, K)} | Tempo Medio Pior Caso: {tmcp_selection_sort(i, K)}")
print("----------------------------------------------------------------------------------------------------------------------------------------")

# Merge Sort
for i in N:
    print(f"Merge Sort | N = {i} | Tempo Medio Caso Medio: {tmcm_divide_and_conquer_sort(i, K)} | Tempo Medio Pior Caso: {tmcp_divide_and_conquer_sort(i, K)}")
print("----------------------------------------------------------------------------------------------------------------------------------------")

# Quick Sort
for i in N:
    print(f"Quick Sort | N = {i} | Tempo Medio Caso Medio: {tmcm_quick_sort(i, K)} | Tempo Medio Pior Caso: {tmcp_quick_sort(i, K)}")
print("----------------------------------------------------------------------------------------------------------------------------------------")