import AulasPraticas.AP_03_ordenacao as ap3
import sys
import random
import time

sys.setrecursionlimit(10**6)

# retorna uma lista aleatória com números de 1 até n (Caso Médio)
def avg_case(N):
    original = [x for x in range(N)]
    my_list = []
    while len(original):
        random_index = random.randint(0, len(original) -1)
        my_list.append(original[random_index])
        original[random_index], original[-1] = original[-1], original[random_index]
        original.pop(-1)
    return my_list

# gera uma lista com o pior caso
def gera_worst_case_quick(N):
    return [x for x in range (N)][::-1]

# calcula o tempo de execução
def perf_algo(sort_algo, N, k, worst_case_fun=None):
    times = []
    for _ in range(k):
        my_list = worst_case_fun(N) if worst_case_fun else avg_case(N)
        start_t = time.perf_counter()
        sort_algo(my_list)
        end_t = time.perf_counter()
        times.append(end_t - start_t)
    return sum(times)/k

# printa a tabela
print("-" * 64)
print(f"{'Testes selection_sort, k = 50':^64}")
print("-" * 64)
print(f'Caso médio, N=100:  {perf_algo(ap3.selection_sort, 100, 50):.6f} s')
print(f'Caso médio, N=500:  {perf_algo(ap3.selection_sort, 500, 50):.6f} s')
print(f'Caso médio, N=1000: {perf_algo(ap3.selection_sort, 1000, 50):.6f} s')
print(f'Caso médio, N=5000: {perf_algo(ap3.selection_sort, 5000, 50):.6f} s')
print()
print(f'Pior caso, N=100:  {perf_algo(ap3.selection_sort, 100, 50, gera_worst_case_quick):.6f} s')
print(f'Pior caso, N=500:  {perf_algo(ap3.selection_sort, 500, 50, gera_worst_case_quick):.6f} s')
print(f'Pior caso, N=1000: {perf_algo(ap3.selection_sort, 1000, 50, gera_worst_case_quick):.6f} s')
print(f'Pior caso, N=5000: {perf_algo(ap3.selection_sort, 5000, 50, gera_worst_case_quick):.6f} s')
print()

print("-" * 64)
print(f"{'Testes quick_sort, k = 50':^64}")
print("-" * 64)
print(f'Caso médio, N=100:  {perf_algo(ap3.quick_sort, 100, 50):.6f} s')
print(f'Caso médio, N=500:  {perf_algo(ap3.quick_sort, 500, 50):.6f} s')
print(f'Caso médio, N=1000: {perf_algo(ap3.quick_sort, 1000, 50):.6f} s')
print(f'Caso médio, N=5000: {perf_algo(ap3.quick_sort, 5000, 50):.6f} s')
print()
print(f'Pior caso, N=100:  {perf_algo(ap3.quick_sort, 100, 50, gera_worst_case_quick):.6f} s')
print(f'Pior caso, N=500:  {perf_algo(ap3.quick_sort, 500, 50, gera_worst_case_quick):.6f} s')
print(f'Pior caso, N=1000: {perf_algo(ap3.quick_sort, 1000, 50, gera_worst_case_quick):.6f} s')
print(f'Pior caso, N=5000: {perf_algo(ap3.quick_sort, 5000, 50, gera_worst_case_quick):.6f} s')
print()

print("-" * 64)
print(f"{'Testes divide_and_conquer_sort, k = 50':^64}")
print("-" * 64)
print(f'Caso médio, N=100:  {perf_algo(ap3.divide_and_conquer_sort, 100, 50):.6f} s')
print(f'Caso médio, N=500:  {perf_algo(ap3.divide_and_conquer_sort, 500, 50):.6f} s')
print(f'Caso médio, N=1000: {perf_algo(ap3.divide_and_conquer_sort, 1000, 50):.6f} s')
print(f'Caso médio, N=5000: {perf_algo(ap3.divide_and_conquer_sort, 5000, 50):.6f} s')
print()
print(f'Pior caso, N=100:  {perf_algo(ap3.divide_and_conquer_sort, 100, 50, gera_worst_case_quick):.6f} s')
print(f'Pior caso, N=500:  {perf_algo(ap3.divide_and_conquer_sort, 500, 50, gera_worst_case_quick):.6f} s')
print(f'Pior caso, N=1000: {perf_algo(ap3.divide_and_conquer_sort, 1000, 50, gera_worst_case_quick):.6f} s')
print(f'Pior caso, N=5000: {perf_algo(ap3.divide_and_conquer_sort, 5000, 50, gera_worst_case_quick):.6f} s')