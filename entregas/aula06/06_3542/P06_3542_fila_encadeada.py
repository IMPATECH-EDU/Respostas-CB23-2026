from P06_3542_pilha_encadeada import PilhaEncadeada


class FilaEncadeada:
    def __init__(self):
        self._pilha_entrada = PilhaEncadeada()
        self._pilha_saida = PilhaEncadeada()

    def _transferir_se_necessario(self):
        if self._pilha_saida.esta_vazia():
            while not self._pilha_entrada.esta_vazia():
                self._pilha_saida.push(self._pilha_entrada.pop())

    def enfileirar(self, item):
        """Insere o item no fim da fila. Complexidade: O(1)"""
        self._pilha_entrada.push(item)

    def desenfileirar(self):
        """Remove e retorna o item da frente. Complexidade: O(1) amortizada"""
        if self.esta_vazia():
            raise IndexError("A fila está vazia. Não é possível remover elementos.")
        self._transferir_se_necessario()
        return self._pilha_saida.pop()

    def frente(self):
        """Retorna o item da frente sem remover. Complexidade: O(1) amortizada"""
        if self.esta_vazia():
            raise IndexError("A fila está vazia. Não há elemento na frente.")
        self._transferir_se_necessario()
        return self._pilha_saida.topo()

    def esta_vazia(self):
        """Retorna True se a fila estiver vazia. Complexidade: O(1)"""
        return self._pilha_entrada.esta_vazia() and self._pilha_saida.esta_vazia()

    def __len__(self):
        """Retorna a quantidade de elementos da fila. Complexidade: O(1)"""
        return len(self._pilha_entrada) + len(self._pilha_saida)

    def __repr__(self):
        """Representação textual da frente para o fim. Complexidade: O(N)"""
        elementos = []
        
        # Elementos na pilha de saída (frente da fila)
        temp_saida = PilhaEncadeada()
        while not self._pilha_saida.esta_vazia():
            item = self._pilha_saida.pop()
            elementos.append(repr(item))
            temp_saida.push(item)
        while not temp_saida.esta_vazia():
            self._pilha_saida.push(temp_saida.pop())
            
        # Elementos na pilha de entrada (fim da fila)
        temp_entrada = PilhaEncadeada()
        elementos_entrada = []
        while not self._pilha_entrada.esta_vazia():
            item = self._pilha_entrada.pop()
            elementos_entrada.append(repr(item))
            temp_entrada.push(item)
        while not temp_entrada.esta_vazia():
            self._pilha_entrada.push(temp_entrada.pop())
            
        elementos.extend(reversed(elementos_entrada))
        return f"FilaEncadeada(Frente -> [{', '.join(elementos)}])"