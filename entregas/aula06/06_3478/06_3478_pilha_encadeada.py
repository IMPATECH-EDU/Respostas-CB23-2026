class _No:
    """Classe auxiliar privada que representa cada nó da lista encadeada."""
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class PilhaEncadeada:
    """Implementação de Pilha sobre lista simplesmente encadeada."""
    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def esta_vazia(self):
        """Retorna True quando não há elementos armazenados. Complexidade: O(1)"""
        return self._tamanho == 0

    def __len__(self):
        """Retorna a quantidade de elementos mantida pelo contador. Complexidade: O(1)"""
        return self._tamanho

    def push(self, item):
        """Insere um novo item no topo da pilha. Complexidade: O(1)"""
        novo_no = _No(item)
        novo_no.proximo = self._topo
        self._topo = novo_no
        self._tamanho += 1

    def pop(self):
        """Remove e retorna o item do topo; levanta IndexError se vazia. Complexidade: O(1)"""
        if self.esta_vazia():
            raise IndexError("A pilha está vazia. Não é possível remover elementos.")
        
        item = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return item

    def topo(self):
        """Retorna o item do topo sem removê-lo; levanta IndexError se vazia. Complexidade: O(1)"""
        if self.esta_vazia():
            raise IndexError("A pilha está vazia. Não há topo para visualizar.")
        
        return self._topo.valor

    def __repr__(self):
        """Representação textual legível, do topo para a base. Complexidade: O(N)"""
        elementos = []
        atual = self._topo
        while atual is not None:
            elementos.append(repr(atual.valor))
            atual = atual.proximo
        return "PilhaEncadeada([" + ", ".join(elementos) + "])"