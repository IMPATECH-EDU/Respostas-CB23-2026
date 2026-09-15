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

def generate_maze(m, n, room=0, wall=1, cheese='.', rat=0, caminho=2, passado=3):
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

    '''    def dfs(x, y):
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
    '''

    def dfs(x, y):
        maze[2 * x + 1][2 * y + 1] = room

        historico = []

        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                historico.append((dx, dy))
                maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                x, y = nx, ny
                maze[2 * x + 1][2 * y + 1] = room
                break

        while historico:
            cont = 0
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                    historico.append((dx, dy))
                    maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                    x, y = nx, ny
                    maze[2 * x + 1][2 * y + 1] = room
                    break
                cont += 1
                if cont >= 4:
                    if not historico:
                        break

                    dx, dy = historico.pop()
                    x, y = x - dx, y - dy
                    maze[2 * x + 1][2 * y + 1] = room



    # Inicia a DFS no canto superior-esquerdo da grade lógica
    dfs(0, 0)

    # Posiciona o queijo em uma sala aleatória (rejeita paredes)
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * m))
        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    def busca_queijo():

        def grau(x, y):
            for dx, dy in directions:
                if maze[x+dx][y+dy] == room or maze[x+dx][y+dy] == cheese:
                    poss_dir = (x+dx, y+dy)
                    return poss_dir
            return

        historico = []
        x, y = 1, 1

        while maze[x][y] != cheese:
            maze[x][y] = passado
            poss_dir = grau(x, y)
            if poss_dir:
                nx, ny = poss_dir[0], poss_dir[1]
                historico.append((x, y))
                x, y = nx, ny
            else:
                while not grau(x, y):
                    if not historico:
                        return None
                    x, y = historico.pop()

        for x, y in historico:
            maze[x][y] = caminho
    

    busca_queijo()

    maze[1][1] = rat

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
    #random.seed(10110)
    maze = generate_maze(m, n)
    print('Maze 1')
    print_maze(maze)

    room = '⬜​​'
    wall = '🟥​​'
    cheese = '🪤 ​'
    rat = '🐭​'
    caminho = '🟩​'
    passado = '🟦​'
    maze = generate_maze(m, n, room, wall, cheese, rat, caminho, passado)
    print('\nMaze 2')
    print_maze(maze)