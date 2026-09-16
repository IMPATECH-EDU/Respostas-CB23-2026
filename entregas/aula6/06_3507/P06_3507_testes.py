

import unittest

from P06_3507_pilha_encadeada import PilhaEncadeada
from P06_3507_fila_encadeada import FilaEncadeada


class TestPilhaEncadeada(unittest.TestCase):

    def test_pilha_inicialmente_vazia(self):
        pilha = PilhaEncadeada()

        self.assertTrue(pilha.esta_vazia())
        self.assertEqual(pilha.len(), 0)

    def test_ordem_lifo(self):
        pilha = PilhaEncadeada()

        pilha.push(1)
        pilha.push(2)
        pilha.push(3)

        self.assertEqual(pilha.pop(), 3)
        self.assertEqual(pilha.pop(), 2)
        self.assertEqual(pilha.pop(), 1)

        self.assertTrue(pilha.esta_vazia())

    def test_topo_sem_remover(self):
        pilha = PilhaEncadeada()

        pilha.push("A")
        pilha.push("B")

        self.assertEqual(pilha.topo(), "B")
        self.assertEqual(pilha.len(), 2)

        self.assertEqual(pilha.pop(), "B")
        self.assertEqual(pilha.pop(), "A")

    def test_pop_pilha_vazia(self):
        pilha = PilhaEncadeada()

        with self.assertRaises(IndexError):
            pilha.pop()

    def test_topo_pilha_vazia(self):
        pilha = PilhaEncadeada()

        with self.assertRaises(IndexError):
            pilha.topo()

    def test_len_insercoes_remocoes(self):
        pilha = PilhaEncadeada()

        self.assertEqual(pilha.len(), 0)

        pilha.push("a")
        self.assertEqual(pilha.len(), 1)

        pilha.push("b")
        self.assertEqual(pilha.len(), 2)

        pilha.pop()
        self.assertEqual(pilha.len(), 1)

        pilha.pop()
        self.assertEqual(pilha.len(), 0)

    def test_alternancia_de_operacoes(self):
        pilha = PilhaEncadeada()

        pilha.push(10)
        self.assertEqual(pilha.pop(), 10)

        pilha.push(20)
        pilha.push(30)

        self.assertEqual(pilha.pop(), 30)

        pilha.push(40)

        self.assertEqual(pilha.pop(), 40)
        self.assertEqual(pilha.pop(), 20)

        self.assertTrue(pilha.esta_vazia())

    def test_tipos_diferentes(self):
        pilha = PilhaEncadeada()

        pilha.push(10)
        pilha.push("texto")
        pilha.push(3.14)
        pilha.push(None)
        pilha.push("texto")

        self.assertEqual(pilha.len(), 5)

        self.assertEqual(pilha.pop(), "texto")
        self.assertIsNone(pilha.pop())
        self.assertEqual(pilha.pop(), 3.14)
        self.assertEqual(pilha.pop(), "texto")
        self.assertEqual(pilha.pop(), 10)

    def test_repr(self):
        pilha = PilhaEncadeada()

        pilha.push("base")
        pilha.push("topo")

        texto = repr(pilha)

        self.assertIn("topo", texto)
        self.assertIn("base", texto)


class TestFilaEncadeada(unittest.TestCase):

    def test_fila_inicialmente_vazia(self):
        fila = FilaEncadeada()

        self.assertTrue(fila.esta_vazia())
        self.assertEqual(fila.len(), 0)

    def test_ordem_fifo(self):
        fila = FilaEncadeada()

        fila.enfileirar(1)
        fila.enfileirar(2)
        fila.enfileirar(3)

        self.assertEqual(fila.desenfileirar(), 1)
        self.assertEqual(fila.desenfileirar(), 2)
        self.assertEqual(fila.desenfileirar(), 3)

        self.assertTrue(fila.esta_vazia())

    def test_frente_sem_remover(self):
        fila = FilaEncadeada()

        fila.enfileirar("A")
        fila.enfileirar("B")

        self.assertEqual(fila.frente(), "A")
        self.assertEqual(fila.len(), 2)

        self.assertEqual(fila.desenfileirar(), "A")

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

        fila.enfileirar(1)
        fila.enfileirar(2)

        self.assertEqual(fila.desenfileirar(), 1)
        self.assertEqual(fila.desenfileirar(), 2)

        self.assertTrue(fila.esta_vazia())

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

    def test_len(self):
        fila = FilaEncadeada()

        self.assertEqual(fila.len(), 0)

        fila.enfileirar("A")
        self.assertEqual(fila.len(), 1)

        fila.enfileirar("B")
        self.assertEqual(fila.len(), 2)

        fila.desenfileirar()
        self.assertEqual(fila.len(), 1)

        fila.desenfileirar()
        self.assertEqual(fila.len(), 0)


if __name__ == "__main__":
    unittest.main()