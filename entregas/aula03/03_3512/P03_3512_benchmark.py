import random
import time


def selection_sort(nums):
    for i in range(len(nums) - 1):
        min_index = i

        for j in range(i + 1, len(nums)):
            if nums[j] < nums[min_index]:
                min_index = j

        nums[i], nums[min_index] = nums[min_index], nums[i]

    return nums


def divide_and_conquer_sort(nums):
    if len(nums) <= 1:
        return nums

    meio = len(nums) // 2
    esquerda = divide_and_conquer_sort(nums[:meio])
    direita = divide_and_conquer_sort(nums[meio:])

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


def quick_sort(nums, inicio=0, fim=None):
    if fim is None:
        fim = len(nums) - 1

    if inicio >= fim:
        return nums

    pivo = nums[fim]
    posicao = inicio

    for i in range(inicio, fim):
        if nums[i] < pivo:
            nums[posicao], nums[i] = nums[i], nums[posicao]
            posicao += 1

    nums[posicao], nums[fim] = nums[fim], nums[posicao]

    quick_sort(nums, inicio, posicao - 1)
    quick_sort(nums, posicao + 1, fim)

    return nums

def lista_aleatoria(n):
    return [random.randint(0, 100000) for _ in range(n)]


def lista_pior_caso(n):
    return list(range(n, 0, -1))

def medir_tempo(algoritmo, lista):
    inicio = time.perf_counter()

    try:
        algoritmo(lista)
        fim = time.perf_counter()
        return fim - inicio
    except RecursionError:
        return None


def calcular_media(algoritmo, gerador, n, repeticoes):
    tempos = []

    for _ in range(repeticoes):
        lista = gerador(n)
        tempo = medir_tempo(algoritmo, lista)

        if tempo is None:
            return None

        tempos.append(tempo)

    return sum(tempos) / len(tempos)


algoritmos = {
    "Selection Sort": selection_sort,
    "Merge Sort": divide_and_conquer_sort,
    "Quick Sort": quick_sort
}

tamanhos = [100, 500, 1000, 5000]
repeticoes = 50

print(f"{'Algoritmo':<18} {'N':>6} {'Caso':<12} {'Tempo médio (s)':>18}")
print("-" * 60)

for nome, algoritmo in algoritmos.items():
    for n in tamanhos:
        for nome_caso, gerador in [
            ("Médio", lista_aleatoria),
            ("Pior", lista_pior_caso)
        ]:
            media = calcular_media(algoritmo, gerador, n, repeticoes)

            if media is None:
                resultado = "RecursionError"
            else:
                resultado = f"{media:.8f}"

            print(f"{nome:<18} {n:>6} {nome_caso:<12} {resultado:>18}")
