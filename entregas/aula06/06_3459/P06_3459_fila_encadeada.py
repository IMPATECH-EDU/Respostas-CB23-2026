from P06_3459_pilha_encadeada import PilhaEncadeada

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




from P06_123456_fila_encadeada import FilaEncadeada

fila = FilaEncadeada()

print("Fila vazia?", fila.esta_vazia())

fila.enfileirar(10)
fila.enfileirar(20)
fila.enfileirar(30)
fila.enfileirar(40)
fila.enfileirar(50)

print("Fila:", fila)
print("Tamanho:", len(fila))
print("Frente:", fila.frente())

print("Saiu:", fila.desenfileirar())
print("Fila:", fila)

print("Saiu:", fila.desenfileirar())
print("Fila:", fila)

fila.enfileirar(60)
fila.enfileirar(70)

print("Fila depois de adicionar 60 e 70:", fila)

print("Saiu:", fila.desenfileirar())
print("Saiu:", fila.desenfileirar())
print("Saiu:", fila.desenfileirar())

print("Fila final:", fila)
print("Tamanho final:", len(fila))