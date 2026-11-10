from P06_3501_pilha_encadeada import PilhaEncadeada
from P06_3501_fila_encadeada import FilaEncadeada

def run_pilha():
    print('Testando a pilha...')
    arr_teste = [1,2,3,3,4,5,6,6,6,None,8,9,10]

    test_pilha = PilhaEncadeada()
    for val in arr_teste:
        test_pilha.push(val)

    if len(test_pilha) != len(arr_teste):
        print('Função len falhou.')
        return

    arr_check = []
    for _ in range(len(test_pilha)):
        arr_check.append(test_pilha.pop())
    
    if arr_check != list(reversed(arr_teste)):
        print('Pilha falhou em criar LIFO')
        return

    if not test_pilha.esta_vazia():
        print('esta_vazia falhou')
        return

    test_pilha.push(arr_teste[0])
    test_pilha.push(arr_teste[1])
    test_pilha.pop()
    test_pilha.push(arr_teste[2])
    if test_pilha.topo() != arr_teste[2]:
        print('Sequência qualquer de operações falhou')
        return
    print('Pilha passou todos os testes com sucesso!')


def run_fila():
    print('Testando a fila...')

    arr_teste = [1,2,3,3,4,5,6,6,6,None,8,9,10]

    test_fila = FilaEncadeada()
    for val in arr_teste:
        test_fila.enfileirar(val)

    if len(test_fila) != len(arr_teste):
        print('Função len falhou.')
        return

    arr_check = []
    for _ in range(len(test_fila)):
        arr_check.append(test_fila.desenfileirar())
    
    if arr_check != arr_teste:
        print('Fila falhou em criar FIFO')
        return

    if not test_fila.esta_vazia():
        print('esta_vazia falhou')
        return

    test_fila.enfileirar(arr_teste[0])
    test_fila.enfileirar(arr_teste[1])
    test_fila.desenfileirar()
    test_fila.enfileirar(arr_teste[2])
    
    if test_fila.frente() != arr_teste[1] or len(test_fila) != 2:
        print('Sequência qualquer de operações falhou')
        return
    
    print('Fila passou todos os testes com sucesso!')


if __name__ == '__main__':
    run_pilha()
    run_fila()

