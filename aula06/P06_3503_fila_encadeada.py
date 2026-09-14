from P06_3503_pilha_encadeada import PilhaEncadeada

class FilaEncadeada:
    def __init__(self):
        self.pilha_entrada = PilhaEncadeada()
        self.pilha_saida = PilhaEncadeada()

    def esta_vazia(self):
        return self.pilha_entrada.esta_vazia() and self.pilha_saida.esta_vazia()
    
    def passar(self):
        if self.pilha_saida.esta_vazia():
            while self.pilha_entrada.esta_vazia() is not True:
                no = self.pilha_entrada.pop()
                self.pilha_saida.push(no)

    def enfileirar(self,item):
        self.pilha_entrada.push(item)

    def desenfileirar(self):
        if self.esta_vazia():
            raise IndexError("Fila Vazia!")
        self.passar()
        return self.pilha_saida.pop()

    def frente(self):
        if self.esta_vazia():
            raise IndexError("Fila Vazia!")
        self.passar()
        return self.pilha_saida.topo()

    def __len__(self):
        return len(self.pilha_saida) + len(self.pilha_entrada)

    def __repr__(self):
        elementos = ""
        separador = ""

        aux_saida = PilhaEncadeada()
        while not self.pilha_saida.esta_vazia():
            val = self.pilha_saida.pop()
            elementos += separador + str(val)
            separador = " -> "
            aux_saida.push(val)

        while not aux_saida.esta_vazia():
            self.pilha_saida.push(aux_saida.pop())

        aux_entrada = PilhaEncadeada()
        while not self.pilha_entrada.esta_vazia():
            aux_entrada.push(self.pilha_entrada.pop())

        while not aux_entrada.esta_vazia():
            val = aux_entrada.pop()
            elementos += separador + str(val)
            separador = " -> "
            self.pilha_entrada.push(val)

        return f"{elementos}"