import AP_03_ordenacao as ord
from time import perf_counter as time
import random

numeros = [100, 500, 1000, 5000]
k=50

def caso_medio(_):
    caso_medio = random.choices(range(1,100), k=_)

    tempo_inicial = time()
    ord.quick_sort(caso_medio)
    tempos_medio["quick_sort"] += time() - tempo_inicial

    tempo_inicial = time()
    ord.divide_and_conquer_sort(caso_medio)
    tempos_medio["divide_and_conquer_sort"] += time() - tempo_inicial

    tempo_inicial = time()
    ord.selection_sort(caso_medio)
    tempos_medio["selection_sort"] += time() - tempo_inicial

def caso_pior(_):
    caso_pior = sorted(random.choices(range(1,100), k=_), reverse=True)

    tempo_inicial = time()
    ord.quick_sort(caso_pior)
    tempos_pior["quick_sort"] += time() - tempo_inicial

    tempo_inicial = time()
    ord.divide_and_conquer_sort(caso_pior)
    tempos_pior["divide_and_conquer_sort"] += time() - tempo_inicial

    tempo_inicial = time()
    ord.selection_sort(caso_pior)
    tempos_pior["selection_sort"] += time() - tempo_inicial

for _ in numeros:
    tempos_medio = {"quick_sort" : 0.0, "divide_and_conquer_sort": 0.0, "selection_sort": 0.0}
    tempos_pior = {"quick_sort" : 0.0, "divide_and_conquer_sort": 0.0, "selection_sort": 0.0}
    for __ in range(k):
        caso_medio(_)
        caso_pior(_)
    print("-" * 80)
    print(f"{'Resultado de Cada algoritimo':<30}{'N':<10}{'Cenário':<15}{'Tempo Médio':>15}")
    for i in tempos_medio:
        print(f"{i:<30}{_:<10}{'Caso Médio':<15}{tempos_medio[i]/k:>15.10f}")
    for i in tempos_pior:
        print(f"{i:<30}{_:<10}{'Caso Pior':<15}{tempos_pior[i]/k:>15.10f}")