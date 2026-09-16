import AulasPraticas.AP_03_ordenacao as AP_03_ordenacao
import time
import random
import sys

sys.setrecursionlimit(max(10000, 6000))

random.seed(1001)

def benchmark(algoritmo, lista, k=50):
    tempos = []
    for _ in range(k):
        inicio = time.perf_counter()
        algoritmo(lista.copy())
        fim = time.perf_counter()
        tempos.append(fim - inicio)
    return sum(tempos) / k

caso_medio1 = random.sample(range(1, 100000), 100)
caso_medio2 = random.sample(range(1, 100000), 500)
caso_medio3 = random.sample(range(1, 100000), 1000)
caso_medio4 = random.sample(range(1, 100000), 5000)

pior_caso1 = list(range(100, 0, -1))
pior_caso2 = list(range(500, 0, -1))
pior_caso3 = list(range(1000, 0, -1))
pior_caso4 = list(range(5000, 0, -1))

casos_medios = [caso_medio1, caso_medio2, caso_medio3, caso_medio4]
piores_casos = [pior_caso1, pior_caso2, pior_caso3, pior_caso4]

resultados_casos_medios = []
resultados_piores_casos = []

for i in casos_medios:
    x = benchmark(AP_03_ordenacao.selection_sort, i)
    y = benchmark(AP_03_ordenacao.divide_and_conquer_sort, i)
    z = benchmark(AP_03_ordenacao.quick_sort, i)
    resultados_casos_medios.append((x, y, z))

for i in piores_casos:
    x = benchmark(AP_03_ordenacao.selection_sort, i)
    y = benchmark(AP_03_ordenacao.divide_and_conquer_sort, i)
    z = benchmark(AP_03_ordenacao.quick_sort, i)
    resultados_piores_casos.append((x, y, z))

tamanhos = [100, 500, 1000, 5000]

# Cabeçalho da tabela
print(f"\n{'Cenário':<15} | {'Tamanho (N)':<12} | {'Selection Sort (s)':<20} | {'Divide & Conquer (s)':<20} | {'Quick Sort (s)':<20}")
print("-" * 97)

# Preenchendo os dados do Caso Médio
for tamanho, tempos in zip(tamanhos, resultados_casos_medios):
    print(f"{'Caso Médio':<15} | {tamanho:<12} | {tempos[0]:<20.6f} | {tempos[1]:<20.6f} | {tempos[2]:<20.6f}")

print("-" * 97)

# Preenchendo os dados do Pior Caso
for tamanho, tempos in zip(tamanhos, resultados_piores_casos):
    print(f"{'Pior Caso':<15} | {tamanho:<12} | {tempos[0]:<20.6f} | {tempos[1]:<20.6f} | {tempos[2]:<20.6f}")