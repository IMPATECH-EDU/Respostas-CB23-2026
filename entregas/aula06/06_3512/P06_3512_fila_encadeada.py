from P06_3512_pilha_encadeada import PilhaEncadeada


class FilaEncadeada:
    """Fila implementada usando duas PilhaEncadeada."""

    def __init__(self):
        """Cria uma fila vazia. O(1)."""
        self._entrada = PilhaEncadeada()
        self._saida = PilhaEncadeada()
        self._tamanho = 0

    def enfileirar(self, item):
        """Adiciona um item ao final da fila. O(1)."""
        self._entrada.push(item)
        self._tamanho += 1

    def _preparar_saida(self):
        """Transfere elementos para a pilha de saída quando necessário."""
        if self._saida.esta_vazia():
            while not self._entrada.esta_vazia():
                self._saida.push(self._entrada.pop())

    def desenfileirar(self):
        """Remove e retorna o primeiro item. O(1) amortizado."""
        if self.esta_vazia():
            raise IndexError("não é possível retirar de uma fila vazia")

        self._preparar_saida()
        item = self._saida.pop()
        self._tamanho -= 1
        return item

    def frente(self):
        """Retorna o primeiro item sem removê-lo. O(1) amortizado."""
        if self.esta_vazia():
            raise IndexError("não é possível consultar uma fila vazia")

        self._preparar_saida()
        return self._saida.topo()

    def esta_vazia(self):
        """Retorna True se a fila estiver vazia. O(1)."""
        return self._tamanho == 0

    def len(self):
        """Retorna a quantidade de elementos da fila. O(1)."""
        return self._tamanho

    def __repr__(self):
        """Retorna a representação da fila da frente para o final. O(N)."""
        self._preparar_saida()

        valores = []
        temporaria = PilhaEncadeada()

        while not self._saida.esta_vazia():
            item = self._saida.pop()
            valores.append(repr(item))
            temporaria.push(item)

        while not temporaria.esta_vazia():
            self._saida.push(temporaria.pop())

        return "FilaEncadeada([" + ", ".join(valores) + "])"


if __name__ == "__main__":
    fila = FilaEncadeada()
    fila.enfileirar(10)
    fila.enfileirar(20)
    fila.enfileirar(30)

    print(fila)
    print("Frente:", fila.frente())
    print("Removido:", fila.desenfileirar())
    print("Tamanho:", fila.len())
    print(fila)
