import random

PAREDE = 1
CAMINHO = 0
DIRECOES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def gerar_labirinto(linhas, colunas):
    """Gera um labirinto perfeito usando DFS iterativo com pilha."""
    labirinto = [[PAREDE] * (2 * colunas + 1) for _ in range(2 * linhas + 1)]

    pilha = [(0, 0)]
    visitados = {(0, 0)}
    labirinto[1][1] = CAMINHO

    while pilha:
        x, y = pilha[-1]

        vizinhos = []
        for dx, dy in DIRECOES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < linhas and 0 <= ny < colunas and (nx, ny) not in visitados:
                vizinhos.append((nx, ny))

        if not vizinhos:
            pilha.pop()
            continue

        nx, ny = random.choice(vizinhos)

        # derruba a parede entre a celula atual e a nova
        labirinto[x + nx + 1][y + ny + 1] = CAMINHO
        labirinto[2 * nx + 1][2 * ny + 1] = CAMINHO

        visitados.add((nx, ny))
        pilha.append((nx, ny))

    celulas = [(i, j)
               for i in range(1, 2 * linhas, 2)
               for j in range(1, 2 * colunas, 2)
               if (i, j) != (1, 1)]
    queijo = random.choice(celulas)

    return labirinto, queijo


def dfs_iterativo(labirinto, inicio, objetivo):
    """Procura um caminho de inicio ate objetivo. Tempo e memoria O(V)."""
    pilha = [(inicio, None)]
    anterior = {}

    while pilha:
        pos, pai = pilha.pop()

        if pos in anterior:
            continue
        anterior[pos] = pai

        if pos == objetivo:
            caminho = [pos]
            while caminho[-1] != inicio:
                caminho.append(anterior[caminho[-1]])
            caminho.reverse()
            return caminho

        x, y = pos
        for dx, dy in DIRECOES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(labirinto) and 0 <= ny < len(labirinto[0]):
                if labirinto[nx][ny] == CAMINHO and (nx, ny) not in anterior:
                    pilha.append(((nx, ny), pos))

    return None


def mostrar_labirinto(labirinto, caminho, inicio, queijo):
    """Imprime o labirinto destacando o caminho encontrado."""
    marcados = set(caminho or [])

    for i in range(len(labirinto)):
        linha = ""
        for j in range(len(labirinto[0])):
            if (i, j) == inicio:
                linha += "🐭"
            elif (i, j) == queijo:
                linha += "🧀"
            elif (i, j) in marcados:
                linha += "🟩"
            elif labirinto[i][j] == PAREDE:
                linha += "⬛"
            else:
                linha += "⬜"
        print(linha)


def main():
    tamanho = 8
    inicio = (1, 1)

    labirinto, queijo = gerar_labirinto(tamanho, tamanho)

    print("LABIRINTO GERADO")
    mostrar_labirinto(labirinto, [], inicio, queijo)

    caminho = dfs_iterativo(labirinto, inicio, queijo)

    print("\nCAMINHO ENCONTRADO COM DFS ITERATIVO")
    if caminho is None:
        print("Nao foi encontrado um caminho ate o queijo.")
    else:
        print(f"Quantidade de movimentos: {len(caminho) - 1}\n")
        mostrar_labirinto(labirinto, caminho, inicio, queijo)


if __name__ == "__main__":
    main()