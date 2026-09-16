from .P06_3465_pilha_encadeada import PilhaEncadeada


class FilaEncadeada:
    def __init__(self) -> None:
        """Inicializa a fila vazia.
        - Complexidade: O(1)
        """
        self._entrada = PilhaEncadeada()
        self._saida = PilhaEncadeada()

    def enfileirar(self, item):
        """Coloca um item de qualquer tipo no final da fila.
        - Complexidade: O(1)

        Args:
            item (Any): O item a ser enfileirado
        """
        self._entrada.push(item)

    @property
    def frente(self):
        """Retorna o item na frente da fila.
        - Complexidade:
            - O(1) (Amortizada)
            - O(n) (Pior caso)

        Raises:
            IndexError: Levanta o erro se a fila estiver vazia

        Returns:
            Any: O item na frente da fila
        """
        try:
            if not self._saida.esta_vazia():
                return self._saida.topo
            while not self._entrada.esta_vazia():
                self._saida.push(self._entrada.pop())
            return self._saida.topo
        except IndexError:
            raise IndexError("Fila vazia")
        
    def desenfileirar(self):
        """Remove o primeiro elemento na fila e o retorna.
        - Complexidade:
            - O(1) (Amortizada)
            - O(n) (Pior caso)

        Returns:
            Any: O item removido
        """
        self.frente
        return self._saida.pop()

    def __len__(self) -> int:
        """Calcula e retorna o tamanho da fila.
        - Complexidade: O(1)

        Returns:
            int: O tamanho da fila
        """
        return len(self._saida) + len(self._entrada)

    def esta_vazia(self) -> bool:
        """Confere se a fila está vazia
        - Complexidade: O(1)

        Returns:
            bool: Se a fila está vazia ou não
        """
        return not len(self)

    def __repr__(self) -> str:
        """Gera e retorna uma representação da fila.
        - Complexidade: O(n)

        Returns:
            str: A representação da fila em string
        """
        if not self._entrada.esta_vazia():
            self.frente
        return repr(self._saida)
