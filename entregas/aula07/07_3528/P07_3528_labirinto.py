"""
Gera labirintos perfeitos com DFS iterativo (Questão 1) e encontra o caminho de (1, 1) até o queijo, exibindo-o sobre o labirinto (Questão 2).
"""

import random
import sys
from collections import deque

Cell = int | str           # valor armazenado em uma célula da matriz
Maze = list[list[Cell]]    # matriz (2m+1) x (2n+1)
Pos = tuple[int, int]      # coordenada (linha, coluna) na matriz expandida

# Representação: a grade lógica de m linhas x n colunas é expandida para uma matriz (2m+1) x (2n+1). As células de coordenadas ímpares (2i+1, 2j+1) são as salas; cada célula entre duas salas adjacentes é uma parede derrubável; as bordas externas são sempre paredes.

# Deslocamentos para os quatro vizinhos cardeais: N, S, W, E.
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))

# Gerador usado quando nenhum random.Random é passado explicitamente.
_RNG = random.Random()


# ---------------------------------------------------------------------------
# Questão 1: geração do labirinto com DFS iterativo
# ---------------------------------------------------------------------------

def _shuffled_directions(rng: random.Random):
    """
    Devolve uma cópia embaralhada de DIRECTIONS.
    """
    # A cópia é essencial: no código base a mesma lista global era embaralhada
    # dentro de cada chamada recursiva enquanto os laços das chamadas anteriores
    # ainda a percorriam por índice. Assim uma direção podia ser examinada duas
    # vezes e outra nunca, deixando salas sem visita e quebrando a garantia de
    # labirinto perfeito.
    dirs = list(DIRECTIONS)
    rng.shuffle(dirs)
    return dirs


def generate_maze(m: int, n: int, room: Cell = 0, wall: Cell = 1, cheese: Cell = ".", rng: random.Random = _RNG):
    """
    Gera um labirinto perfeito de m x n salas com DFS iterativo e posiciona o queijo em uma sala aleatória.
    """
    if m < 1 or n < 1:
        raise ValueError("m e n devem ser inteiros positivos")

    # Inicializa a matriz expandida com todas as células como parede.
    maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

    # Pilha de quadros (linha lógica, coluna lógica, direções pendentes), em que
    # "pendentes" é um iterador sobre as direções ainda não testadas na sala.
    # Guardar o iterador — e não só a coordenada — reproduz a semântica da
    # recursão: ao desempilhar um filho, o pai retoma o laço de onde parou.
    stack = []

    # Início da busca no canto superior-esquerdo da grade lógica.
    maze[1][1] = room
    stack.append((0, 0, iter(_shuffled_directions(rng))))

    while stack:
        x, y, pending = stack[-1]
        advanced = False

        # Consome o iterador do topo até achar um vizinho ainda não visitado.
        for dx, dy in pending:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                # Derruba a parede entre (x, y) e (nx, ny) e desce para o vizinho.
                maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
                maze[2 * nx + 1][2 * ny + 1] = room
                stack.append((nx, ny, iter(_shuffled_directions(rng))))
                advanced = True
                break  # o iterador guardado retoma daqui quando este quadro voltar

        if not advanced:
            # Direções esgotadas: retrocede (equivalente ao `return` da recursão).
            stack.pop()

    # Posiciona o queijo em uma sala aleatória, por amostragem com rejeição.
    # No código base o sorteio da coluna usava 2*m no lugar de 2*n, o que
    # confinava o queijo às primeiras colunas quando n > m.
    while True:
        i = rng.randrange(2 * m + 1)
        j = rng.randrange(2 * n + 1)
        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze


# ---------------------------------------------------------------------------
# Questão 2 — busca do caminho de (1, 1) até o queijo
# ---------------------------------------------------------------------------

class SearchResult:
    """
    Resultado de uma busca: caminho encontrado e métricas de custo.
    """

    __slots__ = ("path", "discovered", "expanded", "max_frontier")

    def __init__(self, path: list[Pos] | None, discovered: int, expanded: int, max_frontier: int):
        self.path = path                     # células da origem ao destino (None se não há caminho)
        self.discovered = discovered         # células inseridas na fronteira
        self.expanded = expanded             # células retiradas da fronteira
        self.max_frontier = max_frontier     # pico de tamanho da fronteira

    def __repr__(self):
        tamanho = "None" if self.path is None else f"{len(self.path)} células"
        return (f"SearchResult(path={tamanho}, discovered={self.discovered}, "
                f"expanded={self.expanded}, max_frontier={self.max_frontier})")


def find_cheese(maze: Maze, cheese: Cell = "."):
    """
    Localiza a célula que contém o queijo, ou None se não houver.
    """
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == cheese:
                return (i, j)
    return None


def _is_open(maze: Maze, pos: Pos, wall: Cell):
    """
    Indica se pos está dentro da matriz e não é parede.
    """
    i, j = pos
    return 0 <= i < len(maze) and 0 <= j < len(maze[0]) and maze[i][j] != wall


def _neighbors(maze: Maze, pos: Pos, wall: Cell):
    """
    Gera os vizinhos cardeais transitáveis de pos.
    """
    # O grafo da busca tem como vértices todas as células não-parede da matriz
    # expandida (salas e paredes derrubadas) e como arestas a adjacência cardeal
    # entre elas; assim o caminho devolvido já é contíguo na exibição.
    i, j = pos
    for di, dj in DIRECTIONS:
        candidate = (i + di, j + dj)
        if _is_open(maze, candidate, wall):
            yield candidate


def _rebuild_path(parent: dict, goal: Pos):
    """
    Reconstrói o caminho da origem até o destino usando a árvore de busca.
    """
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path


def solve_maze_bfs(maze: Maze, goal: Pos, start: Pos = (1, 1), wall: Cell = 1):
    """
    Busca em largura (BFS) de start até goal — estratégia adotada na entrega.
    """
    # A fronteira é uma fila (FIFO), logo as células são expandidas em ordem não
    # decrescente de distância à origem e o primeiro caminho encontrado é mínimo.
    # Custo: O(V + E) = Θ(m·n) em tempo e Θ(m·n) em memória (dicionário parent).
    if not _is_open(maze, start, wall) or not _is_open(maze, goal, wall):
        return SearchResult(None, 0, 0, 0)

    parent = {start: None}
    frontier = deque([start])
    discovered, expanded, max_frontier = 1, 0, 1

    while frontier:
        current = frontier.popleft()   # FIFO: a célula mais antiga da fronteira
        expanded += 1

        if current == goal:
            return SearchResult(_rebuild_path(parent, goal), discovered, expanded, max_frontier)

        for neighbor in _neighbors(maze, current, wall):
            if neighbor not in parent:   # ainda não descoberto
                parent[neighbor] = current
                discovered += 1
                frontier.append(neighbor)

        max_frontier = max(max_frontier, len(frontier))

    return SearchResult(None, discovered, expanded, max_frontier)


def solve_maze_dfs(maze: Maze, goal: Pos, start: Pos = (1, 1), wall: Cell = 1):
    """
    Busca em profundidade (DFS) iterativa, usada apenas como comparação.
    """
    # Idêntica à BFS a menos da disciplina da fronteira: pilha (LIFO) em vez de
    # fila. Num labirinto perfeito devolve o mesmo caminho, porque o caminho
    # simples entre duas células é único; com ciclos, pode devolver um caminho
    # arbitrariamente mais longo que o mínimo.
    if not _is_open(maze, start, wall) or not _is_open(maze, goal, wall):
        return SearchResult(None, 0, 0, 0)

    parent = {start: None}
    frontier = [start]
    discovered, expanded, max_frontier = 1, 0, 1

    while frontier:
        current = frontier.pop()       # LIFO: a célula mais recente da fronteira
        expanded += 1

        if current == goal:
            return SearchResult(_rebuild_path(parent, goal), discovered, expanded, max_frontier)

        for neighbor in _neighbors(maze, current, wall):
            if neighbor not in parent:
                parent[neighbor] = current
                discovered += 1
                frontier.append(neighbor)

        max_frontier = max(max_frontier, len(frontier))

    return SearchResult(None, discovered, expanded, max_frontier)


# ---------------------------------------------------------------------------
# Exibição
# ---------------------------------------------------------------------------

def render_maze(maze: Maze, path: list | None = None, path_mark: Cell = "*", start_mark: Cell = "S"):
    """
    Devolve o labirinto como texto, opcionalmente com o caminho destacado.
    """
    grid = [[str(value) for value in row] for row in maze]

    if path:
        for i, j in path:
            grid[i][j] = str(path_mark)
        # Preserva os símbolos das pontas: queijo no destino, marca na origem.
        gi, gj = path[-1]
        grid[gi][gj] = str(maze[gi][gj])
        si, sj = path[0]
        grid[si][sj] = str(start_mark)

    return "\n".join(" ".join(row) for row in grid)


def print_maze(maze: Maze):
    """
    Imprime o labirinto no terminal.
    """
    print(render_maze(maze))


def print_maze_with_path(maze: Maze, path: list | None, path_mark: Cell = "*", start_mark: Cell = "S"):
    """
    Imprime o labirinto com o caminho encontrado destacado.
    """
    if path is None:
        print("(nenhum caminho encontrado até o queijo)")
        print_maze(maze)
        return
    print(render_maze(maze, path, path_mark, start_mark))


def print_report(label: str, result: SearchResult, start: Pos, goal: Pos):
    """
    Imprime as métricas de uma busca.
    """
    if result.path is None:
        print(f"{label}: sem caminho de {start} até {goal}.")
        return
    print(f"{label}: caminho com {len(result.path)} células "
          f"({len(result.path) - 1} passos) de {start} até {goal} | "
          f"descobertas: {result.discovered} | expandidas: {result.expanded} | "
          f"fronteira máxima: {result.max_frontier}")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

USAGE = """
Uso: [linhas] [colunas] [semente] [--sem-comparacao]
Gera um labirinto perfeito com DFS iterativo e encontra o caminho de (1, 1) até o queijo.

Argumentos posicionais (opcionais, nesta ordem):
  linhas            número de linhas da grade lógica (padrão: 10)
  colunas           número de colunas da grade lógica (padrão: 14)
  semente           semente do gerador aleatório (padrão: 10110)

Opções:
  --sem-comparacao  não executa a busca em profundidade de comparação
  -h, --help        mostra esta mensagem e encerra
"""


def parse_args(argv: list):
    """
    Interpreta a linha de comando e devolve (linhas, colunas, semente, comparar).
    """
    valores = [10, 14, 10110]    # linhas, colunas, semente (padrões)
    comparar = True
    posicionais = []

    for arg in argv:
        if arg in ("-h", "--help"):
            print(USAGE)
            raise SystemExit(0)
        if arg == "--sem-comparacao":
            comparar = False
        elif arg.startswith("-"):
            raise SystemExit(f"erro: opção desconhecida {arg!r}\n\n{USAGE}")
        else:
            posicionais.append(arg)

    if len(posicionais) > 3:
        raise SystemExit(f"erro: argumentos demais\n\n{USAGE}")

    for i, texto in enumerate(posicionais):
        try:
            valores[i] = int(texto)
        except ValueError:
            raise SystemExit(f"erro: {texto!r} não é um inteiro\n\n{USAGE}") from None

    linhas, colunas, semente = valores
    if linhas < 1 or colunas < 1:
        raise SystemExit(f"erro: linhas e colunas devem ser >= 1\n\n{USAGE}")

    return linhas, colunas, semente, comparar


def main(argv: list | None = None):
    """
    Gera dois labirintos de exemplo, resolve cada um e exibe os resultados.
    """
    m, n, semente, comparar = parse_args(sys.argv[1:] if argv is None else argv)
    rng = random.Random(semente)
    start = (1, 1)

    # --- Labirinto 1: símbolos numéricos padrão ---
    maze = generate_maze(m, n, rng=rng)
    goal = find_cheese(maze, ".")
    print("Maze 1")
    print_maze(maze)

    if goal is None:
        print("Queijo não encontrado no labirinto 1.")
        return 1

    bfs = solve_maze_bfs(maze, goal, start, 1)
    print("\nMaze 1 — caminho (S = início, * = caminho, . = queijo)")
    print_maze_with_path(maze, bfs.path, "*", "S")
    print()
    print_report("BFS", bfs, start, goal)

    if comparar:
        dfs = solve_maze_dfs(maze, goal, start, 1)
        print_report("DFS", dfs, start, goal)
        if bfs.path is not None and dfs.path is not None:
            iguais = "sim" if bfs.path == dfs.path else "não"
            print(f"Caminhos idênticos (labirinto perfeito ⇒ caminho único): {iguais}")

    # --- Labirinto 2: símbolos personalizados ---
    room, wall, cheese = " ", "W", "*"
    maze2 = generate_maze(m, n, room, wall, cheese, rng)
    goal2 = find_cheese(maze2, cheese)
    print("\nMaze 2")
    print_maze(maze2)

    if goal2 is None:
        print("Queijo não encontrado no labirinto 2.")
        return 1

    bfs2 = solve_maze_bfs(maze2, goal2, start, wall)
    print("\nMaze 2 — caminho (S = início, o = caminho, * = queijo)")
    print_maze_with_path(maze2, bfs2.path, "o", "S")
    print()
    print_report("BFS", bfs2, start, goal2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())