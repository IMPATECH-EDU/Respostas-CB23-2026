# python 3

# Selection Sort
def selection_sort(nums):
    """Ordena a lista em ordem crescente usando o algoritmo Selection Sort.

    A cada iteração, encontra o menor elemento do restante não ordenado
    da lista e o troca de posição com o primeiro elemento dessa região.

    Args:
        nums (list): Lista de elementos comparáveis a ser ordenada.
            A lista é modificada em-lugar (in-place).

    Returns:
        list: A própria lista `nums`, agora ordenada.
    """

    def argmin(NX):
        """Retorna o índice e o valor do menor elemento de `NX`.

        Args:
            NX (list): Sublista onde a busca será feita.

        Returns:
            tuple[int, Any]: Índice (relativo a `NX`) e valor do menor elemento.
        """
        min_index = 0
        min_x = NX[0]
        for count, x in enumerate(NX):
            if x < min_x:
                min_index = count
                min_x = x
        return min_index, min_x

    for i in range(len(nums) - 1):
        idx, _ = argmin(nums[i:])
        nums[i], nums[idx + i] = nums[idx + i], nums[i]
    return nums


# Merge Sort
def divide_and_conquer_sort(nums):
    """Ordena a lista em ordem crescente usando o algoritmo Merge Sort.

    Divide recursivamente a lista ao meio até restarem sublistas de um
    único elemento e depois as intercala (merge) em ordem crescente.

    Args:
        nums (list): Lista de elementos comparáveis a ser ordenada.
            Não é modificada em-lugar; uma nova lista ordenada é retornada.

    Returns:
        list: Nova lista contendo os elementos de `nums` em ordem crescente.
    """
    if len(nums) > 1:
        n1 = divide_and_conquer_sort(nums[: len(nums) // 2])
        n2 = divide_and_conquer_sort(nums[len(nums) // 2 :])
    else:
        return nums
    orded = []
    while len(n1) > 0 and len(n2) > 0:
        if n1[0] <= n2[0]:
            orded.append(n1.pop(0))
        else:
            orded.append(n2.pop(0))
    orded += n1 + n2
    return orded


# Quick Sort
def quick_sort(nums, b=0, u=None):
    """Ordena a lista em ordem crescente usando o algoritmo Quick Sort.

    Utiliza o último elemento do intervalo [b, u] como pivô, particiona
    a lista em torno dele e ordena recursivamente as partições resultantes.

    Args:
        nums (list): Lista de elementos comparáveis a ser ordenada.
            A lista é modificada em-lugar (in-place).
        b (int, opcional): Índice inicial do intervalo a ordenar. Padrão: 0.
        u (int | None, opcional): Índice final do intervalo a ordenar.
            Se None, é definido como `len(nums) - 1`. Padrão: None.

    Returns:
        list | None: A lista `nums` ordenada quando a chamada corresponde
            ao intervalo completo; None nas chamadas recursivas internas
            em que o intervalo já está ordenado (`b >= u`).
    """
    if u is None:
        u = len(nums) - 1
    if b >= u:
        return
    pb = b
    pivot = nums[u]
    for i in range(b, u):
        if pivot > nums[i]:
            nums[pb], nums[i] = nums[i], nums[pb]
            pb += 1
    nums[pb], nums[u] = nums[u], nums[pb]
    quick_sort(nums, b, pb - 1)
    quick_sort(nums, pb + 1, u)
    return nums


if __name__ == "__main__":
    print("-" * 64)
    print(f"{'Test 1':^64}")
    print("-" * 64)
    X = [5, 6, 2, 4, 6, 1, 2, 9, -1, -2, -3, 10, 3, 4, 5, 0, 28, -10]
    print(selection_sort(X.copy()))
    print(divide_and_conquer_sort(X.copy()))
    print(quick_sort(X.copy()))
    print("--")
    print(X)
