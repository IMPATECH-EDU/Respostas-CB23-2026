import AulasPraticas.AP_03_ordenacao as ap3
import sys
import random
import time
sys.setrecursionlimit(10**6)



def avg_case(N):
    my_list = []
    og = [x for x in range(N)]
    while len(og):
        random_index = random.randint(0,len(og)-1)
        my_list.append(og[random_index])
        og[random_index], og[-1] = og[-1], og[random_index]
        og.pop(-1)
    return my_list

def worst_case(N):
    return [x for x in range(N)]

def prf_algo(sort_algo,N,k,worst = False):
    times = []
    for _ in range(k):
        my_list = avg_case(N) if not worst else worst_case(N)
        start_t = time.perf_counter()
        sort_algo(my_list)
        end_t = time.perf_counter()
        times.append(end_t - start_t)
    return sum(times)/k

tempos = []
nomes = []
testes = [1000,5000,10000]
for i in testes:
    for j in [ap3.selection_sort,ap3.divide_and_conquer_sort,ap3.quick_sort]:
        tempos.append(prf_algo(j,i,50))
        tempos.append(prf_algo(j,i,50,True))
        nomes.append(j.__name__)
        nomes.append(j.__name__ +"_worst")


    

for _ in range(len(tempos)):
    if _ % 6 == 0:
        print(f"{'Método':<25} {testes[_//6]}{' testes':<20} Tempo (s)")
        print("-" * 60)
    print(f"{nomes[_] :<50} {tempos[_]:.6f}")

