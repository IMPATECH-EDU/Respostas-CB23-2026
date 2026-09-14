import importlib

#Importando a Pilha do arquivo anterior de forma segura (pois o nome começa com número)
modulo_pilha = importlib.import_module("06_3478_pilha_encadeada")
PilhaEncadeada = modulo_pilha.PilhaEncadeada

class FilaEncadeada:
    """Fila construída através de composição utilizando duas Pilhas Encadeadas."""
    def __init__(self):
        self.pilha_entrada = PilhaEncadeada()
        self.pilha_saida = PilhaEncadeada()

    def esta_vazia(self):
        """Retorna True quando não há elementos. Complexidade: O(1)"""
        return self.pilha_entrada.esta_vazia() and self.pilha_saida.esta_vazia()

    def __len__(self):
        """Retorna a quantidade de elementos da fila. Complexidade: O(1)"""
        return len(self.pilha_entrada) + len(self.pilha_saida)

    def _transferir_se_necessario(self):
        """Transfere elementos da entrada para a saída apenas quando a saída esvazia."""
        if self.pilha_saida.esta_vazia():
            while not self.pilha_entrada.esta_vazia():
                self.pilha_saida.push(self.pilha_entrada.pop())

    def enfileirar(self, item):
        """Insere o item no fim da fila. Complexidade: O(1)"""
        self.pilha_entrada.push(item)

    def desenfileirar(self):
        """Remove e retorna o item da frente. Complexidade: O(1) amortizada"""
        if self.esta_vazia():
            raise IndexError("A fila está vazia. Não é possível remover elementos.")
        
        self._transferir_se_necessario()
        return self.pilha_saida.pop()

    def frente(self):
        """Retorna o item da frente sem removê-lo. Complexidade: O(1) amortizada"""
        if self.esta_vazia():
            raise IndexError("A fila está vazia. Não há frente para visualizar.")
        
        self._transferir_se_necessario()
        return self.pilha_saida.topo()

    def __repr__(self):
        """Retorna uma representação da frente para o fim. Complexidade: O(N)"""
        elementos_saida = []
        elementos_entrada = []
        pilha_temp = PilhaEncadeada()
        
        #Percorre a pilha de saída e restaura sua ordem original
        while not self.pilha_saida.esta_vazia():
            item = self.pilha_saida.pop()
            elementos_saida.append(repr(item))
            pilha_temp.push(item)

        while not pilha_temp.esta_vazia():
            self.pilha_saida.push(pilha_temp.pop())
            
        #Percorre a pilha de entrada e restaura sua ordem original
        while not self.pilha_entrada.esta_vazia():
            item = self.pilha_entrada.pop()
            elementos_entrada.append(repr(item))
            pilha_temp.push(item)

        while not pilha_temp.esta_vazia():
            self.pilha_entrada.push(pilha_temp.pop())
            
        elementos_entrada.reverse()
        todos_elementos = elementos_saida + elementos_entrada
        
        return "FilaEncadeada([" + ", ".join(todos_elementos) + "])"