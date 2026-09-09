class No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class PilhaEncadeada:
    def __init__(self):
        self.cabeca = None
        self.tamanho = 0

    def push(self, valor):
        """
        Adiciona um novo elemento no topo da pilha.
        Complexidade: O(1).
        """
        novo_no = No(valor)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no
        self.tamanho += 1

    def pop(self):
        """
        Remove e retorna o elemento do topo da pilha.
        Complexidade: O(1).
        """
        if self.esta_vazia():
            raise IndexError("A pilha está vazia.")
        novo_topo = self.cabeca.proximo
        top = self.cabeca
        self.cabeca = novo_topo
        self.tamanho -= 1
        return top.valor

    def topo(self):
        """
        Retorna o elemento do topo da pilha sem removê-lo.
        Complexidade: O(1).
        """
        if self.esta_vazia():
            raise IndexError("A pilha está vazia.")
        return self.cabeca.valor

    def esta_vazia(self):
        """
        Confere se a pilha está vazia.
        Complexidade: O(1).
        """
        if self.cabeca == None:
            return True
        return False

    def __len__(self):
        """
        Retorna o tamanho da pilha.
        Complexidade: O(1)
        """
        return self.tamanho

    def __repr__(self):
        """
        Retorna uma representação em str.
        Comlexidade: O(N)
        """
        no_atual = self.cabeca
        pilha = ""
        while True:
            if no_atual == None:
                break
            pilha += f"{no_atual.valor}  🠒  "
            no_atual = no_atual.proximo
        return pilha
