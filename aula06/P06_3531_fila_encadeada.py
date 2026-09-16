from P06_3531_pilha_encadeada import PilhaEncadeada


class FilaEncadeada:
    """
    Estrutura de dados Fila (FIFO) implementada utilizando duas pilhas encadeadas.
    """

    def __init__(self):
        """
        Inicializa uma fila encadeada vazia composta por duas pilhas internas.

        Complexidade de tempo: O(1)
        """
        self.pilha1 = PilhaEncadeada()
        self.pilha2 = PilhaEncadeada()

    def enfileirar(self, valor):
        """
        Insere um novo elemento no final da fila.

        Complexidade de tempo: O(1)
        """
        self.pilha1.push(valor)

    def desenfileirar(self):
        """
        Remove e retorna o elemento localizado no início da fila.
        Lança IndexError se a fila estiver vazia.

        Complexidade de tempo: O(1) amortizado (Pior caso O(N) na troca de pilhas)
        """
        if self.esta_vazia():
            raise IndexError("A fila está vazia.")

        if self.pilha2.esta_vazia():
            while not self.pilha1.esta_vazia():
                self.pilha2.push(self.pilha1.pop())

        return self.pilha2.pop()

    def frente(self):
        """
        Retorna o elemento do início da fila sem removê-lo.
        Lança IndexError se a fila estiver vazia.

        Complexidade de tempo: O(1) amortizado (Pior caso O(N) na troca de pilhas)
        """
        if self.esta_vazia():
            raise IndexError("A fila está vazia.")

        if self.pilha2.esta_vazia():
            while not self.pilha1.esta_vazia():
                self.pilha2.push(self.pilha1.pop())

        return self.pilha2.topo()

    def esta_vazia(self):
        """
        Verifica se a fila não possui elementos em nenhuma das pilhas.

        Complexidade de tempo: O(1)
        """
        return self.pilha1.esta_vazia() and self.pilha2.esta_vazia()

    def __len__(self):
        """
        Retorna a quantidade total de elementos armazenados na fila.

        Complexidade de tempo: O(1)
        """
        return len(self.pilha1) + len(self.pilha2)

    def __repr__(self):
        """
        Retorna a representação em string da fila, do início ao fim, sem alterar o estado interno.

        Complexidade de tempo: O(N)
        """
        if self.esta_vazia():
            return "FilaEncadeada(Fila Vazia)"

        elementos = []


        atual = self.pilha2.cabeca
        while atual is not None:
            elementos.append(str(atual.valor))
            atual = atual.proximo


        temp = PilhaEncadeada()
        atual = self.pilha1.cabeca
        while atual is not None:
            temp.push(atual.valor)
            atual = atual.proximo

        atual = temp.cabeca
        while atual is not None:
            elementos.append(str(atual.valor))
            atual = atual.proximo

        return f"FilaEncadeada({' -> '.join(elementos)})"