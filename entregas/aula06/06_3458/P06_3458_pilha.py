class _No:
    """Nó da lista encadeada."""
    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo

    def __str__(self):
        return str(self.valor)


class PilhaEncadeada:
    """Implementação de Pilha sobre Lista Encadeada."""

    def __init__(self):
        self.len = 0
        self.top = None

    def push(self, item):
        """Insere o item no topo da pilha. Complexidade: O(1)"""
        self.top = _No(item, self.top)
        self.len += 1

    def pop(self):
        """Remove e retorna o item do topo; levanta IndexError se vazia. Complexidade: O(1)"""
        if self.esta_vazia():
            raise IndexError("A pilha está vazia.")
        temp = self.top
        self.top = self.top.proximo
        self.len -= 1
        return temp.valor 

    def topo(self):
        """Retorna o item do topo sem removê-lo; levanta IndexError se vazia. Complexidade: O(1)"""
        if self.esta_vazia():
            raise IndexError("A pilha está vazia.")
        return self.top.valor
    def esta_vazia(self):
        """Retorna True quando não há elementos armazenados. Complexidade: O(1)"""
        return self.len == 0

    def __repr__(self):
        """Representação textual legível, do topo para a base. Complexidade: O(N)"""
        itens = []
        t = self.top
        while t is not None:
            itens.append(repr(t.valor))
            t = t.proximo
        return '[' + ', '.join(itens) + ']'

    def __len__(self):
        """Retorna a quantidade de elementos. Complexidade: O(1)"""
        return self.len


if __name__ == "__main__":
    a = PilhaEncadeada()

