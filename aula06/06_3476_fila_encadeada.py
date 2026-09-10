import importlib

modulo = importlib.import_module("06_3476_pilha_encadeada")
PilhaEncadeada = modulo.PilhaEncadeada

class FilaEncadeada:
    """Estrutura de dados Fila implementada via composição com duas pilhas."""

    def __init__(self):
        self._entrada = PilhaEncadeada()
        self._saida = PilhaEncadeada()

    def _transferir_se_necessario(self):
        """Transfere os elementos da pilha de entrada para a de saída se a de saída estiver vazia."""
        if self._saida.esta_vazia():
            while not self._entrada.esta_vazia():
                self._saida.push(self._entrada.pop())

    def enfileirar(self, item):
        """Insere o item no fim da fila.

        Complexidade de tempo: O(1)
        """
        self._entrada.push(item)

    def desenfileirar(self):
        """Remove e retorna o item da frente da fila.

        Complexidade de tempo: O(1) amortizada
        """
        if self.esta_vazia():
            raise IndexError("Operação inválida: a fila está vazia.")
        self._transferir_se_necessario()
        return self._saida.pop()

    def frente(self):
        """Retorna o item da frente sem removê-lo.

        Complexidade de tempo: O(1) amortizada
        """
        if self.esta_vazia():
            raise IndexError("Operação inválida: a fila está vazia.")
        self._transferir_se_necessario()
        return self._saida.topo()

    def esta_vazia(self):
        """Informa se a fila está vazia.

        Complexidade de tempo: O(1)
        """
        return self._entrada.esta_vazia() and self._saida.esta_vazia()

    def __len__(self):
        """Retorna a quantidade total de elementos na fila.

        Complexidade de tempo: O(1)
        """
        return len(self._entrada) + len(self._saida)

    def len(self):
        """Método auxiliar para obtenção da quantidade de elementos.

        Complexidade de tempo: O(1)
        """
        return len(self)

    def __repr__(self):
        """Representação textual legível, da frente para o fim.

        Complexidade de tempo: O(N)
        """
        elementos_saida = []
        elementos_entrada = []

        while not self._saida.esta_vazia():
            elementos_saida.append(self._saida.pop())
        for item in reversed(elementos_saida):
            self._saida.push(item)

        while not self._entrada.esta_vazia():
            elementos_entrada.append(self._entrada.pop())
        for item in reversed(elementos_entrada):
            self._entrada.push(item)

        todos = elementos_saida + list(reversed(elementos_entrada))
        return "Frente -> [" + ", ".join(repr(x) for x in todos) + "] <- Fim"

    def repr(self):
        """Método auxiliar de representação textual.

        Complexidade de tempo: O(N)
        """
        return repr(self)
