class Nodo:
    """
    Representa um nó individual de uma estrutura encadeada.
    """
    def __init__(self, valor):
        """
        Inicializa o nó com um valor e define o ponteiro para o próximo elemento como None.

        Complexidade de tempo: O(1)
        """
        self.valor = valor
        self.proximo = None


class PilhaEncadeada:
    """
    Estrutura de dados Pilha (LIFO) armazenada via encadeamento de nós.
    """
    def __init__(self):
        """
        Inicializa uma pilha encadeada vazia.

        Complexidade de tempo: O(1)
        """
        self.cabeca = None
        self.tamanho = 0

    def push(self, valor):
        """
        Insere um novo elemento no topo da pilha.

        Complexidade de tempo: O(1)
        """
        novo_nodo = Nodo(valor)
        novo_nodo.proximo = self.cabeca
        self.cabeca = novo_nodo
        self.tamanho += 1

    def pop(self):
        """
        Remove e retorna o elemento do topo da pilha.
        Lança IndexError se a pilha estiver vazia.

        Complexidade de tempo: O(1)
        """
        if self.cabeca is None:
            raise IndexError("A pilha está vazia.")
        
        valor = self.cabeca.valor
        self.cabeca = self.cabeca.proximo
        self.tamanho -= 1
        return valor

    def topo(self):
        """
        Retorna o valor armazenado no topo da pilha sem removê-lo.
        Lança IndexError se a pilha estiver vazia.

        Complexidade de tempo: O(1)
        """
        if self.cabeca is None:
            raise IndexError("A pilha está vazia.")
        return self.cabeca.valor

    def esta_vazia(self):
        """
        Verifica se a pilha não possui elementos.

        Complexidade de tempo: O(1)
        """
        return self.cabeca is None

    def __len__(self):
        """
        Retorna a quantidade total de elementos armazenados na pilha.

        Complexidade de tempo: O(1)
        """
        return self.tamanho

    def __repr__(self):
        """
        Retorna a representação em string da pilha, do topo até a base.

        Complexidade de tempo: O(N)
        """
        if self.esta_vazia():
            return "PilhaEncadeada(Pilha Vazia)"

        atual = self.cabeca
        elementos = []

        while atual is not None:
            elementos.append(str(atual.valor))
            atual = atual.proximo

        return f"PilhaEncadeada({' -> '.join(elementos)})"