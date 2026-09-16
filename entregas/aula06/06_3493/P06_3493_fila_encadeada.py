from .P06_3493_pilha_encadeada import PilhaEncadeada


class FilaEncadeada:
    def __init__(self) -> None:
        self._in = PilhaEncadeada()
        self._out = PilhaEncadeada()

    def _transferir_para_saida(self):
        while not self._in.esta_vazia():
            self._out.push(self._in.pop())

    def enfileirar(self, item):
        """Enfileira o item ao fim da fila em O(1)

        Args:
            item (Any): O item que será enfileirado
        """
        self._in.push(item)

    def desenfileirar(self):
        """Desenfileira o primeiro elemento na fila em O(1) amortizado e em O(n) no pior caso

        Returns:
            Any: O item desenfileirado
        """
        if not self._out.esta_vazia():
            return self._out.pop()
        self._transferir_para_saida()
        if self._out.esta_vazia():
            raise IndexError("Fila vazia")
        return self._out.pop()

    def frente(self):
        """Mostra o item na frente da fila em O(1) no caso amortizado e em O(n) no pior caso

        Raises:
            IndexError: Se a fila estiver vazia

        Returns:
            Any: O item na frente da fila
        """
        if not self._out.esta_vazia():
            return self._out.topo()
        self._transferir_para_saida()
        if self._out.esta_vazia():
            raise IndexError("Fila vazia")
        return self._out.topo()

    def esta_vazia(self) -> bool:
        """Avalia se a fila está vazia em O(1)
        
        Returns:
            bool: Se a fila está vazia
        """
        return len(self) == 0

    def __len__(self) -> int:
        """Retorna o tamanho da fila em O(1)
        
        Returns:
            int: O tamanho da fila
        """
        return len(self._in) + len(self._out)

    def __repr__(self) -> str:
        """Retorna uma representação da fila em O(n)

        Returns:
            str: Uma representação em string da fila
        """
        if not self._in.esta_vazia():
            self._transferir_para_saida()
        return repr(self._out)
