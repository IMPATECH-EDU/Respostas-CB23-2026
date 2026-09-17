# python 3

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

    def dfs_iterativa(x, y):
        """Abre passagens iterativamente a partir da sala (x, y).
        A cada passo, a partir de uma sala escolhe uma sala que nao foi visitada e
        abre a parede entre essas duas salas e adiciona a nova sala a pilha."""
        maze[2 * x + 1][2 * y + 1] = room
        pilha = [(x,y)]

        # Ordem aleatória garante labirintos distintos a cada execução
        random.shuffle(directions)
        while pilha:
            x,y = pilha.pop()
            random.shuffle(directions)
            for dx,dy in directions:
                nx,ny = x+dx,y+dy
                if 0<=nx<m and 0<=ny<n and maze[2*nx+1][2*ny+1] == wall:
                    maze[2 * x + 1+dx][2*y+1+dy] = room
                    maze[2 * nx + 1][2*ny+1] = room
                    pilha.append((nx,ny))

    # Inicia a DFS no canto superior-esquerdo da grade lógica
    dfs_iterativa(0, 0)

    # Posiciona o queijo em uma sala aleatória (rejeita paredes)
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * m))
        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze
def solve(maze,inicio,wall=1,cheese="."):
    """Encontra um caminho da posição inicial até o queijo usando DFS.

    A busca utiliza uma pilha para explorar o labirinto em profundidade.
    O dicionário `pai` guarda de qual posição cada posição foi alcançada,
    permitindo reconstruir o caminho depois que o queijo é encontrado.

    Parameters
    ----------
    maze : list[list]
        Labirinto no qual a busca será realizada.
    inicio : tuple
        Posição inicial no labirinto.
    wall : int or str
        Valor usado para representar paredes.
    cheese : str
        Símbolo que representa o queijo.

    Returns
    -------
    list
        Lista de posições que formam o caminho do início até o queijo.
        Retorna None caso o queijo não seja encontrado.
    """
    pilha = [inicio]
    visitados = {inicio}
    pai = {inicio:None}
    direções = [(1,0),(-1,0),(0,1),(0,-1)]

    queijo = None

    while pilha:
        x,y = pilha.pop()

        if maze[x][y] == cheese:
            queijo = (x,y)

        for dx,dy in direções:
            nx, ny = x+dx,y+dy

            if 0<= nx < len(maze) and 0<= ny < len(maze[0]) and (nx,ny) not in visitados and maze[nx][ny] != wall:
                visitados.add((nx,ny))
                pai[(nx,ny)] = (x,y)
                pilha.append((nx,ny))
        caminho = []
        atual = queijo

    while atual is not None:
        caminho.append(atual)  
        atual = pai[atual]

    caminho.reverse()
    return caminho
def print_maze_com_caminho(maze, caminho, cheese='.'):
    """Imprime o labirinto destacando o caminho encontrado.

    Uma cópia do labirinto é utilizada para que o labirinto original
    não seja modificado.
    """

    maze_copia = [row[:] for row in maze]

    for x, y in caminho:
        # Não substitui o queijo pelo símbolo do caminho
        if maze_copia[x][y] != cheese:
            maze_copia[x][y] = '*'

    for row in maze_copia:
        print(" ".join(map(str, row)))


def print_maze(maze):
    """Imprime o labirinto no terminal, uma linha por vez.

    Parameters
    ----------
    maze : list[list]
        Matriz retornada por :func:`generate_maze`.
    """
    for row in maze:
        print(" ".join(map(str, row)))

if __name__ == '__main__':
    m, n = 10, 14
    room = ' '
    wall = 'W'
    cheese = 'X'

    maze = generate_maze(m, n, room, wall, cheese)

    print('Labirinto:')
    print_maze(maze)

    # A posição (1, 1) é a primeira sala do labirinto físico
    inicio = (1, 1)

    caminho = solve(maze,inicio,wall,cheese)
    print("labirinto resolvido:")
    print_maze_com_caminho(maze,caminho,cheese)