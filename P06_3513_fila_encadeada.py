from P06_3513_pilha_encadeada import PilhaEncadeada


class FilaEncadeada:
    #Fila implementada por composicao utilizando duas pilhas encadeadas

    def __init__(self):
        self._pilha_entrada = PilhaEncadeada()
        self._pilha_saida = PilhaEncadeada()

    def enfileirar(self, item):
        #Insere um item no fim da fila. O(1)
        self._pilha_entrada.push(item)

    def desenfileirar(self):
        #Remove e retorna o item da frente. Levanta IndexError se vazia. O(1) amortizado
        if self.esta_vazia():
            raise IndexError("A fila esta vazia.")
        self._transferir_se_necessario()
        return self._pilha_saida.pop()

    def frente(self):
        #Retorna o item da frente sem remove-lo. Levanta IndexError se vazia. O(1) amortizado
        if self.esta_vazia():
            raise IndexError("A fila esta vazia.")
        self._transferir_se_necessario()
        return self._pilha_saida.topo()

    def esta_vazia(self):
        #Retorna True se a fila estiver vazia. O(1)
        return len(self._pilha_entrada) == 0 and len(self._pilha_saida) == 0

    def __len__(self):
        #Retorna a quantidade de elementos na fila. O(1)
        return len(self._pilha_entrada) + len(self._pilha_saida)

    def _transferir_se_necessario(self):
        if self._pilha_saida.esta_vazia():
            while not self._pilha_entrada.esta_vazia():
                self._pilha_saida.push(self._pilha_entrada.pop())

    def __repr__(self):
        #Representacao textual da fila da frente para o fim. O(N)
        elementos = []
        atual_saida = self._pilha_saida._topo
        while atual_saida is not None:
            elementos.append(repr(atual_saida.valor))
            atual_saida = atual_saida.proximo

        temp = []
        atual_entrada = self._pilha_entrada._topo
        while atual_entrada is not None:
            temp.append(repr(atual_entrada.valor))
            atual_entrada = atual_entrada.proximo

        elementos.extend(reversed(temp))
        return f"FilaEncadeada([{', '.join(elementos)}])"