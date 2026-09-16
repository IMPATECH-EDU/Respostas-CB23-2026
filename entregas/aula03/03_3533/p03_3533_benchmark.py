import AulasPraticas.AP_03_ordenacao as ap3
import sys
import time
import random

sys.setrecursionlimit(10**6)

# Gera uma lista de tamanho N com os termos em uma ordem aleatória.
def avg_case(N):
    lista = [x for x in range(N)]
    minha_l = []
    while len(lista):
        random_index = random.randint(0, len(lista) - 1)
        minha_l.append(lista[random_index])
        lista[random_index], lista[-1] = lista[-1], lista[random_index]
        lista.pop()
    return minha_l

# Gera uma lista que representa o pior caso de ordenação do método quick.
# Os métodos selection_sort e divide_and_conquer_sort não possuem um pior caso, tendo
# em vista que realizam o mesmo número de processos independente da ordenação inicial.
def gera_wost_case_quick(N):
    return [x for x in range(N)][::-1]

# Função que aplica um dos métodos e calcula o tempo médio das operações.
def perf_algo(sort_algo, N, k, worst_case_fun=None):
    times = []
    for p in range(k):
        my_list = worst_case_fun(N) if worst_case_fun else avg_case(N)
        start_t = time.perf_counter()
        sort_algo(my_list)
        end_t = time.perf_counter()
        times.append(end_t - start_t)
    return sum(times) / k

# Estrutura com os cenários de teste
# Formato: (função, nome_exibição, N, K, função_pior_caso, nome_cenário)
experimentos = [
    (ap3.divide_and_conquer_sort, "Divide & Conquer", 100, 5, None, "Médio"),
    (ap3.quick_sort, "Quick Sort", 100, 5, None, "Médio"),
    (ap3.quick_sort, "Quick Sort", 100, 5, gera_wost_case_quick, "Pior"),
    (ap3.selection_sort, "Selection Sort", 100, 5, None, "Médio"),
    (ap3.divide_and_conquer_sort, "Divide & Conquer", 500, 5, None, "Médio"),
    (ap3.quick_sort, "Quick Sort", 500, 5, None, "Médio"),
    (ap3.quick_sort, "Quick Sort", 500, 5, gera_wost_case_quick, "Pior"),
    (ap3.selection_sort, "Selection Sort", 500, 5, None, "Médio"),
    (ap3.divide_and_conquer_sort, "Divide & Conquer", 1000, 5, None, "Médio"),
    (ap3.quick_sort, "Quick Sort", 1000, 5, None, "Médio"),
    (ap3.quick_sort, "Quick Sort", 1000, 5, gera_wost_case_quick, "Pior"),
    (ap3.selection_sort, "Selection Sort", 1000, 5, None, "Médio"),
    (ap3.divide_and_conquer_sort, "Divide & Conquer", 5000, 5, None, "Médio"),
    (ap3.quick_sort, "Quick Sort", 5000, 5, None, "Médio"),
    (ap3.quick_sort, "Quick Sort", 5000, 5, gera_wost_case_quick, "Pior"),
    (ap3.selection_sort, "Selection Sort", 5000, 5, None, "Médio"),
]

# Construção da tabela no terminal
cabecalho = f"| {'Algoritmo':<22} | {'N':<6} | {'Cenário':<8} | {'Tempo Médio (s)':<15} |"
linhas = "-" * len(cabecalho)

print(linhas)
print(cabecalho)
print(linhas)

for algo, nome, N, k, fn_pior, cenario in experimentos:
    tempo_m = perf_algo(algo, N, k, worst_case_fun=fn_pior)
    print(f"| {nome:<22} | {N:<6} | {cenario:<8} | {tempo_m:<15.6f} |")
    if nome == "Selection Sort":
        print(linhas)