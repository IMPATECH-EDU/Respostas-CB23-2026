import random
import copy
from collections import deque

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def generate_maze_iterative(m, n, room=0, wall=1, cheese='.'):
    """Gera um labirinto perfeito de m X n células usando DFS iterativo."""
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]


   
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
        if maze[i][j] == room:
            maze[i][j] = cheese
            cheese_pos = (i, j)
            break

    return maze, cheese_pos

def solve_maze_bfs(maze, start=(1, 1),target=None):
    """Resolve o labirinto utilizando Busca em Largura (BFS).

    Destaca as células vasculhadas com '.' e o menor caminho até o objetivo com 'o'.
    """
    rows = len(maze)
    cols = len(maze[0])

    if not target:
        print("Objetivo (queijo) não informado no labirinto.")
        return maze

    # 2. Inicialização da Fila (FIFO), conjunto de visitados e ponteiros de pai
    queue = deque([start])
    visited = {start}
    parent = {start: None}  # Permite reconstruir a rota no final

    found = False

    # 3. Laço principal do BFS (Exploração por camadas)
    while queue:
        curr = queue.popleft()

        if curr == target:
            found = True
            break

        r, c = curr
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            # Valida bordas, paredes e células já processadas
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and maze[nr][nc] not in ('🟦', 1)
                and neighbor not in visited
            ):
                visited.add(neighbor)
                parent[neighbor] = curr
                queue.append(neighbor)

    if not found:
        print("Caminho até o queijo não encontrado.")
        return maze

    # 4. Renderização do resultado visual
    visual_maze = copy.deepcopy(maze)

    # Marca todas as posições vasculhadas pela fronteira do BFS
    for r, c in visited:
        if (r, c) != start and (r, c) != target:
            visual_maze[r][c] = '🟥'

    # Sobrescreve o menor caminho rastreando os pais a partir do queijo
    curr = parent[target]
    while curr and curr != start:
        r, c = curr
        visual_maze[r][c] = '🟩'
        curr = parent[curr]

    # Marca a posição inicial
    visual_maze[start[0]][start[1]] = '🐀'


    return visual_maze

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
    m, n = 10, 14 
    room = '⬛'
    wall = '🟦'
    cheese = '🧀'
    maze = generate_maze_iterative(m, n, room, wall, cheese)


    solve_maze = solve_maze_bfs(maze[0], start=(1, 1), target=maze[1])
    print('\nSolved Maze 1')
    print_maze(solve_maze)


