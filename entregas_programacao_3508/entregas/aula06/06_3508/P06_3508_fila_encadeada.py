from P06_3508_pilha_encadeada import PilhaEncadeada


class FilaEncadeada:
    def __init__(self):
        self._entrada = PilhaEncadeada()
        self._saida = PilhaEncadeada()
        self._tamanho = 0

    def _transferir(self):
        while not self._entrada.esta_vazia():
            self._saida.push(self._entrada.pop())

    def enfileirar(self, item):
        self._entrada.push(item)
        self._tamanho += 1

    def desenfileirar(self):
        if self.esta_vazia():
            raise IndexError("nao e possivel remover de uma fila vazia")

        if self._saida.esta_vazia():
            self._transferir()

        self._tamanho -= 1
        return self._saida.pop()

    def frente(self):
        if self.esta_vazia():
            raise IndexError("a fila esta vazia")

        if self._saida.esta_vazia():
            self._transferir()

        return self._saida.topo()

    def esta_vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho

    def __repr__(self):
        auxiliar = PilhaEncadeada()
        texto = "FilaEncadeada(["
        primeiro = True

        while not self._saida.esta_vazia():
            valor = self._saida.pop()
            if not primeiro:
                texto += ", "
            texto += repr(valor)
            primeiro = False
            auxiliar.push(valor)

        while not auxiliar.esta_vazia():
            self._saida.push(auxiliar.pop())

        while not self._entrada.esta_vazia():
            auxiliar.push(self._entrada.pop())

        while not auxiliar.esta_vazia():
            valor = auxiliar.pop()
            if not primeiro:
                texto += ", "
            texto += repr(valor)
            primeiro = False
            self._entrada.push(valor)

        return texto + "])"
