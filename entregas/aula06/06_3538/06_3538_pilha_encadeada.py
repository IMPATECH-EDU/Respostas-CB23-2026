class PilhaEncadeada:
    """
    Estrutura de dados Pilha (LIFO) baseada em lista simplesmente encadeada.
    """
    class _No:
        def __init__(self, item):
            self.item = item
            self.proximo = None

    def __init__(self):
        """
        Inicializa uma pilha vazia.
        Complexidade: O(1)
        """
        self._topo = None
        self.tamanho = 0

    def push(self, item):
        """
        Insere o item no topo da pilha.
        Complexidade: O(1)
        """
        novo_no = self._No(item)
        novo_no.proximo = self._topo
        self._topo = novo_no
        self.tamanho += 1

    def pop(self):
        """
        Remove e retorna o item do topo.
        Levanta IndexError se a pilha estiver vazia.
        Complexidade: O(1)
        """
        if self.tamanho > 0:
            no_removido = self._topo
            self._topo = self._topo.proximo
            self.tamanho -= 1
            return no_removido.item
        else: 
            raise IndexError("A pilha está vazia")
        
    def topo(self):
        """
        Retorna o item do topo sem removê-lo.
        Levanta IndexError se a pilha estiver vazia.
        Complexidade: O(1)
        """
        if self.tamanho >= 1:
            return self._topo.item
        else:
            raise IndexError("A pilha está vazia")
        
    def esta_vazia(self):
        """
        Retorna True quando não há elementos armazenados.
        Complexidade: O(1)
        """
        if self.tamanho == 0:
            return True
        else:
            return False
        
    def __len__(self):
        """
        Retorna a quantidade de elementos na pilha.
        Complexidade: O(1)
        """
        return self.tamanho
    
    def __repr__(self):
        """
        Representação textual legível, do topo para a base.
        Complexidade: O(N)
        """
        if self.tamanho == 0:
            return ""
        
        texto = ""
        atual = self._topo
        while atual:
            texto += f"{atual.item} -> "
            atual = atual.proximo
        return texto