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
import collections


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
        """Abre passagens recursivamente a partir da sala (x, y)."""
        maze[2 * x + 1][2 * y + 1] = room

        # Ordem aleatória garante labirintos distintos a cada execução
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                # Derruba a parede entre (x,y) e (nx,ny)
                maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                print(f"x: {nx}, y: {ny}")
                dfs(nx, ny)

    # Inicia a DFS no canto superior-esquerdo da grade lógica
    #dfs(0, 0)

    def iter_dfs(x,y):
        """Abre passagens iterativamente a partir da sala (x,y)"""
        class step():
            def __init__(self, x, y, directions):
                self.x = x
                self.y = y
                self.dir = directions.copy()
                random.shuffle(self.dir)
                self.index = 0

        maze[2 * x + 1][2 * y + 1] = room

        # Ordem aleatória garante labirintos distintos a cada execução
        random.shuffle(directions)

        next_step = step(x,y, directions)
        #Usaremos collections.deque para replicar uma pilha sem as complicações de memória de uma lista em Python
        paths = collections.deque()
        paths.append(next_step)

        while paths:
            cur_room = paths[-1]
            x = cur_room.x
            y = cur_room.y
            dx, dy = cur_room.dir[cur_room.index]
            cur_room.index += 1
            if(cur_room.index == 4):
                paths.pop()
            
            next_x, next_y = x + dx, y + dy
            if (0 <= next_x < m and 0 <= next_y < n) and (maze[2 * next_x + 1][2 * next_y + 1] == wall):
                # Derruba a parede entre (x,y) e (nx,ny)
                maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                maze[2 * next_x + 1][2 * next_y + 1] = room
                next_step = step(next_x, next_y, directions)
                paths.append(next_step)
                
    #dfs(0,0)
    iter_dfs(0,0)

    # Posiciona o queijo em uma sala aleatória (rejeita paredes)
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * n)) #Aqui o queijo era gerado com base no 'n', mas isso estava errado e podia dar erro
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

def solve_maze(maze, start=(1,1), room=0, cheese='.', character='c'):
    """Resolve o labirinto e o modifica para incluir a solução usando um algoritmo bfs
    
    Parameters
    ----------
    maze: list[list]
        Matriz que representa o labirinto
    start: tuple[int1, int2]
        Representa de onde a solução começa
    room : int or str, optional
        Valor usado para representar passagens abertas. Padrão: 0.
    cheese : str, optional
        Símbolo colocado aleatoriamente em uma sala como objetivo. Padrão: '.'."""
    def find_path(maze, room, cheese):
        m, n = len(maze), len(maze[0])
        queue = collections.deque()
        queue.append([start])
        visited = {start}
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))

        while queue:
            current_path = queue.popleft()
            x, y = current_path[-1]
            if maze[x][y] == cheese:
                return current_path

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n:
                    if maze[nx][ny] == cheese or maze[nx][ny] == room:
                        if (nx, ny) not in visited:
                            visited.add((nx,ny))
                            new_path = current_path + [(nx, ny)]
                            queue.append(new_path)
        return None

    path = find_path(maze, room, cheese)
    if path is not None:
        for pos in path:
            x, y = pos
            maze[x][y] = character
        maze[path[-1][0]][path[-1][1]] = cheese

# Example usage:
if __name__ == '__main__':
    m, n = 20, 20
    room = ' '
    wall = '■'
    cheese = '𝐗'

    maze = generate_maze(m, n, room, wall, cheese)
    print('\nMaze 3')
    print_maze(maze)

    print("\n\n")
    solve_maze(maze, (1,1), room, cheese, character='⸬')

    print_maze(maze)

