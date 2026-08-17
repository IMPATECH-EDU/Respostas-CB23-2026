import time
import random
import sys
from AulasPraticas.AP_03_ordenacao import selection_sort, divide_and_conquer_sort, quick_sort

random.seed(1001)
sys.setrecursionlimit(max(10000))

def listaCasoMed(N):
    return [random.randint(0, 1000000) for _ in range(N)]

def listaCasoPior(N):
    return list(range(N - 1, -1, -1))

def benchmark_CM():
    metodos_tempos = {
        "selection": {"medium": {}, "worst": {}},
        "divide": {"medium": {}, "worst": {}},
        "quick": {"medium": {}, "worst": {}}
    }
    tamanhos = [100,500,1000,5000]
    
    for num in tamanhos:
        lista_CM_Atual = listaCasoMed(num)
        
        metodos_tempos["selection"]["medium"][str(num)] = bench_selec(lista_CM_Atual)
        metodos_tempos["divide"]["medium"][str(num)] = bench_divide(lista_CM_Atual)
        metodos_tempos["quick"]["medium"][str(num)] = bench_quick(lista_CM_Atual)

        metodos_tempos["selection"]["worst"][str(num)] = bench_selec(listaCasoPior(num))
        metodos_tempos["divide"]["worst"][str(num)] = bench_divide(lista_CM_Atual)
        metodos_tempos["quick"]["worst"][str(num)] = bench_quick(listaCasoPior(num))

    return metodos_tempos
    
def bench_selec(lista_original):
    tempo_final = 0
    for _ in range(50):
        lista_teste = lista_original.copy()
        temp_inicial = time.perf_counter()
        lista_selec = selection_sort(lista_teste)
        tempo_selec = time.perf_counter() - temp_inicial
        tempo_final += tempo_selec
    return tempo_final / 50

def bench_divide(lista_original):
    tempo_final = 0
    for _ in range(50):
        lista_teste = lista_original.copy()
        temp_inicial = time.perf_counter()
        lista_divide = divide_and_conquer_sort(lista_teste)
        tempo_divide = time.perf_counter() - temp_inicial
        tempo_final += tempo_divide
    return tempo_final / 50

def bench_quick(lista_original):
    tempo_final = 0
    for _ in range(50):
        lista_teste = lista_original.copy()
        temp_inicial = time.perf_counter()
        lista_quick = quick_sort(lista_teste)
        tempo_quick = time.perf_counter() - temp_inicial
        tempo_final += tempo_quick
    return tempo_final / 50


resultados_CN = benchmark_CM()

#print(f"""Selection: 100 = {resultados_CN["selection"]["medium"]["100"]:.6f}s, 500 = {resultados_CN["selection"]["medium"]["500"]:.6f}s, 1000 = {resultados_CN["selection"]["medium"]["1000"]:.6f}s, 5000 = {resultados_CN["selection"]["medium"]["5000"]:.6f}s
#Divide: 100 = {resultados_CN["divide"]["medium"]["100"]:.6f}s, 500 = {resultados_CN["divide"]["medium"]["500"]:.6f}s, 1000 = {resultados_CN["divide"]["medium"]["1000"]:.6f}s, 5000 = {resultados_CN["divide"]["medium"]["5000"]:.6f}s
#Quick: 100 = {resultados_CN["quick"]["medium"]["1000"]:.6f}s, 50０ = {resultados_CN["quick"]["medium"]["5０００"]:.6f}s, 1０００ = {resultados_CN["quick"]["medium"]["1０００"]:.6f}s, 5０００ = {resultados_CN["quick"]["medium"]["5０００"]:.6f}s""")

print("=" * 67)
print(f"{'Algoritmo':<12} {'Caso':<10} {'100':>10} {'500':>10} {'1000':>10} {'5000':>10}")
print("=" * 67)

for algoritmo in ["selection", "divide", "quick"]:
    for caso in ["medium", "worst"]:
        print(
            f"{algoritmo.capitalize():<12} "
            f"{caso.capitalize():<10} "
            f"{resultados_CN[algoritmo][caso]['100']:>10.6f} "
            f"{resultados_CN[algoritmo][caso]['500']:>10.6f} "
            f"{resultados_CN[algoritmo][caso]['1000']:>10.6f} "
            f"{resultados_CN[algoritmo][caso]['5000']:>10.6f}"
        )
    print("-" * 67)