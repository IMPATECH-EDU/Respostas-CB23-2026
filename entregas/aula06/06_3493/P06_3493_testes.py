import unittest
from .P06_3493_pilha_encadeada import PilhaEncadeada
from .P06_3493_fila_encadeada import FilaEncadeada


class TestePilhaEncadeada(unittest.TestCase):
    def setUp(self):
        self.pilha = PilhaEncadeada()

    def test_ordem_lifo(self):
        elementos = [10, 20, 30]
        for elem in elementos:
            self.pilha.push(elem)
            self.assertEqual(self.pilha.topo(), elem)

        for elem in reversed(elementos):
            self.assertEqual(self.pilha.pop(), elem)

    def test_excecoes_pilha_vazia(self):
        with self.assertRaises(IndexError):
            self.pilha.topo()
        with self.assertRaises(IndexError):
            self.pilha.pop()

    def test_coerencia_len(self):
        self.assertEqual(len(self.pilha), 0)
        self.pilha.push(1)
        self.pilha.push(2)
        self.assertEqual(len(self.pilha), 2)
        self.pilha.pop()
        self.assertEqual(len(self.pilha), 1)
        self.pilha.pop()
        self.assertEqual(len(self.pilha), 0)

    def test_alternancia_operacoes(self):
        self.pilha.push(3)
        self.pilha.push(5)
        self.assertEqual(self.pilha.topo(), 5)
        self.assertEqual(self.pilha.pop(), 5)
        self.assertFalse(self.pilha.esta_vazia())
        self.assertEqual(self.pilha.pop(), 3)
        self.assertTrue(self.pilha.esta_vazia())
        self.pilha.push(4)
        self.assertEqual(self.pilha.topo(), 4)

    def test_itens_tipos_diversos(self):
        itens = [None, None, None, 1, 1, "Teste", 1, 1, "Teste", "Teste"]
        for item in itens:
            self.pilha.push(item)

        self.assertEqual(len(self.pilha), len(itens))
        for item in reversed(itens):
            self.assertEqual(self.pilha.pop(), item)


class TesteFilaEncadeada(unittest.TestCase):
    def setUp(self):
        self.fila = FilaEncadeada()

    def test_ordem_fifo(self):
        elementos = [1, 2, 3]
        for elem in elementos:
            self.fila.enfileirar(elem)

        for elem in elementos:
            self.assertEqual(self.fila.frente(), elem)
            self.assertEqual(self.fila.desenfileirar(), elem)

    def test_intercalacao_operacoes(self):
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.assertEqual(self.fila.desenfileirar(), 1)
        self.fila.enfileirar(3)
        self.assertEqual(self.fila.desenfileirar(), 2)
        self.assertEqual(self.fila.desenfileirar(), 3)

    def test_esvaziar_e_reutilizar(self):
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.fila.desenfileirar()
        self.fila.desenfileirar()
        self.assertTrue(self.fila.esta_vazia())

        self.fila.enfileirar(3)
        self.fila.enfileirar(4)
        self.assertFalse(self.fila.esta_vazia())
        self.assertEqual(self.fila.frente(), 3)

    def test_excecoes_fila_vazia(self):
        with self.assertRaises(IndexError):
            self.fila.desenfileirar()
        with self.assertRaises(IndexError):
            self.fila.frente()

    def test_coerencia_len(self):
        self.assertEqual(len(self.fila), 0)
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.assertEqual(len(self.fila), 2)
        self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 1)
        self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 0)


if __name__ == '__main__':
    unittest.main()
