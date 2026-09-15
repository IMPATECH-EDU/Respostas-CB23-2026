from P06_3515_pilha_encadeada import PilhaEncadeada


class FilaEncadeada:
    def __init__(self):
        """
        Cria uma fila vazia.

        Complexidade: O(1).
        """
        self._entrada = PilhaEncadeada()
        self._saida = PilhaEncadeada()
        self._tamanho = 0

    def enfileirar(self, item):
        """
        Insere um item no fim da fila.

        Complexidade: O(1).
        """
        self._entrada.push(item)
        self._tamanho += 1

    def _transferir_se_necessario(self):
        """
        Transfere os elementos da pilha de entrada
        para a pilha de saída somente quando necessário.

        Cada elemento é transferido no máximo uma vez
        da entrada para a saída.

        Complexidade:
            O(N) quando ocorre transferência.
            O(1) quando não ocorre transferência.
        """
        if self._saida.esta_vazia():

            while not self._entrada.esta_vazia():
                self._saida.push(
                    self._entrada.pop()
                )

    def desenfileirar(self):
        """
        Remove e retorna o item da frente da fila.

        Levanta IndexError se a fila estiver vazia.

        Complexidade:
            O(N) em uma chamada isolada no pior caso.
            O(1) amortizada.
        """
        if self.esta_vazia():
            raise IndexError(
                "Não é possível desenfileirar: a fila está vazia."
            )

        self._transferir_se_necessario()

        item = self._saida.pop()
        self._tamanho -= 1

        return item

    def frente(self):
        """
        Retorna o item da frente sem removê-lo.

        Levanta IndexError se a fila estiver vazia.

        Complexidade:
            O(N) em uma chamada isolada quando há transferência.
            O(1) amortizada.
        """
        if self.esta_vazia():
            raise IndexError(
                "Não é possível consultar a frente: a fila está vazia."
            )

        self._transferir_se_necessario()

        return self._saida.topo()

    def esta_vazia(self):
        """
        Retorna True se a fila estiver vazia.

        Complexidade: O(1).
        """
        return self._tamanho == 0

    def len(self):
        """
        Retorna a quantidade de elementos da fila.

        Complexidade: O(1).
        """
        return self._tamanho

    def __repr__(self):
        """
        Retorna uma representação da frente para o fim.

        A fila é restaurada ao estado original após a consulta.

        Complexidade: O(N).
        """
        if self.esta_vazia():
            return "FilaEncadeada([])"

        self._transferir_se_necessario()

        temporaria = PilhaEncadeada()
        resultado = "FilaEncadeada(["
        primeiro = True

        while not self._saida.esta_vazia():

            item = self._saida.pop()
            temporaria.push(item)

            if not primeiro:
                resultado += ", "

            resultado += repr(item)
            primeiro = False

        while not temporaria.esta_vazia():
            self._saida.push(
                temporaria.pop()
            )

        resultado += "])"

        return resultado


if __name__ == "__main__":
    fila = FilaEncadeada()

    fila.enfileirar("A")
    fila.enfileirar("B")
    fila.enfileirar("C")

    print(fila)
    print("Frente:", fila.frente())
    print("Removido:", fila.desenfileirar())
    print("Tamanho:", fila.len())
    print(fila)