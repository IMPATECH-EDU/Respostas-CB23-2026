import unittest

from P06_3506_pilha_encadeada import PilhaEncadeada
from P06_3506_fila_encadeada import FilaEncadeada


class TestPilhaEncadeada(unittest.TestCase):

    def test_lifo(self):
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

    def test_tamanho(self):
        pilha = PilhaEncadeada()

        self.assertEqual(len(pilha), 0)

        pilha.push(10)
        pilha.push(20)

        self.assertEqual(len(pilha), 2)

        pilha.pop()

        self.assertEqual(len(pilha), 1)

    def test_operacoes_alternadas(self):
        pilha = PilhaEncadeada()

        pilha.push(1)
        pilha.push(2)

        self.assertEqual(pilha.pop(), 2)

        pilha.push(3)

        self.assertEqual(pilha.topo(), 3)
        self.assertEqual(pilha.pop(), 3)
        self.assertEqual(pilha.pop(), 1)

    def test_tipos_diferentes(self):
        pilha = PilhaEncadeada()

        pilha.push(10)
        pilha.push("texto")
        pilha.push(None)
        pilha.push(10)

        self.assertEqual(pilha.pop(), 10)
        self.assertIsNone(pilha.pop())
        self.assertEqual(pilha.pop(), "texto")
        self.assertEqual(pilha.pop(), 10)


class TestFilaEncadeada(unittest.TestCase):

    def test_fifo(self):
        fila = FilaEncadeada()

        fila.enfileirar(10)
        fila.enfileirar(20)
        fila.enfileirar(30)

        self.assertEqual(fila.desenfileirar(), 10)
        self.assertEqual(fila.desenfileirar(), 20)
        self.assertEqual(fila.desenfileirar(), 30)

    def test_operacoes_intercaladas(self):
        fila = FilaEncadeada()

        fila.enfileirar(1)
        fila.enfileirar(2)

        self.assertEqual(fila.desenfileirar(), 1)

        fila.enfileirar(3)

        self.assertEqual(fila.desenfileirar(), 2)
        self.assertEqual(fila.desenfileirar(), 3)

    def test_reutilizar_fila(self):
        fila = FilaEncadeada()

        fila.enfileirar(1)
        self.assertEqual(fila.desenfileirar(), 1)

        fila.enfileirar(2)

        self.assertEqual(fila.frente(), 2)
        self.assertEqual(fila.desenfileirar(), 2)

    def test_fila_vazia(self):
        fila = FilaEncadeada()

        with self.assertRaises(IndexError):
            fila.desenfileirar()

        with self.assertRaises(IndexError):
            fila.frente()

    def test_tamanho(self):
        fila = FilaEncadeada()

        self.assertEqual(len(fila), 0)

        fila.enfileirar(10)
        fila.enfileirar(20)

        self.assertEqual(len(fila), 2)

        fila.desenfileirar()

        self.assertEqual(len(fila), 1)


if __name__ == "__main__":
    unittest.main()