
"""
maze_builder.py

Geração procedural de labirintos perfeitos usando busca em profundidade (DFS)

com retrocesso (backtracking).

Um labirinto "perfeito" possui exactamente um caminho entre quaisquer dois

pontos — equivalente a uma árvore geradora aleatória sobre a grade m x n.

Representação interna

~~~~~~~~~~~~~~~~~~~~~

A grade lógica de m linhas X n colunas é expandida para uma matriz de

(2m+1) X (2n+1) células, onde:

  - células de coordenadas ímpares (2i+1, 2j+1) representam salas (rooms);

  - células entre duas salas adjacentes representam paredes derrubáveis;

  - as bordas externas são sempre paredes.

O queijo (cheese) é colocado aleatoriamente em qualquer sala.

"""

import random


def generate_maze(m, n, room=0, wall=1, cheese='.'):
    """Gera um labirinto perfeito de m X n células usando DFS com backtracking.

    Parameters
    ----------
    m : int
        Número de linhas da grade lógica.

    n : int
        Número de colunas da grade lógica.

    room : int or str, optional
        Valor usado para representar passagens abertas. Padrão: 0.

    wall : int or str, optional
        Valor usado para representar paredes. Padrão: 1.

    cheese : str, optional
        Símbolo colocado aleatoriamente em uma sala como objetivo. Padrão: '.'.

    Returns
    -------
    list[list]
        Matriz (2m+1) X (2n+1) representando o labirinto gerado.
    """

    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs_iterativo(x, y):
        pilha = [(x, y)]
        visitados = {(x, y)}

        maze[2 * x + 1][2 * y + 1] = room

        while pilha:
            x, y = pilha[-1]

            vizinhos = []

            for dx, dy in directions:
                nx = x + dx
                ny = y + dy

                if 0 <= nx < m and 0 <= ny < n:
                    if (nx, ny) not in visitados:
                        vizinhos.append((dx, dy, nx, ny))

            if vizinhos:
                dx, dy, nx, ny = random.choice(vizinhos)

                maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                maze[2 * nx + 1][2 * ny + 1] = room

                visitados.add((nx, ny))
                pilha.append((nx, ny))

            else:
                pilha.pop()

    dfs_iterativo(0, 0)

    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * m))

        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze


def print_maze(maze):
    """Imprime o labirinto no terminal, uma linha por vez."""

    for row in maze:
        print(" ".join(map(str, row)))


def encontrar_caminho(maze, wall=1, cheese='.'):
    """Encontra um caminho da posição (1,1) até o queijo usando DFS iterativo."""

    inicio = (1, 1)

    pilha = [inicio]
    visitados = {inicio}
    anterior = {}

    direcoes = [
        (-2, 0),
        (2, 0),
        (0, -2),
        (0, 2)
    ]

    while pilha:
        x, y = pilha.pop()

        if maze[x][y] == cheese:
            caminho = [(x, y)]
            atual = (x, y)

            while atual != inicio:
                atual = anterior[atual]
                caminho.append(atual)

            caminho.reverse()
            return caminho

        for dx, dy in direcoes:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
                meio_x = x + dx // 2
                meio_y = y + dy // 2

                if maze[meio_x][meio_y] != wall:
                    if maze[nx][ny] != wall and (nx, ny) not in visitados:
                        visitados.add((nx, ny))
                        anterior[(nx, ny)] = (x, y)
                        pilha.append((nx, ny))

    return None


def mostrar_caminho(maze, caminho, cheese='.'):
    """Mostra o labirinto destacando o caminho encontrado."""

    copia = [linha[:] for linha in maze]

    for i in range(len(caminho)):
        x, y = caminho[i]

        if copia[x][y] != cheese:
            copia[x][y] = '*'

        if i < len(caminho) - 1:
            nx, ny = caminho[i + 1]

            meio_x = (x + nx) // 2
            meio_y = (y + ny) // 2

            if copia[meio_x][meio_y] != cheese:
                copia[meio_x][meio_y] = '*'

    print_maze(copia)


if __name__ == '__main__':
    m, n = 10, 14

    random.seed(100)

    maze = generate_maze(m, n)

    print('Maze 1')
    print_maze(maze)

    room = ' '
    wall = 'W'
    cheese = 'Q'

    maze = generate_maze(m, n, room, wall, cheese)

    print('\nMaze 2')
    print_maze(maze)

    caminho = encontrar_caminho(maze, wall, cheese)

    if caminho is not None:
        print('\nCAMINHO ENCONTRADO')
        print(caminho)

        print('\nLABIRINTO COM O CAMINHO')
        mostrar_caminho(maze, caminho, cheese)
    else:
        print('\nCaminho não encontrado.')

