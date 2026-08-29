from AP_03_ordenacao import selection_sort, divide_and_conquer_sort, quick_sort
import time
import random 
#funções auxiliares:
def aleatoria(n):
    ''' Gera uma lista de n elementos aleatórios entre 0 e 10000.
    '''
    return [random.randint(0,10000) for a in range(n)] 
def desfavoravel(n):
    '''Gera listas invertidas/desfavoráveis (pior caso) para múltiplos valores de N '''
    return list(range(n,0,-1))
def tempo(alg,contas,k=50):
    '''Vejo o tempo com o time.perfcounter() para o algoritmo alg, com os dados contas, repetindo k vezes e retornando
    a média aritmética do tempo gasto.'''
    soma = 0
    for i in range(k):
        inicio = time.perf_counter() 
        dados = contas.copy() 
        alg(dados) 
        fim = time.perf_counter() 
        media = (fim-inicio)
        soma += media 
    return soma/k  

# tabela 
algoritmos = {'Selection Sort': selection_sort, 'Merge Sort': divide_and_conquer_sort,
              'Quick Sort': quick_sort} 
cenario = {'Lista Aleatória': aleatoria, 'Lista Desfavorável/Invertida': desfavoravel}
num = [100, 500, 1000, 5000] 
tempo_total = {'Tempo Médio (s)': tempo} 

resultados = [] 

print(f"{'algoritmo':<18} | {'tamanho (N)':<11} | {'cenário':<28} | {'tempo médio (s)':<15}")
print("-" * 80)

for nome_cenario, func_geradora in cenario.items():
    for n in num:
        dados = func_geradora(n)
        
        for nome_alg, func_alg in algoritmos.items():
            try:
                tempo_medio = tempo(func_alg, dados, k=50)
                print(f"{nome_alg:<18} | {n:<11} | {nome_cenario:<28} | {tempo_medio:<15.6f}")
            except Exception:
                print(f"{nome_alg:<18} | {n:<11} | {nome_cenario:<28} | {'limite esgotado':<15}")
