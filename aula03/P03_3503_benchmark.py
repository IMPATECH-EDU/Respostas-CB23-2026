import AulasPraticas.AP_03_ordenacao as ap3
import sys
import random
import time

sys.setrecursionlimit(10**5)

#cria uma lista aleatória com nums de 1 até n
def caso_medio(N):
    lista = []
    lista_inteira = [i for i in range(N)]
    while len(lista_inteira):
        indice_p_tirar = random.randint(0,len(lista_inteira)-1)
        lista.append(lista_inteira[indice_p_tirar])
        lista_inteira[indice_p_tirar],lista_inteira[-1] = lista_inteira[-1],lista_inteira[indice_p_tirar]
        lista_inteira.pop(-1)
    return lista

def pior_caso_quick(N):
    return [i for i in range(N)][::-1] 
#lista ao contrário, faz com que fique O(n²), pois o pivo é o último
#entao chama a função recursiva só com 1 elemento a menos


#a selection_sort sempre varre toda a lista em todos os passos
#então sempre tem a mesma complexidade n + (n-1) + ... + 1 = (n²+n)/2 = O(n²)
#NAO TEM PIOR CASO!!!!!!!!!!!!!

#a divide_and_conquer sempre varre da mesma maneira, independente dos elementos da lista
#então sempre tem a mesma complexidade nlog(n)
#NÃO TEM PIOR CASO!!!!!!!!!!!!!


def tempo(algoritmo,N,k,pior = None):
    #ideia do monitor henrique de colocar os 3 algoritmos numa função só
    tempos = []
    for i in range(k):
        lista = pior(N) if pior else caso_medio(N)
        #no caso do quick, vai pegar a lista invertida para o pior caso
        tempo_inicio = time.perf_counter()
        algoritmo(lista)
        tempo_final = time.perf_counter()
        tempos.append(tempo_final - tempo_inicio)
    return sum(tempos)/k

print("-" * 64)
print("SELECTION SORT")
print("-" * 64)
print("(sem pior caso - explicação nos comentários)")
print("-" * 32)
print("N \t Cenário \t \tTempo Médio")
print(f"100 \t médio \t \t \t {tempo(ap3.selection_sort,100,50)}ms")
print(f"500 \t médio \t \t \t {tempo(ap3.selection_sort,500,50)}ms")
print(f"1000 \t médio \t \t \t {tempo(ap3.selection_sort,1000,50)}ms")
print(f"5000 \t médio \t \t \t {tempo(ap3.selection_sort,5000,50)}ms")
print("-" * 64)
print("DIVIDE AND CONQUER SORT")
print("-" * 64)
print("(sem pior caso - explicação nos comentários)")
print("-" * 32)
print("N \t Cenário \t \tTempo Médio")
print(f"100 \t médio \t \t \t {tempo(ap3.divide_and_conquer_sort,100,50)}ms")
print(f"500 \t médio \t \t \t {tempo(ap3.divide_and_conquer_sort,500,50)}ms")
print(f"1000 \t médio \t \t \t {tempo(ap3.divide_and_conquer_sort,1000,50)}ms")
print(f"5000 \t médio \t \t \t {tempo(ap3.divide_and_conquer_sort,5000,50)}ms")
print("-" * 64)
print("QUICK SORT")
print("-" * 64)
print("N \t Cenário \t \tTempo Médio")
print(f"100 \t médio \t \t \t {tempo(ap3.quick_sort,100,50)}ms")
print(f"100 \t 'pior' \t \t {tempo(ap3.quick_sort,100,50,pior_caso_quick)}ms")
print(f"500 \t médio \t \t \t {tempo(ap3.quick_sort,500,50)}ms")
print(f"500 \t 'pior' \t \t {tempo(ap3.quick_sort,500,50,pior_caso_quick)}ms")
print(f"1000 \t médio \t \t \t {tempo(ap3.quick_sort,1000,50)}ms")
print(f"1000 \t 'pior' \t \t {tempo(ap3.quick_sort,1000,50,pior_caso_quick)}ms")
print(f"5000 \t médio \t \t \t {tempo(ap3.quick_sort,5000,50)}ms")
print(f"5000 \t 'pior' \t \t {tempo(ap3.quick_sort,5000,50,pior_caso_quick)}ms")
print("-" * 64)