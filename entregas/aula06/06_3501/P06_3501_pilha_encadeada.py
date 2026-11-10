class _Empty:
    pass

_EMPTY = _Empty()

class _node:
    def __init__(self, data):
        self.data = data
        self.next = _EMPTY
    def __str__(self):
        return str(self.data)

class PilhaEncadeada:
    def __init__(self):
            self._first = _EMPTY
            self._length = 0
    '''Adiciona um elemento à pilha, O(1) amortizado
    '''
    def push(self, data):
        n = _node(data)
        if self._first is _EMPTY:
            self._first = n
            self._length = 1
            return

        tmp = self._first
        self._first = n
        n.next = tmp # type: ignore
        self._length += 1
    '''Retira o elemento do topo da pilha em LIFO, O(1)
    '''
    def pop(self):
        if self._first is _EMPTY:
            raise IndexError('Pilha vazia')

        tmp = self._first
        self._first = self._first.next
        self._length -= 1

        return tmp.data
    '''Observa o elemento do topo da pilha em LIFO, O(1)
    '''
    def topo(self):
        if self._first is _EMPTY:
            raise IndexError('Pilha vazia')
        return self._first.data
    '''Retorna o número de elementos na pilha, O(1)
    '''
    def __len__(self):
        return self._length
    '''Retorna se a pilha está vazia, O(1)
    '''
    def esta_vazia(self):
        return len(self) == 0
    '''Representação em string da instância da pilha
    '''
    def __repr__(self):
        r = []
        cur  = self._first
        while cur is not _EMPTY:
            r.append(cur.data)
            cur = cur.next

        return f'Pilha<[{', '.join(map(str, r))}]>'


if __name__ == '__main__':
    arr = PilhaEncadeada()
    while (nonempty := input().strip()) != '':
        arr.push(int(nonempty))

    print(arr)
# for i in range(len(arr)):
#     print(arr.pop())
