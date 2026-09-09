import AulasPraticas.AP_03_ordenacao  as ap3
import random
import time
import sys
sys.setrecursionlimit(10**6)

# Retorna uma lista aleatória com os números de 1 até N
def avg_case(N):
    original = [ x for x in range(N)]
    my_list = []
    while len(original):
        random_index = random.randint(0, len(original) -1)
        my_list.append(original[random_index])
        original[random_index], original[-1] = original[-1], original[random_index]
        original.pop(-1)
    return my_list

def gera_worst_case_quick(N):
    return [x for x in range(N)][::-1]

def perf_algo(sort_algo, N, k, worst_case_bool = False):
    times = []
    for _ in range(k):
        my_list = avg_case(N) if not worst_case_bool else [x for x in range(N)][::-1] 
        start_t = time.perf_counter()
        sort_algo(my_list)
        end_t = time.perf_counter()
        times.append(end_t - start_t)
    return sum(times)/k



# print(ap3.quick_sort(my_list))
# resultados de cada algoritmo, N, cenário e tempo médio

def printa_tabela(lista_funcs, lista_n, worst_case):
    print(f'{"Resultados":>26} | {"Quant de números":^18} | {"Cenário":^12} | {"Tempo médio":^15}')
    k_execucoes = 50

    for N in lista_n:
        for nome_func, func in lista_funcs:
            tempo_avg_seg = perf_algo(func, N, k_execucoes, worst_case_bool = False)
            tempo_avg_ms = tempo_avg_seg * 1000

            print(f'{nome_func:>26} | {N:^18} | {"avg case":^12} | {tempo_avg_ms:>8.4f} ms')

            if worst_case:
                tempo_worst_seg = perf_algo(func, N, k_execucoes, worst_case_bool=True)
                tempo_worst_ms = tempo_worst_seg * 1000

                print(f'{nome_func:>26} | {N:^18} | {"worst case":^12} | {tempo_worst_ms:>8.4f} ms')

lista_func = [
    ("selection_sort", ap3.selection_sort),
    ("quick_sort", ap3.quick_sort),
    ("divide_and_conquer_sort", ap3.divide_and_conquer_sort)
]

tamanhos_n = [1000, 2000, 5000]

printa_tabela(lista_func, tamanhos_n, worst_case = True)