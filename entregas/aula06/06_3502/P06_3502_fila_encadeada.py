from P06_3502_pilha_encadeada import PilhaEncadeada

class FilaEncadeada():

    def __init__(self): 
        """Inicializa a classe com as instâncias da pilha. A pilha de saida mantém a ordem correta da fila.""" 
        self.entrada = PilhaEncadeada()
        self.saida = PilhaEncadeada()
        self.comprimento = 0

    def enfileirar(self, other): 
        """Adiciona no fim da fila; complexidade O(1)."""
        self.entrada.push(other)
        self.comprimento += 1

    def transferir(self): 
        """Transfere da pilha de entrada para a de saida; complexidade O(n)."""
        while not self.entrada.esta_vazia():
            self.saida.push(self.entrada.pop())

    def desenfileirar(self): 
        """Retira um elemento do inicio da fila; complexidade O(1) amortizado."""
        if self.comprimento == 0:
             raise IndexError
        if self.saida.esta_vazia():
             self.transferir()

        self.comprimento -= 1
        return self.saida.pop()

    def frente(self): 
        """Retorna o elemento do inicio da fila sem retirá-lo; complexidade O(1) amortizado."""
        if self.comprimento == 0:
            raise IndexError
        if self.saida.esta_vazia():
            self.transferir()

        return self.saida.topo()

    def esta_vazia(self): 
        """Indica se a fila está vazia; complexidade O(1)."""
        return self.comprimento == 0

    def __len__(self): 
        """Retorna o comprimento da fila; complexidade O(1)."""
        return self.comprimento

    def __repr__(self): 
        """Cria uma representação textual da fila sem alterar seu conteúdo; complexidade O(n)."""
        saida_temp = PilhaEncadeada()
        entrada_temp = PilhaEncadeada()
        s = ""
        while not self.saida.esta_vazia():
            item = self.saida.pop()
            saida_temp.push(item)

            if s:
                s += f" -> {item}"
            else:
                s += str(item)
        while not saida_temp.esta_vazia():
            item = saida_temp.pop()
            self.saida.push(item)

        while not self.entrada.esta_vazia():
            entrada_temp.push(self.entrada.pop())

        entrada_temp2 = PilhaEncadeada()
        while not entrada_temp.esta_vazia():
            item = entrada_temp.pop()
            entrada_temp2.push(item)

            if s:
                s += f" -> {item}"
            else:
                s += str(item)
        while not entrada_temp2.esta_vazia():
            self.entrada.push(entrada_temp2.pop())
            
        return s
