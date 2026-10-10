
import random
def generate_maze(m, n, room=0, wall=1, cheese='.'):
    
    # Inicializa a matriz expandida com todas as células como parede
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    # Deslocamentos para os quatro vizinhos cardeais: N, S, W, E
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(a,b):
        """Abre passagens iterativamente a partir da sala (a, b) usando uma pilha explícita."""
        
        # Embaralha as direções para garantir a geração de labirintos distintos a cada execução
        random.shuffle(directions)

        # A pilha armazena a sala atual e as direções que ainda não foram exploradas
        pilha=[((a,b),directions.copy())]

        while pilha:
            # Obtém as coordenadas da sala localizada no topo da pilha
            x,y = pilha[-1][0]

            # Marca a sala atual como uma passagem aberta
            maze[2 * x + 1][2 * y + 1] = room

            # Obtém as direções que ainda podem ser exploradas a partir da sala atual
            direcao = pilha[-1][1]

            # Se não houver mais direções para explorar, remove a sala da pilha
            # e realiza o retrocesso (backtracking)
            if not direcao:
                pilha.pop()
                continue
            
            # Percorre as direções restantes da sala atual
            for _ in range(len(direcao)):
                # Retira uma direção e calcula as coordenadas da sala vizinha
                dx,dy = direcao.pop()
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                    # Derruba a parede entre a sala atual e a sala vizinha
                    maze[2 * x + 1 + dx][2 * y + 1 + dy] = room

                    # Embaralha novamente as direções para manter a aleatoriedade
                    random.shuffle(directions)

                    # Adiciona a nova sala e suas direções à pilha
                    pilha.append(((nx,ny),directions.copy()))

                    # Interrompe a exploração das demais direções da sala atual
                    # para continuar a busca a partir da nova sala
                    break
            



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
def print_maze(maze):
    """Imprime o labirinto no terminal, uma linha por vez.

    Parameters
    ----------
    maze : list[list]
        Matriz retornada por :func:`generate_maze`.
    """
    for row in maze:
        print(" ".join(map(str, row)))


def caminho_do_queijo(maze,cheese):
    """Encontra um caminho entre a posição (1, 1) e o queijo usando busca em profundidade (DFS).

    Parameters
    ----------
    maze : list[list]
        Matriz representando o labirinto.
    cheese : int or str
        Valor utilizado para representar o queijo no labirinto.

    Returns
    -------
    list[tuple]
        Lista de coordenadas que representa o caminho entre a posição inicial
        (1, 1) e o queijo.
    """

    # Obtém o valor utilizado para representar as paredes do labirinto
    parede=maze[0][0]

    # Armazena cada posição visitada e a posição de onde ela foi alcançada
    caminho={
        (1,1):None
    }

    # Pilha utilizada para controlar a busca em profundidade
    pilha=[]

    # Deslocamentos para os quatro vizinhos cardeais: W, N, E, S
    direcoes=[(0,-1),(-1,0),(0,1),(1,0)]

    # Inicia a busca na posição (1,1)
    x,y=1,1

    while maze[x][y]!=cheese:
        # Explora as quatro direções possíveis a partir da posição atual
        for dx,dy in direcoes:
            nx,ny=x+dx,y+dy

            # Verifica se a posição é uma passagem e se ainda não foi visitada
            if maze[nx][ny]!=parede and (nx,ny) not in caminho:
                # Armazena a posição anterior da nova posição encontrada
                caminho[(nx,ny)]=(x,y)

                # Adiciona a nova posição à pilha para continuar a busca
                pilha.append((nx,ny))

        # Remove da pilha a próxima posição que será explorada
        x,y = pilha.pop()

    # Lista utilizada para armazenar o caminho encontrado
    caminho_final = []

    # Percorre os predecessores para reconstruir o caminho até a posição inicial
    while caminho[(x,y)]:
        x,y=caminho[(x,y)]
        caminho_final.append((x,y))

    # Inverte a ordem para obter o caminho da posição inicial até o queijo
    caminho_final.reverse()

    return caminho_final


def resolver_labirinto(maze,queijo,simbolo="°"):
    """Exibe o labirinto com o caminho entre a posição (1, 1) e o queijo marcado.

    Parameters
    ----------
    maze : list[list]
        Matriz representando o labirinto.
    queijo : int or str
        Valor utilizado para representar o queijo no labirinto.
    simbolo : int or str, optional
        Símbolo utilizado para representar o caminho encontrado. Padrão: "°".
    """

    # Obtém o caminho entre a posição inicial e o queijo
    for x,y in caminho_do_queijo(maze,queijo):
        # Marca cada posição do caminho encontrado com o símbolo escolhido
        maze[x][y]=simbolo

    # Exibe o labirinto com o caminho marcado
    print_maze(maze)



    
        
# Example usage:
if __name__ == '__main__':
    m, n = 10, 14  # Grid size
    random.seed(354623)
    maze = generate_maze(m, n)
    print('Maze 1')
    print_maze(maze)

    room = ' '
    wall = 'w'
    cheese = '*'
    maze = generate_maze(m, n, room, wall, cheese)
    print('\nMaze 2')
    resolver_labirinto(maze,cheese,"^")

