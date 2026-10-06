def dfs_iterativo(labirinto, inicio):
    """
    Realiza uma busca em profundidade (DFS) de forma iterativa.

    A busca utiliza uma pilha para armazenar as posições que ainda
    precisam ser visitadas.

    Args:
        labirinto: matriz representando o labirinto.
        inicio: tupla (linha, coluna) indicando a posição inicial.

    Returns:
        Um dicionário contendo, para cada posição visitada, a posição
        anterior utilizada para chegar até ela.
    """

    linhas = len(labirinto)
    colunas = len(labirinto[0])

    pilha = [inicio]
    visitados = {inicio}

    # Guarda de onde cada posição foi alcançada.
    anteriores = {inicio: None}

    # Movimentos possíveis: cima, baixo, esquerda e direita.
    movimentos = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while pilha:
        atual = pilha.pop()

        linha, coluna = atual

        # Verifica os vizinhos da posição atual.
        for dl, dc in movimentos:
            nova_linha = linha + dl
            nova_coluna = coluna + dc

            vizinho = (nova_linha, nova_coluna)

            # Verifica se a posição está dentro do labirinto.
            if not (0 <= nova_linha < linhas and
                    0 <= nova_coluna < colunas):
                continue

            # Ignora paredes.
            if labirinto[nova_linha][nova_coluna] == "#":
                continue

            # Ignora posições já visitadas.
            if vizinho in visitados:
                continue

            visitados.add(vizinho)
            anteriores[vizinho] = atual
            pilha.append(vizinho)

    return anteriores


def encontrar_queijo(labirinto):
    """
    Procura a posição do queijo no labirinto.

    O queijo é representado pelo caractere 'Q'.

    Returns:
        Tupla (linha, coluna) da posição do queijo.

    Raises:
        ValueError: caso o queijo não seja encontrado.
    """

    for linha in range(len(labirinto)):
        for coluna in range(len(labirinto[linha])):
            if labirinto[linha][coluna] == "Q":
                return linha, coluna

    raise ValueError("O queijo não foi encontrado no labirinto.")


def reconstruir_caminho(anteriores, inicio, objetivo):
    """
    Reconstrói o caminho entre o início e o objetivo.

    Args:
        anteriores: dicionário produzido pela busca.
        inicio: posição inicial.
        objetivo: posição final.

    Returns:
        Lista contendo as posições do caminho.
        Retorna None caso não exista caminho.
    """

    if objetivo not in anteriores:
        return None

    caminho = []
    atual = objetivo

    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]

    caminho.reverse()

    if caminho[0] != inicio:
        return None

    return caminho


def encontrar_caminho(labirinto, inicio=(1, 1)):
    """
    Encontra um caminho da posição inicial até o queijo.

    Utiliza DFS iterativo para explorar o labirinto.
    """

    objetivo = encontrar_queijo(labirinto)

    anteriores = dfs_iterativo(labirinto, inicio)

    return reconstruir_caminho(
        anteriores,
        inicio,
        objetivo
    )


def exibir_labirinto(labirinto, caminho=None):
    """
    Exibe o labirinto no terminal.

    As posições pertencentes ao caminho são representadas por '*'.
    A posição inicial continua sendo 'S' e o queijo continua sendo 'Q'.
    """

    if caminho is None:
        caminho = []

    caminho = set(caminho)

    for linha in range(len(labirinto)):
        texto = ""

        for coluna in range(len(labirinto[linha])):
            posicao = (linha, coluna)

            if posicao == (1, 1):
                texto += "S"
            elif labirinto[linha][coluna] == "Q":
                texto += "Q"
            elif posicao in caminho:
                texto += "*"
            else:
                texto += labirinto[linha][coluna]

        print(texto)


def resolver_labirinto(labirinto):
    """
    Encontra e exibe o caminho do início até o queijo.
    """

    inicio = (1, 1)

    caminho = encontrar_caminho(
        labirinto,
        inicio
    )

    print("Labirinto:")

    exibir_labirinto(labirinto)

    print()

    if caminho is None:
        print("Não existe caminho até o queijo.")
        return

    print("Caminho encontrado:")

    exibir_labirinto(
        labirinto,
        caminho
    )

    print()
    print("Posições do caminho:")
    print(caminho)


def main():
    """
    Executa um exemplo de labirinto.
    """

    labirinto = [
        "#######",
        "#     #",
        "# ### #",
        "#   # #",
        "### # #",
        "#     #",
        "####Q##"
    ]

    resolver_labirinto(labirinto)


if __name__ == "__main__":
    main()
