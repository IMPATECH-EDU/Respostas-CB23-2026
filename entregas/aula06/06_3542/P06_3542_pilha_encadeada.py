
class _No:
    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class PilhaEncadeada:
    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def push(self, item):
        """Insere o item no topo. Complexidade: O(1)"""
        novo_no = _No(item, self._topo)
        self._topo = novo_no
        self._tamanho += 1

    def pop(self):
        """Remove e retorna o topo. Complexidade: O(1)"""
        if self.esta_vazia():
            raise IndexError("A pilha está vazia. Não é possível remover elementos.")
        
        item_removido = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return item_removido

    def topo(self):
        """Retorna o topo sem remover. Complexidade: O(1)"""
        if self.esta_vazia():
            raise IndexError("A pilha está vazia. Não há topo a ser exibido.")
        return self._topo.valor

    def esta_vazia(self):
        """Retorna True se vazia. Complexidade: O(1)"""
        return self._tamanho == 0

    def __len__(self):
        """Retorna a quantidade de elementos. Complexidade: O(1)"""
        return self._tamanho

    def __repr__(self):
        """Representação textual do topo à base. Complexidade: O(N)"""
        elementos = []
        atual = self._topo
        while atual is not None:
            elementos.append(repr(atual.valor))
            atual = atual.proximo
        return f"PilhaEncadeada(Topo -> [{', '.join(elementos)}])"