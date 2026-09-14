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

    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]
    
    # Deslocamentos para os quatro vizinhos cardeais: N, S, W, E
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(x, y):
        """Abre passagens iterativamente a partir da sala (x, y)."""
        stack = [(x,y)]
        maze[2 * x + 1][2 * y + 1] = room
        visited = []

        while stack: 

            # Ordem aleatória garante labirintos distintos a cada execução
            random.shuffle(directions)

            x, y = stack.pop()
            maze[2 * x + 1][2 * y + 1] = room

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < m and 0 <= ny < n and (nx,ny) not in visited and maze[2*nx+1][2*ny+1] == wall:
                    stack.append((nx, ny))
                    maze[2 * x + 1 + dx][2 * y + 1 + dy] = room

            visited.append((x,y))
        
    # Inicia a DFS no canto superior-esquerdo da grade lógica
    dfs(0, 0)

    # Posiciona o queijo em uma sala aleatória (rejeita paredes)
    while True:

        i = int(random.uniform(0, 2 * m + 1))
        j = int(random.uniform(0, 2 * n + 1))

        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze

def find_cheese(x=1, y=1) :

    queue = [(x, y)]
    visited = []
    dad = {(x, y): None}   
    end = None

    while queue :
        x, y = queue.pop(0)

        # se algum ponto tiver mais de uma opção de caminho escolhe uma e adiciona as outras na fila
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        if maze[x][y] == '.' :
            end = (x,y)
            break

        for dx, dy in directions :
            nx, ny = x + dx, y + dy

            if 0 <= nx < 2*m+1 and 0 <= ny < 2*n+1 and (nx,ny) not in visited and maze[nx][ny] != 1:
                queue.append((nx, ny))
                dad[(nx, ny)] = (x,y)

        visited.append((x,y))

    way = []
    current = end

    while current is not None :
        way.append(current)
        current = dad[current]
    way.reverse()

    for x, y in way:
        if maze[x][y] == '.':
            maze[x][y] = 'Q'
        else:
            maze[x][y] = 'X'

    return way
        
def print_maze(maze):
    """Imprime o labirinto no terminal, uma linha por vez.

    Parameters
    ----------
    maze : list[list]
        Matriz retornada por :func:`generate_maze`.
    """
    symbol_map = {
        1: '██',    
        0: '  ',    
        'X': '··',  
        'Q': '🧀',   
        '.': '🧀'    
    }

    for row in maze:
        # Substitui cada célula pelo seu equivalente visual
        line = "".join(symbol_map.get(cell, str(cell) * 2) for cell in row)
        print(line)
    
# Example usage:
if __name__ == '__main__':

    m, n = 10, 14

    random.seed(10110)

    maze = generate_maze(m, n)

    print('\nMaze 1')
    print_maze(maze)

    way = find_cheese()

    print('\nMaze com caminho:')
    print_maze(maze)
