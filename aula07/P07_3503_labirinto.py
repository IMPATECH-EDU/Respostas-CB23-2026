import random

def generate_maze(m, n, room=0, wall=1, cheese='.'):
    """Gera um labirinto perfeito de m X n células usando DFS com backtracking.

    Parameters
    ----------
    m : int
        Número de linhas da grade lógica.
    n : int
        Número de colunas da grade lógica.
    room : int or str, optional
        Valor usado para representar passagens abertas. Padrão: 0.
    wall : int or str, optional
        Valor usado para representar paredes. Padrão: 1.
    cheese : str, optional
        Símbolo colocado aleatoriamente em uma sala como objetivo. Padrão: '.'.

    Returns
    -------
    list[list]
        Matriz (2m+1) X (2n+1) representando o labirinto gerado.
    """
    # Inicializa a matriz expandida com todas as células como parede
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    # Deslocamentos para os quatro vizinhos cardeais: N, S, W, E
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs_iterativo(start_x, start_y):
        lista = [(start_x, start_y)]
        #começa com a coordenada inicial
        
        maze[2 * start_x + 1][2 * start_y + 1] = room
        #marcou a primeira casa como room
        #vai usar a mesma estratégia de expandir o labiirnto

        while lista:
            #começa na casa atual
            x, y = lista[-1]
            
            vizinhos_nao_visitados = []
            #vai procurar os vizinhos que não são a borda que não foram visitados
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                #vai ver se tá dentro da borda e se é parede
                if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                    vizinhos_nao_visitados.append((nx, ny, dx, dy))
            
            if vizinhos_nao_visitados:
                nx, ny, dx, dy = random.choice(vizinhos_nao_visitados)
                #escolhe um vizinho aleatório
                
                maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                #derruba a parede entre a casa atual e a próxima e vai abrir outra
                maze[2 * nx + 1][2 * ny + 1] = room
                
                lista.append((nx, ny))

            else:
                #se não tiver para onde ir volta removendo a casa da lista
                lista.pop()

    dfs_iterativo(0, 0)

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


#Função para resolver
def resolve(maze, start_x=1, start_y=1, wall=1, cheese='.'):
    linhas = len(maze)
    colunas = len(maze[0])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    #vai ter uma lista que vai guardar (x,y,caminho_ate_aqui)
    lista = [(start_x, start_y, [(start_x, start_y)])]
    
    visitou = set()
    visitou.add((start_x, start_y))
    
    while lista:
        x, y, caminho = lista.pop(0)
        
        #se chegar no queijo
        if maze[x][y] == cheese:
            return caminho
            
        #se não chegar no queijo vai olhar os vizinhos
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            #vê se está dentro das bordas
            if 0 <= nx < linhas and 0 <= ny < colunas:
                #se der para avançar
                if maze[nx][ny] != wall and (nx, ny) not in visitou:
                    visitou.add((nx, ny))
                    #coloca o vizinho na fila com o caminho atualizado
                    lista.append((nx, ny, caminho + [(nx, ny)]))
                    
    return None

#Função para printar o tracejado
def print_maze_resolvido(maze, caminho, rastro='X'):
    copia = [linha[:] for linha in maze]

    #vai colocar o rastro em tudo que é o caminho
    for x, y in caminho:
        if (x, y) != caminho[-1]:  
            copia[x][y] = rastro

    print_maze(copia)

# Example usage:
if __name__ == '__main__':
    m, n = 10, 10
    random.seed(3503)
    
    maze1 = generate_maze(m, n)
    print('Maze 1')
    print_maze(maze1)
    print()
    print("Maze 1 Resolvido:")
    print_maze_resolvido(maze1, resolve(maze1))

    room = ' '
    wall = 'W'
    cheese = '*'
    maze2 = generate_maze(m, n, room, wall, cheese)
    print('\nMaze 2')
    print_maze(maze2)
    caminho2 = resolve(maze2, wall=wall, cheese=cheese)
    print("\nMaze 2 Resolvido:")
    print_maze_resolvido(maze2, caminho2, rastro='x')