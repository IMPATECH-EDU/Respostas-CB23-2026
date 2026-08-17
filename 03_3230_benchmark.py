import AulasPraticas.AP_03_ordenacao as ap
import time
import random
import sys

sys.setrecursionlimit(max(10000, 6000))
random.seed(1001) 

def ListaAleatoria(n):
    lista = []
    for i in range(1, n+1):
        x = random.randint(1,50000)
        lista.append(x)
    return lista

def ListaInvertida(n):
    lista = []
    for i in range(n, 0, -1):
        x = random.randint(1,50000)
        lista.append(x)
    return lista

def Tempo(algoritmo, lista, repeticoes=50):
    tempo = 0
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        algoritmo(lista)
        fim = time.perf_counter()
        tempo += fim - inicio
    return tempo/repeticoes

def benchmark():
    algoritmos = [ap.selection_sort, ap.divide_and_conquer_sort, ap.quick_sort]
    for algoritmo in algoritmos:
        for n in [100, 500, 1000, 5000]:
            caso_medio = ListaAleatoria(n)
            pior_caso = ListaInvertida(n)
            tempo_medio = Tempo(algoritmo, caso_medio)
            tempo_pior = Tempo(algoritmo, pior_caso)
            print(f"Algoritmo{algoritmo.__name__}, n={n}, tempo_medio={tempo_medio:.6f}, pior_caso={tempo_pior:.6f}")

benchmark()
















