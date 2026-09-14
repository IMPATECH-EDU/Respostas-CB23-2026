class _No:
    def __init__(self,valor):
        self.valor = valor
        self.proximo = None

class PilhaEncadeada:
    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def push(self,item):
        novo = _No(item)
        novo.proximo = self._topo
        self._topo = novo
        self._tamanho += 1

    def esta_vazia(self):
        return self._topo is None

    def pop(self):
        if self.esta_vazia() is True:
            raise IndexError("Pilha Vazia!")
        valor = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return valor

    def topo(self):
        if self.esta_vazia():
            raise IndexError("Pilha Vazia!")
        return self._topo.valor

    def __len__(self):
        return self._tamanho

    def __repr__(self):
        atual = self._topo
        texto = ""
        while atual is not None:
            texto += str(atual.valor)
            if atual.proximo is not None:
                texto += " -> "
            atual = atual.proximo
        return texto