import importlib

pilha = importlib.import_module("06_3533_pilha_encadeada")
No = pilha.No
PilhaEncadeada = pilha.PilhaEncadeada

class FilaEncadeada:
    def __init__(self):
        self.entrada = PilhaEncadeada()
        self.saida = PilhaEncadeada()
    def enfileirar(self,item):
        """
        Adiciona um novo elemento no final da fila.
        Complexidade: O(1).
        """
        self.entrada.push(item)
    def desenfileirar(self):
        """
        Remove e retorna o elemento do início da fila.
        Complexidade: O(1) no caso médio, O(n) no pior caso.
        """
        if self.saida.esta_vazia():
            while not self.entrada.esta_vazia():
                self.saida.push(self.entrada.pop())
        return self.saida.pop()
    def frente(self):
        """
        Retorna o elemento no início da fila sem removê-lo.
        Complexidade: O(1) no caso médio, O(n) no pior caso.
        """
        if self.saida.esta_vazia():
            while not self.entrada.esta_vazia():
                self.saida.push(self.entrada.pop())
        return self.saida.topo()
    def esta_vazia(self):
        """
        Confere se a fila está vazia.
        Complexidade: O(1)
        """
        return self.entrada.esta_vazia() and self.saida.esta_vazia()
    def __len__(self):
        """
        Retorna o tamanho da fila.
        Comlexidade: O(1)
        """
        return len(self.entrada) + len(self.saida)
    def __repr__(self):
        """
        Retorna uma representação em str.
        Complexiadade: O(N)
        """
        temp = PilhaEncadeada()
        while not self.entrada.esta_vazia():
            temp.push(self.entrada.pop())
        return f"{self.saida}{temp}"

