import time
import AP_03_ordenacao as ordena
import random 


tamanho = [100, 200, 400, 800, 1000, 5000, 10000]

caso_medio=[]
pior_caso=[]

for i in tamanho:
    caso_medio.append([random.randint(1, 5000) for _ in range(i)])
    l=[]
    for num in range(i,0,-1):
        l.append(num)
    pior_caso.append(l)


def executar_medio(tipo, algoritmo, k, recursao=False):
    print(f"-----------{tipo} Sort - Caso Médio------------")
    print(f"{'Tamanho':>7} | {'Execuções':>9} | {'Tempo Médio'}")
    for lista in caso_medio:
        if recursao and len(lista)>900:
            break
        tempo_total=0
        for _ in range(k):
            copia=lista.copy()
            tempo_inicial=time.perf_counter()
            algoritmo(copia)
            tempo_final=time.perf_counter()
            tempo_total+=(tempo_final-tempo_inicial)
        print(f"{len(lista):>7} | {k:^9} | {(tempo_total/k):>11.6f} s")
    print()

def executar_pior(tipo, algoritmo, k, recursao=False):
    print(f"------------{tipo} Sort - Pior Caso------------")
    print(f"{'Tamanho':>7} | {'Execuções':>9} | {'Tempo Médio'}")
    for lista in pior_caso:
        if recursao and len(lista)>900:
            break
        tempo_total=0
        for _ in range(k):
            copia=lista.copy()
            tempo_inicial=time.perf_counter()
            algoritmo(copia)
            tempo_final=time.perf_counter()
            tempo_total+=(tempo_final-tempo_inicial)
        print(f"{len(lista):>7} | {k:^9} | {(tempo_total/k):>11.6f} s")
    print()

k=50 #número de vezes que ordena cada lista
executar_medio("Selection",ordena.selection_sort, k)
executar_pior("Selection",ordena.selection_sort, k)
print()
executar_medio("Merge",ordena.divide_and_conquer_sort, k)
executar_pior("Merge",ordena.divide_and_conquer_sort, k)
print()
executar_medio("Quick",ordena.quick_sort, k)
executar_pior("Quick",ordena.quick_sort, k, True) #a partir de 1000 a recursão atinge o limite