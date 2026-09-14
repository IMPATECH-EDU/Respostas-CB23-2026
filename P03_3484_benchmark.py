from AulasPraticas.AP_03_ordenacao import selection_sort, divide_and_conquer_sort, quick_sort 
from time import perf_counter
import random
import sys

sys.setrecursionlimit(max(10_000, 6_000))
random.seed(1001)  # Para reprodutibilidade dos resultados

# Selection sort
def test_medio_selection_sort(num_entrada, num_testes):
    results = list()
    for _ in range(num_testes):
        lista_teste = random.sample(range(1,num_entrada+1), num_entrada)
        start = perf_counter()
        selection_sort(lista_teste)
        finish = perf_counter()
        time = finish - start
        results.append(time/num_testes)

    return sum(results) 

def test_pior_selection_sort(num_entrada, num_testes):
    results = list()
    lista_teste = list(range(num_entrada,0,-1))
    for _ in range(num_testes):
        start = perf_counter()
        selection_sort(lista_teste)
        finish = perf_counter()
        time = finish - start
        results.append(time/num_testes)

    return sum(results) 



# Merge sort
def test_medio_merge_sort(num_entrada, num_testes):
    results = list()
    for _ in range(num_testes):
        lista_teste = random.sample(range(1,num_entrada+1), num_entrada)
        start = perf_counter()
        divide_and_conquer_sort(lista_teste)
        finish = perf_counter()
        time = finish - start
        results.append(time/num_testes)

    return sum(results) 

def test_pior_merge_sort(num_entrada, num_testes):
    results = list()
    lista_teste = list(range(num_entrada,0,-1))
    for _ in range(num_testes):
        start = perf_counter()
        divide_and_conquer_sort(lista_teste)
        finish = perf_counter()
        time = finish - start
        results.append(time/num_testes)

    return sum(results) 



# Quick sort
def test_medio_quick_sort(num_entrada, num_testes):
    results = list()
    for _ in range(num_testes):
        lista_teste = random.sample(range(1,num_entrada+1), num_entrada)
        start = perf_counter()
        quick_sort(lista_teste)
        finish = perf_counter()
        time = finish - start
        results.append(time/num_testes)

    return sum(results) 

def test_pior_quick_sort(num_entrada, num_testes):
    results = list()
    lista_teste = list(range(num_entrada,0,-1))
    for _ in range(num_testes):
        start = perf_counter()
        quick_sort(lista_teste)
        finish = perf_counter()
        time = finish - start
        results.append(time/num_testes)

    return sum(results) 



# formatação
def format(dados):
    #cabeçalho
    print(f"{'Algoritmo':<22} | {'Caso Médio':^22} | {'Pior Caso':^22} | {'Entrada':>10}")
    print("-" * 68)

    for algoritmo, dicionario in dados.items():
        for tamanho, (time_caso_medio, time_pior_caso) in dicionario.items():
            print(f"{algoritmo:<22} | {time_caso_medio:^22} | {time_pior_caso:^22} | {tamanho:>10}")
    

dados = dict()
dados["Selection sort"] = {
    "100": (test_medio_selection_sort(100, 50), test_pior_selection_sort(100, 50)),
    "500": (test_medio_selection_sort(500, 50), test_pior_selection_sort(500, 50)),
    "1000": (test_medio_selection_sort(1000, 50), test_pior_selection_sort(1000, 50)),
    "5000": (test_medio_selection_sort(5000, 50), test_pior_selection_sort(5000, 50))
}

dados["Merge sort"] = {
    "100": (test_medio_merge_sort(100, 50), test_medio_merge_sort(100, 50)),
    "500": (test_medio_merge_sort(500, 50), test_medio_merge_sort(500, 50)),
    "1000": (test_medio_merge_sort(1000, 50), test_medio_merge_sort(1000, 50)),
    "5000": (test_medio_merge_sort(5000, 50), test_medio_merge_sort(5000, 50))
}

dados["Quick sort"] = {
    "100": (test_medio_quick_sort(100, 50), test_pior_quick_sort(100, 50)),
    "500": (test_medio_quick_sort(500, 50), test_pior_quick_sort(500, 50)),
    "1000": (test_medio_quick_sort(1000, 50), test_pior_quick_sort(1000, 50)),
    "5000": (test_medio_quick_sort(5000, 50), test_pior_quick_sort(5000, 50))
}

format(dados)