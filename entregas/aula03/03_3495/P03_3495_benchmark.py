import AP_03_ordenacao as ap3
import sys
import random
import time

sys.setrecursionlimit(10**6)
my_list = [134, 341, 6, 7, 1, 2, 56]

def avg_case(N):
    original = [x for x in range(N)]
    my_list = []
    while len(original):
        random_index = random.randint(0, len(original) - 1)
        my_list.append(original[random_index])
        original[random_index], original[-1] = original[-1], original[random_index]
        original.pop(-1)
    return my_list

def gera_worst_case_quick(N):
    return [x for x in range(N)][::-1]

def perf_algo(sort_algo, N, k, worst_case_fun = None):
    times = []
    for _ in range(k):
        my_list = worst_case_fun(N) if worst_case_fun else avg_case(N)
        start_t = time.perf_counter()
        sort_algo(my_list)
        end_t = time.perf_counter()
        times.append(end_t - start_t)
    return sum(times)/k

#print(f"quick: {perf_algo(ap3.quick_sort, 1000, 50)} ms")
#print(f"select: {perf_algo(ap3.selection_sort, 1000, 50)} ms")
#print(f"merge: {perf_algo(ap3.divide_and_conquer_sort, 1000, 50)} ms")

print("Dados do Quick Sort:")
print(f"  Cenário  | Valor do N |   Tempo médio")
for n in [100, 500, 1000, 5000]:
    print(f"caso médio |    {n}    | {perf_algo(ap3.quick_sort, n, 50)} ms")
for n in [100, 500, 1000, 5000]:
    print(f"pior caso  |    {n}    | {perf_algo(ap3.quick_sort, n, 50, gera_worst_case_quick)} ms")

print()
print("Dados do Selection Sort:")
print(f"  Cenário  | Valor do N |   Tempo médio")
for n in [100, 500, 1000, 5000]:
    print(f"caso médio |    {n}    | {perf_algo(ap3.selection_sort, n, 50)} ms")
for n in [100, 500, 1000, 5000]:
    print(f"pior caso  |    {n}    | {perf_algo(ap3.selection_sort, n, 50)} ms")

print()
print("Dados do Merge Sort:")
print(f"  Cenário  | Valor do N |   Tempo médio")
for n in [100, 500, 1000, 5000]:
    print(f"caso médio |    {n}    | {perf_algo(ap3.divide_and_conquer_sort, n, 50)} ms")
for n in [100, 500, 1000, 5000]:
    print(f"pior caso  |    {n}    | {perf_algo(ap3.divide_and_conquer_sort, n, 50)} ms")