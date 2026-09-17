from P06_3495_pilha_encadeada import PilhaEncadeada as pe

class FilaEncadeada:
    def __init__(self):
        self.entrada = pe()
        self.saida = pe()

    def enfileirar(self, item):
        '''
            Insere o item no fim da fila,
            tem complexidade de tempo O(1).
        '''
        self.entrada.push(item)

    def desenfileirar(self):
        '''
            Remove e retorna o item da frente da fila; 
            levanta IndexError se a fila estiver vazia.
            Tem complexidade de tempo O(1) amortizada (caso médio).
        '''
        if self.esta_vazia():
            raise IndexError("Não é possível desenfileirar fila vazia.")
        if len(self.saida) == 0:
            while len(self.entrada) > 0:
                self.saida.push(self.entrada.pop())
        return self.saida.pop()

    def frente(self):
        '''
            Retorna o item da frente da fila sem removê-lo; 
            levanta IndexError se a fila estiver vazia.
            Tem complexidade de tempo O(1) amortizada (caso médio).
        '''
        if self.esta_vazia():
            raise IndexError("Não é possível acessar frente de fila vazia.")
        if len(self.saida) == 0:
            while len(self.entrada) > 0:
                self.saida.push(self.entrada.pop())
        return self.saida.topo()

    def esta_vazia(self):
        '''
            Retorna True quando não há elementos armazenados na fila
            e False quando há.
            Tem complexidade de tempo O(1).
        '''        
        if len(self) == 0:
            return True
        return False

    def __len__(self):
        '''
            Retorna a quantidade de elementos da fila.
            Tem complexidade de tempo O(1).
        '''
        return len(self.entrada) + len(self.saida)

    def __repr__(self):
        '''
            Retorna uma representação textual legível da fila.
            Se a fila estiver vazia retorna uma string vazia.
            Caso contrário, cada elemento da fila é escrito em uma linha, 
            sendo que na primeira linha é apresentado o elemento da frente
            da fila e na última linha é apresentado o elemento do final da fila.
            Tem complexidade de tempo O(N).
        '''
        aux = pe()
        if self.esta_vazia():
            s = ""
        elif len(self.saida) > len(self.entrada):
            while len(self.entrada) > 0:
                aux.push(self.entrada.pop())
            s = str(self.saida) + str(aux)
            while len(aux) > 0:
                self.entrada.push(aux.pop())
        else:
            while len(self.saida) > 0:
                aux.push(self.saida.pop())
            while len(self.entrada) > 0:
                self.saida.push(self.entrada.pop())
            while len(aux) > 0:
                self.saida.push(aux.pop())
            s = str(self.saida)
        return s
