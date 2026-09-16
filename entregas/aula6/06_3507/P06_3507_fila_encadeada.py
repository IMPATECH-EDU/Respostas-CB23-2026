"""
Questão 2 - Fila construída sobre duas pilhas.

"""

from P06_3507_pilha_encadeada import PilhaEncadeada


class FilaEncadeada:
    """
    Implementa o TAD Fila utilizando duas PilhaEncadeada.

    pilha_entrada:
        recebe novos elementos.

    pilha_saida:
        fornece os elementos na ordem FIFO.
    """

    def __init__(self):
        """Cria uma fila vazia. Complexidade: O(1)."""
        self._entrada = PilhaEncadeada()
        self._saida = PilhaEncadeada()
        self._tamanho = 0

    def enfileirar(self, item):
        """
        Insere um item no final da fila.

        Complexidade: O(1).
        """
        self._entrada.push(item)
        self._tamanho += 1

    def _transferir(self):
        """
        Transfere elementos da pilha de entrada para a pilha de saída.

        A transferência ocorre somente quando a pilha de saída está vazia.

        Complexidade:
            O(N) quando ocorre uma transferência.
            A transferência é O(1) amortizada por elemento.
        """
        if self._saida.esta_vazia():
            while not self._entrada.esta_vazia():
                self._saida.push(self._entrada.pop())

    def desenfileirar(self):
        """
        Remove e retorna o primeiro elemento da fila.

        Levanta IndexError se a fila estiver vazia.

        Complexidade:
            O(N) em uma chamada que exige transferência.
            O(1) amortizada.
        """
        if self.esta_vazia():
            raise IndexError("Não é possível desenfileirar: a fila está vazia.")

        self._transferir()

        item = self._saida.pop()
        self._tamanho -= 1

        return item

    def frente(self):
        """
        Retorna o primeiro elemento da fila sem removê-lo.

        Levanta IndexError se a fila estiver vazia.

        Complexidade:
            O(N) se for necessária uma transferência.
            O(1) amortizada.
        """
        if self.esta_vazia():
            raise IndexError("Não é possível consultar a frente: a fila está vazia.")

        self._transferir()

        return self._saida.topo()

    def esta_vazia(self):
        """
        Retorna True se a fila estiver vazia.

        Complexidade: O(1).
        """
        return self._tamanho == 0

    def len(self):
        """
        Retorna a quantidade de elementos da fila.

        Complexidade: O(1).
        """
        return self._tamanho

    def __repr__(self):
        """
        Retorna uma representação textual da fila, da frente para o fim.

        Complexidade: O(N).
        """
        valores = []

        
        temporaria = PilhaEncadeada()

        while not self._saida.esta_vazia():
            item = self._saida.pop()
            valores.append(repr(item))
            temporaria.push(item)

        while not temporaria.esta_vazia():
            self._saida.push(temporaria.pop())

        entrada_temporaria = PilhaEncadeada()

        while not self._entrada.esta_vazia():
            item = self._entrada.pop()
            entrada_temporaria.push(item)

        entrada_valores = []

        while not entrada_temporaria.esta_vazia():
            item = entrada_temporaria.pop()
            entrada_valores.append(repr(item))
            self._entrada.push(item)

        return "FilaEncadeada([" + ", ".join(reversed(entrada_valores)) + (
            ", " if valores and entrada_valores else ""
        ) + ", ".join(valores) + "])"