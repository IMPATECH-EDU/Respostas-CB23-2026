from P06_3464_pilha_encadeada import PilhaEncadeada

class FilaEncadeada():
    def __init__(self):
        """Inicializa a fila"""
        self._Pilha_1 = PilhaEncadeada()
        self._Pilha_2 = PilhaEncadeada()

        self._size = 0

    def enfileirar(self, item):
        """Adiciona um elemento no final da fila.

        Parameters:
        -----------
        item : int
            Elemento a ser adicionado na fila
        
        Tempo de execução: O(1)
        ------------------
        """
        self._Pilha_1.push(item)
        self._size += 1

    def desenfileirar(self):
        """Remove um elemento do início da fila.
        
        Returns:
        --------
        
        Object
            Elemento removido do início da fila

        Tempo de execução: O(1) amortizado
        ----------------------------------
        """
        if len(self._Pilha_2) == 0:
            if len(self._Pilha_1) == 0:
                raise IndexError("A fila está vazia.")

            #Move os elementos para a pilha 2
            while len(self._Pilha_1) > 0:
                self._Pilha_2.push(self._Pilha_1.pop())

            self._size -= 1
            return self._Pilha_2.pop()
        self._size -= 1
        return self._Pilha_2.pop()

    def frente(self):
        """Retorna o elemento no início da fila.
        
        Returns:
        --------
        
        Object
            Elemento no início da fila
        
        Tempo de execução: O(1) amortizado
        ----------------------------------"""
        if len(self._Pilha_2) == 0:
            if len(self._Pilha_1) == 0:
                raise IndexError("A fila está vazia.")

            #Transferência de elementos entre as pilhas
            while len(self._Pilha_1) > 0:
                self._Pilha_2.push(self._Pilha_1.pop())
        return self._Pilha_2.topo()

    def esta_vazia(self):
        """Retorna um boolean que indica se a fila está vazia ou não.

        Returns:
        --------

        bool
            True se a lista está vazia. False no contrário.

        Tempo de execução: O(1)
        ----------------------
        """
        return len(self) == 0

    def __len__(self):
        """Retorna o tamanho da fila.
        
        Returns:
        --------
        
        int 
            Tamanho da fila
        
        Tempo de execução: O(1)
        -----------------------"""
        return self._size

    def __repr__(self):
        """Retorna uma string com a formatação padrão do objeto.
        
        Returns:
        --------
        
        str
            Formatação padrão do objeto
            
        Tempo de execução: O(n)
        -----------------------
        """
        rep = ''
        if len(self._Pilha_2) > 0:
            rep = f"{self._Pilha_2}"
            if len(self._Pilha_1) > 0:
                rep += " -> "
        #Move todos (exceto o último) elemento da pilha 1 para a pilha 2
        target = len(self._Pilha_1) #Armazena o número de elementos originalmente na pilha 1
        while len(self._Pilha_1) > 0:
            self._Pilha_2.push(self._Pilha_1.pop())

        #Move de volta os elementos da pilha 1 enquanto formata os valores
        while target > 1:
            self._Pilha_1.push(self._Pilha_2.pop())
            rep += f"{self._Pilha_1.topo()} -> "
            target -= 1

        if target == 1:
            self._Pilha_1.push(self._Pilha_2.pop())
            rep += f"{self._Pilha_1.topo()}"

        return rep

if __name__ == "__main__":
    fila = FilaEncadeada()

    print(fila)

    fila.enfileirar(1)
    fila.enfileirar(2)
    fila.enfileirar(3)

    print(fila)

    fila.enfileirar(4)
    print(fila)
    print(fila.desenfileirar())

    print(fila)

    fila.enfileirar(5)
    print(fila)

    print(fila.desenfileirar())
    print(fila)

    print(fila.frente())

    print(f"LEN: {len(fila)}")
    print(fila.esta_vazia())

    while len(fila) > 0:
        print(fila.desenfileirar())

    print(fila)
    print(fila.esta_vazia())