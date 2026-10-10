from P06_3492_pilha_encadeada import PilhaEncadeada as PE

class FilaEncadeada:
    def __init__(self):
        """Inicializa a fila encadeada utilizando duas pilhas encadeadas (entrada e saída).
        
        Complexidade de tempo: O(1)
        """
        self._entrada = PE()
        self._saida = PE()

    def enfileirar(self, item):
        """Insere um elemento ao final da fila.
        
        Complexidade de tempo: O(1)
        """
        self._entrada.push(item)

    def desenfileirar(self):
        """Remove e retorna o primeiro elemento inserido na fila.
        
        Complexidade de tempo: O(1) amortizado; O(n) no pior caso, onde n é o total de elementos na fila.
        """
        if self._saida.esta_vazia():
            if self._entrada.esta_vazia():
                raise TypeError("Fila vazia")
            for _ in range(len(self._entrada)):
                self._saida.push(self._entrada.pop())
        return self._saida.pop()

    def frente(self):
        """Retorna o primeiro elemento da fila sem removê-lo.
        
        Complexidade de tempo: O(1) amortizado; O(n) no pior caso, onde n é o total de elementos na fila.
        """
        if self._saida.esta_vazia():
            if self._entrada.esta_vazia():
                raise TypeError("Fila vazia")
            for _ in range(len(self._entrada)):
                self._saida.push(self._entrada.pop())
        return self._saida.topo()

    def __len__(self):
        """Retorna o total de elementos presentes na fila.
        
        Complexidade de tempo: O(1)
        """
        return len(self._entrada) + len(self._saida)

    def esta_vazia(self):
        """Verifica se a fila não contém elementos.
        
        Complexidade de tempo: O(1)
        """
        return len(self) == 0

    def __repr__(self):
        """Retorna a representação gráfica em string dos elementos contidos na fila mantendo a ordem correta.
        
        Complexidade de tempo: O(n), onde n é a quantidade total de elementos na fila.
        """
        texto = f"{self._saida}"
        if  not self._entrada.esta_vazia():
            if not self._saida.esta_vazia():
                texto += " → "
            texto2 = ""
            provisorio = PE()
            q = len(self._entrada)
            for _ in range(q):
                provisorio.push(self._entrada.pop())
            n = provisorio.pop()
            texto2 += f"{n}"
            self._entrada.push(n)
            for _ in range(q - 1):
                n = provisorio.pop()
                texto2 += f" → {n}"
                self._entrada.push(n)
            texto += texto2
        return texto