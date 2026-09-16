class PilhaEncadeada:
    class _No:
        """Classe que representa um nó que compõe a pilha encadeada.
        Complexidade das operações: O(1)
        """
        def __init__(self, valor, prox: "PilhaEncadeada._No | None" = None) -> None:
            self.valor = valor
            self.prox = prox

        def __repr__(self) -> str:
            return str(self.valor)

    def __init__(self) -> None:
        """Inicializa a pilha vazia.
        - Complexidade: O(1)
        """
        self._topo: "PilhaEncadeada._No | None" = None
        self._tamanho = 0

    def push(self, item) -> None:
        """Adiciona um item no topo da pilha.
        - Complexidade: O(1)

        Args:
            item (Any): O item a ser empilhado
        """
        self._topo = self._No(item, self._topo)
        self._tamanho += 1

    def pop(self):
        """Remove o item no topo da pilha.
        - Complexidade: O(1)

        Raises:
            IndexError: Caso a pilha esteja vazia e, assim, não
            exista elemento a ser desempilhado

        Returns:
            Any: O item desempilhado
        """
        if self.esta_vazia():
            raise IndexError("Nao ha como remover um elemento de uma lista vazia")
        no = self._topo
        self._topo = no.prox
        valor = no.valor
        del no
        self._tamanho -= 1
        return valor

    def esta_vazia(self) -> bool:
        """Verifica se a pilha está vazia.
        - Complexidade: O(1)

        Returns:
            bool: Se a pilha está vazia ou não
        """
        return self._topo is None

    @property
    def topo(self):
        """Exibe o elemento no topo da pilha.
        - Complexidade: O(1)

        Raises:
            IndexError: Caso a pilha esteja vazia e, assim, não
            exista elemento a ser mostrado

        Returns:
            Any: O elemento no topo da pilha
        """
        if self.esta_vazia():
            raise IndexError("A pilha esta vazia")
        return self._topo.valor

    def __len__(self) -> int:
        """Retorna a quantidade de elementos na pilha.
        - Complexidade: O(1)

        Returns:
            int: O número de elementos na pilha
        """
        return self._tamanho

    def __repr__(self) -> str:
        """Gera e retorna uma representação da pilha.
        - Complexidade: O(n)

        Returns:
            str: A representação da pilha
        """
        if self.esta_vazia():
            return "{}"
        no = self._No(None, self._topo)
        return f"{{{' -> '.join([
            repr((no := no.prox).valor) for _ in range(len(self))
        ])}}}"
