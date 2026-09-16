from p06_3533_pilha_encadeada import PilhaEncadeada
from p06_3533_fila_encadeada import FilaEncadeada
import unittest

class TestFilaEncadeada(unittest.TestCase):
    def setUp(self):
        self.fila = FilaEncadeada()
    def test_enfileirar(self):
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.fila.enfileirar(3)
        self.assertEqual(len(self.fila), 3)
    def test_desenfileirar(self):
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.fila.enfileirar(3)
        self.assertEqual(self.fila.desenfileirar(), 1)
        self.assertEqual(self.fila.desenfileirar(), 2)
        self.assertEqual(self.fila.desenfileirar(), 3)
    def test_frente(self):
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.fila.enfileirar(3)
        self.assertEqual(self.fila.frente(), 1)
        self.fila.desenfileirar()
        self.assertEqual(self.fila.frente(), 2)
    def test_esta_vazia(self):
        self.assertTrue(self.fila.esta_vazia())
        self.fila.enfileirar(1)
        self.assertFalse(self.fila.esta_vazia())
        self.fila.desenfileirar()
        self.assertTrue(self.fila.esta_vazia())
    def test_len(self):
        self.assertEqual(len(self.fila), 0)
        self.fila.enfileirar(1)
        self.assertEqual(len(self.fila), 1)
        self.fila.enfileirar(2)
        self.assertEqual(len(self.fila), 2)
        self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 1)
    def test_repr(self):
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.fila.enfileirar(3)
        self.assertEqual(repr(self.fila), "1  🠒  2  🠒  3  🠒  ")
    def test_desenfileirar_vazia(self):
        with self.assertRaises(IndexError):
            self.fila.desenfileirar()
    def test_frente_vazia(self):
        with self.assertRaises(IndexError):
            self.fila.frente()

    # =====================*=========================

# Testes obrigatórios (unittest) para a pilha: ordem LIFO em sequência de push/pop; pop e topo em pilha vazia; coerência de len após inserções e remoções; alternância de operações; armazenamento de itens de tipos diferentes, incluindo valores repetidos e None.


class TestPilhaEncadeada(unittest.TestCase):
    def setUp(self):
        self.pilha = PilhaEncadeada()
    def test_push(self):
        self.pilha.push(1)
        self.pilha.push(2)
        self.pilha.push(3)
        self.assertEqual(len(self.pilha), 3)
    def test_LIFO_order(self):
        self.pilha.push(1)
        self.pilha.push(2)
        self.pilha.push(3)
        self.assertEqual(self.pilha.pop(), 3)
        self.assertEqual(self.pilha.pop(), 2)
        self.assertEqual(self.pilha.pop(), 1)
    def test_pop_empty(self):
        with self.assertRaises(IndexError):
            self.pilha.pop()
    def test_topo_empty(self):
        with self.assertRaises(IndexError):
            self.pilha.topo()
    def test_len_coherence(self):
        self.assertEqual(len(self.pilha), 0)
        self.pilha.push(1)
        self.assertEqual(len(self.pilha), 1)
        self.pilha.push(2)
        self.assertEqual(len(self.pilha), 2)
        self.pilha.pop()
        self.assertEqual(len(self.pilha), 1)
    def test_alternating_operations(self):
        self.pilha.push(1)
        self.assertEqual(self.pilha.pop(), 1)
        self.pilha.push(2)
        self.assertEqual(self.pilha.topo(), 2)
        self.pilha.push(3)
        self.assertEqual(self.pilha.pop(), 3)
        self.assertEqual(self.pilha.pop(), 2)
    def test_different_types(self):
        self.pilha.push(1)
        self.pilha.push("string")
        self.pilha.push(None)
        self.assertEqual(self.pilha.pop(), None)
        self.assertEqual(self.pilha.pop(), "string")
        self.assertEqual(self.pilha.pop(), 1)