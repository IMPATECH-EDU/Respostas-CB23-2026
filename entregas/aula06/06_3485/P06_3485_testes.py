import unittest
from P06_3485_pilha_encadeada import PilhaEncadeada
from P06_3485_fila_encadeada import FilaEncadeada


class TestPilhaEncadeada(unittest.TestCase):

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

    def test_coerencia_tamanho(self):
        self.assertEqual(len(self.pilha), 0)
        self.pilha.push("A")
        self.assertEqual(len(self.pilha), 1)
        self.pilha.pop()
        self.assertEqual(len(self.pilha), 0)


class TestFilaEncadeada(unittest.TestCase):

    def setUp(self):
        self.fila = FilaEncadeada()

    def test_ordem_fifo(self):
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.fila.enfileirar(3)
        self.assertEqual(self.fila.desenfileirar(), 1)
        self.assertEqual(self.fila.desenfileirar(), 2)
        self.assertEqual(self.fila.desenfileirar(), 3)

    def test_excecao_fila_vazia(self):
        with self.assertRaises(IndexError):
            self.fila.desenfileirar()
        with self.assertRaises(IndexError):
            self.fila.frente()

    def test_intercalacao_e_reuso(self):
        self.fila.enfileirar(10)
        self.fila.enfileirar(20)
        self.assertEqual(self.fila.desenfileirar(), 10)
        self.fila.enfileirar(30)
        self.assertEqual(self.fila.frente(), 20)
        self.assertEqual(self.fila.desenfileirar(), 20)
        self.assertEqual(self.fila.desenfileirar(), 30)
        self.assertTrue(self.fila.esta_vazia())


if __name__ == "__main__":
    unittest.main()