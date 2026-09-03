class No:
    """Cria um Nó, o qual tem um ponteiro e um valor"""

    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class PilhaEncadeada:
    """Inicia a Pilha com tamanho 0 e sem topo"""

    def __init__(self):
        self._topo = None
        self.tamanho = 0

    def esta_vazia(self):
        """Retorna True se a Pilha estiver vazia. O(1)"""

        return self._topo is None

    def push(self,valor):
        """Insere um novo Nó na Pilha, o qual aponta para o antigo topo. O(1)"""

        novo_valor = No(valor)

        novo_valor.proximo = self._topo

        self._topo = novo_valor

        self.tamanho += 1

    def pop(self):
        """Retira o elemento no topo da Pilha e retorna o seu valor, 
        além de tornar o seu ponteiro como novo topo, se a lista estiver vazia, levanta erro. O(1)"""

        if self.esta_vazia():
            raise IndexError("Essa pilha está vazia!!!")
        
        valor_retirado = self._topo.valor

        self._topo = self._topo.proximo

        self.tamanho -= 1

        return valor_retirado

    def topo(self):
        """Acessa o item no topo da Pilha, retornando-o. O(1)"""

        if self.esta_vazia():
            raise IndexError("Essa pilha está vazia!!!")

        return self._topo.valor

    def __len__(self):
        """Retorna o tamanho da Pilha. O(1)"""
        return self.tamanho


    def  __repr__(self):
        """Retorna uma representação textual da Pilha, do topo para a base, caso esteja vazia, retorna que esta vazia.
        O(N) pois percorre todos os itens para serem citados."""
        if self.esta_vazia():
            return ("Essa pilha está vazia!!!")
            
        else:
            atual = self._topo
            texto_final = '[Topo] '
            while True:
                if atual.proximo is None:
                    texto_final = texto_final + f'{atual.valor} [Base]'
                    break

                texto_final = texto_final + f"{atual.valor} -> "
                atual = atual.proximo

            return texto_final

