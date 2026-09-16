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

    stack: deque[tuple[int, int]] = deque()

    maze[1][1] = room
    stack.append((0, 0))

    while stack:
        x, y = stack[-1]

        # Ordem aleatória garante labirintos distintos a cada execução
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                maze[2 * nx + 1][2 * ny + 1] = room
                stack.append((nx, ny))
                break
        else:
            stack.pop()
    
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * m))
        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze


def solve_maze(maze, wall=1, cheese='.'):
    m, n = len(maze), len(maze[0])
    cheese_pos = (-1, -1)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    parent_dist = [[((0, 0), m * n) for _ in range(n)] for _ in range(m)]

    queue = deque()
    queue.append(((1, 1), 0))
    parent_dist[1][1] = (1, 1), 0

    while queue:
        (x, y), d = queue.popleft()

        if maze[x][y] == cheese:
            cheese_pos = x, y
            break

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if d + 1 >= parent_dist[nx][ny][1] or maze[nx][ny] == wall:
                continue
            parent_dist[nx][ny] = (x, y), d + 1
            queue.append(((nx, ny), d + 1))

    x, y = cheese_pos
    (x, y), d = parent_dist[x][y]
    for _ in range(d):
        maze[x][y] = '+'
        (x, y), _ = parent_dist[x][y]


def print_maze(maze):
    """Imprime o labirinto no terminal, uma linha por vez.

    Parameters
    ----------
    maze : list[list]
        Matriz retornada por :func:`generate_maze`.
    """
    for row in maze:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    maze = generate_maze(10, 15, ' ', 'W', '*')
    solve_maze(maze, 'W', '*')
    print_maze(maze)
