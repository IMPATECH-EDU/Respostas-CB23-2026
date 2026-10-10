from P06_3492_fila_encadeada import FilaEncadeada as FE
from P06_3492_pilha_encadeada import PilhaEncadeada as PE
import traceback

def test_pilha_ordem_lifo():
    pilha = PE()
    elementos = [10, 20, 30, 40]
    for elem in elementos:
        pilha.push(elem)

    resultado = []
    while not pilha.esta_vazia():
        resultado.append(pilha.pop())
    assert resultado == [40, 30, 20, 10]


def test_pilha_vazia_pop_e_topo():
    pilha = PE()
    assert pilha.esta_vazia()
    
    pop_lancou = False
    try:
        pilha.pop()
    except IndexError:
        pop_lancou = True
    assert pop_lancou

    topo_lancou = False
    try:
        pilha.topo()
    except IndexError:
        topo_lancou = True
    assert topo_lancou


def test_pilha_coerencia_len():
    pilha = PE()
    assert len(pilha) == 0
    assert pilha.esta_vazia()

    for i in range(1, 6):
        pilha.push(i)
        assert len(pilha) == i
        assert not pilha.esta_vazia()

    for i in range(5, 0, -1):
        assert len(pilha) == i
        pilha.pop()

    assert len(pilha) == 0
    assert pilha.esta_vazia()


def test_pilha_alternancia_operacoes():
    pilha = PE()
    pilha.push("A")
    pilha.push("B")
    assert pilha.pop() == "B"

    pilha.push("C")
    assert pilha.topo() == "C"
    assert pilha.pop() == "C"
    assert pilha.pop() == "A"
    assert pilha.esta_vazia()


def test_pilha_tipos_diferentes_repetidos_e_none():
    pilha = PE()
    dados = [100, "texto", None, 3.14, None, "texto", [1, 2], True]
    for item in dados:
        pilha.push(item)

    assert len(pilha) == len(dados)
    for item in reversed(dados):
        assert pilha.pop() == item


def test_fila_ordem_fifo():
    fila = FE()
    elementos = ["primeiro", "segundo", "terceiro", "quarto"]
    for elem in elementos:
        fila.enfileirar(elem)

    resultado = []
    while not fila.esta_vazia():
        resultado.append(fila.desenfileirar())
    assert resultado == elementos


def test_fila_intercalacao_enfileirar_desenfileirar():
    fila = FE()
    fila.enfileirar(1)
    fila.enfileirar(2)
    assert fila.desenfileirar() == 1

    fila.enfileirar(3)
    assert fila.frente() == 2
    assert fila.desenfileirar() == 2

    fila.enfileirar(4)
    assert fila.desenfileirar() == 3
    assert fila.desenfileirar() == 4
    assert fila.esta_vazia()


def test_fila_esvaziar_e_reutilizar_instancia():
    fila = FE()
    fila.enfileirar("X")
    fila.enfileirar("Y")
    assert fila.desenfileirar() == "X"
    assert fila.desenfileirar() == "Y"
    assert fila.esta_vazia()

    fila.enfileirar(100)
    fila.enfileirar(200)
    assert len(fila) == 2
    assert fila.frente() == 100
    assert fila.desenfileirar() == 100
    assert fila.desenfileirar() == 200
    assert fila.esta_vazia()


def test_fila_vazia_desenfileirar_e_frente():
    fila = FE()
    assert fila.esta_vazia()

    desenfileirar_lancou = False
    try:
        fila.desenfileirar()
    except TypeError:
        desenfileirar_lancou = True
    assert desenfileirar_lancou

    frente_lancou = False
    try:
        fila.frente()
    except TypeError:
        frente_lancou = True
    assert frente_lancou


def test_fila_coerencia_len():
    fila = FE()
    assert len(fila) == 0
    assert fila.esta_vazia()

    fila.enfileirar("A")
    assert len(fila) == 1
    assert not fila.esta_vazia()
    
    fila.enfileirar("B")
    assert len(fila) == 2

    fila.desenfileirar()
    assert len(fila) == 1

    fila.desenfileirar()
    assert len(fila) == 0
    assert fila.esta_vazia()


def executar_testes():
    testes = [
        test_pilha_ordem_lifo,
        test_pilha_vazia_pop_e_topo,
        test_pilha_coerencia_len,
        test_pilha_alternancia_operacoes,
        test_pilha_tipos_diferentes_repetidos_e_none,
        test_fila_ordem_fifo,
        test_fila_intercalacao_enfileirar_desenfileirar,
        test_fila_esvaziar_e_reutilizar_instancia,
        test_fila_vazia_desenfileirar_e_frente,
        test_fila_coerencia_len
    ]

    for t in testes:
        try:
            t()
            print(f"✅ {t.__name__}: OK")
        except Exception as e:
            print(f"❌ {t.__name__}: FALHOU")
            traceback.print_exc()

if __name__ == "__main__":
    executar_testes()