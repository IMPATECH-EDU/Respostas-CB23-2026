import random


def generate_maze(m, n, room=0, wall=1, cheese='.'):
    """gera um labirinto perfeito usando uma DFS iterativa """
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    def dfs_iterativo(x, y):
        maze[2 * x + 1][2 * y + 1] = room
        pilha = [(x, y)]
        while pilha:
            x, y = pilha[-1]
            random.shuffle(directions)
            found = False

            for dx, dy in directions:
                nx = x + dx
                ny = y + dy

                if (
                    0 <= nx < m
                    and 0 <= ny < n
                    and maze[2 * nx + 1][2 * ny + 1] == wall
                ):
                    maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                    maze[2 * nx + 1][2 * ny + 1] = room

                    pilha.append((nx, ny))

                    found = True
                    break

            if not found:
                pilha.pop()

    dfs_iterativo(0, 0)

    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * m))

        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze


def print_maze(maze):
    for row in maze:
        print(" ".join(map(str, row)))

def find_path(maze, inicio=(1, 1), wall=1, cheese='.'):
    """encontra um caminho do ponto inicial até o queijo usando uma DFS iterativa"""

    pilha = [inicio]
    visitados = {inicio}
    anterior = {
        inicio: None
    }

    while pilha:
        atual = pilha.pop()
        x, y = atual

        if maze[x][y] == cheese:
            destino = atual
            break

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            vizinho = (nx, ny)

            if (
                0 <= nx < len(maze)
                and 0 <= ny < len(maze[0])
                and maze[nx][ny] != wall
                and vizinho not in visitados
            ):
                visitados.add(vizinho)

                anterior[vizinho] = atual

                pilha.append(vizinho)

    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = anterior[atual]

    caminho.reverse()

    return caminho

def show_path(maze, caminho, wall=1, cheese='.'):
    """exibe o labirinto destacando o caminho encontrado"""

    caminho = set(caminho)

    for i in range(len(maze)):
        linha = ""

        for j in range(len(maze[i])):
            posicao = (i, j)

            if posicao == (1, 1):
                linha += "S "

            elif maze[i][j] == cheese:
                linha += "* "

            elif posicao in caminho:
                linha += ". "

            elif maze[i][j] == wall:
                linha += "█ "

            else:
                linha += "  "

        print(linha)

if __name__ == '__main__':
    m, n = 10, 14

    random.seed(10110)

    maze = generate_maze(m, n)

    caminho = find_path(maze)

    print("Labirinto original:")
    print_maze(maze)

    print()
    print("Caminho encontrado:")
    show_path(maze, caminho)