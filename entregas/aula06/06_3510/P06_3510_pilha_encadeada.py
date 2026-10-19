class No:
    def __init__(self, valor):
        self.valor = valor
        self.next = None

class PilhaEncadeada:
    def __init__(self):
        self.head = None
        self.quant = 0

    def push(self, valor):
        """
        Insere o item passado como argumento no topo da pilha, tornando-o a cabeça, apontando para a cabeça anterior.
        Complexidade constante, O(1).
        """

        item = No(valor)
        if self.head is None:
            self.head = item
        else:
            item.next = self.head
            self.head = item
        self.quant += 1

    def pop(self):
        """
        Remove o item do topo e retorna seu valor. Levanta 'IndexError' caso a pilha estiver vazia e interrompe o programa.
        Complexidade constante, O(1).
        """

        if self.head is None:
            raise IndexError("Pilha vazia.")
        else:
            top = self.head.valor
            self.head = self.head.next
            self.quant -= 1
        return top

    def topo(self):
        """
        Retorna o valor do item no topo, mas não o remove. Levanta 'IndexError' caso a pilha estiver vazia e interrompe o programa.
        Complexidade constante, O(1).
        """

        if self.head is None:
            raise IndexError("Pilha vazia.")
        top = self.head.valor
        return top

    def esta_vazia(self):
        """
        Retorna True caso a pilha estiver vazia.
        Complexidade constante, O(1).
        """
        
        if self.head is None:
            return True
        else:
            return False
        

    def __len__(self):
        """
        Retorna o número de elementos da pilha.
        Complexidade constante, O(1).
        """

        return self.quant

    def __repr__(self):
        """
        Retorna uma representação textual da pilha, item a item, começando do topo.
        Complexidade linear, O(n).
        """

        atual = self.head
        if atual is None:
            texto = ''
        else:    
            texto = f'{atual.valor}'
            while atual.next is not None:
                texto = texto + f' --> {atual.next.valor}'
                atual = atual.next
        return texto


        

        
