"""
maze_builder.py
---------------
Geração procedural de labirintos perfeitos usando busca em profundidade (DFS)
com retrocesso (backtracking).

Um labirinto "perfeito" possui exactamente um caminho entre quaisquer dois
pontos — equivalente a uma árvore geradora aleatória sobre a grade m x n.

Representação interna
~~~~~~~~~~~~~~~~~~~~~
A grade lógica de m linhas X n colunas é expandida para uma matriz de
(2m+1) X (2n+1) células, onde:
  - células de coordenadas ímpares (2i+1, 2j+1) representam salas (rooms);
  - células entre duas salas adjacentes representam paredes derrubáveis;
  - as bordas externas são sempre paredes.

O queijo (cheese) é colocado aleatoriamente em qualquer sala.
"""

import random


def generate_maze(m, n, room=0, wall=1, cheese='.'):
    #Gera um labirinto perfeito de m X n células usando DFS com backtracking.
    """
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

    def meudfs_iterativo(x=0,y=0): 
        maze[2 * x + 1][2 * y + 1] = room 
        # Agora segue para a pilha com as informações obtidas até o momento
        pilha = [(x,y)] 
        # Enquanto houver elementos na minha pilha, continua construindo o labirinto
         
        while len(pilha) != 0:
            sala_vizinha = [] # Aqui serão armazenadas as salas vizinhas válidas 
            x, y = pilha[-1]
            # Ordem aleatória para garantir labirintos distintos a cada execução
            random.shuffle(directions) 

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                    sala_vizinha.append((nx,ny,dx,dy)) 
            if len(sala_vizinha) !=0: 
                # Escolhe um vizinho aleatório 
                nx, ny, dx, dy = random.choice(sala_vizinha) 
                # Derruba a parede entre onde está e a escolha de vizinho 
                maze[2 * x + 1 + dx][2 * y + 1 + dy] = room 
                # Abre a matriz do labirinto 
                maze[2 * nx + 1][2* ny + 1] = room 
                pilha.append((nx, ny)) 
            else:
                pilha.pop() 

    # Inicia a DFS no canto superior-esquerdo da grade lógica
    meudfs_iterativo(0, 0)

    # O queijo entra em uma sala válida
    while True:
        i = random.randint(0, 2 * m)
        j = random.randint(0, 2 * n) # OBS.: havia um pequeno erro no código que recebemos, coluna e linha tinham a mesma variável como limite
        if maze[i][j] == room and (i, j) != (1, 1):
            maze[i][j] = cheese
            break

    return maze 

# Encontra o queijo com base na posição inicial (1, 1)
def encontrar_queijo(maze, x=1, y=1, wall=1, cheese='.'):  
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    fila = [[(x, y)]]
    visitados = set() # Conjunto para não repetir células visitadas 
    visitados.add((x, y)) 

    while len(fila) != 0: 
        onde_estou = fila.pop(0) # retira o primeiro elemento da lista (FIFO)
        cx, cy = onde_estou[-1]  
        
        if maze[cx][cy] == cheese: 
            return onde_estou 
        
        direcc = list(directions)
        random.shuffle(direcc) 

        for dx, dy in direcc:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != wall:
                if (nx, ny) not in visitados:
                    visitados.add((nx, ny)) 
                    cam = onde_estou + [(nx, ny)] 
                    fila.append(cam) 
    return None # Caso não encontre o queijo 


def print_maze(maze):
    """Imprime o labirinto no terminal, uma linha por vez.

    Parameters
    ----------
    maze : list[list]
        Matriz retornada por :func:`generate_maze`.
    """
    for row in maze:
        print(" ".join(map(str, row)))

def print_solucao(maze, caminho, passo='.', cheese='*'): 
    if not caminho: # Caso o caminho seja None ou vazio, o queijo não foi encontrado 
        print("\n caminho não foi possível")
        return

    for x, y in caminho:
        if maze[x][y] != cheese:
            maze[x][y] = passo
    for linha in maze:
        print(" ".join(map(str, linha)))


if __name__ == '__main__':
    m, n = 10, 14  
    random.seed(10110)
    maze = generate_maze(m, n)
    print('Maze 1')
    print_maze(maze)

    room = ' '
    wall = 'W'
    cheese = '*'
    maze = generate_maze(m, n, room, wall, cheese)
    print('\nMaze 2')
    print_maze(maze)

        
    caminho = encontrar_queijo(maze, 1, 1, wall=wall, cheese=cheese) 
    print('\nMaze com solução')
    print_solucao(maze, caminho, passo='.', cheese=cheese)