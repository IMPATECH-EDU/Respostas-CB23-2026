
import random
import collections as c

def generate_maze(m, n, room="🟦", wall='🟩', cheese='🟨'):
    # Inicializa a matriz expandida com todas as células como parede
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    # Deslocamentos para os quatro vizinhos cardeais: N, S, W, E
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(x, y):
        visitados = set([(x,y)])
        atual = c.deque([(x, y)])
        maze[2 * x + 1][2 * y + 1] = room
        while atual:
            cx, cy = atual[-1]
            random.shuffle(directions)
            encontrou_vizinhos = False
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in visitados and maze[2 * nx + 1][2 * ny + 1] == wall:
                    maze[2 * cx + 1 + dx][2 * cy + 1 + dy] = room
                    maze[2 * nx + 1][2 * ny + 1] = room
                    visitados.add((nx,ny))
                    atual.append((nx, ny))
                    encontrou_vizinhos = True
                    break
            if not encontrou_vizinhos:
                atual.pop() 

    # Inicia a DFS no canto superior-esquerdo da grade lógica
    dfs(0, 0)

    # Posiciona o queijo em uma sala aleatória (rejeita paredes)
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * m))
        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze

def achar_queijo(maze, cheese="🟨", start=(1,1), path_marker='⬜', wall='🟩', personagem="🐭"):
    x, y = start[0], start[1]
    maze[x][y] = personagem
    linhas, colunas = len(maze), len(maze[0])
    visitados = set()
    visitados.add(start)
    pilha = c.deque([[start]])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while pilha:
        caminho = pilha.pop()
        r,t = caminho[-1]
        if maze[r][t]==cheese:
            for nr, nt in caminho[1:-1]:
                maze[nr][nt] = path_marker
            return maze

        for dr, dt in directions:
            nr = r + dr
            nt = t + dt
            if 0 <= nr < linhas and 0 <= nt < colunas:
                if maze[nr][nt] != wall and (nr, nt) not in visitados:
                    visitados.add((nr,nt))
                    pilha.append(caminho+[(nr,nt)])
    return maze

def print_maze(maze):
    for row in maze:
        print("".join(map(str, row)))

# Example usage:
if __name__ == '__main__':
    m, n = 8, 7  # Grid size
    random.seed(10110)
    maze = generate_maze(m, n)
    print('\n-------------------------------\nMaze 1 (Estado original do labirinto)\n-------------------------------')
    print_maze(maze)
    maze = generate_maze(m, n)
    print('\n-------------------------------\nMaze 2 (Caminho até o queijo)\n-------------------------------')
    a = achar_queijo(maze)
    print_maze(maze)

