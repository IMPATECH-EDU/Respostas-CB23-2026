import random

from maze_builder import print_maze


def generate_maze_iterativo(m, n, room=' ', wall='W', cheese='*'):
    """
    Gera um labirinto perfeito usando DFS iterativa com backtracking.

    A pilha substitui as chamadas recursivas utilizadas na implementação
    original de maze_builder.py.
    """
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    direcoes = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    # Começa na sala lógica (0, 0), correspondente a (1, 1) na matriz.
    maze[1][1] = room
    pilha = [(0, 0)]

    while pilha:
        x, y = pilha[-1]

        vizinhos = []

        for dx, dy in direcoes:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < m and 0 <= ny < n:
                linha = 2 * nx + 1
                coluna = 2 * ny + 1

                # Uma sala ainda com valor de parede ainda não foi visitada.
                if maze[linha][coluna] == wall:
                    vizinhos.append((nx, ny, dx, dy))

        if vizinhos:
            nx, ny, dx, dy = random.choice(vizinhos)

            # Derruba a parede entre a sala atual e a próxima.
            maze[2 * x + 1 + dx][2 * y + 1 + dy] = room

            # Marca a nova sala como aberta.
            maze[2 * nx + 1][2 * ny + 1] = room

            pilha.append((nx, ny))

        else:
            # Não há vizinhos não visitados: retrocede.
            pilha.pop()

    # Coloca o queijo em uma sala aleatória diferente da posição inicial.
    while True:
        x = random.randrange(m)
        y = random.randrange(n)

        linha = 2 * x + 1
        coluna = 2 * y + 1

        if (linha, coluna) != (1, 1):
            maze[linha][coluna] = cheese
            break

    return maze


def encontrar_queijo(maze, cheese='*'):
    """Retorna a posição do queijo no labirinto."""
    for linha in range(len(maze)):
        for coluna in range(len(maze[linha])):
            if maze[linha][coluna] == cheese:
                return linha, coluna

    raise ValueError("Queijo não encontrado no labirinto.")


def encontrar_caminho_dfs(maze, inicio=(1, 1), wall='W', cheese='*'):
    """
    Encontra iterativamente, usando DFS, um caminho do início até o queijo.

    Retorna uma lista de posições pertencentes ao caminho.
    """
    objetivo = encontrar_queijo(maze, cheese)

    pilha = [inicio]
    visitados = {inicio}

    # Guarda de onde cada posição foi alcançada para reconstruir o caminho.
    anterior = {}

    direcoes = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    while pilha:
        atual = pilha.pop()

        if atual == objetivo:
            break

        linha, coluna = atual

        for dl, dc in direcoes:
            nova_linha = linha + dl
            nova_coluna = coluna + dc

            if not (
                0 <= nova_linha < len(maze)
                and 0 <= nova_coluna < len(maze[0])
            ):
                continue

            proxima = (nova_linha, nova_coluna)

            if proxima in visitados:
                continue

            # É possível caminhar por qualquer posição que não seja parede.
            if maze[nova_linha][nova_coluna] == wall:
                continue

            visitados.add(proxima)
            anterior[proxima] = atual
            pilha.append(proxima)

    if objetivo not in visitados:
        raise ValueError("Não foi possível encontrar um caminho até o queijo.")

    # Reconstrói o caminho do queijo até o início.
    caminho = []
    atual = objetivo

    while atual != inicio:
        caminho.append(atual)
        atual = anterior[atual]

    caminho.append(inicio)
    caminho.reverse()

    return caminho


def exibir_caminho(
    maze,
    caminho,
    inicio=(1, 1),
    cheese='*',
    marcador='.',
):
    """Exibe uma cópia do labirinto destacando o caminho encontrado."""
    exibicao = [linha.copy() for linha in maze]

    objetivo = encontrar_queijo(maze, cheese)

    for linha, coluna in caminho:
        if (linha, coluna) != inicio and (linha, coluna) != objetivo:
            exibicao[linha][coluna] = marcador

    # Marca explicitamente a posição inicial.
    exibicao[inicio[0]][inicio[1]] = 'S'

    print_maze(exibicao)


def main():
    m = 10
    n = 14

    random.seed(10110)

    maze = generate_maze_iterativo(
        m,
        n,
        room=' ',
        wall='W',
        cheese='*',
    )

    print("LABIRINTO GERADO")
    print()
    print_maze(maze)

    caminho = encontrar_caminho_dfs(
        maze,
        inicio=(1, 1),
        wall='W',
        cheese='*',
    )

    print()
    print("CAMINHO DE (1, 1) ATÉ O QUEIJO")
    print()

    exibir_caminho(
        maze,
        caminho,
        inicio=(1, 1),
        cheese='*',
        marcador='.',
    )

    print()
    print(f"Tamanho do caminho: {len(caminho)} posições")


if __name__ == "__main__":
    main()
