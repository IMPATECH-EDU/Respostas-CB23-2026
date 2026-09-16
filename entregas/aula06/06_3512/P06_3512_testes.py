import unittest

from P06_3512_pilha_encadeada import PilhaEncadeada
from P06_3512_fila_encadeada import FilaEncadeada


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

        self.assertEqual(pilha.len(), 0)

        pilha.push(10)
        pilha.push(20)

        self.assertEqual(pilha.len(), 2)

        pilha.pop()

        self.assertEqual(pilha.len(), 1)

        pilha.pop()

        self.assertEqual(pilha.len(), 0)

    def test_operacoes_alternadas(self):
        pilha = PilhaEncadeada()

        pilha.push("A")
        pilha.push("B")
        self.assertEqual(pilha.pop(), "B")

        pilha.push("C")
        self.assertEqual(pilha.topo(), "C")
        self.assertEqual(pilha.pop(), "C")
        self.assertEqual(pilha.pop(), "A")

    def test_diferentes_valores(self):
        pilha = PilhaEncadeada()

        valores = [10, "texto", None, 3.14, 10]

        for valor in valores:
            pilha.push(valor)

        for valor in reversed(valores):
            self.assertEqual(pilha.pop(), valor)


class TestFilaEncadeada(unittest.TestCase):

    def test_fifo(self):
        fila = FilaEncadeada()

        fila.enfileirar(10)
        fila.enfileirar(20)
        fila.enfileirar(30)

        self.assertEqual(fila.desenfileirar(), 10)
        self.assertEqual(fila.desenfileirar(), 20)
        self.assertEqual(fila.desenfileirar(), 30)

    def test_frente(self):
        fila = FilaEncadeada()

        fila.enfileirar("A")
        fila.enfileirar("B")

        self.assertEqual(fila.frente(), "A")
        self.assertEqual(fila.len(), 2)

        fila.desenfileirar()

        self.assertEqual(fila.frente(), "B")

    def test_operacoes_intercaladas(self):
        fila = FilaEncadeada()

        fila.enfileirar(1)
        fila.enfileirar(2)

        self.assertEqual(fila.desenfileirar(), 1)

        fila.enfileirar(3)
        fila.enfileirar(4)

        self.assertEqual(fila.desenfileirar(), 2)
        self.assertEqual(fila.desenfileirar(), 3)
        self.assertEqual(fila.desenfileirar(), 4)

    def test_fila_vazia_e_reutilizacao(self):
        fila = FilaEncadeada()

        self.assertTrue(fila.esta_vazia())

        with self.assertRaises(IndexError):
            fila.desenfileirar()

        with self.assertRaises(IndexError):
            fila.frente()

        fila.enfileirar(100)
        self.assertEqual(fila.desenfileirar(), 100)
        self.assertTrue(fila.esta_vazia())

        fila.enfileirar(200)
        self.assertEqual(fila.frente(), 200)
        self.assertEqual(fila.desenfileirar(), 200)

    def test_tamanho(self):
        fila = FilaEncadeada()

        self.assertEqual(fila.len(), 0)

        fila.enfileirar("A")
        fila.enfileirar("B")
        fila.enfileirar("C")

        self.assertEqual(fila.len(), 3)

        fila.desenfileirar()
        self.assertEqual(fila.len(), 2)

        fila.desenfileirar()
        self.assertEqual(fila.len(), 1)

        fila.desenfileirar()
        self.assertEqual(fila.len(), 0)

    def test_diferentes_valores(self):
        fila = FilaEncadeada()

        valores = [10, "texto", None, 3.14, 10]

        for valor in valores:
            fila.enfileirar(valor)

        for valor in valores:
            self.assertEqual(fila.desenfileirar(), valor)


if __name__ == "__main__":
    unittest.main()
