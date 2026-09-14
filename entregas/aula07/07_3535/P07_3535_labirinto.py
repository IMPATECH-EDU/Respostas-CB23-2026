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

    stack = [(0,0)]

    while True:
        actual_room = stack[-1]
        x, y = actual_room[0], actual_room[1]  

        maze[2 * x + 1][2 * y + 1] = room

        valid_direction = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                valid_direction.append((dx,dy))

        if valid_direction != []:
            random.shuffle(valid_direction)
            choice = valid_direction[0]

            dx,dy = choice[0], choice[1]

            maze[2 * x + 1 + dx][2 * y + 1 + dy] = room

            stack.append((x + dx,y + dy))
        elif actual_room != (0,0):
            stack.pop()
        else: 
            break


    # Posiciona o queijo em uma sala aleatória (rejeita paredes)
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * n))
        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze


def find_cheese(maze, wall=1, cheese='.'):
    if maze[1][1] == cheese:
        return [row.copy() for row in maze]

    stack = [(1,1)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = [(1,1)]

    while True:
        actual_place = stack[-1]
        x, y = actual_place[0], actual_place[1]
        valid_direction = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if maze[nx][ny] != wall and (nx,ny) not in visited:
                valid_direction.append((nx,ny))

        if valid_direction != []:
            random.shuffle(valid_direction)
            choice = valid_direction[0]
            if maze[choice[0]][choice[1]] == cheese:
                break
            else:
                stack.append(choice)
                visited.append(choice)
        else:
            stack.pop()

    maze_way = [row.copy() for row in maze]

    for x, y in stack:
        maze_way[x][y] = "·"

    return maze_way


def print_maze_and_way(maze,maze_way):
    for row in maze:
        print(" ".join(map(str, row)))

    print()

    for row in maze_way:
        print(" ".join(map(str, row)))

if __name__ == '__main__':
    m, n = 10, 14
    random.seed(10110)
    room = ' '
    wall = 'W'
    cheese = '*'
    maze = generate_maze(m, n, room, wall, cheese)
    maze_way = find_cheese(maze, wall,cheese)
    print('\nMaze 2')
    print_maze_and_way(maze,maze_way)
