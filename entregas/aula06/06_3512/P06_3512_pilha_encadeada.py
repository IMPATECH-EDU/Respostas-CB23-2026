class _No:
    """Nó de uma lista simplesmente encadeada."""

    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class PilhaEncadeada:
    """Pilha implementada com uma lista simplesmente encadeada."""

    def __init__(self):
        """Cria uma pilha vazia. O(1)."""
        self._topo = None
        self._tamanho = 0

    def push(self, item):
        """Insere item no topo da pilha. O(1)."""
        novo = _No(item, self._topo)
        self._topo = novo
        self._tamanho += 1

    def pop(self):
        """Remove e retorna o item do topo. O(1)."""
        if self.esta_vazia():
            raise IndexError("não é possível retirar de uma pilha vazia")

        item = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return item

    def topo(self):
        """Retorna o item do topo sem removê-lo. O(1)."""
        if self.esta_vazia():
            raise IndexError("não é possível consultar uma pilha vazia")

        return self._topo.valor

    def esta_vazia(self):
        """Retorna True se a pilha estiver vazia. O(1)."""
        return self._tamanho == 0

    def len(self):
        """Retorna a quantidade de elementos da pilha. O(1)."""
        return self._tamanho

    def __repr__(self):
        """Retorna a representação da pilha do topo para a base. O(N)."""
        valores = []
        atual = self._topo

        while atual is not None:
            valores.append(repr(atual.valor))
            atual = atual.proximo

        return "PilhaEncadeada([" + ", ".join(valores) + "])"


if __name__ == "__main__":
    pilha = PilhaEncadeada()
    pilha.push(10)
    pilha.push(20)
    pilha.push(30)

    print(pilha)
    print("Topo:", pilha.topo())
    print("Removido:", pilha.pop())
    print("Tamanho:", pilha.len())
