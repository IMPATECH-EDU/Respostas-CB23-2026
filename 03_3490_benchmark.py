import AP_03_ordenacao as ap
import random
import time
import sys

sys.setrecursionlimit(10**6)

#função para uma lista aleatoria de 1 a n
def lista_med(n):
    lista=[]  #lista de 1 ate n, onde iremos reordená-los de forma aleatória
    for i in range(1, n+1):
        lista.append(i)
    mlista=[]
    while len(lista)!=0:
        ind=random.randint(0, len(lista)-1)
        mlista.append(lista[ind])
        lista[ind]=lista[-1]
        lista[-1]=lista[ind]
        del lista[-1]
    return mlista

#função que faz uma lista ordenada de 1 ate n, e depois coloca-na na ordem inversa
def lista_invers(n):
    lista=[]
    for i in range(1, n+1):
        lista.append(i)
    return lista[::-1]

#lista com os n's que iremos testar os algoritmos
casos=[10, 50, 100, 500, 1000]

#agora devo fazer a parte em que testo cada um dos algoritmos de ordenação e faço a tabela para ser printada no terminal.

#laço para fazer o teste com os casos escolhidos na lista "casos"

#Algoritmo "selection sort"
tempo_medio=0
tempo_pior=0

#Algoritmo "quick sort"
t_medio=0
t_pior=0

#Algoritmo divide and conquer sort
T_medio=0
T_pior=0

#tabela dos resultados
tabela={}

#parte em que faço a análise com o algoritmo selection sort
for i in casos:
    for _ in range(50):   #testo 50 vezes o algoritmo com o caso "i", isto é, a lista com "i" itens
        l=lista_med(i)
        k=lista_invers(i)
        ini = time.perf_counter()         #inicio a contagem do tempo
        ap.selection_sort(l)
        end = time.perf_counter()         #finalizo a contagem do tempo

        a= time.perf_counter()
        ap.quick_sort(l)
        b= time.perf_counter()

        n= time.perf_counter()
        ap.divide_and_conquer_sort(l)
        m= time.perf_counter()

#faço o mesmo raciocínio, mas agora com a função lista_invers, para ser o pior caso
        star= time.perf_counter()
        ap.selection_sort(k)
        fim= time.perf_counter()

        r= time.perf_counter()
        ap.quick_sort(k)
        s= time.perf_counter()

        x= time.perf_counter()
        ap.divide_and_conquer_sort(k)
        y= time.perf_counter()
#calculo os tempos de cada caso executado pelo algoritmo
        time_pior=fim-star
        time_medio=end-ini

#calculo os tempos medios em cada caso
        tempo_medio+=time_medio
        tempo_pior+=time_pior
        t_medio+=(b-a)/50
        t_pior+=(s-r)/50
        T_medio+=(m-n)/50
        T_pior+=(y-x)/50
#calculo os tempos médio de execução do algoritmo com i itens feito 50 vezes no caso medio e pior
    temp_med_medio=tempo_medio/50
    temp_med_pior=tempo_pior/50


#adiciono os resultados para esse i da lista casos no dict tabela, e, após isso, reinicio os tempos totais
    tabela[(" Selection Sort ",i)]=[["Médio", temp_med_medio], ["Pior", temp_med_pior]]
    tabela[("   Quick Sort   ",i)]=[["Médio", t_medio], ["Pior", t_pior]]
    tabela[("Divide & Conquer",i)]=[["Médio", T_medio], ["Pior", T_pior]]
    tempo_medio=0
    tempo_pior=0
    t_medio=0
    t_pior=0
    T_medio=0
    T_pior=0

    continue


print("—"*69,"\n|      Algoritmo      |   Caso    |     N    |    Tempo médio (s)   |")
for chave, valor in tabela.items():
    if chave[1]<99:
        casa=f"    {chave[1]}    "
    elif chave[1]<999:
        casa=f"    {chave[1]}   "
    else:
        casa=f"   {chave[1]}   "
    print("—"*69,f"\n|  {chave[0]}   |   {valor[0][0]}   |{casa}|{valor[0][1]}", end="")#fim do laço dos resultados dos casos medios

for key, valo in tabela.items():
    if key[1]<99:
        cas=f"    {key[1]}    "
    elif key[1]<999:
        cas=f"    {key[1]}   "
    else:
        cas=f"   {key[1]}   "
    print("—"*69,f"\n|  {key[0]}   |   {valo[1][0]}    |{cas}|{valo[1][1]}")
print("\nCada algoritmo foi rodado 50 vezes por caso e lista.")