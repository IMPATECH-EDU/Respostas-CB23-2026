class PilhaEncadeada:
    """Implementa uma lista encadeada"""

    class No:
        """Implementa um nó de lista encadeada"""
        def __init__(self, valor, proximo=None):
            self.valor = valor
            self.proximo = proximo

    def __init__(self):
        self.primeiro_no = None
        self.comprimento = 0

    def repr(self):
        no = self.primeiro_no
        s = ""
        while no is not None:
            s += f" → {no.valor}" if s else str(no.valor)
            no = no.proximo

        return s

    def len(self):
        return self.comprimento

    def topo(self):
        if self.comprimento == 0:
            raise IndexError
        return self.primeiro_no.valor

    def esta_vazia(self):
        if self.comprimento == 0:
            return True
        return False


    def push(self, item):

        novo_no = self.No(item, self.primeiro_no)
        self.primeiro_no = novo_no

        self.comprimento += 1

    def pop(self, ind=0):
        """Remove e retorna item da posição ind (padrão 0)"""

        if self.comprimento == 0:
            raise IndexError

        item = self.primeiro_no.valor
        self.primeiro_no = self.primeiro_no.proximo
        self.comprimento -= 1
        return item

