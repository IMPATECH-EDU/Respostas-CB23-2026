# o nome do arquivo teve que ser esse pois o python não permite importar arquivos py que começam com número
class _No:
    def __init__(self, data):
        """Inicializa um nó para a estrutura encadeada contendo o valor e o ponteiro para o próximo nó.
        
        Complexidade de tempo: O(1)
        """
        self.proximo = None
        self.valor = data


class PilhaEncadeada:
    def __init__(self):
        """Inicializa uma pilha encadeada vazia.
        
        Complexidade de tempo: O(1)
        """
        self.tamanho = 0
        self.head = None

    def push(self, item):
        """Insere um novo elemento no topo da pilha.
        
        Complexidade de tempo: O(1)
        """
        n = _No(item)
        n.proximo = self.head
        self.head = n
        self.tamanho += 1

    def __repr__(self):
        """Retorna uma representação em formato de string de todos os elementos da pilha.
        
        Complexidade de tempo: O(n), onde n é a quantidade de elementos na pilha.
        """
        texto = ""
        if self.tamanho != 0:
            n = self.head
            texto += f"{n.valor}"
            n = n.proximo
            for _ in range(self.tamanho - 1):
                texto += f" → {n.valor}"
                n = n.proximo
        return texto

    def __len__(self):
        """Retorna a quantidade de elementos armazenados na pilha.
        
        Complexidade de tempo: O(1)
        """
        return self.tamanho

    def esta_vazia(self):
        """Verifica se a pilha está vazia.
        
        Complexidade de tempo: O(1)
        """
        return self.tamanho == 0

    def topo(self):
        """Retorna o valor do elemento no topo da pilha sem removê-lo.
        
        Complexidade de tempo: O(1)
        """
        if self.tamanho == 0:
            raise IndexError("Pilha vazia")
        return self.head.valor

    def pop(self):
        """Remove e retorna o elemento localizado no topo da pilha.
        
        Complexidade de tempo: O(1)
        """
        if self.tamanho == 0:
            raise IndexError("Pilha vazia")
        n = self.head
        self.head = n.proximo
        self.tamanho -= 1
        return n.valor