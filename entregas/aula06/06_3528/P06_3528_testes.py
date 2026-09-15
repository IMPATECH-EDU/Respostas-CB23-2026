import unittest
from collections import deque

from P06_3528_pilha_encadeada import PilhaEncadeada
from P06_3528_fila_encadeada import FilaEncadeada


class TestPilhaEncadeada(unittest.TestCase):
    """
    Casos obrigatorios da secao 3 do enunciado para a pilha.
    """

    def setUp(self):
        """
        Cria uma pilha vazia antes de cada teste.
        """
        self.pilha = PilhaEncadeada()

    def test_ordem_lifo(self):
        """
        Verifica a ordem LIFO em uma sequencia de push seguida de pop.
        """
        for i in range(1, 6):
            self.pilha.push(i)
        for esperado in range(5, 0, -1):
            self.assertEqual(self.pilha.pop(), esperado)
        self.assertTrue(self.pilha.esta_vazia())

    def test_topo_nao_remove(self):
        """
        Verifica que topo retorna o item do topo sem remover o item da pilha.
        """
        self.pilha.push("a")
        self.pilha.push("b")
        self.assertEqual(self.pilha.topo(), "b")
        self.assertEqual(self.pilha.topo(), "b")
        self.assertEqual(len(self.pilha), 2)

    def test_pop_em_pilha_vazia(self):
        """
        Verifica que pop em pilha vazia levanta IndexError com mensagem nao vazia.
        """
        with self.assertRaises(IndexError) as ctx:
            self.pilha.pop()
        self.assertTrue(str(ctx.exception).strip())

    def test_topo_em_pilha_vazia(self):
        """
        Verifica que topo em pilha vazia levanta IndexError com mensagem nao vazia.
        """
        with self.assertRaises(IndexError) as ctx:
            self.pilha.topo()
        self.assertTrue(str(ctx.exception).strip())

    def test_pop_apos_esvaziar(self):
        """
        Verifica que pop e topo levantam IndexError depois que a pilha e esvaziada.
        """
        self.pilha.push(1)
        self.pilha.pop()
        with self.assertRaises(IndexError):
            self.pilha.pop()
        with self.assertRaises(IndexError):
            self.pilha.topo()

    def test_len_coerente(self):
        """
        Verifica que len acompanha cada insercao e cada remocao.
        """
        self.assertEqual(len(self.pilha), 0)
        for i in range(10):
            self.pilha.push(i)
            self.assertEqual(len(self.pilha), i + 1)
        for i in range(10, 0, -1):
            self.pilha.pop()
            self.assertEqual(len(self.pilha), i - 1)
        self.assertTrue(self.pilha.esta_vazia())

    def test_len_inalterado_por_erro(self):
        """
        Verifica que uma remocao invalida nao altera len.
        """
        with self.assertRaises(IndexError):
            self.pilha.pop()
        self.assertEqual(len(self.pilha), 0)

    def test_alternancia_de_operacoes(self):
        """
        Verifica o comportamento com push, pop e topo alternados.
        """
        self.pilha.push(1)
        self.pilha.push(2)
        self.assertEqual(self.pilha.pop(), 2)
        self.pilha.push(3)
        self.assertEqual(self.pilha.topo(), 3)
        self.pilha.push(4)
        self.assertEqual(self.pilha.pop(), 4)
        self.assertEqual(self.pilha.pop(), 3)
        self.pilha.push(5)
        self.assertEqual(len(self.pilha), 2)
        self.assertEqual(self.pilha.pop(), 5)
        self.assertEqual(self.pilha.pop(), 1)
        self.assertTrue(self.pilha.esta_vazia())

    def test_tipos_diferentes_repetidos_e_none(self):
        """
        Verifica o armazenamento de itens de tipos diferentes, incluindo valores repetidos e None.
        """
        itens = [1, "texto", 3.5, None, [1, 2], (3, 4), {"k": "v"}, 1, None, True]
        for item in itens:
            self.pilha.push(item)
        self.assertEqual(len(self.pilha), len(itens))
        for esperado in reversed(itens):
            self.assertEqual(self.pilha.pop(), esperado)
        self.assertTrue(self.pilha.esta_vazia())

    def test_none_nao_confunde_com_vazia(self):
        """
        Verifica que uma pilha contendo apenas None nao e considerada vazia.
        """
        self.pilha.push(None)
        self.assertFalse(self.pilha.esta_vazia())
        self.assertEqual(len(self.pilha), 1)
        self.assertIsNone(self.pilha.topo())
        self.assertIsNone(self.pilha.pop())
        self.assertTrue(self.pilha.esta_vazia())

    def test_repr_do_topo_para_a_base(self):
        """
        Verifica a representacao textual da pilha vazia e da pilha com itens, do topo para a base.
        """
        self.assertEqual(repr(self.pilha), "PilhaEncadeada(vazia)")
        for item in (1, "b", None):
            self.pilha.push(item)
        self.assertEqual(repr(self.pilha), "PilhaEncadeada(topo -> None, 'b', 1 <- base)")

    def test_armazenamento_nao_usa_colecoes_proibidas(self):
        """
        Verifica que nenhum atributo interno da pilha e list, tuple, dict ou deque.
        """
        for i in range(3):
            self.pilha.push(i)
        for atributo in vars(self.pilha).values():
            self.assertNotIsInstance(atributo, (list, tuple, dict, deque))


class TestFilaEncadeada(unittest.TestCase):
    """
    Casos obrigatorios da secao 3 do enunciado para a fila.
    """

    def setUp(self):
        """
        Cria uma fila vazia antes de cada teste.
        """
        self.fila = FilaEncadeada()

    def test_ordem_fifo(self):
        """
        Verifica a ordem FIFO em uma sequencia de enfileirar seguida de desenfileirar.
        """
        for i in range(1, 6):
            self.fila.enfileirar(i)
        for esperado in range(1, 6):
            self.assertEqual(self.fila.desenfileirar(), esperado)
        self.assertTrue(self.fila.esta_vazia())

    def test_frente_nao_remove(self):
        """
        Verifica que frente retorna o item da frente sem remover o item da fila.
        """
        self.fila.enfileirar("a")
        self.fila.enfileirar("b")
        self.assertEqual(self.fila.frente(), "a")
        self.assertEqual(self.fila.frente(), "a")
        self.assertEqual(len(self.fila), 2)

    def test_intercalacao(self):
        """
        Verifica a intercalacao de enfileirar e desenfileirar.
        Caso critico: novos itens chegam a pilha de entrada enquanto a pilha de saida ainda tem itens, e a ordem FIFO precisa ser mantida.
        """
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.fila.enfileirar(3)
        self.assertEqual(self.fila.desenfileirar(), 1)
        self.fila.enfileirar(4)
        self.fila.enfileirar(5)
        self.assertEqual(self.fila.desenfileirar(), 2)
        self.fila.enfileirar(6)
        self.assertEqual(self.fila.frente(), 3)
        self.assertEqual(self.fila.desenfileirar(), 3)
        self.assertEqual(self.fila.desenfileirar(), 4)
        self.assertEqual(self.fila.desenfileirar(), 5)
        self.assertEqual(self.fila.desenfileirar(), 6)
        self.assertTrue(self.fila.esta_vazia())

    def test_intercalacao_contra_modelo(self):
        """
        Compara uma sequencia longa e deterministica de operacoes com um modelo de referencia (deque).
        """
        modelo = deque()
        for i in range(300):
            if i % 3 == 2 and modelo:
                self.assertEqual(self.fila.desenfileirar(), modelo.popleft())
            else:
                self.fila.enfileirar(i)
                modelo.append(i)
            self.assertEqual(len(self.fila), len(modelo))
            if modelo:
                self.assertEqual(self.fila.frente(), modelo[0])
        while modelo:
            self.assertEqual(self.fila.desenfileirar(), modelo.popleft())
        self.assertTrue(self.fila.esta_vazia())

    def test_esvaziar_e_reutilizar(self):
        """
        Verifica que a mesma instancia volta a funcionar normalmente depois de esvaziada.
        """
        for i in range(3):
            self.fila.enfileirar(i)
        for i in range(3):
            self.assertEqual(self.fila.desenfileirar(), i)
        self.assertTrue(self.fila.esta_vazia())
        with self.assertRaises(IndexError):
            self.fila.desenfileirar()
        for letra in "xyz":
            self.fila.enfileirar(letra)
        self.assertEqual(len(self.fila), 3)
        self.assertEqual(self.fila.desenfileirar(), "x")
        self.assertEqual(self.fila.desenfileirar(), "y")
        self.assertEqual(self.fila.desenfileirar(), "z")
        self.assertTrue(self.fila.esta_vazia())

    def test_desenfileirar_em_fila_vazia(self):
        """
        Verifica que desenfileirar em fila vazia levanta IndexError com mensagem nao vazia.
        """
        with self.assertRaises(IndexError) as ctx:
            self.fila.desenfileirar()
        self.assertTrue(str(ctx.exception).strip())

    def test_frente_em_fila_vazia(self):
        """
        Verifica que frente em fila vazia levanta IndexError com mensagem nao vazia.
        """
        with self.assertRaises(IndexError) as ctx:
            self.fila.frente()
        self.assertTrue(str(ctx.exception).strip())

    def test_len_coerente(self):
        """
        Verifica que len acompanha as operacoes e nao muda com a transferencia entre as pilhas.
        """
        self.assertEqual(len(self.fila), 0)
        for i in range(5):
            self.fila.enfileirar(i)
            self.assertEqual(len(self.fila), i + 1)
        self.fila.frente()
        self.assertEqual(len(self.fila), 5)
        self.fila.desenfileirar()
        self.fila.enfileirar(99)
        self.assertEqual(len(self.fila), 5)
        while not self.fila.esta_vazia():
            self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 0)

    def test_none_como_item(self):
        """
        Verifica que None e tratado como item comum, e nao como sinal de fila vazia.
        """
        self.fila.enfileirar(None)
        self.fila.enfileirar(0)
        self.assertFalse(self.fila.esta_vazia())
        self.assertIsNone(self.fila.frente())
        self.assertIsNone(self.fila.desenfileirar())
        self.assertEqual(self.fila.desenfileirar(), 0)

    def test_repr_da_frente_para_o_fim(self):
        """
        Verifica a representacao textual da frente para o fim, inclusive com itens nas duas pilhas, e que repr nao altera a fila.
        """
        self.assertEqual(repr(self.fila), "FilaEncadeada(vazia)")
        for i in (1, 2, 3):
            self.fila.enfileirar(i)
        self.assertEqual(repr(self.fila), "FilaEncadeada(frente -> 1, 2, 3 <- fim)")
        self.fila.frente()
        self.fila.enfileirar(4)
        self.assertEqual(repr(self.fila), "FilaEncadeada(frente -> 1, 2, 3, 4 <- fim)")
        self.assertEqual(len(self.fila), 4)
        self.assertEqual(self.fila.desenfileirar(), 1)

    def test_armazenamento_apenas_pilhas(self):
        """
        Verifica que os atributos internos da fila sao apenas instancias de PilhaEncadeada.
        """
        self.fila.enfileirar(1)
        for atributo in vars(self.fila).values():
            self.assertIsInstance(atributo, PilhaEncadeada)


if __name__ == "__main__":
    unittest.main()