import P06_3473_pilha_encadeada

class FilaEncadeada:

    def __init__(self):

        self.entrada = P06_3473_pilha_encadeada.PilhaEncadeada()
        self.saida = P06_3473_pilha_encadeada.PilhaEncadeada()
        self.tamanho = 0

    def enfileirar(self, item):
        """ 
        Insere um item no fim da fila.
        Complexidade: O(1)
        """
        self.entrada.push(item)
        self.tamanho += 1
        
    def desenfileirar(self):
        """
        Remove e retorna o item da frente; levanta IndexError se a fila estiver vazia.
        Complexidade: 
            Pior caso: O(N).
            Caso médio: O(1) amortizado.
        """
        if self.saida.esta_vazia():
            while not self.entrada.esta_vazia():
                aux = self.entrada.pop()
                self.saida.push(aux)
     
        if self.saida.esta_vazia():

            raise IndexError("A fila está vazia.")
        
        item = self.saida.pop()
        self.tamanho -= 1
        return item
        
    
    def frente(self):
        """
        Retorna o item da frente; levanta IndexError se a fila estiver vazia.
        Complexidade: 
            Pior caso: O(N)
            Caso médio: O(1) amortizado
        """

        if self.saida.esta_vazia():
            while not self.entrada.esta_vazia():
                aux = self.entrada.pop()
                self.saida.push(aux)

        if self.saida.esta_vazia():
            raise IndexError("A fila está vazia.")
        
        item = self.saida.topo()
        return item


    def esta_vazia(self):
        """
        Retorna True quando a fila está vazia
        Complexidade: O(1)
        """
        return self.tamanho == 0

    def __len__(self):
        """
        Retorna a quantidade de elementos que há na fila.
        Complexidade: O(1)
        """
        return self.tamanho

    def __repr__(self):
        """
        Retorna uma representação da fila da frente para o fim.
        Complexidade: O(N)
        """

        fila = ""
        auxiliar = P06_3473_pilha_encadeada.PilhaEncadeada()

        while not self.saida.esta_vazia():
            item = self.saida.pop()

            if fila != "":
                fila += " -> "

            fila += str(item)
            auxiliar.push(item)

        while not auxiliar.esta_vazia():
            self.saida.push(auxiliar.pop())

        while not self.entrada.esta_vazia():
            auxiliar.push(self.entrada.pop())

        while not auxiliar.esta_vazia():
            item = auxiliar.pop()

            if fila != "":
                fila += " -> "

            fila += str(item)
            self.entrada.push(item)

        return fila
            
