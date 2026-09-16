class _No:
    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class PilhaEncadeada:
    """Pilha implementada sobre uma lista simplesmente encadeada."""

    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def push(self, item):
        """Insere um item no topo da pilha. O(1)"""
        novo_no = _No(item, self._topo)
        self._topo = novo_no
        self._tamanho += 1

    def pop(self):
        """Remove e retorna o item do topo. Levanta IndexError se vazia. O(1)"""
        if self.esta_vazia():
            raise IndexError("A pilha esta vazia.")
        valor = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return valor

    def topo(self):
        """Retorna o item do topo sem remove-lo. Levanta IndexError se vazia. O(1)"""
        if self.esta_vazia():
            raise IndexError("A pilha esta vazia.")
        return self._topo.valor

    def esta_vazia(self):
        """Retorna True se a pilha nao contiver elementos. O(1)"""
        return self._tamanho == 0

    def __len__(self):
        """Retorna a quantidade de elementos na pilha. O(1)"""
        return self._tamanho

    def __repr__(self):
        """Representacao textual da pilha, do topo para a base. O(N)"""
        elementos = []
        atual = self._topo
        while atual is not None:
            elementos.append(repr(atual.valor))
            atual = atual.proximo
        return f"PilhaEncadeada([{', '.join(elementos)}])"