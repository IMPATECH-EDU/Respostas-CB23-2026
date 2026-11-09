import AulasPraticas.AP_03_ordenacao as ord
import random
import time
import sys

random.seed(1001)

sys.setrecursionlimit(max(10000, 6000))

N_testes = 100
t_listas = [10, 100, 200, 500, 1000, 2000]

# Selection Sort
for n in t_listas:
    piorcaso = list(range(n,0,-1))

    print(80*"-")

    tempos = []
    for _ in range(N_testes):
        X = random.sample(range(1, n +1), n)
        start = time.perf_counter()
        ord.selection_sort(X)
        tempos.append(time.perf_counter() - start)
    media = sum(tempos) / N_testes
    print(f"{'Selection Sort':<15} | N: {n:^5} | Cenário: ALEATORIO | Tempo Médio: {media:>15}")

    tempos = []
    for _ in range(N_testes):
        start = time.perf_counter()
        ord.selection_sort(piorcaso)
        tempos.append(time.perf_counter() - start)
    media = sum(tempos) / N_testes
    print(f"{'Selection Sort':<15} | N: {n:^5} | Cenário: PIOR CASO | Tempo Médio: { media:>15}")

print(80*"-")

# Merge Sort
for n in t_listas:
    piorcaso = list(range(n,0,-1))
    
    print(80*"-")

    tempos = []
    for _ in range(N_testes):
        X = random.sample(range(1, n +1), n)
        start = time.perf_counter()
        ord.divide_and_conquer_sort(X)
        tempos.append(time.perf_counter() - start)
    media = sum(tempos) / N_testes
    print(f"{'Merge Sort':<15} | N: {n:^5} | Cenário: ALEATORIO | Tempo Médio: { media:>15}")

    tempos = []
    for _ in range(N_testes):
        start = time.perf_counter()
        ord.divide_and_conquer_sort(piorcaso)
        tempos.append(time.perf_counter() - start)
    media = sum(tempos) / N_testes
    print(f"{'Merge Sort':<15} | N: {n:^5} | Cenário: PIOR CASO | Tempo Médio: { media:>15}")

print(80*"-")

# Quick Sort
for n in t_listas:
    piorcaso = list(range(n,0,-1))
    
    print(80*"-")
    
    tempos = []
    for _ in range(N_testes):
        X = random.sample(range(1, n + 1), n)
        start = time.perf_counter()
        ord.quick_sort(X)
        tempos.append(time.perf_counter() - start)
    media = sum(tempos) / N_testes
    print(f"{'Quick Sort':<15} | N: {n:^5} | Cenário: ALEATORIO | Tempo Médio: { media:>15}")

    tempos = []
    for _ in range(N_testes):
        start = time.perf_counter()
        ord.quick_sort(piorcaso)
        tempos.append(time.perf_counter() - start)
    media = sum(tempos) / N_testes
    print(f"{'Quick Sort':<15} | N: {n:^5} | Cenário: PIOR CASO | Tempo Médio: { media:>15}")