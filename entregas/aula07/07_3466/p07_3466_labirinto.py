# python 3

"""
maze_builder.py
---------------
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
    # Inicializa a matriz expandida com todas as células como parede
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    # Deslocamentos para os quatro vizinhos cardeais: N, S, W, E
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(x, y):
        stack = [(0, 0)]

        maze[1][1] = room

        while stack:
            x, y = stack[-1]

            # Embaralha as direções para produzir labirintos diferentes.
            random.shuffle(directions)

            neighbor = False

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                    # Derruba a parede entre as duas salas.
                    maze[2 * x + 1 + dx][2 * y + 1 + dy] = room

                    # Abre a nova sala.
                    maze[2 * nx + 1][2 * ny + 1] = room

                    # Continua a DFS a partir da nova sala.
                    stack.append((nx, ny))

                    neighbor = True
                    break

            # Se não houver vizinhos não visitados, faz backtracking.
            if not neighbor:
                stack.pop()
                    

    # Inicia a DFS no canto superior-esquerdo da grade lógica
    dfs(0, 0)

    # Posiciona o queijo em uma sala aleatória (rejeita paredes)
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * m))
        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze


def print_maze(maze):
    """Imprime o labirinto no terminal, uma linha por vez.

    Parameters
    ----------
    maze : list[list]
        Matriz retornada por :func:`generate_maze`.
    """
    for row in maze:
        print(" ".join(map(str, row)))


def solve_maze(maze,direction = 0,pos_x = 1, pos_y = 1,path = 'x'):
    options = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    solution = maze
    if direction != 0:
        to_remove = list(filter(lambda tup: tup[0] == -1 * direction[0] and tup[1] == -1 * direction[1], options))
        options.remove(to_remove[0])
    for i in options:
        new_x = pos_x + i[0]
        new_y = pos_y + i[1]
        if maze[new_x][new_y] == room:
            if solve_maze(maze, i, new_x, new_y, path) == True:
                solution[new_x][new_y] = path
                if pos_x == 1 and pos_y == 1:
                    return print_maze(solution)
                return True
        elif maze[new_x][new_y] == cheese:
            return True

# Example usage:
if __name__ == '__main__':
    m, n = 10, 14  # Grid size
    random.seed(10110)
    maze = generate_maze(m, n)
    print('Maze 1')
    print_maze(maze)

    room = ' '
    wall = 'W'
    cheese = '*'
    maze = generate_maze(m, n, room, wall, cheese)
    print('\nMaze 2')
    print_maze(maze)
    print()
    solve_maze(maze)


