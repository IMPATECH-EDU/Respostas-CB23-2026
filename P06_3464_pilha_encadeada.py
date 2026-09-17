class PilhaEncadeada:
    class _No:
        def __init__(self, valor):
            """Inicializa o Nó."""
            self.valor = valor
            self.proximo = None

    def __init__(self):
        """Inicializa a pilha."""
        self.No = None
        self._size = 0

    def push(self, item):
        """Insere um item na pilha.
        
        Parameters:
        -----------
        
        item : int
            O elemento que será inserido na pilha.
            
        Tempo de execução: O(1)
        -----------------------"""
        novo_No = self._No(item)
        novo_No.proximo = self.No
        self.No = novo_No
        self._size += 1

    def pop(self):
        """Remove o elemento no topo da pilha e o retorna.
        
        Returns:
        --------
        
        Object
            O elemento que foi removido
        
        Tempo de execução: O(1)
        -----------------------"""
        if self.No is None:
            raise IndexError("A pilha está vazia.")
        data = self.No.valor
        self.No = self.No.proximo
        self._size -= 1
        return data

    def topo(self):
        """Retorna o item no topo da pilha.
        
        Returns:
        --------
        
        Object
            O elemento que foi removido
            
        Tempo de execução: O(1)
        -----------------------"""
        if self.No is None:
            raise IndexError("A pilha está vazia.")
        return self.No.valor

    def esta_vazia(self):
        """Retorna um boolean que indica se a pilha está vazia ou não.
        
        Returns:
        --------
        
        bool
            True se a pilha está vazia. False no contrário.
            
        Temp o de execução: O(1)
        ------------------------"""
        if self.No is None:
            return True
        return False

    def __len__(self):
        """Retorna o tamanho da pilha.
        
        Returns:
        --------
        
        int
            O tamanho da pilha.
            
        Tempo de execução: O(1)
        -----------------------"""
        return self._size

    def __repr__(self):
        """Retorna uma string que é a representação padrão do objeto.
        
        Returns:
        --------
        
        str
            A representação padrão do objeto
            
        Tempo de execução: O(n)
        -----------------------"""
        rep = ''
        current = self.No
        if current is not None:
            while current.proximo is not None:
                rep += f"{current.valor} -> "
                current = current.proximo
            rep += f"{current.valor}"

        return rep

if __name__ == "__main__":
    pilha = PilhaEncadeada()

    print(pilha)

    pilha.push(1)
    pilha.push(2)
    pilha.push('a')


    print(pilha)

    print(pilha.pop())

    print(pilha)

    print(len(pilha))