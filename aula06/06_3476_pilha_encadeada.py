class _No:
    """Classe auxiliar privada para nó de lista encadeada."""

    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class PilhaEncadeada:
    """Estrutura de dados Pilha sobre lista encadeada."""

    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def push(self, item):
        """Insere um item no topo da pilha.

        Complexidade de tempo: O(1)
        """
        self._topo = _No(item, self._topo)
        self._tamanho += 1

    def pop(self):
        """Remove e retorna o item do topo da pilha.

        Complexidade de tempo: O(1)
        """
        if self.esta_vazia():
            raise IndexError("Operação inválida: a pilha está vazia.")
        valor = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return valor

    def topo(self):
        """Retorna o item do topo sem removê-lo.

        Complexidade de tempo: O(1)
        """
        if self.esta_vazia():
            raise IndexError("Operação inválida: a pilha está vazia.")
        return self._topo.valor

    def esta_vazia(self):
        """Informa se a pilha está vazia.

        Complexidade de tempo: O(1)
        """
        return self._tamanho == 0

    def __len__(self):
        """Retorna a quantidade de elementos na pilha.

        Complexidade de tempo: O(1)
        """
        return self._tamanho

    def len(self):
        """Método auxiliar para obtenção da quantidade de elementos.

        Complexidade de tempo: O(1)
        """
        return len(self)

    def __repr__(self):
        """Representação textual da pilha, do topo para a base.

        Complexidade de tempo: O(N)
        """
        elementos = []
        atual = self._topo
        while atual is not None:
            elementos.append(repr(atual.valor))
            atual = atual.proximo
        return "Topo -> [" + ", ".join(elementos) + "]"

    def repr(self):
        """Método auxiliar de representação textual.

        Complexidade de tempo: O(N)
        """
        return repr(self)