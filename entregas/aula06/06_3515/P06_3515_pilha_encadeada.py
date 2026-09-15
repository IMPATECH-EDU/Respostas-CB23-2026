class _No:
    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class PilhaEncadeada:
    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def push(self, item):
        novo_no = _No(item, self._topo)
        self._topo = novo_no
        self._tamanho += 1

    def pop(self):
        if self.esta_vazia():
            raise IndexError(
                "Não é possível remover: a pilha está vazia."
            )
        item = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return item

    def topo(self):
        if self.esta_vazia():
            raise IndexError(
                "Não é possível consultar o topo: a pilha está vazia."
            )

        return self._topo.valor

    def esta_vazia(self):
        return self._tamanho == 0

    def len(self):
        return self._tamanho

    def __repr__(self):
        resultado = "PilhaEncadeada(["
        atual = self._topo
        primeiro = True
        while atual is not None:
            if not primeiro:
                resultado += ", "
            resultado += repr(atual.valor)
            primeiro = False
            atual = atual.proximo
        resultado += "])"

        return resultado


if __name__ == "__main__":
    pilha = PilhaEncadeada()

    pilha.push(10)
    pilha.push(20)
    pilha.push(30)

    print(pilha)
    print("Topo:", pilha.topo())
    print("Removido:", pilha.pop())
    print("Tamanho:", pilha.len())
    print(pilha)