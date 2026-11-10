from P06_3501_pilha_encadeada import PilhaEncadeada, _EMPTY

class FilaEncadeada:
    def __init__(self):
        self._inp = PilhaEncadeada()
        self._outp = PilhaEncadeada()

    '''
    Adiciona um elemento à fila, O(1) amortizado
    '''
    def enfileirar(self, data):
        self._inp.push(data)
    '''
    Retira um elemento em FIFO, O(1) amortizado
    '''
    def desenfileirar(self):
        if self._outp.esta_vazia():
            for _ in range(len(self._inp)):
                self._outp.push(self._inp.pop())
    
        return self._outp.pop()
    '''
    Espia o elemento da frente, O(1) amortizado
    '''
    def frente(self):
        if self._outp.esta_vazia():
            for _ in range(len(self._inp)):
                self._outp.push(self._inp.pop())
        
        return self._outp.topo()
    '''
    Verifica se está vazia, O(1)
    '''
    def esta_vazia(self):
        return self._inp.esta_vazia() and self._outp.esta_vazia()
    '''Comprimento da fila, O(1)
    '''
    def __len__(self):
        return len(self._inp) + len(self._outp)
    '''Representação em string da instância da fila
    '''
    def __repr__(self):
        tmp = []
        cur = self._outp._first

        while cur is not _EMPTY:
            tmp.append(cur.data)
            cur = cur.next

        cur = self._inp._first
        while cur is not _EMPTY:
            tmp.append(cur.data)
            cur = cur.next

        start = len(self._outp)
        tmp[start:] = reversed(tmp[start:])

        return f'Fila<[{', '.join(map(str, tmp))}]>'
