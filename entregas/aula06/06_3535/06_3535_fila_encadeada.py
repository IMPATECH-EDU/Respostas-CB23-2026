import importlib

pilha_module = importlib.import_module("06_3535_pilha_encadeada")
PilhaEncadeada = pilha_module.PilhaEncadeada

class FilaEncadeada:
    def __init__(self):
        """Inicia com duas Pilhas, uma para entrada e outra para saída"""

        self.entrada = PilhaEncadeada()
        self.saida = PilhaEncadeada()

    def enfileirar(self, item):
        """Coloca o item no topo da Pilha de Entrada. O(1)"""

        self.entrada.push(item)

    def mover_se_necessario(self):
        """Se a Pilha de saída estiver, passa todos os itens da Pilha de entrada para a de saída, 
        de forma que o topo da Pilha de saída seja o primeiro que entrou."""

        if self.saida.esta_vazia():
            while not self.entrada.esta_vazia():
                self.saida.push(self.entrada.pop())

    def desenfileirar(self):
        """Remove e retorna o item da frente, movendo os itens da entrada caso necessário. O(1) Amortizada"""

        self.mover_se_necessario()

        if self.saida.esta_vazia():
            raise IndexError("A fila está vazia.")
        
        return self.saida.pop()

    def frente(self):
        """Retorna o item que entrou primeiro da Fila atual, como não é permitido acessar o topo,
        o item é retirada e adicionado novamente no topo, para conseguir o seu valor, 
        movendo os itens da entrada caso necessário. O(1) Amortizada"""

        self.mover_se_necessario()
        if self.saida.esta_vazia():
            raise IndexError("A fila está vazia.")
        
        item = self.saida.pop()
        self.saida.push(item)
        return item

    def esta_vazia(self):
        """Retorna True quando ambas Pilhas estão vazias. O(1)"""

        return self.entrada.esta_vazia() and self.saida.esta_vazia()

    def __len__(self):
        """Retorna o número de elementos em ambas Pilhas somadas, ou seja, o número de elementos da Fila. O(1)"""

        return len(self.entrada) + len(self.saida)

    def __repr__(self):
        """REtorna de forma textual como está a Fila, do ínicio da Fila para o fim, caso esteja vazia, retorna que esta vazia.
        O(N) pois percorre todos os elementos para serem citados."""

        if self.entrada.esta_vazia() and self.saida.esta_vazia():
            return ("Essa fila está vazia!!!")
                    
        else:
            elementos_saida = []

            while not self.saida.esta_vazia():
                elementos_saida.append(self.saida.pop())

            for item in reversed(elementos_saida):
                self.saida.push(item)
                
            elementos_entrada = []

            pilha_aux = PilhaEncadeada()
            while not self.entrada.esta_vazia():
                pilha_aux.push(self.entrada.pop())

            while not pilha_aux.esta_vazia():
                item = pilha_aux.pop()
                elementos_entrada.append(item)
                self.entrada.push(item)
                
            todos_elementos = elementos_saida + elementos_entrada

            texto_final = "[Frente] " + " -> "

            for i in range(len(todos_elementos)):
                if i == len(todos_elementos) - 1:
                    texto_final += f"{todos_elementos[i]} [Final]"
                else:
                    texto_final += f"{todos_elementos[i]} -> "

            return texto_final

