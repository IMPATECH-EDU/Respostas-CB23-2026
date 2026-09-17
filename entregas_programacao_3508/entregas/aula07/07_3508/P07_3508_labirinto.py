import random


def generate_maze(m, n, room=0, wall=1, cheese='.'):
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    maze[1][1] = room
    stack = [(0, 0)]

    while stack:
        x, y = stack[-1]
        vizinhos = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < m and 0 <= ny < n:
                if maze[2 * nx + 1][2 * ny + 1] == wall:
                    vizinhos.append((nx, ny, dx, dy))

        if vizinhos:
            nx, ny, dx, dy = random.choice(vizinhos)

            maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
            maze[2 * nx + 1][2 * ny + 1] = room
            stack.append((nx, ny))
        else:
            stack.pop()

    while True:
        i = random.randrange(1, 2 * m, 2)
        j = random.randrange(1, 2 * n, 2)

        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze


def encontrar_caminho(maze, wall='W', cheese='*', inicio=(1, 1)):
    linhas = len(maze)
    colunas = len(maze[0])

    pilha = [inicio]
    visitados = {inicio}
    anterior = {inicio: None}

    destino = None

    while pilha:
        x, y = pilha.pop()

        if maze[x][y] == cheese:
            destino = (x, y)
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < linhas and 0 <= ny < colunas:
                if maze[nx][ny] != wall and (nx, ny) not in visitados:
                    visitados.add((nx, ny))
                    anterior[(nx, ny)] = (x, y)
                    pilha.append((nx, ny))

    if destino is None:
        return []

    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = anterior[atual]

    caminho.reverse()
    return caminho


def exibir_caminho(maze, caminho, cheese='*'):
    copia = [linha.copy() for linha in maze]

    for x, y in caminho:
        if copia[x][y] != cheese:
            copia[x][y] = '.'

    for linha in copia:
        print(" ".join(map(str, linha)))


if __name__ == "__main__":
    random.seed(10110)

    room = ' '
    wall = 'W'
    cheese = '*'

    maze = generate_maze(10, 14, room, wall, cheese)
    caminho = encontrar_caminho(maze, wall, cheese)

    if caminho:
        print("Labirinto com o caminho ate o queijo:")
        exibir_caminho(maze, caminho, cheese)
    else:
        print("Nao foi encontrado um caminho ate o queijo.")
