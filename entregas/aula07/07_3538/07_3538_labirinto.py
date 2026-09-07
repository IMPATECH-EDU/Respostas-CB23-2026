import random
from collections import deque


def generate_maze(m, n, room=0, wall=1, cheese='.'):
    """Gera um labirinto perfeito de m X n células usando DFS iterativo."""
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    stack = [(0, 0)]
    maze[1][1] = room

    while stack:
        x, y = stack[-1]

        unvisited = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                unvisited.append((dx, dy, nx, ny))

        if unvisited:
            dx, dy, nx, ny = random.choice(unvisited)
            maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
            maze[2 * nx + 1][2 * ny + 1] = room
            stack.append((nx, ny))
        else:
            stack.pop()

    while True:
        i = random.randint(0, 2 * m)
        j = random.randint(0, 2 * n)
        if maze[i][j] == room and (i, j) != (1, 1):
            maze[i][j] = cheese
            break

    return maze


def solve_maze_bfs(maze, start=(1, 1), wall='W', cheese='*'):
    """Encontra o caminho mais curto até o queijo usando BFS."""
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, [start])])
    visited = set([start])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        (x, y), path = queue.popleft()

        if maze[x][y] == cheese:
            return path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # 1. Checa limites da matriz
            # 2. Checa se não é parede
            # 3. Checa se ainda não foi visitado
            if (0 <= nx < rows and 0 <= ny < cols and 
                maze[nx][ny] != wall and (nx, ny) not in visited):
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))

    return None


def print_maze_with_path(maze, path, cheese='*', path_symbol='o'):
    """Exibe o labirinto no terminal com o caminho percorrido destacado."""
    maze_copy = [row[:] for row in maze]

    if path:
        for r, c in path:
            # Preserva a posição inicial e a do queijo
            if (r, c) != (1, 1) and maze_copy[r][c] != cheese:
                maze_copy[r][c] = path_symbol

    for row in maze_copy:
        print(" ".join(map(str, row)))


if __name__ == '__main__':
    m, n = 5, 4
    #random.seed(10110)

    wall_char = 'W'
    cheese_char = '*'
    room_char = ' '

    maze = generate_maze(m, n, room=room_char, wall=wall_char, cheese=cheese_char)

    print("\n Labirinto Original")
    print_maze_with_path(maze, path=[], cheese=cheese_char)

    print("\nLabirinto Resolvido (Caminho com '0')")
    path = solve_maze_bfs(maze, start=(1, 1), wall=wall_char, cheese=cheese_char)
    print_maze_with_path(maze, path, cheese=cheese_char, path_symbol='-')