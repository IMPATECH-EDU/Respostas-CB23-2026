import P06_3461_pilha_encadeada as pilha 

class FilaEncadeada:
    def __init__(self): # A ideia é usar duas pilhas, uma de entrada e outra de saída. Obs: se há termos na de saída, eles estão na frente dos termos na de entrada
        self.entrada = pilha.PilhaEncadeada() # A ordem da fila está de baixo para cima (quem entrou primeiro está na frente da fila, mas sai por último na pilha)
        self.saida = pilha.PilhaEncadeada() # A ordem da fila está de cima para baixo (quem entrou por último está na frente da fila, e sai primeiro na pilha)
        self.tam = 0

    def enfileirar(self, valor):
        '''Insere o item no fim da fila. Complexidade O(1)'''
        self.entrada.push(valor)
        self.tam += 1

    def desenfileirar(self):
        '''Remove e retorna o item da frente; 
        levanta IndexError se a fila estiver vazia. 
        Complexidade O(n). Caso médio: O(1).'''
        if self.entrada.esta_vazia():
            if self.saida.esta_vazia():
                raise IndexError("Erro: A fila está vazia!")
            else: # Se a pilha de saída não estiver vazia, então basta retirar o topo dela
                self.tam -= 1
                return self.saida.pop()
        else: 
            self.tam -= 1
            if self.saida.esta_vazia(): # Se só houverem itens na entrada, adicione todos eles na pilha de saída e depois retorne o pop do último adicionado
                while self.entrada.esta_vazia() == False: # Adiciona todos os elementos da pilha de entrada na pilha de saída
                    self.saida.push(self.entrada.pop())
                return self.saida.pop() # Retorna e remove o último termo adicionado na pilha de saída 
            else: # Se a pilha de saída não estiver vazia, então basta retirar o topo dela
                return self.saida.pop()

    def frente(self):
        ''' Retorna o item da frente sem removê-lo; 
        levanta IndexError se a fila estiver vazia.
        Complexidade O(n). Caso médio: O(1).'''
        if self.saida.esta_vazia(): # Se não há nenhum elemento na pilha de saída
            if self.entrada.esta_vazia():
                raise IndexError("Erro: A fila está vazia!")
            else: # Caso só hajam elementos na pilha de entrada, leva todos para a pilha de saída e retorna o último adicionado (ou seja, o da frente)
                while self.entrada.esta_vazia() == False:
                    self.saida.push(self.entrada.pop())
                return self.saida.topo()
        else: # Caso haja ao menos um elemento na pilha de saída, basta retornar o topo
            return self.saida.topo()

    def esta_vazia(self):
        '''Retorna True quando não há elementos armazenados. Complexidade O(1).'''
        if self.saida.esta_vazia() and self.entrada.esta_vazia():
            return True
        else:
            return False

    def len(self):
        '''Retorna a quantidade de elementos da fila. Complexidade O(1).'''
        return self.tam

    def repr(self):
        '''Representação textual legível, da frente para o fim; 
        levanta IndexError se a fila estiver vazia. Complexidade O(n).'''
        if self.tam == 0:
            raise IndexError("Erro: A fila está vazia!")
        aux_saida = pilha.PilhaEncadeada() # Servirá para restaurar a pilha de saída da fila original
        aux_entrada = pilha.PilhaEncadeada() # Servirá para restaurar a pilha de entrada da fila original
        linha1 = ""
        linha2 = ""
        while self.saida.esta_vazia() == False: # Enquanto a pilha de saída estiver vazia, clona o topo para a auxiliar e adiciona-o na linha1 com um pop da original
            aux_saida.push(self.saida.topo()) # Obs: note que estamos armazenando os elementos na ordem inversa (o próximo while conserta isso)
            linha1 = linha1 + f"{self.saida.pop()} <- " # Adiciona o próximo á direita do atual
        while aux_saida.esta_vazia() == False: # Serve para restaurar a pilha de saída original, que agora está vazia, mantendo também a ordem original
            self.saida.push(aux_saida.pop())
        while self.entrada.esta_vazia() == False:
            aux_entrada.push(self.entrada.topo())
            linha2 = f"{self.entrada.pop()} <- " + linha2 # Adiciona o próximo á esquerda do atual (a ordem da pilha de entrada é inversa à da pilha de saída)
        while aux_entrada.esta_vazia() == False:
                self.entrada.push(aux_entrada.pop())
        return linha1 + linha2