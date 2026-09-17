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
from collections import deque


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

    x = 0
    y = 0
    maze[2*x + 1][2*y + 1] = room

    arestas = []
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < m and 0 <= ny < n and maze[2*nx + 1][2*ny + 1] == wall:
            arestas.append([(2*x + 1 + dx, 2*y + 1 + dy), (2*nx + 1, 2*ny + 1), (nx, ny)])

    while arestas:
        t = arestas.pop()
        parede_i = t[0][0]
        parede_j = t[0][1]
        fim_i = t[1][0]
        fim_j = t[1][1]
        if maze[fim_i][fim_j] == wall:
            maze[fim_i][fim_j] = room
            maze[parede_i][parede_j] = room
            x = t[2][0]
            y = t[2][1]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and maze[2*nx + 1][2*ny + 1] == wall:
                    arestas.append([(2*x + 1 + dx, 2*y + 1 + dy), (2*nx + 1, 2*ny + 1), (nx, ny)])     

    # Posiciona o queijo em uma sala aleatória (rejeita paredes)
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * n))
        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze

def solve(maze, room, wall, cheese):
    m = len(maze) # m é o número de linhas do labirinto
    n = len(maze[0]) # n é o número de colunas do labirinto
    x, y = (1, 1)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visitados = {(1,1)} 
    avisitar = deque([[(1, 1), [(1, 1)]]]) # célula, e o caminho feito até essa célula
    while avisitar:
        atual = avisitar.popleft()
        x, y = atual[0]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and ((nx, ny) not in visitados):
                visitados.add((nx, ny))
                if maze[nx][ny] == room:
                    caminho = atual[1].copy()
                    caminho.append((nx, ny))
                    avisitar.append([(nx, ny), caminho])
                elif maze[nx][ny] == cheese:
                    caminho = atual[1].copy()
                    caminho.append((nx, ny))
                    return caminho




def print_maze(maze):
    """Imprime o labirinto no terminal, uma linha por vez.

    Parameters
    ----------
    maze : list[list]
        Matriz retornada por :func:`generate_maze`.
    """
    for row in maze:
        print(" ".join(map(str, row)))

# Example usage:
if __name__ == '__main__':
    m, n = 10, 14  # Grid size
    random.seed(10110)

    room = ' '
    wall = 'W'
    cheese = '*'
    maze = generate_maze(m, n, room, wall, cheese)
    print('Labirinto gerado:\n')
    print_maze(maze)

    caminho = solve(maze, room, wall, cheese)
    for x, y in caminho:
        maze[x][y] = "."
    q = caminho[-1]
    maze[1][1] = "o"
    maze[q[0]][q[1]] = "*"
    print("\n\nLabirinto com o caminho, do início até o queijo, encontrado:\n")
    print_maze(maze)