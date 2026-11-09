import random
from collections import deque


def generate_maze_iterative(m, n, room=0, wall=1, cheese="."):
    """Gera um labirinto perfeito de m x n usando DFS iterativo.

    A estrutura do labirinto é a mesma de maze_builder.py:
    uma grade lógica m x n é representada por uma matriz
    (2m+1) x (2n+1), com salas nas coordenadas ímpares.

    Complexidade:
        Tempo: O(m*n)
        Espaço adicional: O(m*n) no pior caso pela pilha e
        pela matriz do labirinto.
    """
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Pilha explícita substitui a pilha de chamadas da DFS recursiva.
    stack = [(0, 0)]
    visited = {(0, 0)}

    maze[1][1] = room

    while stack:
        x, y = stack[-1]

        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in visited:
                neighbors.append((nx, ny, dx, dy))

        if not neighbors:
            # Não há vizinhos novos: backtracking.
            stack.pop()
            continue

        # Mantém o comportamento aleatório da versão original.
        nx, ny, dx, dy = random.choice(neighbors)

        # Derruba a parede entre a sala atual e a nova sala.
        maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
        maze[2 * nx + 1][2 * ny + 1] = room

        visited.add((nx, ny))
        stack.append((nx, ny))

    # Escolhe o queijo entre as salas da grade lógica.
    room_positions = [
        (2 * x + 1, 2 * y + 1)
        for x in range(m)
        for y in range(n)
    ]
    i, j = random.choice(room_positions)
    maze[i][j] = cheese

    return maze


def find_cheese(maze, room=0, cheese="."):
    """Encontra um caminho de (1, 1) até o queijo usando BFS.

    Retorna uma lista de coordenadas, incluindo a origem e a posição
    do queijo. Retorna None caso não exista caminho.

    Complexidade:
        Tempo: O(R*C), onde R e C são as dimensões da matriz.
        Espaço: O(R*C).
    """
    rows = len(maze)
    cols = len(maze[0])

    start = (1, 1)

    cheese_position = None
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == cheese:
                cheese_position = (i, j)
                break
        if cheese_position is not None:
            break

    if cheese_position is None:
        return None

    if maze[start[0]][start[1]] not in (room, cheese):
        return None

    queue = deque([start])
    parent = {start: None}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current = queue.popleft()

        if current == cheese_position:
            break

        x, y = current

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < rows and 0 <= ny < cols):
                continue

            if (nx, ny) in parent:
                continue

            if maze[nx][ny] not in (room, cheese):
                continue

            parent[(nx, ny)] = current
            queue.append((nx, ny))

    if cheese_position not in parent:
        return None

    # Reconstrói o caminho a partir do queijo.
    path = []
    current = cheese_position

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def show_maze(maze, path=None, room=0, cheese="."):
    """Exibe o labirinto e, opcionalmente, o caminho encontrado.

    O caminho é marcado com '*' nas posições que não são o queijo.
    """
    display = [row[:] for row in maze]

    if path is not None:
        for i, j in path:
            if display[i][j] != cheese:
                display[i][j] = "*"

        # Mantém a origem destacada.
        if path:
            start_i, start_j = path[0]
            display[start_i][start_j] = "S"

    for row in display:
        print(" ".join(map(str, row)))


def main():
    m, n = 10, 14

    random.seed(10110)

    maze = generate_maze_iterative(m, n)

    print("Labirinto:")
    show_maze(maze)

    path = find_cheese(maze)

    print("\nLabirinto com caminho:")
    show_maze(maze, path)

    if path is None:
        print("\nNão foi encontrado caminho até o queijo.")
    else:
        print(f"\nCaminho encontrado com {len(path) - 1} movimentos.")


if __name__ == "__main__":
    main()
