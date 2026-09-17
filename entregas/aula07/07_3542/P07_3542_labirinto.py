import random
from collections import deque
from copy import deepcopy


class GraphAdjMatrix:
    def __init__(self, adj_Matrix=None, node2index=None, edges=None):
        if edges is not None:
            self._adjacency, self._nd2idx, self._idx2n = self.edge_to_adj_matriz(
                edges
            )
        else:
            self._adjacency = (
                deepcopy(adj_Matrix) if adj_Matrix is not None else []
            )
            if node2index is not None:
                self._nd2idx = deepcopy(node2index)
                self._idx2n = {self._nd2idx[n]: n for n in self._nd2idx}
            elif self._adjacency:
                self._nd2idx = {i: i for i in range(len(self._adjacency))}
                self._idx2n = self._nd2idx
            else:
                self._nd2idx = {}
                self._idx2n = {}

    def adjacent(self, n1, n2):
        return bool(self._adjacency[self._nd2idx[n1]][self._nd2idx[n2]])

    def neighbors(self, node):
        neigh = []
        idx = self._nd2idx[node]
        for i in range(len(self._nd2idx)):
            if self._adjacency[idx][i] > 0:
                neigh.append(self._idx2n[i])
        return neigh

    def add_vertex(self, node):
        idx = len(self._nd2idx)
        self._nd2idx[node] = idx
        self._idx2n[idx] = node
        for i in range(idx):
            self._adjacency[i].append(0)
        self._adjacency.append([0] * (idx + 1))

    def add_edge(self, node1, node2, v=1):
        self._adjacency[self._nd2idx[node1]][self._nd2idx[node2]] = v

    @staticmethod
    def edge_to_adj_matriz(edges):
        nodes = set()
        for ed in edges:
            nodes.add(ed[0])
            nodes.add(ed[1])
        node2Index = {n: idx for idx, n in enumerate(nodes)}
        index2Node = {idx: n for n, idx in node2Index.items()}
        Adj_Matriz = [[0] * len(nodes) for _ in range(len(nodes))]
        for ed in edges:
            Adj_Matriz[node2Index[ed[0]]][node2Index[ed[1]]] = 1
        return Adj_Matriz, node2Index, index2Node


class Labirinto:
    def __init__(self, largura=15, altura=15):
        self.largura = largura if largura % 2 != 0 else largura + 1
        self.altura = altura if altura % 2 != 0 else altura + 1
        self.grid = [["#" for _ in range(self.largura)] for _ in range(self.altura)]
        self.grafo = GraphAdjMatrix()

    def gerar_dfs_iterativo(self):
        for y in range(self.altura):
            for x in range(self.largura):
                if x % 2 == 1 and y % 2 == 1:
                    self.grafo.add_vertex((x, y))

        pilha = [(1, 1)]
        visitados = {(1, 1)}
        self.grid[1][1] = " "

        while pilha:
            cx, cy = pilha[-1]
            vizinhos = []

            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = cx + dx, cy + dy
                if 1 <= nx < self.largura - 1 and 1 <= ny < self.altura - 1:
                    if (nx, ny) not in visitados:
                        vizinhos.append((nx, ny, dx, dy))

            if vizinhos:
                nx, ny, dx, dy = random.choice(vizinhos)
                self.grid[cy + dy // 2][cx + dx // 2] = " "
                self.grid[ny][nx] = " "
                
                self.grafo.add_edge((cx, cy), (nx, ny))
                self.grafo.add_edge((nx, ny), (cx, cy))

                visitados.add((nx, ny))
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