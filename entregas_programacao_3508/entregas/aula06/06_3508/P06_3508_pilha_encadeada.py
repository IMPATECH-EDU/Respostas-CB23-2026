class _No:
    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class PilhaEncadeada:
    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def push(self, item):
        novo = _No(item, self._topo)
        self._topo = novo
        self._tamanho += 1

    def pop(self):
        if self.esta_vazia():
            raise IndexError("nao e possivel remover de uma pilha vazia")

        valor = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return valor

    def topo(self):
        if self.esta_vazia():
            raise IndexError("a pilha esta vazia")
        return self._topo.valor

    def esta_vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho

    def __repr__(self):
        texto = "PilhaEncadeada(["
        atual = self._topo
        primeiro = True

        while atual is not None:
            if not primeiro:
                texto += ", "
            texto += repr(atual.valor)
            primeiro = False
            atual = atual.proximo

        return texto + "])"

