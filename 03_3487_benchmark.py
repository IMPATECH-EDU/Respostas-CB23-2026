import AP_03_ordenacao as ord
import time
import random
import sys
sys.setrecursionlimit(10000)
while True:

   try:
       tamanho=int(input("Digite o tamanho da lista desodernada original que quer gerar (Natural<=1024), ela será dobrada e processada pelo Benchmark até o caso limite: "))
       if tamanho<1024 and tamanho>0:
           break
       else:
           print("Digite um inteiro maior que 0 e menor que 1025")
   except (ValueError):
       print("Tipo de instância inapropriada, digite um Natural")

while True:

   try:
       Ciclos=int(input("Digite o número de ciclos de geração/ordenação de listas randomicas (Natural<=300), a fim de tornar a média tão bem estatisticamente distribuida quanto queira: "))
       if Ciclos<1024 and Ciclos>0:
           break
       else:
           print("Digite um inteiro maior que 0 e menor que 301")
   except (ValueError):
       print("Tipo de instância inapropriada, digite um Natural")


def criarlistarandom(tamanho):
        listan=[random.getrandbits(64) for _ in range(tamanho)]
        return listan  

def benchmark(tamanho, Ciclos):  
    totalselectrand=0
    totalselectworst=0
    totaldacsrand=0
    totaldacsworst=0
    totalquickrand=0
    totalquickworst=0
    for _ in range(Ciclos):  
        l=criarlistarandom(tamanho)
        m = [l.copy() for _ in range(6)]


        b=time.perf_counter()
        ord.selection_sort(m[1])
        a=time.perf_counter()
        totalselectrand+=(a-b)
        a,b=0,0
        
        m[2].sort(reverse=True)
        b=time.perf_counter()
        ord.selection_sort(m[2])
        a=time.perf_counter()
        totalselectworst+=(a-b)
        a,b=0,0
        
        b=time.perf_counter()
        ord.divide_and_conquer_sort(m[3])
        a=time.perf_counter()
        totaldacsrand+=(a-b)
        a,b=0,0

        m[4].sort()
        w=[]
        metade = tamanho // 2
        for k in range(metade):
            w.append(m[4][k])
            w.append(m[4][k + metade])
        b=time.perf_counter()
        ord.divide_and_conquer_sort(w)
        a=time.perf_counter()
        totaldacsworst+=(a-b)
        a,b=0,0

        b=time.perf_counter()
        ord.quick_sort(m[5])
        a=time.perf_counter()
        totalquickrand+=(a-b)
        a,b=0,0
    
        m[0].sort()
        b=time.perf_counter()
        ord.quick_sort(m[0])
        a=time.perf_counter()
        totalquickworst+=(a-b)
        a,b=0,0
    
    





    print(" Selection_sort ", end=""), print(f"          {tamanho}  ", end=""), print(f" Caso médio ", end=""), print(f" {(totalselectrand/Ciclos):.6f} segundo(s)  ")
    print(" Selection_sort ", end=""), print(f"          {tamanho}  ", end=""), print(f" Pior caso  ", end=""),  print(f" {(totalselectworst/Ciclos):.6f} segundo(s) ")
    print(" Divide_and_conquer_sort ", end=""), print(f" {tamanho}  ", end=""), print(f" Caso médio ", end=""), print(f" {(totaldacsrand/Ciclos):.6f} segundo(s)")
    print(" Divide_and_conquer_sort ", end=""), print(f" {tamanho}  ", end=""), print(f" Pior caso  ", end=""),  print(f" {(totaldacsworst/Ciclos):.6f} segundo(s) ")
    print(" Quick_sort ", end=""), print(f"              {tamanho}  ", end=""), print(f" Caso médio ", end=""), print(f" {(totalquickrand/Ciclos):.6f} segundo(s) ")
    print(" Quick_sort ", end=""), print(f"              {tamanho}  ", end=""), print(f" Pior caso  ", end=""),  print(f" {(totalquickworst/Ciclos):.6f} segundo(s)")

print("  Algoritmo  ", end=""), print("             N  ", end=""), print("  Cenário  ", end=""),print("  Tempo médio  ", end=""),print()

while tamanho<=1024:
    benchmark(tamanho, Ciclos)
    tamanho+=(tamanho)