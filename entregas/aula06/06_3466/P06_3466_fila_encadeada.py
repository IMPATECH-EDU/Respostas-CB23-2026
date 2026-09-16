from P06_3466_pilha_encadeada import PilhaEncadeada as LE

class FilaEncadeada:
    def __init__(self):
        self.A = LE()
        self.B = LE()

    def enfileirar(self, entrada):
        self.A.push(entrada)

    def desenfileirar(self):
        if self.B.len() == 0:
            if self.A.len() == 0:
                raise IndexError
            else:
                while self.A.len() != 0:
                    self.B.push(self.A.pop())
        return self.B.pop()

    def frente(self):
        if self.B.len() == 0:
            if self.A.len() == 0:
                raise IndexError
            else:
                while self.A.len() != 0:
                    self.B.push(self.A.pop())
        return self.B.primeiro_no.valor

    def esta_vazia(self):
        if self.A.len() + self.B.len() == 0:
            return True
        return False



    def len(self):
        return self.A.len() + self.B.len()

    def repr(self):
        if self.A.len() == 0:
            return self.B.repr()
        if self.B.len() == 0:
            return self.A.repr()[::-1]
        return self.B.repr() + " → " + self.A.repr()[::-1]
    
        