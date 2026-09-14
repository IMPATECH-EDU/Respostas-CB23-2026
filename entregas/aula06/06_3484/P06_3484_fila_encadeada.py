import importlib

pe = importlib.import_module("06_3484_pilha_encadeada")

class FilaEncadeada():

    def __init__(self):
        self.pilha_entrada = pe.PilhaEncadeada()
        self.pilha_saida = pe.PilhaEncadeada()


    def enfileirar(self, item):
        """
        Insere o item no fim da fila

        rtype: None
        custo: O(1)
        """
        self.pilha_entrada.push(item)


    def desenfileirar(self):
        """
        Remove e retorna o item da frente

        custo: O(1) amortizado (caso médio)
        """
        return self.last_item(self.pilha_saida.pop)
        

    def frente(self):
        """
        Retorna o item da frente sem removê-lo

        custo: O(1) amortizada (caso médio)
        """
        return self.last_item(self.pilha_saida.topo)  # só posso passar função, pois depois é chamado func()


    def last_item(self, func):
        """
        "factor out" dos métodos desenfileirar() e frente(), que avalia e retorna o procedimento passado como argumento
        """
        if self.esta_vazia():
            raise IndexError("A fila está vazia.")

        # primeiro vemos se a pilha de saída contém algo
        if not self.pilha_saida.esta_vazia():
            return func()

        # se chegou até aqui, é porque a saída está vazia, mas a entrada não
        while not self.pilha_entrada.esta_vazia():
            self.pilha_saida.push(self.pilha_entrada.pop())
        return func()


    def esta_vazia(self):
        """
        Retorna True quando não há elementos armazenados

        rtype: Bool
        custo: O(1)
        """
        return self.pilha_entrada.esta_vazia() and self.pilha_saida.esta_vazia()

    def __len__(self):
        """
        Retorna a quantidade de elementos da fila.

        rtype: int
        custo: O(1)
        """
        return len(self.pilha_saida) + len(self.pilha_entrada)


    def __repr__(self):
        """
        Representação textual legível, da frente para o fim.

        rtype: str
        custo: O(N)
        """
        saida = str(self.pilha_saida).replace('>', "")
        add = " - ".join(str(self.pilha_entrada).replace(" ", "").split("->")[::-1])
        saida = saida.strip() + " - " + add if add else ""
        return saida

def main():
    fila = FilaEncadeada()
    fila.enfileirar(10)
    fila.enfileirar(20)
    fila.enfileirar(30)
    print(fila.desenfileirar())
    print(fila)
    fila.enfileirar(40)
    print(fila)
    print(fila.frente())
    fila.desenfileirar()
    print(fila)
    fila.enfileirar(60)
    fila.enfileirar(70)
    print(fila)
    
if __name__ == "__main__":
    main()