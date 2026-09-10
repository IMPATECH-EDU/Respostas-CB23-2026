import time
import random


TAMANHOS = [100, 500, 1000, 5000]
K = 50


def selection_sort_iterativo(nums):
    lista = nums.copy()

    for i in range(len(lista) - 1):
        menor = i

        for j in range(i + 1, len(lista)):
            if lista[j] < lista[menor]:
                menor = j

        lista[i], lista[menor] = lista[menor], lista[i]

    return lista


def merge(esquerda, direita):
    resultado = []

    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):

        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1

        else:
            resultado.append(direita[j])
            j += 1

    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])

    return resultado


def merge_sort_iterativo(nums):
    lista = nums.copy()
    tamanho = 1

    while tamanho < len(lista):

        resultado = []

        for inicio in range(0, len(lista), 2 * tamanho):

            meio = min(inicio + tamanho, len(lista))
            fim = min(inicio + 2 * tamanho, len(lista))

            esquerda = lista[inicio:meio]
            direita = lista[meio:fim]

            resultado.extend(merge(esquerda, direita))

        lista = resultado
        tamanho *= 2

    return lista


def particionar(lista, inicio, fim):
    pivo = lista[fim]

    i = inicio - 1

    for j in range(inicio, fim):

        if lista[j] <= pivo:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]

    lista[i + 1], lista[fim] = lista[fim], lista[i + 1]

    return i + 1


def quick_sort_iterativo(nums):
    lista = nums.copy()

    if len(lista) <= 1:
        return lista

    pilha = [(0, len(lista) - 1)]

    while pilha:

        inicio, fim = pilha.pop()

        if inicio < fim:

            posicao_pivo = particionar(
                lista,
                inicio,
                fim
            )
            pilha.append(
                (inicio, posicao_pivo - 1)
            )

            pilha.append(
                (posicao_pivo + 1, fim)
            )

    return lista


def gerar_caso_medio(n):
    return [
        random.randint(0, 100000)
        for _ in range(n)
    ]


def gerar_pior_caso(n):
    return list(range(n, 0, -1))


def medir_tempo(algoritmo, lista):
    inicio = time.perf_counter()

    algoritmo(lista)

    fim = time.perf_counter()

    return fim - inicio


def benchmark(algoritmo, gerador, n):
    tempos = []

    for _ in range(K):

        lista = gerador(n)

        tempo = medir_tempo(
            algoritmo,
            lista
        )

        tempos.append(tempo)

    return sum(tempos) / len(tempos)



def imprimir_resultado(
    nome_algoritmo,
    n,
    caso,
    media
):
    print(
        f"{nome_algoritmo:<20}"
        f"{n:<10}"
        f"{caso:<15}"
        f"{media:.6f} s"
    )


def main():

    algoritmos = [
        ("Selection Sort", selection_sort_iterativo),
        ("Merge Sort", merge_sort_iterativo),
        ("Quick Sort", quick_sort_iterativo)
    ]

    print("-" * 70)
    print("BENCHMARK DE ALGORITMOS DE ORDENAÇÃO")
    print("-" * 70)

    print(
        f"{'Algoritmo':<20}"
        f"{'N':<10}"
        f"{'Caso':<15}"
        f"{'Tempo médio'}"
    )

    print("-" * 70)

    for nome, algoritmo in algoritmos:

        for n in TAMANHOS:
            media = benchmark(
                algoritmo,
                gerar_caso_medio,
                n
            )

            imprimir_resultado(
                nome,
                n,
                "Caso Médio",
                media
            )
            media = benchmark(
                algoritmo,
                gerar_pior_caso,
                n
            )

            imprimir_resultado(
                nome,
                n,
                "Pior Caso",
                media
            )

    print("-" * 70)
    print("Benchmark finalizado.")
    print("-" * 70)


if __name__ == "__main__":
    main()