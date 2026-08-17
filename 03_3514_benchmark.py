#Lourenzo Francisco Balonekr dos Santos 3514
#Código realizado pra 50 testes
import time
import random
import AP_03_ordenacao
random.seed(2)
testes = []
ordenado = []
K = 50
N = 500
def select(n, caso = 0):
    if caso == 0:     
     inicio = time.perf_counter()
     for i in range(n):
         x = time.perf_counter()
         AP_03_ordenacao.selection_sort(testes[i])
         y = time.perf_counter()
         tempocada= y-x
     a = time.perf_counter()
     fim = a - inicio
     media = fim/n
    else:
        inicio = time.perf_counter()
        for i in range(n):
              x = time.perf_counter()
              AP_03_ordenacao.selection_sort(ordenado[i])
              y = time.perf_counter()
              tempocada= y-x
        a = time.perf_counter()
        fim = a - inicio
        media = fim/n
    return media

def merge(n, caso = 0):
    if caso == 0:
     inicio = time.perf_counter()
     for i in range(n):
         x = time.perf_counter()
         AP_03_ordenacao.divide_and_conquer_sort(testes[i])
         y = time.perf_counter()
         tempocada= y-x
     a = time.perf_counter()
     fim = a - inicio
     media = fim/n
    else:
        inicio = time.perf_counter()
        for i in range(n):
          x = time.perf_counter()
          AP_03_ordenacao.divide_and_conquer_sort(ordenado[i])
          y = time.perf_counter()
          tempocada= y-x
        a = time.perf_counter()
        fim = a - inicio
        media = fim/n
    return media    
def quick(n, caso = 0):
    if caso == 0:
     inicio = time.perf_counter()
     for i in range(n):
         x = time.perf_counter()
         AP_03_ordenacao.quick_sort(testes[i])
         y = time.perf_counter()
         tempocada= y-x
     a = time.perf_counter()
     fim = a - inicio
     media = fim/n
    else:
        inicio = time.perf_counter()
        for i in range(n):
          x = time.perf_counter()
          AP_03_ordenacao.quick_sort(ordenado[i])
          y = time.perf_counter()
          tempocada= y-x
        a = time.perf_counter()
        fim = a - inicio
        media = fim/n
    return media
lista = [100, 500, 1000, 5000]
for r in lista:
   testes = []
   for i in range(K):
    x = random.sample(range(100, 10000), N)
    testes.append(x)
    ordenado.append(sorted(x, reverse= True))
   print(f"-------------\nQuantidade de elementos em cada lista = {N}\n-----------")      
   print(f"Média de tempo obtido nos seguintes algoritmos usando {K} listas com {N} elementos")
   print("--------------\nMerge sort")
   print(f"Caso médio:{merge(K)} O(nlogn)\nPior caso :{merge(K, 1)} O(nlogn)")
   print("--------------\nQuick sort")
   print(f"Caso médio:{quick(K)} O(nlogn)\nPior caso :{quick(K, 1)} O(nlogn)")
   print("--------------\nSelection sort")
   print(f"Caso médio:{select(K)} O(n^2)\nPior caso :{select(K, 1)} O(n^2)")
   N = r
#Embora listados como tendo "pior caso" tanto o merge quanto o selection sort apresentam estabilidade
#Sendo então a variação de resultados apenas ruído
