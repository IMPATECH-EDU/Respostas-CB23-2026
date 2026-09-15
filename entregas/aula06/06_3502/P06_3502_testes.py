import unittest

from P06_3502_pilha_encadeada import PilhaEncadeada
from P06_3502_fila_encadeada import FilaEncadeada

class TestPilhaEncadeada(unittest.TestCase):

    def test_ordem_lifo(self):
        pilha = PilhaEncadeada()

        pilha.push(1)
        pilha.push(2)
        pilha.push(3)

        self.assertEqual(pilha.pop(), 3)
        self.assertEqual(pilha.pop(), 2)
        self.assertEqual(pilha.pop(), 1)

    def test_pop_pilha_vazia(self):
        pilha = PilhaEncadeada()

        with self.assertRaises(IndexError):
            pilha.pop()

    def test_topo_pilha_vazia(self):
        pilha = PilhaEncadeada()

        with self.assertRaises(IndexError):
            pilha.topo()

    def test_len_pilha(self):
        pilha = PilhaEncadeada()

        self.assertEqual(pilha.len(), 0)

        pilha.push(10)
        self.assertEqual(pilha.len(), 1)

        pilha.push(20)
        self.assertEqual(pilha.len(), 2)

        pilha.pop()
        self.assertEqual(pilha.len(), 1)

        pilha.pop()
        self.assertEqual(pilha.len(), 0)

    def test_alternancia_operacoes(self):
        pilha = PilhaEncadeada()

        pilha.push("A")
        self.assertEqual(pilha.topo(), "A")

        pilha.push("B")
        self.assertEqual(pilha.pop(), "B")

        pilha.push("C")
        self.assertEqual(pilha.topo(), "C")

        self.assertEqual(pilha.pop(), "C")
        self.assertEqual(pilha.pop(), "A")

        self.assertTrue(pilha.esta_vazia())

    def test_tipos_diferentes_repetidos_e_none(self):
        pilha = PilhaEncadeada()

        pilha.push(10)
        pilha.push("texto")
        pilha.push(3.14)
        pilha.push(True)
        pilha.push(10)
        pilha.push(None)

        self.assertEqual(pilha.len(), 6)

        self.assertIsNone(pilha.pop())
        self.assertEqual(pilha.pop(), 10)
        self.assertEqual(pilha.pop(), True)
        self.assertEqual(pilha.pop(), 3.14)
        self.assertEqual(pilha.pop(), "texto")
        self.assertEqual(pilha.pop(), 10)

        self.assertTrue(pilha.esta_vazia())


class TestFilaEncadeada(unittest.TestCase):

    def test_ordem_fifo(self):
        fila = FilaEncadeada()

        fila.enfileirar(1)
        fila.enfileirar(2)
        fila.enfileirar(3)

        self.assertEqual(fila.desenfileirar(), 1)
        self.assertEqual(fila.desenfileirar(), 2)
        self.assertEqual(fila.desenfileirar(), 3)

    def test_intercalacao_enfileirar_desenfileirar(self):
        fila = FilaEncadeada()

        fila.enfileirar("A")
        fila.enfileirar("B")

        self.assertEqual(fila.desenfileirar(), "A")

        fila.enfileirar("C")

        self.assertEqual(fila.desenfileirar(), "B")

        fila.enfileirar("D")
        fila.enfileirar("E")

        self.assertEqual(fila.desenfileirar(), "C")
        self.assertEqual(fila.desenfileirar(), "D")
        self.assertEqual(fila.desenfileirar(), "E")

    def test_esvaziar_e_reutilizar(self):
        fila = FilaEncadeada()

        fila.enfileirar(1)
        fila.enfileirar(2)

        self.assertEqual(fila.desenfileirar(), 1)
        self.assertEqual(fila.desenfileirar(), 2)

        self.assertTrue(fila.esta_vazia())
        self.assertEqual(fila.len(), 0)

        fila.enfileirar(3)
        fila.enfileirar(4)

        self.assertEqual(fila.desenfileirar(), 3)
        self.assertEqual(fila.desenfileirar(), 4)

        self.assertTrue(fila.esta_vazia())

    def test_desenfileirar_fila_vazia(self):
        fila = FilaEncadeada()

        with self.assertRaises(IndexError):
            fila.desenfileirar()

    def test_frente_fila_vazia(self):
        fila = FilaEncadeada()

        with self.assertRaises(IndexError):
            fila.frente()

    def test_len_fila(self):
        fila = FilaEncadeada()

        self.assertEqual(fila.len(), 0)

        fila.enfileirar("A")
        self.assertEqual(fila.len(), 1)

        fila.enfileirar("B")
        self.assertEqual(fila.len(), 2)

        fila.enfileirar("C")
        self.assertEqual(fila.len(), 3)

        fila.desenfileirar()
        self.assertEqual(fila.len(), 2)

        fila.desenfileirar()
        self.assertEqual(fila.len(), 1)

        fila.desenfileirar()
        self.assertEqual(fila.len(), 0)


if __name__ == "__main__":
    unittest.main()
