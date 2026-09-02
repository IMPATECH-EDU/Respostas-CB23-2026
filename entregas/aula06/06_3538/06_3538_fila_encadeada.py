import importlib

# Importa o módulo pelo nome em formato de string
modulo_pilha = importlib.import_module("06_3538_pilha_encadeada")
PilhaEncadeada = modulo_pilha.PilhaEncadeada

class FilaEncadeada:
    """
    Estrutura de dados Fila (FIFO) implementada por composição usando duas instâncias de PilhaEncadeada.
    """
    def __init__(self):
        """
        Inicializa uma fila vazia com duas pilhas (entrada e saída).
        Complexidade: O(1)
        """
        self.pilha_entrada = PilhaEncadeada()
        self.pilha_saida = PilhaEncadeada()

    def enfileirar(self, item):
        """
        Insere o item no fim da fila.
        Complexidade: O(1)
        """
        self.pilha_entrada.push(item)

    def desenfileirar(self):
        """
        Remove e retorna o item da frente da fila.
        Levanta IndexError se a fila estiver vazia.
        Complexidade: O(1) amortizada (caso médio)
        """
        # Passo 1: Se a saída estiver vazia, transferimos o "estoque" da entrada para ela
        if self.pilha_saida.esta_vazia():
            while not self.pilha_entrada.esta_vazia():
                objeto = self.pilha_entrada.pop()
                self.pilha_saida.push(objeto)
        # Passo 2: Se mesmo após a transferência a saída continuar vazia, a fila toda está vazia!
        if self.pilha_saida.esta_vazia():
            raise IndexError("A fila está vazia")
        # Passo 3: Se chegamos até aqui, basta remover e retornar quem está no topo da saída
        return self.pilha_saida.pop()

    def frente(self):
        """
        Retorna o item da frente sem removê-lo.
        Levanta IndexError se a fila estiver vazia.
        Complexidade: O(1) amortizada (caso médio)
        """
        # Passo 1: Se a saída estiver vazia, transferimos o "estoque" da entrada para ela
        if self.pilha_saida.esta_vazia():
            while not self.pilha_entrada.esta_vazia():
                objeto = self.pilha_entrada.pop()
                self.pilha_saida.push(objeto)
        # Passo 2: Se mesmo após a transferência a saída continuar vazia, a fila toda está vazia!
        if self.pilha_saida.esta_vazia():
            raise IndexError("A fila está vazia")
        # Passo 3: Se chegamos até aqui, retorna quem está no topo da saída
        return self.pilha_saida.topo()
    
    def esta_vazia(self):
        """
        Retorna True quando não há elementos armazenados na fila.
        Complexidade: O(1)
        """
        return (len(self.pilha_saida) + len(self.pilha_entrada)) == 0

    def __len__(self):
        """
        Retorna a quantidade total de elementos na fila.
        Complexidade: O(1)
        """
        return (len(self.pilha_entrada) + len(self.pilha_saida))

    def __repr__(self):
        """
        Representação textual legível, da frente para o fim.
        Complexidade: O(N)
        """
        texto1 = repr(self.pilha_saida)
        texto2 = ""
        
        if not self.pilha_entrada.esta_vazia():
            pilha_temp = PilhaEncadeada()
            
            while not self.pilha_entrada.esta_vazia():
                objeto = self.pilha_entrada.pop()
                pilha_temp.push(objeto)
                
            texto2 = repr(pilha_temp)
            
            while not pilha_temp.esta_vazia():
                objeto_devolvido = pilha_temp.pop()
                self.pilha_entrada.push(objeto_devolvido)
                
        return texto1 + texto2