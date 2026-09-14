import random


def generate_maze(m, n, room=0, wall=1, cheese='.'):
    
    # Inicializa a matriz expandida com todas as células como parede
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    # Deslocamentos para os quatro vizinhos cardeais: N, S, W, E
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


    import random

    def dfs():
        # Cada elemento da pilha guarda: [(x, y), indice_direcao, lista_de_direcoes_embaralhada]
        dirs_iniciais = list(directions)
        random.shuffle(dirs_iniciais)
        
        # Pilha usa listas mutáveis
        stack = [[(0, 0), 0, dirs_iniciais]]
        maze[1][1] = room

        while len(stack) > 0:
            (x, y), path, local_dirs = stack[-1]

            # Se já testou as 4 direções, desempilha (backtracking)
            if path >= 4:
                stack.pop()
                if len(stack) > 0:
                    stack[-1][1] += 1  # Incrementa o path do pai ao voltar
                continue

            dx, dy = local_dirs[path]
            nx, ny = x + dx, y + dy

            if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                # Derruba a parede intermediária
                maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                maze[2 * nx + 1][2 * ny + 1] = room

                # Cria um conjunto de direções embaralhado exclusivo para o novo nó
                next_dirs = list(directions)
                random.shuffle(next_dirs)
                
                # Adiciona o novo nó à pilha
                stack.append([(nx, ny), 0, next_dirs])
                continue

            # Se o caminho é inválido, passa para a próxima direção da sala atual
            stack[-1][1] += 1

    dfs()

    # Posiciona o queijo em uma sala aleatória (rejeita paredes)
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * m))
        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze


def print_maze(maze):
    """Imprime o labirinto no terminal, uma linha por vez.

    Parameters
    ----------
    maze : list[list]
        Matriz retornada por :func:`generate_maze`.
    """
    for row in maze:
        print(" ".join(map(str, row)))


def solve_maze(maze, start=(1, 1), wall=1, cheese='.'):
    """
    Encontra o caminho da posição inicial até o queijo.
    Retorna uma lista de tuplas (x, y) representando o caminho.
    """
    stack = [start]       # A pilha guarda o nosso caminho atual
    visited = {start}     # Conjunto para rastrear por onde já passamos
    
    # Direções: Norte, Sul, Oeste, Leste
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        cx, cy = stack[-1]

        # Se achamos o queijo, a pilha contém exatamente o caminho correto
        if maze[cx][cy] == cheese:
            return stack

        moved = False
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            
            # Verifica se o vizinho está dentro da matriz, não é parede e não foi visitado
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
                if maze[nx][ny] != wall and (nx, ny) not in visited:
                    stack.append((nx, ny))
                    visited.add((nx, ny))
                    moved = True
                    break  # Mergulha nessa nova direção (comportamento DFS)
        
        # Se não há vizinhos válidos (beco sem saída), retrocedemos
        if not moved:
            stack.pop()

    return []  # Retorna lista vazia se não achar caminho (não deve ocorrer em labirintos perfeitos)


def print_solved_maze(maze, path, path_char='·'):
    """
    Exibe o labirinto desenhando o caminho percorrido.
    """
    # Cria uma cópia da matriz para não alterar o labirinto original
    maze_copy = [row[:] for row in maze]

    # Preenche o caminho no labirinto copiado
    for x, y in path:
        # Só substituímos se não for a posição exata do queijo
        if maze_copy[x][y] not in [cheese]: 
            maze_copy[x][y] = path_char

    print("\n--- Labirinto Resolvido ---")
    for row in maze_copy:
        print(" ".join(map(str, row)))



if __name__ == '__main__':
    m, n = 10, 14  # Grid size
    #random.seed(10110)
    room = ' '
    wall = 'W'
    cheese = '*'
    
    labirinto = generate_maze(m, n, room, wall, cheese)
    
    print('Labirinto Original:')
    print_maze(labirinto)
    
    caminho = solve_maze(labirinto, start=(1, 1), wall=wall, cheese=cheese)
    
    print_solved_maze(labirinto, caminho, path_char='·')