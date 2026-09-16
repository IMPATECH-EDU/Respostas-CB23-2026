class _No:

    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo

class PilhaEncadeada:

    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def push(self, item):
        """
        Insere um item no topo da pilha.

        Complexidade: O(1)
        """

        novo_item = _No(item)

        novo_item.proximo = self._topo
        self._topo = novo_item
        self._tamanho += 1

    def pop(self):
        """
        Remove e retorna o item do topo da pilha.

        Levanta IndexError se a pilha estiver vazia.

        Complexidade: O(1)
        """

        if self._topo is None:
            raise IndexError("A pilha está vazia.")

        item = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1

        return item

    def topo(self):
        """
        Retorna o item do topo sem removê-lo.

        Levanta IndexError se a pilha estiver vazia.

        Complexidade: O(1)
        """

        if self._topo is None:
            raise IndexError("A pilha está vazia.")

        return self._topo.valor

    def esta_vazia(self):
        """
        Retorna True se a pilha estiver vazia.

        Complexidade: O(1)
        """

        return self._topo is None

    def __len__(self):
        """
        Retorna a quantidade de elementos da pilha.

        Complexidade: O(1)
        """

        return self._tamanho

    def __repr__(self):
        """
        Retorna uma representação da pilha do topo para a base.

        Complexidade: O(N)
        """

        pilha = ""
        atual = self._topo

        while atual is not None:

            if pilha != "":
                pilha += " -> "

            pilha += str(atual.valor)
            atual = atual.proximo

        return pilha


