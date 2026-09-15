
import unittest

from P06_3510_pilha_encadeada import PilhaEncadeada
from P06_3510_fila_encadeada import FilaEncadeada


class TestPilhaEncadeada(unittest.TestCase):

    # Ordem LIFO em sequência de push/pop
    def test_ordem_lifo(self):
        pilha = PilhaEncadeada()

        pilha.push(1)
        pilha.push(23)
        pilha.push(356)

        self.assertEqual(pilha.pop(), 356)
        self.assertEqual(pilha.pop(), 23)
        self.assertEqual(pilha.pop(), 1)

    # pop e topo em pilha vazia
    def test_operacoes_pilha_vazia(self):
        pilha = PilhaEncadeada()

        with self.assertRaises(IndexError):
            pilha.pop()

        with self.assertRaises(IndexError):
            pilha.topo()

    # Coerência de len após inserções e remoções
    def test_len(self):
        pilha = PilhaEncadeada()

        self.assertEqual(len(pilha), 0)

        pilha.push(104)
        self.assertEqual(len(pilha), 1)

        pilha.push(2230)
        pilha.push(-23)
        self.assertEqual(len(pilha), 3)

        pilha.pop()
        self.assertEqual(len(pilha), 2)

        pilha.pop()
        self.assertEqual(len(pilha), 1)

        pilha.pop()
        self.assertEqual(len(pilha), 0)

    # Alternância de operações
    def test_alternancia(self):
        pilha = PilhaEncadeada()

        pilha.push(21)
        self.assertEqual(pilha.pop(), 21)

        pilha.push(76)
        pilha.push(67)
        self.assertEqual(pilha.topo(), 67)

        pilha.push(4)
        self.assertEqual(pilha.pop(), 4)
        self.assertEqual(pilha.pop(), 67)

        pilha.push(0)
        self.assertEqual(pilha.topo(), 0)

    # Tipos diferentes, valores repetidos e None
    def test_tipos_diferentes(self):
        pilha = PilhaEncadeada()

        pilha.push(10)
        pilha.push("abc")
        pilha.push(3.14)
        pilha.push(None)
        pilha.push(10)

        self.assertEqual(pilha.pop(), 10)
        self.assertIsNone(pilha.pop())
        self.assertEqual(pilha.pop(), 3.14)
        self.assertEqual(pilha.pop(), "abc")
        self.assertEqual(pilha.pop(), 10)


class TestFilaEncadeada(unittest.TestCase):

    # Ordem FIFO
    def test_ordem_fifo(self):
        fila = FilaEncadeada()

        fila.enfileirar(12)
        fila.enfileirar(21)
        fila.enfileirar(33)

        self.assertEqual(fila.desenfileirar(), 12)
        self.assertEqual(fila.desenfileirar(), 21)
        self.assertEqual(fila.desenfileirar(), 33)

    # Intercalação de enfileirar e desenfileirar
    def test_intercalacao(self):
        fila = FilaEncadeada()

        fila.enfileirar(451)
        fila.enfileirar(7)

        self.assertEqual(fila.desenfileirar(), 451)

        fila.enfileirar(32)
        fila.enfileirar(4)

        self.assertEqual(fila.desenfileirar(), 7)
        self.assertEqual(fila.desenfileirar(), 32)

        fila.enfileirar(55)

        self.assertEqual(fila.desenfileirar(), 4)
        self.assertEqual(fila.desenfileirar(), 55)

    # Esvaziar e voltar a usar a mesma instância
    def test_esvaziar_e_reutilizar(self):
        fila = FilaEncadeada()

        fila.enfileirar(11)
        fila.enfileirar('as')

        self.assertEqual(fila.desenfileirar(), 11)
        self.assertEqual(fila.desenfileirar(), 'as')

        self.assertTrue(fila.esta_vazia())

        # reutiliza a mesma fila
        fila.enfileirar(3)
        fila.enfileirar(7)

        self.assertEqual(fila.desenfileirar(), 3)
        self.assertEqual(fila.desenfileirar(), 7)

        self.assertTrue(fila.esta_vazia())

    # desenfileirar e frente em fila vazia
    def test_operacoes_fila_vazia(self):
        fila = FilaEncadeada()

        with self.assertRaises(IndexError):
            fila.desenfileirar()

        with self.assertRaises(IndexError):
            fila.frente()

    # Coerência de len
    def test_len(self):
        fila = FilaEncadeada()

        self.assertEqual(len(fila), 0)

        fila.enfileirar(108)
        self.assertEqual(len(fila), 1)

        fila.enfileirar(2)
        fila.enfileirar(30)
        self.assertEqual(len(fila), 3)

        fila.desenfileirar()
        self.assertEqual(len(fila), 2)

        fila.desenfileirar()
        self.assertEqual(len(fila), 1)

        fila.desenfileirar()
        self.assertEqual(len(fila), 0)


if __name__ == "__main__":
    unittest.main()

