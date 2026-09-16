class _No:
    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class PilhaEncadeada:
    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def push(self, item):
        """insere um item no topo da pilha em O(1)."""
        novo_no = _No(item, self._topo)
        self._topo = novo_no
        self._tamanho += 1

    def pop(self):
        """remove e retorna o item do topo em O(1)."""
        if self.esta_vazia():
            raise IndexError("Não é possível remover de uma pilha vazia.")

        valor = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1

        return valor

    def topo(self):
        """retorna o item do topo sem remove-lo em O(1)."""
        if self.esta_vazia():
            raise IndexError("A pilha está vazia.")

        return self._topo.valor

    def esta_vazia(self):
        """retorna true se a pilha estiver vazia em O(1)."""
        return self._tamanho == 0

    def __len__(self):
        """retorna a quantidade de elementos da pilha em O(1)."""
        return self._tamanho

    def __repr__(self):
        """retorna a pilha do topo para a base em O(N)."""
        atual = self._topo
        resultado = ""

        while atual is not None:
            if resultado != "":
                resultado += " -> "

            resultado += str(atual.valor)
            atual = atual.proximo

        return resultado


if __name__ == "__main__":
    pilha = PilhaEncadeada()

    pilha.push(10)
    pilha.push(20)
    pilha.push(30)

    print("Pilha:", pilha)
    print("Topo:", pilha.topo())
    print("Tamanho:", len(pilha))

    print("Removido:", pilha.pop())
    print("Pilha:", pilha)