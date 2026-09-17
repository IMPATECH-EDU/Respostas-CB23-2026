from AulasPraticas.AP_03_ordenacao import selection_sort,quick_sort,divide_and_conquer_sort
import sys
import random
import time

sys.setrecursionlimit(max(10000,6000))
algoritmos = [selection_sort,quick_sort,divide_and_conquer_sort]
caso_medio = {selection_sort: [], quick_sort: [], divide_and_conquer_sort: []}
pior_caso = {selection_sort: [], quick_sort: [], divide_and_conquer_sort: []}

def random_list(N):
    """Retorna uma lista aleatória formada por N números entre 1 e 1000000."""
    mylist = random.sample(range(1,100000),N)
    return mylist
def tempo_alg(algoritmo,N):
    """Retorna o tempo de execução de um algoritmo."""
    lista = random_list(N)
    inicio = time.perf_counter()
    list_sort = algoritmo(lista)
    fim = time.perf_counter()
    return (fim-inicio)
def media_alg(algoritmo,N,K,funcao):
    """Avalia o tempo médio de K execuções de um algoritmo de sort com N elementos
    a serem ordenados."""
    media = 0
    for _ in range(K):
        media += (funcao(algoritmo,N))/K
    return media
def list_invertida(N):
    """retorna uma lista ordenada do maior para o menor"""
    return list(range(N,0,-1))
def pior_merge(N):
    a = list(range(0,N+1))
    n1 = a[::2].copy()
    n2 = a[1::2].copy()
    return n1+n2
def run_piorcaso(algoritmo,N):
    if algoritmo == selection_sort or algoritmo == quick_sort:
        lista = list_invertida(N)
        inicio = time.perf_counter()
        resolver = algoritmo(lista)
        fim = time.perf_counter()
        return fim-inicio
    else:
        lista = pior_merge(N)
        inicio = time.perf_counter()
        resolver = algoritmo(lista)
        fim = time.perf_counter()
        return fim-inicio
testes = [100,500,1000,5000]
for N in testes:
    for alg in algoritmos:
        caso_medio[alg].append(media_alg(alg,N,50,tempo_alg))
        pior_caso[alg].append(media_alg(alg,N,50,run_piorcaso))
print("N\tSelection_sort médio\tSelection_sort pior\tQuick_sort médio\tQuick_sort pior\tDivid_conquer médio\tDivide_conquer pior")

for i, N in enumerate(testes):
    print(
        f"{N}\t"
        f"{caso_medio[selection_sort][i]:.6f}\t"
        f"{pior_caso[selection_sort][i]:.6f}\t"
        f"{caso_medio[quick_sort][i]:.6f}\t"
        f"{pior_caso[quick_sort][i]:.6f}\t"
        f"{caso_medio[divide_and_conquer_sort][i]:.6f}\t"
        f"{pior_caso[divide_and_conquer_sort][i]:.6f}"
    )