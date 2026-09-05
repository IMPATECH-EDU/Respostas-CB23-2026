class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        if not self.head:
            self.head = Node(value)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(value)

    def __str__(self):
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        return ' -> '.join(values)

    def search(self, value):
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def remove(self, value):
        if self.head.value == value:
            self.head = self.head.next
        else:
            current = self.head
            while current.next:
                if current.next.value == value:
                    current.next = current.next.next
                    return
                current = current.next


class PilhaEncadeada(LinkedList):
    def __init__(self):
        super().__init__()
        self._len = 0


    def push(self, item):
        """
        Insere o item no topo da pilha
        
        custo: O(1)
        """
        node = Node(item)
        tmp = self.head
        self.head = node
        node.next = tmp
        self._len += 1

    def esta_vazia(self):
        """
        Retorna se está vazia ou não

        custo: O(1)
        """
        return self.head == None

    def pop(self):
        """
        Remove e retorna o item do topo da pilha

        custo: O(1)
        """
        if self.esta_vazia():
            raise IndexError("A pilha está vazia")
        value = self.head.value
        self.head = self.head.next
        self._len -= 1
        return value


    def topo(self):
        """
        Retorna o item do topo sem removê-lo

        custo: O(1)
        """
        if self.esta_vazia():
            raise IndexError("A pilha está vazia")
        return self.head.value


    def __len__(self):
        """
        Retorna o comprimento da pilha.

        rtype: int
        custo: O(1)
        """
        return self._len


    def __repr__(self):
        """
        Representação detalhada do estado atual da pilha.

        rtype: str
        custo: O(N)
        """
        return super().__str__()


def main():
    
    pilha = PilhaEncadeada()
    pilha.push(10)
    pilha.push(20)
    pilha.push(30)
    print(pilha)
    pilha.pop()
    print(pilha)
    print(pilha.esta_vazia())
    print(len(pilha))
    print(pilha.topo())
    pilha.append(10)

if __name__ == "__main__":
    main()