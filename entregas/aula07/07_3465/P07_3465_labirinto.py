import random
from collections import deque


def generate_maze(m, n, room: int | str = 0, wall: int | str = 1, cheese='.'):
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

    stack: deque[tuple[int, int, int, int]] = deque()
    stack.append((0, 0, 0, 0))

    while stack:
        x, y, i, j = stack.pop()
        if maze[2 * x + 1][2 * y + 1] != wall:
            continue
        maze[2 * (x - i) + 1 + i][2 * (y - j) + 1 + j] = maze[2 * x + 1][2 * y + 1] = room

        # Ordem aleatória garante labirintos distintos a cada execução
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                stack.append((nx, ny, dx, dy))

    # Posiciona o queijo em uma sala aleatória (rejeita paredes)
    while True:
        i = int(random.uniform(0, 2 * m))
        j = int(random.uniform(0, 2 * m))
        if maze[i][j] == room:
            maze[i][j] = cheese
            break

    return maze


class _PerfectMazeSolver:
    def __init__(self, maze, room: int | str = 0, wall: int | str = 1, cheese='.', path='+', start_pos=(1, 1)):
        self._maze = maze
        self._m = len(maze)
        self._n = len(maze[0])
        self._room = room
        self._wall = wall
        self._start_pos = start_pos
        self._cheese = cheese
        self._cheese_pos = None
        self._cheese_dist = -1
        self._path = path

        self._directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self._parent_direction = {
            self._start_pos: (0, 0)
        }

    def _solve_dfs(self, x, y, dist=0):
        if self._cheese_pos is not None:
            return

        if self._cheese == self._maze[x][y]:
            self._cheese_pos = (x, y)
            self._cheese_dist = dist
            return

        for dx, dy in self._directions:
            nx, ny = x + dx, y + dy
            if (
                self._maze[nx][ny] == self._wall
                or (nx, ny) in self._parent_direction
            ):
                continue
            self._parent_direction[(nx, ny)] = (-dx, -dy)
            self._solve_dfs(nx, ny, dist + 1)

    def solve_dfs(self):
        self._solve_dfs(*self._start_pos)
        self._color_maze_path(self._retrieve_path(self._cheese_dist))

    def _retrieve_path(self, dist: int) -> list[tuple[int, int]]:
        assert self._cheese_pos is not None
        p = self._cheese_pos
        return [
            (
                p := (
                    p[0] + self._parent_direction[p[0], p[1]][0],
                    p[1] + self._parent_direction[p[0], p[1]][1]
                )
            ) for _ in range(dist)
        ]

    def _color_maze_path(self, path: list[tuple[int, int]]):
        for x, y in path:
            self._maze[x][y] = self._path


def solve_perfect_maze(maze, room: int | str = 0, wall: int | str = 1, cheese='.', path='+', start_pos=(1, 1)):
    _PerfectMazeSolver(maze, room, wall, cheese, path, start_pos).solve_dfs()


def print_maze(maze):
    """Imprime o labirinto no terminal, uma linha por vez.

    Parameters
    ----------
    maze : list[list]
        Matriz retornada por :func:`generate_maze`.
    """
    for row in maze:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    room, wall, cheese, path = ' ', '■', 'X', '·'

    maze = generate_maze(15, 15, room, wall, cheese)
    solve_perfect_maze(maze, room, wall, cheese, path)
    print_maze(maze)
