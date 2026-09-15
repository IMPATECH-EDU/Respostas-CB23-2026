# David Marcos da Silva

import AP_03_ordenacao
import time
import random
import copy
import sys
sys.setrecursionlimit(100000)

def gerar_medio(n):
    temp = []
    for i in range(n):
        temp.append(random.randint(0,n))
    return temp

def gerar_pior(n):
    temp = []
    for i in range(n,0,-1):
        temp.append(i)
    return temp

k = 50
valores_n = [100, 500, 1000, 5000]

print(f"{'Algoritmo':<15} | {'N':<6} | {'Cenário':<12} | {'Tempo Médio (s)'}")
print("-" * 52)

for n in valores_n:
    dvd1, dvd2, qs1, qs2, ss1, ss2 = [], [], [], [], [], []

    testes = {}
    for i in range(k):
        testes[i] = (gerar_medio(n))
    testes['pior'] = (gerar_pior(n))

    for i in range(k):
        lista = testes[i]
        pior = testes['pior']

        t1 = time.perf_counter()
        AP_03_ordenacao.divide_and_conquer_sort(copy.copy(lista))
        dvd1.append(time.perf_counter() - t1)

        t1 = time.perf_counter()
        AP_03_ordenacao.divide_and_conquer_sort(copy.copy(pior))
        dvd2.append(time.perf_counter() - t1)

        t1 = time.perf_counter()
        AP_03_ordenacao.quick_sort(copy.copy(lista))
        qs1.append(time.perf_counter() - t1)

        t1 = time.perf_counter()
        AP_03_ordenacao.quick_sort(copy.copy(pior))
        qs2.append(time.perf_counter() - t1)

        t1 = time.perf_counter()
        AP_03_ordenacao.selection_sort(copy.copy(lista))
        ss1.append(time.perf_counter() - t1)

        t1 = time.perf_counter()
        AP_03_ordenacao.selection_sort(copy.copy(pior))
        ss2.append(time.perf_counter() - t1)

    # Exibição organizada em formato de tabela
    print(f"{'Merge Sort':<15} | {n:<6} | {'Médio':<12} | {sum(dvd1)/k:.6f}")
    print(f"{'Merge Sort':<15} | {n:<6} | {'Pior':<12} | {sum(dvd2)/k:.6f}")
    print(f"{'Quick Sort':<15} | {n:<6} | {'Médio':<12} | {sum(qs1)/k:.6f}")
    print(f"{'Quick Sort':<15} | {n:<6} | {'Pior':<12} | {sum(qs2)/k:.6f}")
    print(f"{'Selection Sort':<15} | {n:<6} | {'Médio':<12} | {sum(ss1)/k:.6f}")
    print(f"{'Selection Sort':<15} | {n:<6} | {'Pior':<12} | {sum(ss2)/k:.6f}")