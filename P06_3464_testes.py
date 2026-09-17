from P06_3464_pilha_encadeada import PilhaEncadeada
from P06_3464_fila_encadeada import FilaEncadeada
import random as rand

def generate_sequence(size, repeat = False, diff_char = []):
    """Gera sequências de caracteres.

    Parameters
    ----------
    size : int
        Tamanho final da sequência.
    repeat : bool, optional
        Define se elementos vão se repetir ou não.
    diff_char : list[list], optional
        Adiciona caracteres especiais.
    
    Returns
    -------
    list[list]
        Sequência final aleatória dos elementos
    """

    characters = list(range(1, size+1-len(diff_char))) + diff_char

    if repeat:
        characters = rand.choices(characters, k=size)
    else:
        rand.shuffle(characters)

    return characters



if __name__ == '__main__':
    pilha = PilhaEncadeada()
    fila = FilaEncadeada()

    characters = ['*', ' ', None, 'J', 'Q', 'K', 'A']

    seq1 = generate_sequence(20, repeat=False)
    seq2 = generate_sequence(20, repeat=True, diff_char=characters)

    print("TESTES COM A PILHA\n")

    print("Tentando dar pop() e topo() em uma pilha vazia:")
    try:
        print(pilha.topo())
    except Exception as e:
        print(f"Esse erro foi levantado: {e}")
    try:
        print(pilha.pop())
    except Exception as e:
        print(f"Esse erro foi levantado: {e}")

    print("----------------------------\nTestando os métodos da pilha\n----------------------------")

    #Adiciona os elementos na pilha e vai printando o topo
    print(f"Adicionando os elementos na pilha:\n\tSequência adicionada: {seq1}\n",end='')
    print("Adiciona elementos e vai printando o topo: ",end='')
    for el in seq1:
        pilha.push(el)
        print(pilha.topo(), end=' ')

    print(f"\nPilha: {pilha}")
    print(f"Tamanho da pilha: {len(pilha)}")

    print("\nRemovendo elementos e adicionando")

    to_remove = rand.randint(1, len(pilha))

    for i in range(to_remove):
        print(f"Elemento {pilha.pop()} removido da pilha")

    print(pilha)

    print(f"\nAdicionando elementos novamente à pilha:\n\tSequência adicionada: {seq2}\n",end='')
    print("Adiciona elementos e vai printando o topo: ",end='')

    for el in seq2:
        pilha.push(el)
        print(pilha.topo(), end=' ')
    print(f"\nPilha: {pilha}")
    print(f"Tamanho da pilha: {len(pilha)}")




    print("\n\nTESTES COM A FILA")

    print("Tentando dar frente() e desenfileirar() em uma fila vazia:")
    try:
        print(fila.frente())
    except Exception as e:
        print(f"Esse erro foi levantado: {e}")
    try:
        print(fila.desenfileirar())
    except Exception as e:
        print(f"Esse erro foi levantado: {e}")


    print("---------------------------\nTestando os métodos da fila\n---------------------------")

    #Adiciona os elementos na fila e vai printando o topo
    print(f"Adicionando os elementos na fila:\n\tSequência adicionada: {seq1}\n",end='')
    print("Adiciona elementos e vai printando a frente: ",end='')
    for el in seq1:
        fila.enfileirar(el)
        print(fila.frente(), end=' ')

    print(f"\nFila: {fila}")
    print(f"Tamanho da fila: {len(fila)}")

    print("\nRemovendo elementos e adicionando")

    to_remove = rand.randint(1, len(fila))

    for i in range(to_remove):
        print(f"Elemento {fila.desenfileirar()} removido da fila")

    print(f"Fila com itens removidos: {fila}")

    print(f"\nAdicionando elementos novamente à fila:\n\tSequência adicionada: {seq2}\n",end='')
    print("Adiciona elementos e vai printando a frente: ",end='')
    for el in seq2:
        fila.enfileirar(el)
        print(fila.frente(), end=' ')
    print(f"\nFila: {fila}")
    print(f"Tamanho da fila: {len(fila)}")

    print("\nVamos agora esvaziar a fila e reutilizá-la:")
    while len(fila) > 0:
        print(fila.desenfileirar(), end=' ')

    print(f"\nA fila está desenfileirada agora. Veja:\nFila: {fila}\nTamanho da Fila: {len(fila)}")

    seq3 = generate_sequence(10, repeat=False)

    print(f"Adicionando elementos novamente... (seq: {seq3})")

    for el in seq3:
        fila.enfileirar(el)

    print(f"Fila final: {fila}")
    print(f"Tamanho da fila final: {len(fila)}")