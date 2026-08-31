import importlib

modulo_pilha = importlib.import_module("06_3467_pilha_encadeada")
PilhaEncadeada = modulo_pilha.PilhaEncadeada

class FilaEncadeada :

    def __init__(self) :
        self.entrance = PilhaEncadeada()
        self.exit = PilhaEncadeada()

    def __len__(self) :
        """
        Retorna o tamanho da Fila
        """
        return len(self.entrance) + len(self.exit)

    def __repr__(self) :
        """
        Retorna representação textual da fila, da frente para o final
        """
        while not self.entrance.esta_vazia() :
            self.exit.push(self.entrance.pop())
        return str(self.exit)

    def enfileirar(self, item) :
        """
        Adiciona elemmento ao fim da fila.
        """
        self.entrance.push(item)

    def desenfileirar(self) :

        """
        Retorna o elemento no inicio da fila (primeiro a entrar)
        """

        if not self.exit.esta_vazia() :
            return self.exit.pop()
        
        if self.entrance.esta_vazia() :
            raise IndexError('A fila está vazia.')
        
        while not self.entrance.esta_vazia():
            self.exit.push(self.entrance.pop())

        return self.exit.pop()

    def frente(self) :
        """
        Retorna o elemento da frente da Fila, sem remover, em complexidade O(1) amortizada
        """
        if not self.exit.esta_vazia() :
            return self.exit.topo()
        
        if self.entrance.esta_vazia() :
            raise IndexError('A fila está vazia.')
        
        while not self.entrance.esta_vazia():
            self.exit.push(self.entrance.pop())

        return self.exit.topo()

    def esta_vazia(self) :
        """
        Retorna True se a fila estiver vazia e False caso contrário
        """
        return self.entrance.esta_vazia() and self.exit.esta_vazia()

