from P06_3458_pilha import PilhaEncadeada

class FilaEncadeada:
    """Implementação de Fila construída sobre duas instâncias de PilhaEncadeada."""

    def __init__(self):
        self.entrada = PilhaEncadeada()
        self.saida = PilhaEncadeada()
        self._len = 0

    def enfileirar(self, item):
        """Insere o item no fim da fila. Complexidade: O(1)"""
        self.entrada.push(item)
        self._len += 1

    def esta_vazia(self):
        """Retorna True quando não há elementos armazenados. Complexidade: O(1)"""
        return self._len == 0

    def __len__(self):
        """Retorna a quantidade de elementos da fila. Complexidade: O(1)"""
        return self._len

    def mover(self):
        """Método auxiliar para transferir elementos da pilha de entrada para a de saída."""
        if self.saida.esta_vazia():
            while not self.entrada.esta_vazia():
                self.saida.push(self.entrada.pop())

    def desenfileirar(self):
        """Remove e retorna o item da frente; levanta IndexError se vazia. Complexidade: O(1) amortizada"""
        if self.esta_vazia():
            raise IndexError("A fila está vazia.")
        self.mover()
        self._len -= 1
        return self.saida.pop()

    def frente(self):
        """Retorna o item da frente sem removê-lo; levanta IndexError se vazia. Complexidade: O(1) amortizada"""
        if self.esta_vazia():
            raise IndexError("A fila está vazia.")
        self.mover()
        return self.saida.topo()

    def __repr__(self):
        """Representação textual legível, da frente para o fim. Complexidade: O(N)"""
        self.mover()
        elementos = []
        temp = PilhaEncadeada()
        while not self.saida.esta_vazia():
            item = self.saida.pop()
            elementos.append(repr(item))
            temp.push(item)
        while not temp.esta_vazia():
            self.saida.push(temp.pop())
        return '[' + ', '.join(elementos) + ']'


if __name__ == "__main__":
    a = FilaEncadeada()