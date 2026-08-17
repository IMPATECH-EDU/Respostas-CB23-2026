import time
import AP_03_ordenacao as ap
import random 
random.seed(1001)
import sys
sys.setrecursionlimit(10**5)
#import AulasPraticas.AP_03_ordenacao

tamanhos = [100, 500, 1000, 5000]

resultados_casomedio = []
resultado_piorcasogeral = []
resultado_piorcaso_qick = []

lista_invertida =  [ item for item in range(100, -1, -1)]


#selectionsort

for num in tamanhos:

    lista = random.sample(range(1, 10**6), num)
    
    acumulador = 0
    for _ in range(50):
    
            inicio = time.perf_counter()
    
            ordenada = ap.selection_sort(lista)
    
            fim = time.perf_counter()
    
            acumulador += (fim - inicio)

    print(f"Tamanho da lista : {num}")

    print(f"Tempo médio: {acumulador/50:.8f} s")

    print()

print("-"*64)

print("Algoritmo Marge sort - Casos médios")

print()

for num in tamanhos:

    lista = random.sample(range(1, 10**6), num)
    
    acumulador = 0
    for _ in range(50):
    
            inicio = time.perf_counter()
    
            ordenada = ap.divide_and_conquer_sort(lista)
    
            fim = time.perf_counter()
    
            acumulador += (fim - inicio)

    print(f"Tamanho da lista : {num}")

    print(f"Tempo médio: {acumulador/50:.8f} s")

    print()

print("-"*64)

print("Algoritmo quick_sort - Casos médios")

print()


for num in tamanhos:

    lista = random.sample(range(1, 10**6), num)
    
    acumulador = 0
    n = 0
    for _ in range(50):

    
                inicio = time.perf_counter()
          
                ordenada = ap.quick_sort(lista)
      
                fim = time.perf_counter()
        
                acumulador += (fim - inicio)



    print(f"Tamanho da lista : {num}")

    print(f"Tempo médio: {acumulador/50:.8f} s")
    print()

print("-"*64)

print(f"Algoritmo Selection Sort não há pior caso")
lista =   [item for item in range(num, -1, -1)]
    
acumulador = 0
for _ in range(50):

                inicio = time.perf_counter()
          
                ordenada = ap.selection_sort(lista)
      
                fim = time.perf_counter()
        
                acumulador += (fim - inicio)

print(f"Tamanho da lista : {100}")
print(f"Tempo médio : {acumulador/50:.8f} s")


print()
print(f"Algoritmo Marge sort não há pior caso")
lista =   [item for item in range(num, -1, -1)]
    
acumulador = 0
for _ in range(50):

                inicio = time.perf_counter()
          
                ordenada = ap.divide_and_conquer_sort(lista)
      
                fim = time.perf_counter()
        
                acumulador += (fim - inicio)

print(f"Tamanho da lista : {100}")
print(f"Tempo médio : {acumulador/50:.8f} s")

print()

print("-"*64)

print(f"Algoritmo Quick Sort")
print(f"O pior caso é 'Lista em ordem decrescente'")
print()

for num in tamanhos:
    lista =   [item for item in range(num, -1, -1)]
    
    acumulador = 0
    for _ in range(50):

                inicio = time.perf_counter()
          
                ordenada = ap.quick_sort(lista)
      
                fim = time.perf_counter()
        
                acumulador += (fim - inicio)

    print(f"Tamanho da lista : {num}")
    print(f"Tempo médio : {acumulador/50:.8f} s")
    print()