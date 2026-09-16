import random

def dfs_iterative(m, n, room=0, wall=1, cheese='.'):
    """Gera um labirinto usando DFS iterativa.

    Parameters
    ----------
    m : int
        Número de linhas da grade lógica.
    n : int
        Número de colunas da grade lógica.
    room : any, optional
        Valor que representa uma sala no labirinto. O padrão é 0.
    wall : any, optional
        Valor que representa uma parede no labirinto. O padrão é 1.
    cheese : any, optional
        Valor que representa o queijo no labirinto. O padrão é '.'.

    Returns
    -------
    list[list]
        Matriz representando o labirinto gerado.
    """
    maze = [[wall] * (2 * n + 1) for i in range (2 * m + 1)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    pilha = [(0, 0)]
    maze[1][1] = room
    while pilha:
        x, y = pilha[-1]

        vizinhos_nao_visitados = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
                vizinhos_nao_visitados.append((nx, ny, dx, dy))
        if vizinhos_nao_visitados:
            nx, ny, dx, dy = random.choice(vizinhos_nao_visitados)
            maze[2 * x + 1 + dx][2 * y + 1 + dy] = room
            maze[2 * nx + 1][2 * ny + 1] = room 
            pilha.append((nx, ny))
        else:
            pilha.pop()
    while True:
        i = int(random.uniform(0, 2 * m + 1))
        j = int(random.uniform(0, 2 * n + 1))
        if 0 <= i < (2 * m + 1) and 0 <= j < (2 * n + 1) and maze[i][j] == room:
            maze[i][j] = cheese
            break
    return maze

def print_maze(maze):
    """"Imprime o labirinto no terminal, uma linha por vez."""
    for row in maze:
        print(' '.join(str(cell) for cell in row))


def encontrar_caminho_dfs(maze, inicio=(1, 1), cheese=".", wall=1):
  """Encontra o caminho do início até o queijo usando a lista nativa do Python como pilha (DFS)."""
  m_linhas = len(maze)
  n_colunas = len(maze[0])

  destino = None
  for r in range(m_linhas):
    for c in range(n_colunas):
      if maze[r][c] == cheese:
        destino = (r, c)
        break
    if destino:
      break

  if not destino:
    raise ValueError("Queijo não encontrado no labirinto.")

  pilha = [inicio]
  visitados = {inicio}
  pais = {inicio: None}
  direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

  while pilha:
    atual = pilha.pop()

    if atual == destino:
      break

    r, c = atual
    for dr, dc in direcoes:
      nr, nc = r + dr, c + dc
      if (
          0 <= nr < m_linhas
          and 0 <= nc < n_colunas
          and maze[nr][nc] != wall
          and (nr, nc) not in visitados
      ):
        visitados.add((nr, nc))
        pais[(nr, nc)] = atual
        pilha.append((nr, nc))

  caminho = []
  passo = destino
  while passo is not None:
    caminho.append(passo)
    passo = pais.get(passo)

  caminho.reverse()
  return caminho


def exibir_labirinto_com_caminho(maze, caminho, simbolo_caminho="•"):
  """Imprime o labirinto no terminal sobrepondo os passos do caminho."""
  matriz_exibicao = [list(map(str, row)) for row in maze]

  for r, c in caminho[:-1]:
    if (r, c) == (1, 1):
      matriz_exibicao[r][c] = "I" 
    else:
      matriz_exibicao[r][c] = simbolo_caminho

  for row in matriz_exibicao:
    print(" ".join(row))


if __name__ == "__main__":
  labirinto = dfs_iterative(m=5, n=7, room=" ", wall="W", cheese="*")
  caminho = encontrar_caminho_dfs(
      labirinto, inicio=(1, 1), cheese="*", wall="W"
  )

  print("--- Labirinto Resolvido ---")
  exibir_labirinto_com_caminho(labirinto, caminho)