import random


def dfs_iterativo(maze, m, n, room=0, wall=1):
    """Gera o labirinto usando busca em profundidade iterativa.

    A pilha substitui a recursão utilizada no código original.
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # A pilha começa com a primeira sala da grade lógica.
    stack = [(0, 0)]

    maze[1][1] = room

    while stack:
        x, y = stack[-1]

        # Embaralha as direções para produzir labirintos diferentes.
        random.shuffle(directions)

        encontrou_vizinho = False

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < m
                and 0 <= ny < n
                and maze[2 * nx + 1][2 * ny + 1] == wall
            ):
                # Derruba a parede entre as duas salas.
                maze[2 * x + 1 + dx][2 * y + 1 + dy] = room

                # Abre a nova sala.
                maze[2 * nx + 1][2 * ny + 1] = room

                # Continua a DFS a partir da nova sala.
                stack.append((nx, ny))

                encontrou_vizinho = True
                break

        # Se não houver vizinhos não visitados, faz backtracking.
        if not encontrou_vizinho:
            stack.pop()


def generate_maze(m, n, room=0, wall=1, cheese="."):
    """Gera um labirinto perfeito de m x n células.

    A geração utiliza uma DFS iterativa.
    """
    # Inicializa a matriz expandida com paredes.
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    # Gera as passagens utilizando DFS iterativa.
    dfs_iterativo(maze, m, n, room, wall)

    # Guarda as posições das salas para escolher onde colocar o queijo.
    salas = []

    for i in range(m):
        for j in range(n):
            salas.append((2 * i + 1, 2 * j + 1))

    # Escolhe uma sala aleatoriamente.
    i, j = random.choice(salas)
    maze[i][j] = cheese

    return maze


def encontrar_caminho(maze, cheese="*", wall="W"):
    """Encontra um caminho de (1, 1) até o queijo usando DFS iterativa.

    Retorna uma lista com as posições do caminho, começando em (1, 1)
    e terminando na posição do queijo.

    Retorna None caso o queijo não possa ser alcançado.
    """
    linhas = len(maze)
    colunas = len(maze[0])

    # Posição inicial exigida pelo enunciado.
    inicio = (1, 1)

    # Pilha utilizada pela busca em profundidade.
    stack = [inicio]

    # Guarda as posições que já foram visitadas.
    visitado = [[False] * colunas for _ in range(linhas)]

    # Guarda o predecessor de cada posição.
    anterior = [[None] * colunas for _ in range(linhas)]

    visitado[inicio[0]][inicio[1]] = True

    # Movimentos para cima, baixo, esquerda e direita.
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while stack:
        linha, coluna = stack.pop()

        # Verifica se o objetivo foi encontrado.
        if maze[linha][coluna] == cheese:
            caminho = []

            atual = (linha, coluna)

            # Reconstrói o caminho voltando pelos predecessores.
            while atual is not None:
                caminho.append(atual)
                atual = anterior[atual[0]][atual[1]]

            # O caminho foi reconstruído do queijo até o início.
            caminho.reverse()

            return caminho

        for dl, dc in directions:
            nova_linha = linha + dl
            nova_coluna = coluna + dc

            if (
                0 <= nova_linha < linhas
                and 0 <= nova_coluna < colunas
                and not visitado[nova_linha][nova_coluna]
                and maze[nova_linha][nova_coluna] != wall
            ):
                visitado[nova_linha][nova_coluna] = True

                anterior[nova_linha][nova_coluna] = (linha, coluna)

                stack.append((nova_linha, nova_coluna))

    return None


def exibir_labirinto_e_caminho(maze, caminho, cheese="*", path="."):
    """Exibe o labirinto marcando o caminho encontrado."""
    # Faz uma cópia para não modificar o labirinto original.
    labirinto = [linha[:] for linha in maze]

    if caminho is not None:
        for linha, coluna in caminho:
            # Mantém o queijo visível.
            if labirinto[linha][coluna] != cheese:
                labirinto[linha][coluna] = path

    for linha in labirinto:
        print(" ".join(map(str, linha)))


if __name__ == "__main__":
    # Tamanho do labirinto.
    m, n = 10, 14

    # Mantém o exemplo reproduzível.
    random.seed(10110)

    room = " "
    wall = "W"
    cheese = "*"
    path = "."

    # Gera o labirinto.
    maze = generate_maze(m, n, room, wall, cheese)

    print("Labirinto com caminho:")

    # Procura o caminho da posição (1, 1) até o queijo.
    caminho = encontrar_caminho(maze, cheese, wall)

    if caminho is None:
        print("Não foi possível encontrar o queijo.")
    else:
        # Exibe o labirinto e o caminho encontrado.
        exibir_labirinto_e_caminho(maze, caminho, cheese, path)

        print()
        print("Legenda: W = parede | . = caminho | * = queijo")