import random
from collections import deque


class Labirinto:
    def __init__(self, largura=15, altura=15):
        self.largura = largura if largura % 2 != 0 else largura + 1
        self.altura = altura if altura % 2 != 0 else altura + 1
        self.grid = [["#" for _ in range(self.largura)] for _ in range(self.altura)]

    def gerar_dfs_iterativo(self):
        pilha = [(1, 1)]
        self.grid[1][1] = " "

        while pilha:
            cx, cy = pilha[-1]
            vizinhos = []

            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = cx + dx, cy + dy
                if 1 <= nx < self.largura - 1 and 1 <= ny < self.altura - 1:
                    if self.grid[ny][nx] == "#":
                        vizinhos.append((nx, ny, dx, dy))

            if vizinhos:
                nx, ny, dx, dy = random.choice(vizinhos)
                self.grid[cy + dy // 2][cx + dx // 2] = " "
                self.grid[ny][nx] = " "
                pilha.append((nx, ny))
            else:
                pilha.pop()

        self.grid[1][1] = "P"
        self.grid[self.altura - 2][self.largura - 2] = "Q"

    def encontrar_caminho(self, inicio=(1, 1), fim=None):
        if fim is None:
            fim = (self.largura - 2, self.altura - 2)

        fila = deque([inicio])
        veio_de = {inicio: None}

        while fila:
            atual = fila.popleft()
            if atual == fim:
                break

            cx, cy = atual
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.largura and 0 <= ny < self.altura:
                    if self.grid[ny][nx] != "#" and (nx, ny) not in veio_de:
                        veio_de[(nx, ny)] = atual
                        fila.append((nx, ny))

        if fim not in veio_de:
            return []

        caminho = []
        passo = fim
        while passo:
            caminho.append(passo)
            passo = veio_de[passo]
        caminho.reverse()
        return caminho

    def exibir(self, caminho=None):
        grid_copia = [linha[:] for linha in self.grid]
        if caminho:
            for x, y in caminho:
                if grid_copia[y][x] not in ("P", "Q"):
                    grid_copia[y][x] = "."

        for linha in grid_copia:
            print("".join(linha))


if __name__ == "__main__":
    lab = Labirinto(21, 21)
    lab.gerar_dfs_iterativo()
    caminho = lab.encontrar_caminho()
    lab.exibir(caminho)