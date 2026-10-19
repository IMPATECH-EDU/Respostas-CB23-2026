import random

def gera_labirinto(m, n, room=0, wall=1, cheese='.'):

    labirinto = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs_iterativo(x, y):

        pilha = []
        labirinto[2 * x + 1][2 * y + 1] = room
        pilha.append((x, y))

        while pilha:
            x, y = pilha[-1]
            random.shuffle(direcoes)
            vizinhos = []
            for dx, dy in direcoes:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and labirinto[2 * nx + 1][2 * ny + 1] == wall:
                    vizinhos.append((nx, ny))

            if vizinhos:
                nx, ny = random.choice(vizinhos)
                labirinto[2 * x + 1 + (nx - x)][2 * y + 1 + (ny - y)] = room
                labirinto[2 * nx + 1][2 * ny + 1] = room

                pilha.append((nx, ny))

            else:
                pilha.pop()

    dfs_iterativo(0, 0)

    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * m))
        if labirinto[i][j] == room:
            labirinto[i][j] = cheese
            break

    return labirinto

def print_labirinto(labirinto):

    for linha in labirinto:
        print(" ".join(map(str, linha)))

  
def achar_queijo(labirinto, start=(1, 1), room=' ', wall='W', cheese='*'):

    pilha = [start]
    percorridos = set()

    dic = {}
    traco = []

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while pilha:

        x, y = pilha.pop()
        if (x, y) in percorridos:
            continue

        percorridos.add((x, y))

        if labirinto[x][y] == cheese:

            caminho = []
            atual = (x, y)

            while atual != start:
                caminho.append(atual)
                atual = dic[atual]

            caminho.append(start)

            while caminho:
                traco.append(caminho[-1])
                caminho.pop()

            return traco

        for dx, dy in direcoes:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < len(labirinto) and 0 <= ny < len(labirinto[0]):

                if labirinto[nx][ny] != wall:
                    if (nx, ny) not in percorridos:

                        dic[(nx, ny)] = (x, y)

                        pilha.append((nx, ny))

def print_solucao(labirinto, traco):
    traco = achar_queijo(labirinto)

    for i in traco:
        labirinto[i[0]][i[1]] = '-'
    queijo = traco[-1]
    labirinto[queijo[0]][queijo[1]] = '*'

    for linha in labirinto:
        print(" ".join(map(str, linha)))


if __name__ == '__main__':
    m, n = 10, 14
    random.seed(10110)
    labirinto = gera_labirinto(m, n)
    print('Labirinto 1')
    print_labirinto(labirinto)

    room = ' '
    wall = 'W'
    cheese = '*'
    labirinto = gera_labirinto(m, n, room, wall, cheese)
    print('\nLabirinto 2')
    print_labirinto(labirinto)

    caminho = achar_queijo(labirinto)
    print('\nCaminho')
    print_solucao(labirinto, caminho)
    



    
