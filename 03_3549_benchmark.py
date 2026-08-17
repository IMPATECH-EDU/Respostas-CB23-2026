import AulasPraticas.AP_03_ordenacao as ap
import random as r
import time as t
import sys as s

s.setrecursionlimit(10000)
r.seed(1001)

def lista_media(n):
    '''
    Docstring for lista_media
    
    :param n: tamanho da lista que será retornada

    Cria uma lista com n elementos aleatórios
    '''
    lista = []
    for i in range(n):
        lista.append(r.randint(1,1000))
    return lista

def lista_pior(n):
    '''
    Docstring para lista_pior
    
    :param n: tamanho da lista que será retornada

    Essa função adiciona à lista que será retornada valores em ordem decrescente, 
    com a ideia de que dessa maneira será mais trabalhoso de ordená-la
    '''
    lista = []
    for i in range(n):
        lista.append(1000 - i)
    return lista

if __name__ == '__main__':
    n_values = [10, 50, 100, 500, 1000, 5000]
    k = 50

    print("Algoritmos\t||\tN\t||\tCenário\t\t||\tTempo médio")

    for n in n_values:
        tempos_s = 0
        tempos_d = 0
        tempos_q = 0
        for _ in range(k):
            lista = lista_media(n)

            start = t.perf_counter()
            ap.selection_sort(lista)
            end = t.perf_counter()
            tempos_s += end - start

            start = t.perf_counter()
            ap.divide_and_conquer_sort(lista)
            end = t.perf_counter()
            tempos_d += end - start

            start = t.perf_counter()
            ap.quick_sort(lista)
            end = t.perf_counter()
            tempos_q += end - start

        tempo_t = tempos_s + tempos_d + tempos_q

        tempos_s /= k
        tempos_d /= k
        tempos_q /= k

        print("-" * 80)
        print(f"Selection\t||\t{n}\t||\tlista média\t||\t{tempos_s:.10f}s")
        print(f"Div n conquer\t||\t{n}\t||\tlista média\t||\t{tempos_d:.10f}s")
        print(f"Quick sort\t||\t{n}\t||\tlista média\t||\t{tempos_q:.10f}s")
        #print(f"---\nTempo total: {tempo_t:.10f}s")

        tempos_s = 0
        tempos_d = 0
        tempos_q = 0
        for _ in range(k):
            tempos = {'select': [],
                      'divNconq': [],
                      'quick': []}
            
            lista = lista_pior(n)

            start = t.perf_counter()
            ap.selection_sort(lista)
            end = t.perf_counter()
            tempos_s += end - start

            start = t.perf_counter()
            ap.divide_and_conquer_sort(lista)
            end = t.perf_counter()
            tempos_d += end - start

            start = t.perf_counter()
            ap.quick_sort(lista)
            end = t.perf_counter()
            tempos_q += end - start
        
        tempo_t = tempos_s + tempos_d + tempos_q

        tempos_s /= k
        tempos_d /= k
        tempos_q /= k

        print("-" * 80)
        print(f"Selection\t||\t{n}\t||\tlista pior\t||\t{tempos_s:.10f}s")
        print(f"Div n conquer\t||\t{n}\t||\tlista pior\t||\t{tempos_d:.10f}s")
        print(f"Quick sort\t||\t{n}\t||\tlista pior\t||\t{tempos_q:.10f}s")
        #print(f"---\nTempo total: {tempo_t:.10f}s")