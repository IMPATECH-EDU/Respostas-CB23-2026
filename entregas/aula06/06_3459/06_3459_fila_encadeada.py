class _No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class PilhaEncadeada:
    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def push(self, item):
        novo_no = _No(item)
        novo_no.proximo = self._topo
        self._topo = novo_no
        self._tamanho += 1

    def pop(self):
        if self.esta_vazia():
            raise IndexError("Subfluxo de pilha: Pilha vazia.")
        valor_removido = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return valor_removido

    def topo(self):
        if self.esta_vazia():
            raise IndexError("Pilha vazia.")
        return self._topo.valor

    def esta_vazia(self):
        return self._topo is None

    def __len__(self):
        return self._tamanho

    def __repr__(self):
        elementos = []
        atual = self._topo
        while atual is not None:
            elementos.append(repr(atual.valor))
            atual = atual.proximo
        return " -> ".join(elementos) if elementos else "Pilha Vazia"


class FilaEncadeada:
    def __init__(self):
        self.pilha_entrada = PilhaEncadeada()
        self.pilha_saida = PilhaEncadeada()

    def enfileirar(self, item):
        self.pilha_entrada.push(item)

    def _transferir_se_necessario(self):
        if self.pilha_saida.esta_vazia():
            while not self.pilha_entrada.esta_vazia():
                self.pilha_saida.push(self.pilha_entrada.pop())

    def desenfileirar(self):
        if self.esta_vazia():
            raise IndexError("Subfluxo de fila: Fila vazia.")
        self._transferir_se_necessario()
        return self.pilha_saida.pop()

    def frente(self):
        if self.esta_vazia():
            raise IndexError("Fila vazia.")
        self._transferir_se_necessario()
        return self.pilha_saida.topo()

    def esta_vazia(self):
        return self.pilha_entrada.esta_vazia() and self.pilha_saida.esta_vazia()

    def __len__(self):
        return len(self.pilha_entrada) + len(self.pilha_saida)

    def __repr__(self):
        if self.esta_vazia():
            return "Fila Vazia"
        
        elementos = []
        atual = self.pilha_saida._topo
        while atual is not None:
            elementos.append(repr(atual.valor))
            atual = atual.proximo
            
        elementos_entrada = []
        atual = self.pilha_entrada._topo
        while atual is not None:
            elementos_entrada.append(repr(atual.valor))
            atual = atual.proximo
        elementos.extend(reversed(elementos_entrada))
        
        return " <- ".join(elementos)
