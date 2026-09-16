import random

from maze_builder import generate_maze, print_maze


def dfs_iterativo(m, n, maze, room=0, wall=1):

    visitados = set()
    pilha = [(0, 0)]

    direcoes = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while pilha:
        x, y = pilha.pop()

        if (x, y) in visitados:
            continue

        if not (0 <= x < m and 0 <= y < n):
            continue

        linha = 2 * x + 1
        coluna = 2 * y + 1

        if maze[linha][coluna] != room:
            continue

        visitados.add((x, y))

        for dx, dy in direcoes:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < m and 0 <= ny < n:
                if (nx, ny) not in visitados:
                    pilha.append((nx, ny))

    return visitados


def encontrar_queijo(maze, room=0, cheese='.'):

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == cheese:
                return i, j

    raise ValueError("O queijo não foi encontrado no labirinto.")


def caminho_dfs(maze, inicio=(1, 1), room=0, cheese='.'):
    inicio_linha, inicio_coluna = inicio

    if not (
        0 <= inicio_linha < len(maze)
        and 0 <= inicio_coluna < len(maze[0])
    ):
        raise ValueError("A posição inicial está fora do labirinto.")

    if maze[inicio_linha][inicio_coluna] != room:
        raise ValueError(
            "A posição inicial (1, 1) não é uma passagem válida."
        )

    direcoes = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    pilha = [inicio]
    visitados = {inicio}

    anterior = {}

    objetivo = encontrar_queijo(maze, room, cheese)

    if inicio == objetivo:
        return [inicio]

    while pilha:

        atual = pilha.pop()

        if atual == objetivo:
            break

        linha, coluna = atual

        for dl, dc in direcoes:

            nova_linha = linha + dl
            nova_coluna = coluna + dc

            vizinho = (nova_linha, nova_coluna)

            if not (
                0 <= nova_linha < len(maze)
                and 0 <= nova_coluna < len(maze[0])
            ):
                continue

            if vizinho in visitados:
                continue

            valor = maze[nova_linha][nova_coluna]

            if valor != room and valor != cheese:
                continue

            visitados.add(vizinho)
            anterior[vizinho] = atual
            pilha.append(vizinho)

    if objetivo not in visitados:
        raise ValueError("Não existe caminho até o queijo.")

    caminho = []
    atual = objetivo

    while atual != inicio:
        caminho.append(atual)
        atual = anterior[atual]

    caminho.append(inicio)
    caminho.reverse()

    return caminho


def exibir_labirinto_com_caminho(
    maze,
    caminho,
    room=0,
    wall=1,
    cheese='.'
):
    """
    Exibe o labirinto.

    O símbolo '*' representa o caminho.


    Complexidade:
        O(L * C), porque percorre a matriz do labirinto.
    """

    caminho_set = set(caminho)

    for i, linha in enumerate(maze):
        texto = []

        for j, valor in enumerate(linha):

            posicao = (i, j)

            if valor == cheese:
                texto.append(str(cheese))

            elif posicao in caminho_set:
                texto.append("*")

            elif valor == room:
                texto.append(" ")

            elif valor == wall:
                texto.append("W")

            else:
                texto.append(str(valor))

        print(" ".join(texto))


def main():
    """
    Gera um labirinto, executa DFS iterativo, encontra o queijo
    e exibe o caminho.
    """

    m = 10
    n = 14

    random.seed(10110)

    room = 0
    wall = 1
    cheese = "."

    maze = generate_maze(
        m,
        n,
        room,
        wall,
        cheese
    )

    print("LABIRINTO")
    print_maze(maze)

    # Questão 1
    visitados = dfs_iterativo(
        m,
        n,
        maze,
        room,
        wall
    )

    print()
    print("Quantidade de salas visitadas pelo DFS iterativo:", len(visitados))

    # Questão 2
    caminho = caminho_dfs(
        maze,
        inicio=(1, 1),
        room=room,
        cheese=cheese
    )

    print()
    print("Caminho encontrado:")
    print(caminho)

    print()
    print("LABIRINTO COM CAMINHO")
    exibir_labirinto_com_caminho(
        maze,
        caminho,
        room,
        wall,
        cheese
    )


if __name__ == "__main__":
    main()