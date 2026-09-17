
import random


def generate_maze(m, n, room=0, wall=1, cheese='.'):
    """Gera um labirinto perfeito usando DFS iterativo."""

    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    stack = [(0, 0)]
    maze[1][1] = room

    while stack:
        x, y = stack[-1]

        neighbors = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < m
                and 0 <= ny < n
                and maze[2 * nx + 1][2 * ny + 1] == wall
            ):
                neighbors.append((nx, ny, dx, dy))

        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)

            maze[2 * x + 1 + dx][2 * y + 1 + dy] = room

            maze[2 * nx + 1][2 * ny + 1] = room

            stack.append((nx, ny))
        else:
            stack.pop()

    rooms = [
        (i, j)
        for i in range(1, 2 * m, 2)
        for j in range(1, 2 * n, 2)
    ]

    cheese_i, cheese_j = random.choice(rooms)
    maze[cheese_i][cheese_j] = cheese

    return maze


def dfs_iterativo(maze, start=(1, 1)):
    stack = [start]
    visited = {start}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        x, y = stack.pop()

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < len(maze)
                and 0 <= ny < len(maze[0])
                and maze[nx][ny] != 1
                and (nx, ny) not in visited
            ):
                visited.add((nx, ny))
                stack.append((nx, ny))

    return visited


def encontrar_queijo(maze, start=(1, 1)):
    rows = len(maze)
    cols = len(maze[0])

    stack = [start]
    visited = {start}

    parent = {start: None}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        current = stack.pop()
        x, y = current

        if maze[x][y] == '.':
            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            path.reverse()
            return path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)

            if (
                0 <= nx < rows
                and 0 <= ny < cols
                and maze[nx][ny] != 1
                and neighbor not in visited
            ):
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return None


def exibir_caminho(maze, path):
    result = [row[:] for row in maze]

    if path is not None:
        for x, y in path:
            if result[x][y] != '.':
                result[x][y] = '*'

    for row in result:
        print(" ".join(map(str, row)))


if __name__ == '__main__':
    m, n = 10, 14

    random.seed(10110)

    maze = generate_maze(m, n)

    print("Labirinto:")
    exibir_caminho(maze, [])

    path = encontrar_queijo(maze)

    print("\nCaminho encontrado:")

    if path is None:
        print("Nenhum caminho encontrado.")
    else:
        exibir_caminho(maze, path)
        print("\nTamanho do caminho:", len(path))