from P06_3506_pilha_encadeada import PilhaEncadeada


class FilaEncadeada:
    def __init__(self):
        self._entrada = PilhaEncadeada()
        self._saida = PilhaEncadeada()

    def _transferir(self):
        """transfere os elementos da pilha de entrada para a de saida."""
        if self._saida.esta_vazia():
            while not self._entrada.esta_vazia():
                self._saida.push(self._entrada.pop())

    def enfileirar(self, item):
        """insere um item no fim da fila em O(1)."""
        self._entrada.push(item)

    def desenfileirar(self):
        """remove e retorna o primeiro item em O(1) amortizado."""
        if self.esta_vazia():
            raise IndexError("Não é possível remover de uma fila vazia.")

        self._transferir()
        return self._saida.pop()

    def frente(self):
        """retorna o primeiro item sem remove-lo em O(1) amortizado."""
        if self.esta_vazia():
            raise IndexError("A fila está vazia.")

        self._transferir()
        return self._saida.topo()

    def esta_vazia(self):
        """retorna true se a fila estiver vazia em O(1)."""
        return self._entrada.esta_vazia() and self._saida.esta_vazia()

    def __len__(self):
        """retorna a quantidade de elementos da fila em O(1)."""
        return len(self._entrada) + len(self._saida)

    def __repr__(self):
        resultado = ""
        auxiliar = PilhaEncadeada()

        while not self._saida.esta_vazia():
            valor = self._saida.pop()

            if resultado:
                resultado += " -> "
            resultado += str(valor)

            auxiliar.push(valor)

        while not auxiliar.esta_vazia():
            self._saida.push(auxiliar.pop())

        while not self._entrada.esta_vazia():
            auxiliar.push(self._entrada.pop())

        while not auxiliar.esta_vazia():
            valor = auxiliar.pop()

            if resultado:
                resultado += " -> "
            resultado += str(valor)

            self._entrada.push(valor)

        return resultado


if __name__ == "__main__":
    fila = FilaEncadeada()

    fila.enfileirar(10)
    fila.enfileirar(20)
    fila.enfileirar(30)

    print("Fila:", fila)
    print("Frente:", fila.frente())
    print("Tamanho:", len(fila))

    print("Removido:", fila.desenfileirar())
    print("Fila:", fila)

    fila.enfileirar(40)
    print("Fila após adicionar 40:", fila)