"""
Questão 1 - Pilha Encadeada

Implementação de uma pilha usando uma lista simplesmente encadeada,
construída manualmente.
"""


class _No:
    """Nó da lista simplesmente encadeada."""

    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class PilhaEncadeada:
    """
    Implementa o TAD Pilha usando uma lista simplesmente encadeada.
    """

    def __init__(self):
        """Cria uma pilha vazia. Complexidade: O(1)."""
        self._topo = None
        self._tamanho = 0

    def push(self, item):
        """
        Insere um item no topo da pilha.

        Complexidade: O(1).
        """
        novo_no = _No(item, self._topo)
        self._topo = novo_no
        self._tamanho += 1

    def pop(self):
        """
        Remove e retorna o item do topo da pilha.

        Levanta IndexError se a pilha estiver vazia.

        Complexidade: O(1).
        """
        if self._topo is None:
            raise IndexError("Não é possível remover: a pilha está vazia.")

        item = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1

        return item

    def topo(self):
        """
        Retorna o item que está no topo sem removê-lo.

        Levanta IndexError se a pilha estiver vazia.

        Complexidade: O(1).
        """
        if self._topo is None:
            raise IndexError("Não é possível consultar o topo: a pilha está vazia.")

        return self._topo.valor

    def esta_vazia(self):
        """
        Retorna True se a pilha estiver vazia.

        Complexidade: O(1).
        """
        return self._tamanho == 0

    def len(self):
        """
        Retorna a quantidade de elementos da pilha.

        O tamanho é mantido por um contador, portanto não é necessário
        percorrer os nós.

        Complexidade: O(1).
        """
        return self._tamanho

    def __repr__(self):
        """
        Retorna uma representação textual da pilha, do topo para a base.

        Complexidade: O(N).
        """
        valores = []

        atual = self._topo

        while atual is not None:
            valores.append(repr(atual.valor))
            atual = atual.proximo

        return "PilhaEncadeada([" + ", ".join(valores) + "])"