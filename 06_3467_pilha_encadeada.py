class Node :
    def __init__(self, data) :
        self.data = data
        self.next = None

class PilhaEncadeada :
    def __init__(self) :
        self.head = None
        self.size = 0

    def __len__(self) :
        """
        Retorna o tamanho da Pilha
        """
        return self.size

    def __repr__(self) :

        """
        Retorna representação textual do topo para a base
        """
        if self.size == 0 :
            return '[]'
        
        ans = '['
        current = self.head

        while current.next is not None :
            ans += str(current.data) + ', '
            current = current.next

        ans += str(current.data) + ']'
        return ans
        
    def esta_vazia(self) :
        """
        Retorna True se a pilha estiver vazia e False se não.
        """
        return self.size == 0

    def push(self, item) :

        """
        Adiciona item ao topo da pilha em complexidade O(1)
        """

        if self.size == 0 :
            self.head = Node(item)
        else :
            item = Node(item)
            item.next, self.head = self.head, item

        self.size += 1

    def pop(self) :
        """ 
        Remove e retorna o item que está no topo da pilha em complexidade O(1)
        """
        
        if self.size == 0 :
            raise IndexError('Pop: A pilha está vazia')
        else :
            oldhead = self.head
            self.head = oldhead.next
            self.size -= 1
            return oldhead.data

    def topo(self) :

        """
        Retorna o item do topo da pilha em complexidade O(1)
        """

        if self.size == 0 :
            raise IndexError('Topo: A pilha está vazia')
        else :
            return self.head.data
