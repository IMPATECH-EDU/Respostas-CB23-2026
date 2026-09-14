import time
import random

try:
    import AP_03_ordenacao as algos
except ImportError:
    pass

def gerar_caso_medio(n):
    return [random.randint(0, 10000) for _ in range(n)]

def gerar_pior_caso(n):
    return list(range(n, 0, -1))

def medir_tempo(funcao_sort, dados, k_repeticoes=30):
    tempo_total = 0.0
    for _ in range(k_repeticoes):
        dados_copia = dados.copy()
        inicio = time.perf_counter()
        funcao_sort(dados_copia)
        fim = time.perf_counter()
        tempo_total += (fim - inicio)
    return tempo_total / k_repeticoes

def executar_benchmark():
    tamanhos_n = [100, 500, 1000, 2000]
    k_repeticoes = 30

    algoritmos = {}
    if 'algos' in globals():
        for nome in dir(algos):
            obj = getattr(algos, nome)
            if callable(obj) and not nome.startswith("_"):
                algoritmos[nome] = obj

    if not algoritmos:
        print("Aviso: Modulo AP_03_ordenacao nao encontrado no mesmo diretorio.")
        return

    print("=" * 70)
    print(f"{'Algoritmo':<20} | {'N':<6} | {'Cenario':<12} | {'Tempo Medio (s)':<15}")
    print("=" * 70)

    for nome_alg, func in algoritmos.items():
        for n in tamanhos_n:
            dados_medio = gerar_caso_medio(n)
            t_medio = medir_tempo(func, dados_medio, k_repeticoes)
            print(f"{nome_alg:<20} | {n:<6} | {'Caso Medio':<12} | {t_medio:.6f} s")

            dados_pior = gerar_pior_caso(n)
            t_pior = medir_tempo(func, dados_pior, k_repeticoes)
            print(f"{nome_alg:<20} | {n:<6} | {'Pior Caso':<12} | {t_pior:.6f} s")
            print("-" * 70)

if __name__ == "__main__":
    executar_benchmark()

