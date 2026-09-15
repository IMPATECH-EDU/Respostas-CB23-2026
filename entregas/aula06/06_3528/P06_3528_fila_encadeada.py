from P06_3528_pilha_encadeada import PilhaEncadeada


class FilaVaziaError(IndexError):
    """
    Erro levantado ao tentar ler ou remover a frente de uma fila vazia.
    """


class FilaEncadeada:

    def __init__(self):
        """
        Cria uma fila vazia.
        Complexidade: O(1).
        """
        self._entrada = PilhaEncadeada()
        self._saida = PilhaEncadeada()

    def _transferir_se_necessario(self):
        """
        Se a pilha de saida estiver vazia, move para ela todos os itens da pilha de entrada.
        A transferencia inverte a ordem: o item mais antigo da entrada, que esta na base, chega ao topo da saida.
        Complexidade: O(k) quando ha transferencia, sendo k o numero de itens da entrada. O(1) caso contrario.
        """
        if self._saida.esta_vazia():
            while not self._entrada.esta_vazia():
                self._saida.push(self._entrada.pop())

    def enfileirar(self, item):
        """
        Insere o item no fim da fila.
        Complexidade: O(1).
        """
        self._entrada.push(item)

    def desenfileirar(self):
        """
        Remove e retorna o item da frente.
        Complexidade: O(N) no pior caso de uma chamada isolada, quando ha transferencia. O(1) amortizada.
        Levanta FilaVaziaError (subclasse de IndexError) se a fila estiver vazia.
        """
        if self.esta_vazia():
            raise FilaVaziaError("desenfileirar() em fila vazia: não há elemento na frente para remover.")
        self._transferir_se_necessario()
        return self._saida.pop()

    def frente(self):
        """
        Retorna o item da frente, sem remover o item da fila.
        Complexidade: O(N) no pior caso de uma chamada isolada, quando ha transferencia. O(1) amortizada.
        Levanta FilaVaziaError (subclasse de IndexError) se a fila estiver vazia.
        """
        if self.esta_vazia():
            raise FilaVaziaError("frente() em fila vazia: não há elemento na frente para consultar.")
        self._transferir_se_necessario()
        return self._saida.topo()

    def esta_vazia(self):
        """
        Retorna True se nao houver elementos armazenados.
        Complexidade: O(1).
        """
        return self._entrada.esta_vazia() and self._saida.esta_vazia()

    def __len__(self):
        """
        Retorna a quantidade de elementos da fila.
        Complexidade: O(1).
        Soma os tamanhos das duas pilhas, cada um obtido em O(1).
        """
        return len(self._entrada) + len(self._saida)

    def __repr__(self):
        """
        Representacao legivel, da frente para o fim.
        Complexidade: O(N).
        Nao modifica as pilhas: percorre a saida do topo para a base e, para obter a entrada da base para o topo, empilha seus itens em uma pilha auxiliar, que os inverte, e percorre essa pilha auxiliar.
        """
        if self.esta_vazia():
            return "FilaEncadeada(vazia)"
        entrada_invertida = PilhaEncadeada()
        for valor in self._entrada:
            entrada_invertida.push(valor)
        partes_saida = ", ".join(repr(v) for v in self._saida)
        partes_entrada = ", ".join(repr(v) for v in entrada_invertida)
        if partes_saida and partes_entrada:
            itens = partes_saida + ", " + partes_entrada
        else:
            itens = partes_saida or partes_entrada
        return f"FilaEncadeada(frente -> {itens} <- fim)"


# Ao rodar o codigo diretamente (sem importacao), os seguintes exemplos de instanceas da implementacao irao ser executados
if __name__ == "__main__":
    fila = FilaEncadeada()
    for x in range(1, 4):
        fila.enfileirar(x)
    print(fila)
    print("frente:", fila.frente())
    fila.enfileirar(4)
    print(fila)
    print("desenfileirar:", fila.desenfileirar())
    print("len:", len(fila))
    while not fila.esta_vazia():
        fila.desenfileirar()
    print(fila, "| vazia?", fila.esta_vazia())
    try:
        fila.desenfileirar()
    except IndexError as erro:
        print(f"{type(erro).__name__}: {erro}")