import random
from collections import deque


def generate_maze(m, n, room=0, wall=1, cheese='.'):
    """Gera um labirinto perfeito de m X n células usando DFS iterativo"""
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Pilha armazena células da grade lógica (x, y)
    stack = [(0, 0)]
    maze[1][1] = room

    while stack:
        x, y = stack[-1]

        # Identifica vizinhos não visitados
        unvisited = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                unvisited.append((dx, dy, nx, ny))

        if unvisited:
            # Escolhe um vizinho aleatório e remove a parede intermediária
            dx, dy, nx, ny = random.choice(unvisited)
            maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
            maze[2 * nx + 1][2 * ny + 1] = room
            stack.append((nx, ny))
        else:
            # Backtracking
            stack.pop()

    # Posiciona o queijo em uma sala aberta aleatória
    while True:
        i = random.randint(0, 2 * m)
        j = random.randint(0, 2 * n)
        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze


def find_path(maze, start=(1, 1), cheese='.'):
    """Encontra o caminho do ponto inicial até o queijo usando Busca em Largura (BFS)"""
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = {start: None}
    cheese_pos = None

    while queue:
        curr = queue.popleft()
        r, c = curr

        if maze[r][c] == cheese:
            cheese_pos = curr
            break

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                # Permite a passagem se não for parede e não tiver sido visitado
                if maze[nr][nc] != 1 and maze[nr][nc] != 'W' and (nr, nc) not in visited:
                    visited[(nr, nc)] = curr
                    queue.append((nr, nc))

    if not cheese_pos:
        return []

    # Reconstrução do caminho a partir dos pais registrados
    path = []
    curr = cheese_pos
    while curr is not None:
        path.append(curr)
        curr = visited[curr]
    path.reverse()
    return path


def print_maze_with_path(maze, path, path_symbol='x'):
    """Exibe o labirinto no terminal demarcando o caminho encontrado com 'x'."""
    maze_copy = [row[:] for row in maze]

    for r, c in path:
        if maze_copy[r][c] not in ('.', '*'):
            maze_copy[r][c] = path_symbol

    for row in maze_copy:
        print(" ".join(map(str, row)))


if __name__ == '__main__':
    # Exemplo de teste
    m, n = 5, 8
    maze = generate_maze(m, n)
    path = find_path(maze, start=(1, 1), cheese='.')

    print("--- Labirinto Solucionado ---")
    print_maze_with_path(maze, path)