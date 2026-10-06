class _No:
    def __init__(self, valor) -> None:
        """
        Cria um nó contendo um valor e uma referência para o próximo nó. 
        Complexidade de tempo: O(1)
        """
        self.valor = valor
        self.proximo = None

class PilhaEncadeada:

    def __init__(self) -> None:
        """
        Inicializa uma pilha vazia. 
        Complexidade de tempo: O(1)
        """
        self.topo = None
        self._tamanho = 0

    def __len__(self):
        '''
        Retorna o tamanho atual da pilha, possui complexidade de tempo O(1)
        '''
        return self._tamanho


    def esta_vazia(self):
        '''
        Verifica se a pilha está vazia ou não.
        Complexidade de tempo O(1)
        '''
        return self.topo is None

    def push(self, valor) -> None:
        '''
        Insere um novo item no topo da pilha.
        Complexidade de tempo O(1)
        '''
        novo_no = _No(valor)
        novo_no.proximo = self.topo
        self.topo = novo_no
        self._tamanho += 1

    def pop(self):
        '''
        Remove e exibe um item do topo da pilha. Caso a pilha esteja vazia, retorna com uma mensagem de IndexError.
        Complexidade de tempo O(1)
        '''
        # VERIFICA SE A PILHA ESTÁ VAZIA
        if self.topo == None:
            raise IndexError('A pilha está vazia!')

        no_retirado = self.topo
        self.topo = self.topo.proximo
        self._tamanho -= 1
        return no_retirado.valor

    def olha_topo(self):
        '''
        Exibe qual é o item que está no topo da pilha.
        Complexidade de tempo O(1)
        '''
        # VERIFICA SE A PILHA ESTÁ VAZIA
        if self.topo == None:
            raise IndexError('A pilha está vazia!')
        return self.topo.valor

    def __repr__(self):
        '''
        Exibe todos os itens que estão na pilha em ordem. Caso ela esteja vazia, exibe uma mensagem de IndexError.
        Complexidade de tempo O(n), sendo n o tamanho atual da pilha.
        '''
        if self.esta_vazia():
            return "Pilha vazia."

        aponta_atual = self.topo
        resultado = ''
        while aponta_atual != None:
            resultado += str(aponta_atual.valor) + ' -> '
            aponta_atual = aponta_atual.proximo
        return resultado[:-4]