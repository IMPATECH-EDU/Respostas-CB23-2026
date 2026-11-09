class No:
    def __init__(self, valor, proximo):
        self.valor = valor
        self.proximo = proximo


class PilhaEncadeada:
    def __init__(self, head = None):
        self.head = No(head, None)
        if self.head.valor == None:
            self.tamanho = 0
        else:
            self.tamanho = 1

    def push(self, valor):
        '''Insere o item no topo da pilha. Complexidade O(1).'''
        self.tamanho += 1
        if self.head.valor == None:
            self.head = No(valor, None)
        else:
            self.head = No(valor, self.head)

    def pop(self):
        '''Remove e retorna o item do topo; levanta IndexError se a pilha estiver vazia. Complexidade O(1).'''
        if self.tamanho == 0:
            raise IndexError("Erro: A pilha está vazia!")
        elif self.head.proximo == None:
            self.tamanho -= 1
            atual = self.head.valor
            self.head.valor = None
            self.head.proximo = None
            return atual
        else:
            self.tamanho -= 1
            atual = self.head.valor
            self.head.valor = self.head.proximo.valor
            self.head = self.head.proximo
            return atual

    def topo(self):
        '''Retorna o item do topo sem removê-lo; levanta IndexError se a pilha estiver vazia. Complexidade O(1).'''
        if self.head.valor == None:
            raise IndexError("Erro: A pilha está vazia!")
        else:
            return self.head.valor

    def esta_vazia(self):
        '''Retorna True quando não há elementos armazenados. Complexidade O(1).'''
        if self.tamanho == 0:
            return True
        else:
            return False

    def len(self):
        "Retorna a quantidade de elementos. Complexidade O(1)."
        return self.tamanho

    def repr(self):
        '''Representação textual legível, do topo para a base;
        levanta IndexError se a pilha estiver vazia. Complexidade O(n).'''
        if self.head.valor == None:
            raise IndexError("Erro: A pilha está vazia!")
        else:
            tam_ref = self.tamanho
            no_ref = self.head
            while tam_ref != 1:
                print(no_ref.valor, end=", ")
                no_ref = no_ref.proximo
                tam_ref -= 1
            print(no_ref.valor)