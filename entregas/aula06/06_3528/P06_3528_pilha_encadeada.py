class PilhaVaziaError(IndexError):
    """
    Erro levantado ao tentar ler ou remover o topo de uma pilha vazia.
    """


class Node:

    def __init__(self, valor, proximo=None):
        """
        Cria um no com o valor dado, apontando para o proximo no. Complexidade: O(1).
        """
        self.valor = valor
        self.proximo = proximo


class PilhaEncadeada:

    def __init__(self):
        """
        Cria uma pilha vazia.
        Complexidade: O(1).
        """
        self._topo = None
        self._tamanho = 0

    def push(self, item):
        """
        Insere o item no topo da pilha.
        Complexidade: O(1).
        O novo no passa a apontar para o antigo topo e se torna o topo.
        """
        self._topo = Node(item, self._topo)
        self._tamanho += 1

    def pop(self):
        """
        Remove e retorna o item do topo.
        Complexidade: O(1).
        Levanta PilhaVaziaError (subclasse de IndexError) se a pilha estiver vazia.
        """
        if self._topo is None:
            raise PilhaVaziaError("pop() em pilha vazia: não há elemento no topo para remover.")
        no = self._topo
        self._topo = no.proximo
        self._tamanho -= 1
        return no.valor

    def topo(self):
        """
        Retorna o item do topo, sem remover o item da pilha.
        Complexidade: O(1).
        Levanta PilhaVaziaError (subclasse de IndexError) se a pilha estiver vazia.
        """
        if self._topo is None:
            raise PilhaVaziaError("topo() em pilha vazia: não há elemento no topo para consultar.")
        return self._topo.valor

    def esta_vazia(self):
        """
        Retorna True se nao houver elementos armazenados.
        Complexidade: O(1).
        A decisao usa o contador, e nao o valor do topo, para que uma pilha contendo None nao seja confundida com uma pilha vazia.
        """
        return self._tamanho == 0

    def __len__(self):
        """
        Retorna a quantidade de elementos.
        Complexidade: O(1), pois usa o contador mantido incrementalmente.
        """
        return self._tamanho

    def __iter__(self):
        """
        Percorre os itens do topo para a base, sem modificar a pilha.
        Complexidade: O(1) por item produzido e O(N) para o percurso completo.
        A pilha nao deve ser modificada durante a iteracao.
        """
        atual = self._topo
        while atual is not None:
            yield atual.valor
            atual = atual.proximo

    def __repr__(self):
        """
        Representacao legivel, do topo para a base. Complexidade: O(N).
        Exemplo: com os itens 1, 2 e 3 inseridos nessa ordem, mostra 3, 2, 1, indicando onde ficam o topo e a base.
        """
        if self._tamanho == 0:
            return "PilhaEncadeada(vazia)"
        itens = ", ".join(repr(valor) for valor in self)
        return f"PilhaEncadeada(topo -> {itens} <- base)"


# Ao rodar o codigo diretamente (sem importacao), os seguintes exemplos de instanceas da implementacao irao ser executados
if __name__ == "__main__":
    pilha = PilhaEncadeada()
    for x in range(1, 4):
        pilha.push(x)
    print(pilha)
    print("len:", len(pilha))
    print("topo:", pilha.topo())
    print("pop:", pilha.pop())
    print(pilha)
    pilha.pop()
    pilha.pop()
    print(pilha, "| vazia?", pilha.esta_vazia())
    try:
        pilha.pop()
    except IndexError as erro:
        print(f"{type(erro).__name__}: {erro}")