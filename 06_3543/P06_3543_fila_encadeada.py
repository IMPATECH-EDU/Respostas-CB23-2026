import P06_3543_pilha_encadeada as pe

class FilaEncadeada:

    def __init__(self) -> None:
        self.pilha_entrada = pe.PilhaEncadeada()
        self.pilha_saida = pe.PilhaEncadeada()
        self._tamanho_fila = 0

    def __len__(self):
        '''
        Retorna o tamanho atual da fila.
        Complexidade de tempo O(1)
        '''
        return self._tamanho_fila

    def enfileirar(self, valor) -> None:
        '''
        Insere um item no final da fila.
        Complexidade de tempo O(1)
        '''
        self.pilha_entrada.push(valor)
        self._tamanho_fila += 1

    def desenfileirar(self):
        '''
        Remove e exibe o primeiro item da fila. Caso a fila esteja vazia, levanta uma mensagem de IndexError.
        Complexidade de tempo
        '''
        if self.esta_vazia():
            raise IndexError('A fila está vazia.')
            
        # Transfere apenas se a saída estiver vazia
        if self.pilha_saida.esta_vazia():
            while not self.pilha_entrada.esta_vazia():
                self.pilha_saida.push(self.pilha_entrada.pop())
                    
        self._tamanho_fila -= 1
        return self.pilha_saida.pop()

    def frente(self):
        '''
        Exibe o primeiro item da fila. Caso a fila esteja vazia, levanta uma mensagem de IndexError
        Complexidade de tempo 
        '''
        if self.esta_vazia():
            raise IndexError('A fila está vaiza.')

        if self.pilha_saida.esta_vazia():  
            while not self.pilha_entrada.esta_vazia():
                self.pilha_saida.push(self.pilha_entrada.pop())

        return self.pilha_saida.olha_topo()

    def esta_vazia(self):
        '''
        Verifica se a fila está vazia.
        Complexidade de tempo O(1)
        '''
        return self.pilha_entrada.esta_vazia() and self.pilha_saida.esta_vazia()

    def __repr__(self):
        '''
        Exibe todos os itens da fila em ordem. Caso a fila esteja vazia, levanta uma mensagem de IndexError.
        Complexidade de tempo O(n), sendo n igual ao tamanho da fila
        '''
        if self.esta_vazia():
            raise IndexError('A fila está vazia.')

        pilha_auxiliar = pe.PilhaEncadeada()
        resultado = ''

        while not self.pilha_saida.esta_vazia():
            pilha_auxiliar.push(self.pilha_saida.pop())
            valor = pilha_auxiliar.olha_topo()
            resultado += str(valor) + ' -> '
        
        while not self.pilha_entrada.esta_vazia():
            self.pilha_saida.push(self.pilha_entrada.pop())

        while not self.pilha_saida.esta_vazia():
            pilha_auxiliar.push(self.pilha_saida.pop())
            valor = pilha_auxiliar.olha_topo()
            resultado += str(valor) + ' -> '

        while not pilha_auxiliar.esta_vazia():
            self.pilha_saida.push(pilha_auxiliar.pop())

        return resultado[:-4]