import random
import sys
import time
from collections import deque

# maze_builder.py precisa estar na mesma pasta deste arquivo.
# Ele só serve para comparar com a versão recursiva.
try:
    import maze_builder
except ImportError:
    maze_builder = None

# N, S, W, E (mesma ordem do maze_builder)
DIRECOES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# ---------------------------------------------------------------------------
# Q1 - dfs iterativa
# ---------------------------------------------------------------------------

def dfs_iterativo(maze, m, n, room, wall, igual_ao_original=False):
    # No lugar da pilha de chamadas do Python uso uma lista.
    # Cada item é [x, y, ordem das direções, k].
    # Com igual_ao_original=True todas as chamadas compartilham a mesma
    # lista de direções (é o que o maze_builder faz, dá problema).
    directions = list(DIRECOES)
    pilha = []

    def visita(x, y):
        maze[2 * x + 1][2 * y + 1] = room
        random.shuffle(directions)
        if igual_ao_original:
            ordem = directions
        else:
            ordem = directions[:]
        pilha.append([x, y, ordem, 0])

    visita(0, 0)
    while pilha:
        topo = pilha[-1]
        x, y, ordem, k = topo
        if k == len(ordem):
            pilha.pop()
            continue
        topo[3] += 1
        dx, dy = ordem[k]
        nx, ny = x + dx, y + dy
        if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
            maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
            visita(nx, ny)


def generate_maze_iterativo(m, n, room=0, wall=1, cheese='.', igual_ao_original=False):
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]
    dfs_iterativo(maze, m, n, room, wall, igual_ao_original)

    # queijo numa célula aberta qualquer. Aqui já usei 2*n (o original usa 2*m)
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * n))
        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze


# ---------------------------------------------------------------------------
# Q2 - caminho até o queijo
# ---------------------------------------------------------------------------

def vizinhos(maze, i, j, wall):
    for di, dj in DIRECOES:
        a, b = i + di, j + dj
        if 0 <= a < len(maze) and 0 <= b < len(maze[a]) and maze[a][b] != wall:
            yield a, b


def monta_caminho(veio_de, fim):
    caminho = []
    atual = fim
    while atual is not None:
        caminho.append(atual)
        atual = veio_de[atual]
    caminho.reverse()
    return caminho


def busca_largura(maze, inicio=(1, 1), wall=1, cheese='.'):
    # BFS com deque. Para no queijo e devolve (caminho, visitadas).
    fila = deque([inicio])
    veio_de = {inicio: None}
    visitadas = 0

    while fila:
        i, j = fila.popleft()
        visitadas += 1
        if maze[i][j] == cheese:
            return monta_caminho(veio_de, (i, j)), visitadas
        for v in vizinhos(maze, i, j, wall):
            if v not in veio_de:
                veio_de[v] = (i, j)
                fila.append(v)

    return None, visitadas


def busca_profundidade(maze, inicio=(1, 1), wall=1, cheese='.'):
    # Mesma coisa com pilha, só para comparar com a BFS
    pilha = [(inicio, None)]
    veio_de = {}
    visitadas = 0

    while pilha:
        atual, anterior = pilha.pop()
        if atual in veio_de:
            continue
        veio_de[atual] = anterior
        visitadas += 1
        i, j = atual
        if maze[i][j] == cheese:
            return monta_caminho(veio_de, atual), visitadas
        for v in vizinhos(maze, i, j, wall):
            if v not in veio_de:
                pilha.append((v, atual))

    return None, visitadas


def mostra_labirinto(maze, caminho=None, wall=1, cheese='.'):
    # ## parede, R rato, Q queijo, o caminho
    no_caminho = set(caminho) if caminho else set()
    inicio = caminho[0] if caminho else (1, 1)

    for i, linha in enumerate(maze):
        texto = ""
        for j, c in enumerate(linha):
            if c == wall:
                texto += "##"
            elif c == cheese:
                texto += "Q "
            elif (i, j) == inicio:
                texto += "R "
            elif (i, j) in no_caminho:
                texto += "o "
            else:
                texto += "  "
        print(texto)


# ---------------------------------------------------------------------------
# testes
# ---------------------------------------------------------------------------

def sem_queijo(maze, room=0, cheese='.'):
    return [[room if c == cheese else c for c in linha] for linha in maze]


def salas_fechadas(maze, m, n, wall=1):
    return sum(1 for x in range(m) for y in range(n) if maze[2 * x + 1][2 * y + 1] == wall)


def abre_paredes(maze, m, n, quantidade, wall=1, room=0):
    # abre paredes entre salas vizinhas para criar ciclos
    quantidade = min(quantidade, (m - 1) * (n - 1))
    abertas = 0
    while abertas < quantidade:
        x, y = random.randrange(m), random.randrange(n)
        dx, dy = random.choice([(1, 0), (0, 1)])
        if x + dx < m and y + dy < n and maze[2 * x + 1 + dx][2 * y + 1 + dy] == wall:
            maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
            abertas += 1


def caminho_valido(maze, caminho, wall=1, cheese='.'):
    if caminho[0] != (1, 1) or maze[caminho[-1][0]][caminho[-1][1]] != cheese:
        return False
    for (a, b), (c, d) in zip(caminho, caminho[1:]):
        if abs(a - c) + abs(b - d) != 1 or maze[c][d] == wall:
            return False
    return len(set(caminho)) == len(caminho)


def testes():
    sorteio = random.Random(2026)

    print("1) dfs_iterativo(igual_ao_original=True) x generate_maze recursivo")
    if maze_builder is None:
        print("   maze_builder.py não encontrado, pulei esse teste")
    else:
        iguais = diferentes = pulados = 0
        for s in range(500):
            m, n = sorteio.randint(1, 30), sorteio.randint(1, 30)
            random.seed(s)
            try:
                original = maze_builder.generate_maze(m, n)
            except IndexError:
                pulados += 1  # bug do 2*m no queijo quando m > n
                continue
            random.seed(s)
            meu = generate_maze_iterativo(m, n, igual_ao_original=True)
            if sem_queijo(original) == sem_queijo(meu):
                iguais += 1
            else:
                diferentes += 1
        print(f"   {iguais} iguais, {diferentes} diferentes, "
              f"{pulados} pulados (IndexError do queijo no original)")

    print("2) salas que ficam fechadas")
    ruins_original = ruins_corrigido = nao_arvore = 0
    for s in range(3000):
        m, n = sorteio.randint(2, 20), sorteio.randint(2, 20)
        random.seed(s)
        if salas_fechadas(generate_maze_iterativo(m, n, igual_ao_original=True), m, n):
            ruins_original += 1
        random.seed(s)
        maze = generate_maze_iterativo(m, n)
        if salas_fechadas(maze, m, n):
            ruins_corrigido += 1
        # árvore com m*n salas tem m*n-1 arestas (paredes derrubadas)
        abertas = sum(1 for linha in maze for c in linha if c != 1)
        if abertas != m * n + (m * n - 1):
            nao_arvore += 1
    print(f"   lista compartilhada (como no original): {ruins_original} de 3000 labirintos")
    print(f"   cada chamada com sua cópia: {ruins_corrigido} de 3000 "
          f"({nao_arvore} com número de passagens diferente de m*n - 1)")

    print("3) labirintos grandes")
    for tam in [30, 50, 100, 200]:
        random.seed(1)
        inicio = time.perf_counter()
        generate_maze_iterativo(tam, tam)
        t = time.perf_counter() - inicio
        if maze_builder is None:
            rec = "sem maze_builder"
        else:
            random.seed(1)
            try:
                maze_builder.generate_maze(tam, tam)
                rec = "ok"
            except RecursionError:
                rec = "RecursionError"
            except IndexError:
                rec = "IndexError"
        print(f"   {tam}x{tam}: iterativa ok em {t:.3f} s | recursiva: {rec}")

    print("4) BFS x DFS para achar o queijo (1000 labirintos de cada tamanho)")
    for m, n in [(10, 14), (30, 30)]:
        iguais = validos = bfs_menos = dfs_menos = 0
        soma_bfs = soma_dfs = soma_passos = 0
        for s in range(1000):
            random.seed(s)
            maze = generate_maze_iterativo(m, n)
            c1, v1 = busca_largura(maze)
            c2, v2 = busca_profundidade(maze)
            validos += caminho_valido(maze, c1) and caminho_valido(maze, c2)
            iguais += c1 == c2
            soma_passos += len(c1) - 1
            soma_bfs += v1
            soma_dfs += v2
            bfs_menos += v1 < v2
            dfs_menos += v2 < v1
        print(f"   {m}x{n}: caminhos válidos {validos}, mesmo caminho nas duas {iguais}, "
              f"passos em média {soma_passos / 1000:.1f}")
        print(f"      células visitadas em média: BFS {soma_bfs / 1000:.1f}, DFS {soma_dfs / 1000:.1f} "
              f"| BFS visitou menos em {bfs_menos}, DFS em {dfs_menos}")

    print("5) e se o labirinto tiver ciclos? (abrindo paredes a mais)")
    for m, n in [(10, 14), (30, 30)]:
        vezes = 500
        dfs_mais_longo = validos = 0
        soma_bfs = soma_dfs = 0
        for s in range(vezes):
            random.seed(s)
            maze = generate_maze_iterativo(m, n)
            abre_paredes(maze, m, n, (m * n) // 10)
            c1, _ = busca_largura(maze)
            c2, _ = busca_profundidade(maze)
            validos += caminho_valido(maze, c1) and caminho_valido(maze, c2)
            soma_bfs += len(c1) - 1
            soma_dfs += len(c2) - 1
            if len(c2) > len(c1):
                dfs_mais_longo += 1
        print(f"   {m}x{n} ({vezes} labirintos, {(m * n) // 10} paredes a mais): "
              f"caminhos válidos {validos}")
        print(f"      passos em média: BFS {soma_bfs / vezes:.1f}, DFS {soma_dfs / vezes:.1f} | "
              f"DFS achou caminho mais longo em {dfs_mais_longo}")


# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    if args and args[0] == "testes":
        testes()
        return

    try:
        m = int(args[0]) if len(args) > 0 else 10
        n = int(args[1]) if len(args) > 1 else 14
        semente = int(args[2]) if len(args) > 2 else random.randrange(100000)
    except ValueError:
        print("uso: python P07_3487_labirinto.py [linhas colunas [semente]]")
        return
    if m < 1 or n < 1:
        print("o labirinto precisa ter pelo menos 1 linha e 1 coluna")
        return

    random.seed(semente)
    maze = generate_maze_iterativo(m, n)
    caminho, visitadas = busca_largura(maze)

    print(f"Labirinto {m}x{n} gerado com a dfs iterativa (semente {semente})")
    print()
    mostra_labirinto(maze, caminho)
    print()
    if caminho is None:
        print("Não tem caminho até o queijo.")
        return
    _, visitadas_dfs = busca_profundidade(maze)
    print("R = rato em (1, 1)   Q = queijo   o = caminho   ## = parede")
    print(f"Queijo na posição {caminho[-1]}, caminho com {len(caminho) - 1} passos")
    print(f"Células visitadas pela BFS: {visitadas} (a DFS, só para comparar, visitaria {visitadas_dfs})")


if __name__ == "__main__":
    main()