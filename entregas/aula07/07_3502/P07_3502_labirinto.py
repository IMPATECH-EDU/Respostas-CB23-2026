import random


class ListaEncadeada:
    class No:
        def __init__(self, valor, proximo=None):
            self.valor = valor
            self.proximo = proximo

    def __init__(self):
        self.head = None
        self.comprimento = 0


class PilhaEncadeada(ListaEncadeada):

    def push(self, valor):
        self.head = self.No(valor, self.head)
        self.comprimento += 1

    def pop(self):
        if self.esta_vazia():
            raise IndexError("A pilha está vazia.")

        topo = self.head
        self.head = topo.proximo
        self.comprimento -= 1

        return topo.valor

    def topo(self):
        if self.esta_vazia():
            raise IndexError("A pilha está vazia.")

        return self.head.valor

    def esta_vazia(self):
        return self.comprimento == 0

    def len(self):
        return self.comprimento

    def __repr__(self):
        no = self.head
        valores = []

        while no is not None:
            valores.append(str(no.valor))
            no = no.proximo

        return " -> ".join(valores)


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

    def dfs(a=0, b=0):
        """Abre passagens recursivamente a partir da sala (x, y)."""
        pilha = [(a, b)]
        maze[2 * a + 1][2 * b + 1] = room

        while pilha:
            x, y = pilha[-1]

            caminho_visitado = True

            # Ordem aleatória garante labirintos distintos a cada execução
            random.shuffle(directions)
        
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                    # Derruba a parede entre (x,y) e (nx,ny)
                    maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                    maze[2 * nx + 1][2 * ny + 1] = room

                    pilha.append((nx, ny))
                    caminho_visitado = False
                    break

            if caminho_visitado:
                pilha.pop()



    # Inicia a DFS no canto superior-esquerdo da grade lógica
    dfs(0, 0)

    # Posiciona o queijo em uma sala aleatória (rejeita paredes)
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * n))
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


def caminho(maze, inicio=(1, 1), cheese='.', wall=1):

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    pilha = PilhaEncadeada()
    pilha.push(inicio)

    visitados = {inicio}
    anterior = {inicio: None}

    while not pilha.esta_vazia():

        atual = pilha.pop()

        linha, coluna = atual

        if maze[linha][coluna] == cheese:

            caminho_encontrado = []
            posicao = atual

            while posicao is not None:
                caminho_encontrado.append(posicao)
                posicao = anterior[posicao]

            caminho_encontrado.reverse()

            resultado = PilhaEncadeada()

            for posicao in caminho_encontrado:
                resultado.push(posicao)

            return resultado

        for dx, dy in directions:

            nova_linha = linha + dx
            nova_coluna = coluna + dy

            if not (0 <= nova_linha < len(maze) and 0 <= nova_coluna < len(maze[0])):
                continue

            if maze[nova_linha][nova_coluna] == wall:
                continue

            nova_posicao = (nova_linha, nova_coluna)

            if nova_posicao in visitados:
                continue

            visitados.add(nova_posicao)
            anterior[nova_posicao] = atual
            pilha.push(nova_posicao)

    return 


def print_caminho(maze, caminho, cheese='.'):
    if caminho is None:
        print("Nenhum caminho encontrado.")
        return

    resultado = [linha[:] for linha in maze]

    posicoes = []

    while not caminho.esta_vazia():
        posicoes.append(caminho.pop())

    for linha, coluna in posicoes:
        if resultado[linha][coluna] != cheese:
            resultado[linha][coluna] = '*'

    for linha in range(len(resultado)):
        for coluna in range(len(resultado[linha])):
            if maze[linha][coluna] == cheese:
                resultado[linha][coluna] = 'C'

    for linha in resultado:
        print(" ".join(map(str, linha)))


if __name__ == '__main__':

    m, n = 10, 14

    random.seed(10110)

    maze = generate_maze(m, n)

    print('Maze 1')
    print_maze(maze)

    caminho_encontrado = caminho(maze, inicio=(1, 1), cheese='.', wall=1)

    print('\nCaminho:')
    print_caminho(maze, caminho_encontrado, '.')

    room = ' '
    wall = 'W'
    cheese = '*'

    maze = generate_maze(m, n, room, wall, cheese)

    print('\nMaze 2')
    print_maze(maze)

    caminho_encontrado = caminho(maze, inicio=(1, 1), cheese=cheese, wall=wall)

    print('\nCaminho:')
    print_caminho(maze, caminho_encontrado, cheese)
