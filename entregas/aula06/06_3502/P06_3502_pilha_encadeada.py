class ListaEncadeada:

    class No(): 
            def __init__(self, valor, proximo=None): 
                """Inicializa o Nó"""
                self.valor = valor
                self.proximo = proximo
    
    def __init__(self): 
        """Inicializa a Lista encadeada"""
        self.head = None
        self.comprimento = 0


class PilhaEncadeada(ListaEncadeada):

    def push(self, other): 
        """Adiciona no topo da pilha; complexidade O(1)."""
        self.head = self.No(other, self.head)
        self.comprimento += 1

    def pop(self): 
        """Retira um elemento do topo da pilha; complexidade O(1)."""
        if self.comprimento == 0:
            raise IndexError
        topo = self.head 
        self.head = topo.proximo
        self.comprimento -= 1
        return topo.valor

    def topo(self): 
        """Retorna o elemento do topo da pilha sem retirá-lo; complexidade O(1)"""
        if self.comprimento == 0:
            raise IndexError
        topo = self.head.valor
        return topo

    def esta_vazia(self): 
        """Indica se a pilha está vazia; complexidade O(1)."""
        return self.comprimento == 0

    def __len__(self): 
        """Retorna o comprimento da pilha; complexidade O(1)."""
        return self.comprimento

    def __repr__(self): 
        """Cria uma representação textual da pilha; complexidade O(n)."""
        no = self.head
        s = ""
        while no is not None:
            if s:
                s += f" -> {no.valor}"
            else:
                s += str(no.valor) 
            no = no.proximo

        return s

print(PilhaEncadeada.esta_vazia)
