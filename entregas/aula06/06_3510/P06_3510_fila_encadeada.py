from P06_3510_pilha_encadeada import PilhaEncadeada

class FilaEncadeada:
    def __init__(self):
        self.entrada = PilhaEncadeada()
        self.saida = PilhaEncadeada()
        self.quant = 0

    def enfileirar(self, item):
        """
        Insere o item passado como argumento no fim da fila (topo da pilha de entrada)
        Complexidade constante, O(1).
        """

        self.entrada.push(item)
        self.quant += 1

    def desenfileirar(self):
        """
        Remove e retorna o item na frente da fila, levanta IndexError caso a fila esteja vazia.
        Caso seja a primeira chamada de desenfileirar(), a complexidade é linear O(n), pois o programa move todos itens da pilha de entrada para a pilha de saída (em ordem inversa), para realizar a operação com êxito.
        Caso a pilha de saída não estiver vazia, a complexidade é constante O(1), pois só precisa remover e retornar o topo da pilha de saída.
        Portanto, a complexidade é O(1) amortizada.
        """

        if self.entrada.esta_vazia() is True and self.saida.esta_vazia() is True:
            raise IndexError('Fila vazia.')
        else:
            if self.saida.esta_vazia() is False:
                t = self.saida.pop()
            else:
                while self.entrada.esta_vazia() is False:
                    self.saida.push(self.entrada.head.valor)
                    self.entrada.pop()
                t = self.saida.pop()
            self.quant -= 1
            return t

    def frente(self):
        """
        Retorna o item na frente da fila, levanta IndexError caso a fila esteja vazia.
        Caso seja a primeira chamada de frente(), a complexidade é linear O(n), pois o programa move todos itens da pilha de entrada para a pilha de saída (em ordem inversa), para realizar a operação com êxito.
        Caso a pilha de saída não estiver vazia, a complexidade é constante O(1), pois só precisa retornar o topo da pilha de saída.
        Portanto, a complexidade é O(1) amortizada.
        """

        if self.entrada.esta_vazia() is True and self.saida.esta_vazia() is True:
            raise IndexError('Fila vazia.')
        else:
            if self.saida.esta_vazia() is False:
                top = self.saida.topo()
            else:
                while self.entrada.esta_vazia() is False:
                    self.saida.push(self.entrada.head.valor)
                    self.entrada.pop()
                    top = self.saida.topo()

        return top


    def esta_vazia(self):
        """
        Verifica se a fila (duas pilhas) está vazia, e retorna True. Caso contrário, retorna False.
        Complexidade constante O(1).
        """

        if self.entrada.esta_vazia() is True and self.saida.esta_vazia() is True:
            return True
        else:
            return False

    def __len__(self):
        """
        Retorna a quantidade de elementos da fila utilizando um contador implantado nas funções enfileirar() e desenfileirar(), que alteram o número de itens.
        Complexidade constante, O(1).
        """

        return self.quant

    def __repr__(self):
        """
        Retorna uma representação visual da fila, com todos os elementos, ordenados desde a frente até o final da fila.
        Complexidade linear, O(n).
        """

        atual1 = self.saida.head
        if atual1 is None:
            texto1 = ''
        else: 
            texto1 = f'{atual1.valor}'
            while atual1.next is not None:
                texto1 = texto1+ f' --> {atual1.next.valor}'
                atual1 = atual1.next
        atual2 = self.entrada.head
        if atual2 is None:
            texto2 = ''
        else:
            texto2 = f' --> {atual2.valor}'
            while atual2.next is not None:
                texto2 = f' --> {atual2.next.valor}' + texto2
                atual2 = atual2.next
        if texto1 == '':
            texto2 = texto2[5::]
        return texto1 + texto2
               
    
    
