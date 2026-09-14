import unittest
from P06_3503_pilha_encadeada import PilhaEncadeada
from P06_3503_fila_encadeada import FilaEncadeada

class TestPilhaEncadeada(unittest.TestCase):

    def setUp(self):
        self.pilha = PilhaEncadeada()

    def test_pilha_inicialmente_vazia(self):
        self.assertTrue(self.pilha.esta_vazia())
        self.assertEqual(len(self.pilha), 0)

    def test_push_e_topo(self):
        self.pilha.push(10)
        self.assertFalse(self.pilha.esta_vazia())
        self.assertEqual(len(self.pilha), 1)
        self.assertEqual(self.pilha.topo(), 10)

        self.pilha.push(20)
        self.assertEqual(len(self.pilha), 2)
        self.assertEqual(self.pilha.topo(), 20)

    def test_pop_ordem_lifo(self):
        self.pilha.push("A")
        self.pilha.push("B")

        self.assertEqual(self.pilha.pop(), "B")
        self.assertEqual(len(self.pilha), 1)
        self.assertEqual(self.pilha.topo(), "A")

        self.assertEqual(self.pilha.pop(), "A")
        self.assertTrue(self.pilha.esta_vazia())
        self.assertEqual(len(self.pilha), 0)

    def test_excecao_pop_pilha_vazia(self):
        with self.assertRaises(IndexError):
            self.pilha.pop()

    def test_excecao_topo_pilha_vazia(self):
        with self.assertRaises(IndexError):
            self.pilha.topo()

    def test_repr(self):
        self.assertEqual(repr(self.pilha), "")
        self.pilha.push(1)
        self.pilha.push(2)
        self.assertEqual(repr(self.pilha), "2 -> 1")

class TestFilaEncadeada(unittest.TestCase):

    def setUp(self):
        self.fila = FilaEncadeada()

    def test_fila_vazia_inicial(self):
        self.assertTrue(self.fila.esta_vazia())
        self.assertEqual(len(self.fila), 0)
        self.assertEqual(repr(self.fila), "")

    def test_enfileirar_e_frente(self):
        self.fila.enfileirar(10)
        self.assertFalse(self.fila.esta_vazia())
        self.assertEqual(len(self.fila), 1)
        self.assertEqual(self.fila.frente(), 10)
        self.assertEqual(repr(self.fila), "10")

    def test_intercalado_com_duas_pilhas(self):
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)

        self.assertEqual(self.fila.frente(), 1)

        self.fila.enfileirar(3)
        self.fila.enfileirar(4)

        self.assertEqual(repr(self.fila), "1 -> 2 -> 3 -> 4")
        self.assertEqual(len(self.fila), 4)

        self.assertEqual(self.fila.desenfileirar(), 1)
        self.assertEqual(repr(self.fila), "2 -> 3 -> 4")

        self.assertEqual(self.fila.desenfileirar(), 2)
        self.assertEqual(repr(self.fila), "3 -> 4")

        self.assertEqual(self.fila.desenfileirar(), 3)
        self.assertEqual(repr(self.fila), "4")

        self.assertEqual(self.fila.desenfileirar(), 4)
        self.assertEqual(repr(self.fila), "")
        self.assertTrue(self.fila.esta_vazia())

    def test_excecoes_fila_vazia(self):
        with self.assertRaises(IndexError):
            self.fila.desenfileirar()

        with self.assertRaises(IndexError):
            self.fila.frente()


if __name__ == "__main__":
    unittest.main()