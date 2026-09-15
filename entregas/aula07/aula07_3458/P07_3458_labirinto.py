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

    fila = deque()
    def dfs():
        fila.append((0,0))
        # DFS em sua versão iteravel usando deque, praticamente a mesma coisa, mas dessa vez utilizando uma fila ao invés de uma recurssão.
        while fila:
            x,y = fila.pop()
            maze[2 * x + 1][2 * y + 1] = room
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                    maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                    maze[2*nx+1][2*ny+1] = room
                    fila.append((nx,ny))
    dfs()

    # Posiciona o queijo em uma sala aleatória (rejeita paredes)
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * n)) # tinha um erro aqui, tava um m ao invés de n
        if maze[i][j] == room:
            maze[i][j] = cheese
            queijo = (i,j)
            break
    def achar_queijo():
    # Monta o caminho até o queijo
        fila.append((1,1))
        anterior = {(1,1): None}
        while fila:
            atual = fila.popleft()

            # Chegamos ao queijo
            if atual == queijo:
                break

            x, y = atual
            for dx, dy in directions:
                nx = x + dx
                ny = y + dy
                if not (0 <= nx < len(maze) and 0 <= ny < len(maze[0])):
                    continue
                proximo = (nx, ny)
                if maze[nx][ny] != wall and proximo not in anterior:
                    anterior[proximo] = atual
                    fila.append(proximo)
        atual = queijo

        while atual != (1,1):
            x, y = atual

            # Não substitui o queijo
            if atual != queijo:
                maze[x][y] = 'x'

            atual = anterior[atual]
        maze[1][1] = 'x'
    achar_queijo()
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

# Example usage:
if __name__ == '__main__':
    m, n = 10, 14  # Grid size
    random.seed()

    room = ' '
    wall = 'W'
    cheese = '*'
    maze = generate_maze(m, n, room, wall, cheese)
    print('\nMaze')
    print_maze(maze)
