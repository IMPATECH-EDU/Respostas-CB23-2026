import time
import random
import sys
import AulasPraticas.AP_03_ordenacao as AP3

sys.setrecursionlimit(10**6)

def gerar_caso_medio(n):
    """Gera uma lista de tamanho N com números inteiros aleatórios."""
    original = [x for x in range(n)]
    my_list = []
    while len(original):
        random_index = random.randint(0, len(original) - 1)
        my_list.append(original[random_index])
        original[random_index], original[-1] = original[-1], original[random_index]
        original.pop(-1)
    return my_list

def gerar_lista_decresc(n):
    """ Gera uma lista em ordem decrescente (totalmente invertida)."""
    return list(range(n, 0, -1))

def gerar_lista_cresc(n):
    """ Gera uma lista em ordem crescente. """
    return list(range(n))

def medir_tempo_medio(sort_algo, n, k, gerador_lista):
    """Mede o tempo médio de execução de um algoritmo para K repetições."""
    times = []
    for _ in range(k):
        my_list = gerador_lista(n)
        start_t = time.perf_counter()
        sort_algo(my_list)
        end_t = time.perf_counter()
        times.append(end_t - start_t)
    return (sum(times) / k) * 1000 # Retornando em milissegundos (ms)

# Configurações do Benchmark
valores_n = [100, 500, 1000, 5000]
k_repeticoes = 50

algoritmos = [
    ("Quick Sort", AP3.quick_sort),
    ("Selection Sort", AP3.selection_sort),
    ("Merge Sort", AP3.divide_and_conquer_sort)
]

cenarios = [
    ("Caso Médio", gerar_caso_medio),
    ("Crescente", gerar_lista_cresc),
    ("Decrescente", gerar_lista_decresc)
]

# Impressão do Cabeçalho da Tabela
print(f"{'Algoritmo':<15} | {'N':<6} | {'Cenário':<15} | {'Tempo Médio (ms)':<15}")
print("-" * 60)

# Execução e formatação dos resultados
for nome_algo, func_algo in algoritmos:
    for n in valores_n:
        for nome_cenario, func_cenario in cenarios:
            tempo = medir_tempo_medio(func_algo, n, k_repeticoes, func_cenario)
            print(f"{nome_algo:<15} | {n:<6} | {nome_cenario:<15} | {tempo:.4f}") 