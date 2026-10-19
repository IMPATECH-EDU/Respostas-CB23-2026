# python 3
from collections import deque
# NOTA: Por causa da ordem de chamadas do random ser diferente, a versão iterativa produz um labirinto diferente da versão recursiva, mesmo usando essencialmente o mesmo algoritmo

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


def generate_maze(m, n, room=0, wall=1, cheese='.', iter=False):
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

    def dfs_iter(x,y):
        stack = [(x,y)]
        maze[2 * x + 1][2 * y + 1] = room

        while len(stack) > 0:
            nodex, nodey = stack.pop()

            # Ordem aleatória garante labirintos distintos a cada execução
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = nodex + dx, nodey + dy
                if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                    # Derruba a parede entre (x,y) e (nx,ny)
                    maze[2 * nodex + 1 + dx][2 * nodey + 1 + dy] = room
                    maze[2 * nx + 1][2 * ny + 1] = room 
                    stack.append((nx, ny))




    def dfs(x, y):
        """Abre passagens recursivamente a partir da sala (x, y)."""
        maze[2 * x + 1][2 * y + 1] = room

        # Ordem aleatória garante labirintos distintos a cada execução
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                # Derruba a parede entre (x,y) e (nx,ny)
                maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                dfs(nx, ny)

    # Inicia a DFS no canto superior-esquerdo da grade lógica
    if iter:
        dfs_iter(0,0)
    else:
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
    s = []
    for row in maze:
        s.append(" ".join(map(str, row)))
    return '\n'.join(s)

def solve(maze, wall, cheese):
    # at each step, process current tile and add every neighbor to a queue.
    visited = set([(1,1)])
    pending = deque([(1,1)])
    
    parent = {(1,1): None}
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    goal_pos = None
    
    while pending:
        current = pending.popleft()

        if maze[current[0]][current[1]] == cheese:
            
            goal_pos = current
            break

        for direction in directions:
            neighbor_pos = (direction[0]+current[0], direction[1]+current[1])
            neighbor = maze[neighbor_pos[0]][neighbor_pos[1]]
            
            if neighbor != wall and neighbor_pos not in visited:
                parent[neighbor_pos] = current
                visited.add(neighbor_pos)
                pending.append(neighbor_pos)

    
    if goal_pos not in parent:
        return None
    
    path = []
    current = goal_pos
    
    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    
    return path

def pretty_path(maze, path, room):
    for pos in path:
        if maze[pos[0]][pos[1]] == room:
            maze[pos[0]][pos[1]] = '-'
    return print_maze(maze)

if __name__ == '__main__':
    m, n = 10, 14  # Grid size
    random.seed(10110)
    
    maze = generate_maze(m, n, iter=True)
    print('Maze 1')
    print(print_maze(maze))

    room = ' '
    wall = 'W'
    cheese = '*'
    random.seed(10111)
    maze = generate_maze(m, n, room, wall, cheese, iter=True)
    print('Maze 2')
    print(print_maze(maze))
    print('Solution')
    solution = solve(maze, wall, cheese)
    print(pretty_path(maze, solution, room))
    
