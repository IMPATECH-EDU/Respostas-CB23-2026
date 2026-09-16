import unittest
from P06_3542_pilha_encadeada import PilhaEncadeada
from P06_3542_fila_encadeada import FilaEncadeada


class TestePilhaEncadeada(unittest.TestCase):
    def setUp(self):
        self.pilha = PilhaEncadeada()

    def test_ordem_lifo(self):
        self.pilha.push(10)
        self.pilha.push(20)
        self.pilha.push(30)
        self.assertEqual(self.pilha.pop(), 30)
        self.assertEqual(self.pilha.pop(), 20)
        self.assertEqual(self.pilha.pop(), 10)

    def test_excecao_pilha_vazia(self):
        with self.assertRaises(IndexError):
            self.pilha.pop()
        with self.assertRaises(IndexError):
            self.pilha.topo()

    def test_coerencia_len(self):
        self.assertEqual(len(self.pilha), 0)
        self.pilha.push("A")
        self.assertEqual(len(self.pilha), 1)
        self.pilha.push("B")
        self.assertEqual(len(self.pilha), 2)
        self.pilha.pop()
        self.assertEqual(len(self.pilha), 1)

    def test_tipos_diferentes_e_none(self):
        self.pilha.push(100)
        self.pilha.push("texto")
        self.pilha.push(None)
        self.assertIsNone(self.pilha.pop())
        self.assertEqual(self.pilha.pop(), "texto")
        self.assertEqual(self.pilha.pop(), 100)


class TesteFilaEncadeada(unittest.TestCase):
    def setUp(self):
        self.fila = FilaEncadeada()

    def test_ordem_fifo(self):
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.fila.enfileirar(3)
        self.assertEqual(self.fila.desenfileirar(), 1)
        self.assertEqual(self.fila.desenfileirar(), 2)
        self.assertEqual(self.fila.desenfileirar(), 3)

    def test_intercalacao(self):
        self.fila.enfileirar("X")
        self.assertEqual(self.fila.desenfileirar(), "X")
        self.fila.enfileirar("Y")
        self.fila.enfileirar("Z")
        self.assertEqual(self.fila.desenfileirar(), "Y")

    def test_excecao_fila_vazia(self):
        with self.assertRaises(IndexError):
            self.fila.desenfileirar()
        with self.assertRaises(IndexError):
            self.fila.frente()

    def test_coerencia_len(self):
        self.assertEqual(len(self.fila), 0)
        self.fila.enfileirar(10)
        self.assertEqual(len(self.fila), 1)
        self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 0)


if __name__ == "__main__":
    unittest.main()