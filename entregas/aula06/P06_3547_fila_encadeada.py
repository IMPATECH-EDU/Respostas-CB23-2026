from P06_3547_pilha_encadeada import PilhaEncadeada

class FilaEncadeada:
    """Uma FilaEncadeada é uma estrutura de dados que funciona como uma fila de banco.
        Args:
            Valor: É o valor que usamos para instaciar a FilaEncadeada
        Atributos:
            entrada: Uma PilhaEncadeade usada para inserir elementos na nossa FilaEncadeada
            saida: Uma PilhaEncadead usada para determinar os elementos que estão no topo."""
    def __init__(self,valor = None):
        self.entrada = PilhaEncadeada(valor)
        self.saida = PilhaEncadeada()
        self.len = len(self.entrada) + len(self.saida)
    def enfileirar(self,item):
        """Insere um elemento no final da FilaEncadeada
            Args:  
                Item: String ou Inteiro que será inserido no final da fila.
            Complexidade: O(1)"""
        self.entrada.push(item)
        self.len += 1
    def desenfileirar(self):
        """Remove e retorna o primeiro item da FilaEncadeada
        Raises:
            IndexError: Caso a fila esteja vazia,não é possível remover.
        Returns:
            Retorna o elemento que está na frente da FilaEncadeada.
        Complexidade: O(1) amortizada. Embora uma operação possa
        custar O(n) ao transferir os elementos de entrada para saída,
        cada elemento é transferido no máximo uma vez antes de ser removido."""
        if self.len == 0:
            raise IndexError("A fila está vazia!")
        if len(self.saida) == 0:
            for i in range(len(self.entrada)):
                self.saida.push(self.entrada.pop())
        self.len -= 1
        return self.saida.pop()
    def frente(self):
        """Calcula o elemento que está na frente da fila.
        Raises:
            IndexError: Caso a lista esteja vazia.
        Returns:
            Retorna o elemento que está na frente da fila.
        Complexidade: O(1) amortizada"""
        if self.len == 0:
            raise IndexError("A fila está vazia!")
        if len(self.saida) == 0:
            for i in range(len(self.entrada)):
                self.saida.push(self.entrada.pop())
        return self.saida.topo()
    def esta_vazia(self):
        """Verifica se a FilaEncadeada está vazia.
        Returns:
            Retorna True se a fila estiver vazia, caso contrário retorna
            False.
        Complexidade: O(1)"""
        if self.len == 0:
            return True
        return False
    def __len__(self):
        """Calcula quantos elementos a fila possui
            Returns:
                Retorna um inteiro que representa quantos elementos tem na fila.
            Complexidade: O(1)"""
        return self.len
    def __repr__(self):
        """Cria uma string para representar uma FilaEncadeada.
            Returns:
                Retorna uma string representando a fila do começo até o final.
            Complexidade: O(n)"""
        if len(self) == 0:
            return "None"
        saida = " | "
        aux =  PilhaEncadeada()
        if len(self.saida) != 0:
            for _ in range(len(self.saida)):
                x = self.saida.pop()
                saida += str(x) + " | "
                aux.push(x)
            for _ in range(len(aux)):
                x = aux.pop()
                self.saida.push(x)
            if len(self.entrada) != 0:
                for _ in range(len(self.entrada)):
                    x = self.entrada.pop()
                    aux.push(x)
                for _ in range(len(aux)):
                    x = aux.pop()
                    saida += str(x) + " | "
                    self.entrada.push(x)
        else:
            for _ in range(len(self.entrada)):
                x = self.entrada.pop()
                aux.push(x)
            for _ in range(len(aux)):
                x = aux.pop()
                saida += str(x) + " | "
                self.entrada.push(x)
        return saida