import unittest

from P06_3508_pilha_encadeada import PilhaEncadeada
from P06_3508_fila_encadeada import FilaEncadeada


class TestPilhaEncadeada(unittest.TestCase):
    def test_ordem_lifo(self):
        pilha = PilhaEncadeada()
        pilha.push(10)
        pilha.push(20)
        pilha.push(30)

        self.assertEqual(pilha.pop(), 30)
        self.assertEqual(pilha.pop(), 20)
        self.assertEqual(pilha.pop(), 10)

    def test_pilha_vazia(self):
        pilha = PilhaEncadeada()

        with self.assertRaises(IndexError):
            pilha.pop()

        with self.assertRaises(IndexError):
            pilha.topo()

    def test_len(self):
        pilha = PilhaEncadeada()
        self.assertEqual(len(pilha), 0)

        pilha.push(1)
        pilha.push(2)
        self.assertEqual(len(pilha), 2)

        pilha.pop()
        self.assertEqual(len(pilha), 1)

    def test_operacoes_alternadas(self):
        pilha = PilhaEncadeada()
        pilha.push("a")
        self.assertEqual(pilha.pop(), "a")
        pilha.push("b")
        pilha.push("c")
        self.assertEqual(pilha.topo(), "c")
        self.assertEqual(pilha.pop(), "c")
        self.assertEqual(pilha.pop(), "b")

    def test_tipos_diferentes(self):
        pilha = PilhaEncadeada()
        pilha.push(5)
        pilha.push("texto")
        pilha.push(None)
        pilha.push(5)

        self.assertEqual(pilha.pop(), 5)
        self.assertIsNone(pilha.pop())
        self.assertEqual(pilha.pop(), "texto")
        self.assertEqual(pilha.pop(), 5)


class TestFilaEncadeada(unittest.TestCase):
    def test_ordem_fifo(self):
        fila = FilaEncadeada()
        fila.enfileirar(10)
        fila.enfileirar(20)
        fila.enfileirar(30)

        self.assertEqual(fila.desenfileirar(), 10)
        self.assertEqual(fila.desenfileirar(), 20)
        self.assertEqual(fila.desenfileirar(), 30)

    def test_intercalacao(self):
        fila = FilaEncadeada()
        fila.enfileirar(1)
        fila.enfileirar(2)
        self.assertEqual(fila.desenfileirar(), 1)

        fila.enfileirar(3)
        fila.enfileirar(4)
        self.assertEqual(fila.desenfileirar(), 2)
        self.assertEqual(fila.desenfileirar(), 3)
        self.assertEqual(fila.desenfileirar(), 4)

    def test_esvaziar_e_reutilizar(self):
        fila = FilaEncadeada()
        fila.enfileirar("a")
        self.assertEqual(fila.desenfileirar(), "a")
        self.assertTrue(fila.esta_vazia())

        fila.enfileirar("b")
        self.assertEqual(fila.frente(), "b")
        self.assertEqual(fila.desenfileirar(), "b")

    def test_fila_vazia(self):
        fila = FilaEncadeada()

        with self.assertRaises(IndexError):
            fila.desenfileirar()

        with self.assertRaises(IndexError):
            fila.frente()

    def test_len(self):
        fila = FilaEncadeada()
        self.assertEqual(len(fila), 0)

        fila.enfileirar(1)
        fila.enfileirar(2)
        fila.enfileirar(3)
        self.assertEqual(len(fila), 3)

        fila.desenfileirar()
        self.assertEqual(len(fila), 2)


if __name__ == "__main__":
    unittest.main()
