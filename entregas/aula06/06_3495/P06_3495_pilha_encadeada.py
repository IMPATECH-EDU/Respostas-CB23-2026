class _No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class PilhaEncadeada:
    def __init__(self):
        self.head = None
        self.size = 0

    def push(self, item):
        '''
            Insere o item no topo da pilha,
            tem complexidade de tempo O(1).
        '''
        self.size += 1
        head = self.head
        self.head = _No(item)
        if head:
            self.head.proximo = head

    def pop(self):
        '''
            Remove e retorna o item do topo da pilha;
            levanta IndexError se a pilha estiver vazia.
            Tem complexidade de tempo O(1).
        '''
        if self.esta_vazia():
            raise IndexError("Não é possível realizar pop() em pilha vazia.")
        else:
            self.size -= 1
            head = self.head
            proximo = self.head.proximo
            if proximo:
                self.head = proximo
            else:
                self.head = None
            return  head.valor

    def topo(self):
        '''
            Retorna o item do topo da pilha sem removê-lo; 
            levanta IndexError se a pilha estiver vazia.
            Tem complexidade de tempo O(1).
        '''
        if self.esta_vazia():
            raise IndexError("Não é possível acessar o topo de pilha vazia")
        return self.head.valor

    def esta_vazia(self):
        '''
            Retorna True quando não há elementos armazenados na pilha
            e False quando há elementos armazenados.
            Tem complexidade de tempo O(1).
        '''
        if len(self) == 0:
            return True
        else:
            return False

    def __len__(self):
        '''
            Retorna a quantidade de elementos da pilha.
            Tem complexidade de tempo O(1).
        '''
        return self.size

    def __repr__(self):
        '''
            Retorna uma representação textual legível da pilha.
            Se a pilha estiver vazia retorna uma string vazia.
            Caso contrário, cada elemento da pilha é escrito em uma linha, 
            sendo que na primeira linha é apresentado o elemento do topo 
            da pilha e na última linha é apresentado o elemento do final da pilha.
            Tem complexidade de tempo O(N).
        '''
        s = ""
        atual = self.head
        if atual:
            s+= f"{atual.valor}"
            while atual.proximo:
                s += f"\n{atual.proximo.valor}"
                atual = atual.proximo
        return s

