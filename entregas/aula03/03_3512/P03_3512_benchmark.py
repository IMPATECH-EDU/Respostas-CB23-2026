import random
import sys
import time

from AP_03_ordenacao import (
    selection_sort,
    divide_and_conquer_sort,
    quick_sort,
)


# O quick sort fornecido é recursivo e pode atingir profundidade O(N)
# no pior caso.
sys.setrecursionlimit(10000)


N_VALORES = [100, 500, 1000, 5000]
REPETICOES = 50


def caso_medio(n):
    """Gera uma lista aleatória para representar o caso médio."""
    return [random.randint(0, 100000) for _ in range(n)]


def pior_caso_selection(n):
    """Gera uma lista em ordem inversa para o Selection Sort."""
    return list(range(n, 0, -1))


def pior_caso_merge(n):
    """Gera uma lista em ordem inversa para o Merge Sort."""
    return list(range(n, 0, -1))


def pior_caso_quick(n):
    """
    Gera o pior caso para o Quick Sort fornecido.

    Como o algoritmo utiliza o último elemento como pivô, uma lista já
    ordenada provoca partições extremamente desbalanceadas.
    """
    return list(range(n))


def medir_tempo(algoritmo, dados):
    """Executa o algoritmo sobre uma cópia e retorna o tempo gasto."""
    copia = dados.copy()

    inicio = time.perf_counter()
    algoritmo(copia)
    fim = time.perf_counter()

    return fim - inicio


def tempo_medio(algoritmo, gerador, n, repeticoes=REPETICOES):
    """Calcula o tempo médio de várias execuções do algoritmo."""
    soma = 0.0

    for _ in range(repeticoes):
        dados = gerador(n)
        soma += medir_tempo(algoritmo, dados)

    return soma / repeticoes


def imprimir_resultados(nome, algoritmo, gerador_pior):
    """Executa e imprime os benchmarks de um algoritmo."""
    print()
    print(nome)
    print(
        f"{'N':>8} | "
        f"{'Caso médio (s)':>18} | "
        f"{'Pior caso (s)':>18}"
    )
    print("-" * 52)

    for n in N_VALORES:
        medio = tempo_medio(
            algoritmo,
            caso_medio,
            n,
        )

        pior = tempo_medio(
            algoritmo,
            gerador_pior,
            n,
        )

        print(
            f"{n:>8} | "
            f"{medio:>18.8f} | "
            f"{pior:>18.8f}"
        )


def main():
    print("BENCHMARK DE ALGORITMOS DE ORDENAÇÃO")

    imprimir_resultados(
        "Selection Sort",
        selection_sort,
        pior_caso_selection,
    )

    imprimir_resultados(
        "Merge Sort",
        divide_and_conquer_sort,
        pior_caso_merge,
    )

    imprimir_resultados(
        "Quick Sort",
        quick_sort,
        pior_caso_quick,
    )


if __name__ == "__main__":
    main()
