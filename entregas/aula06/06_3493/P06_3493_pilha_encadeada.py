class PilhaEncadeada:
    class _No:
        def __init__(self, item, next):
            self.item = item
            self.next = next

    def __init__(self) -> None:
        self._top = None
        self._len = 0

    def push(self, item) -> None:
        """Empilha um item em O(1)

        Args:
            item (Any): O que será empilhado
        """
        self._top = self._No(item, self._top)
        self._len += 1

    def pop(self):
        """Desempilha o item do topo em O(1)

        Raises:
            IndexError: Se a pilha estiver vazia

        Returns:
            Any: O item desempilhado
        """
        if self.esta_vazia():
            raise IndexError("Pilha vazia")
        valor = self._top.item
        self._top = self._top.next
        self._len -= 1
        return valor

    def topo(self):
        """Mostra o item no topo da pilha em O(1)

        Raises:
            IndexError: Se a pilha está vazia

        Returns:
            Any: O item no topo da pilha
        """
        if self.esta_vazia():
            raise IndexError("Pilha vazia")
        return self._top.item

    def esta_vazia(self) -> bool:
        """Avalia se a pilha está vazia em O(1)

        Returns:
            bool: Se a pilha está vazia
        """
        return len(self) == 0

    def __len__(self) -> int:
        """Retorna o tamanho da pilha em O(1)

        Returns:
            int: O tamanho da pilha
        """
        return self._len

    def __repr__(self) -> str:
        """Retorna uma representação da pilha em O(n)

        Returns:
            str: Uma representação em string da pilha
        """
        nos = []
        no = self._top
        while no is not None:
            nos.append(str(no.item))
            no = no.next
        return "[" + ", ".join(nos) + "]"
