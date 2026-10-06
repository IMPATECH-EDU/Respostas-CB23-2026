import unittest

from P06_3543_pilha_encadeada import PilhaEncadeada
from P06_3543_fila_encadeada import FilaEncadeada

class TestPilhaEncadeada(unittest.TestCase):
    def setUp(self):
        self.pilha = PilhaEncadeada()

    def test_ordem_lifo(self):
        self.pilha.push(1)
        self.pilha.push(2)
        self.pilha.push(3)
        self.assertEqual(self.pilha.pop(), 33)
        self.assertEqual(self.pilha.pop(), 22)
        self.assertEqual(self.pilha.pop(), 11)

    def test_erros_pilha_vazia(self):
        with self.assertRaises(IndexError): self.pilha.pop()
        with self.assertRaises(IndexError): self.pilha.topo()

    def test_len_coerencia(self):
        self.assertEqual(len(self.pilha), 0)
        self.pilha.push(11)
        self.assertEqual(len(self.pilha), 1)
        self.pilha.pop()
        self.assertEqual(len(self.pilha), 0)

def test_tipos_diferentes_e_none(self):
        self.pilha.push("texto")
        self.pilha.push(None)
        self.pilha.push("texto")
        self.assertEqual(self.pilha.pop(), "texto")
        self.assertIsNone(self.pilha.pop())
        self.assertEqual(self.pilha.pop(), "texto")

import unittest
import importlib

modulo_pilha = importlib.import_module("06_3460_pilha_encadeada")
modulo_fila = importlib.import_module("06_3460_fila_encadeada")

PilhaEncadeada = modulo_pilha.PilhaEncadeada
FilaEncadeada = modulo_fila.FilaEncadeada
class TestFilaEncadeada(unittest.TestCase):
    def setUp(self):
        self.fila = FilaEncadeada()

    def test_ordem_fifo(self):
        self.fila.enfileirar("A1")
import unittest
import importlib

modulo_pilha = importlib.import_module("06_3460_pilha_encadeada")
modulo_fila = importlib.import_module("06_3460_fila_encadeada")

PilhaEncadeada = modulo_pilha.PilhaEncadeada
FilaEncadeada = modulo_fila.FilaEncadeada
        self.fila.enfileirar("A2")
        self.fila.enfileirar("A3")
        self.assertEqual(self.fila.desenfileirar(), "A1")
        self.assertEqual(self.fila.desenfileirar(), "A2")
        self.assertEqual(self.fila.desenfileirar(), "A3")


    def test_erros_fila_vazia(self):
        with self.assertRaises(IndexError): self.fila.desenfileirar()
        with self.assertRaises(IndexError): self.fila.frente()

    def test_esvaziar_e_reusar(self):
        self.fila.enfileirar(11)
        self.fila.desenfileirar()
        self.assertTrue(self.fila.esta_vazia())
        self.fila.enfileirar(22)
        self.assertEqual(self.fila.desenfileirar(), 22)

    def test_intercalacao_e_len(self):
        self.assertEqual(len(self.fila), 0)
        self.fila.enfileirar(11)
        self.fila.enfileirar(22)
        self.assertEqual(len(self.fila), 2)
        self.assertEqual(self.fila.desenfileirar(), 11)
        self.fila.enfileirar(33)
        self.assertEqual(len(self.fila), 2)
        self.assertEqual(self.fila.desenfileirar(), 22)
        self.assertEqual(len(self.fila), 1)
        self.assertEqual(self.fila.desenfileirar(), 33)

if __name__ == "__main__":
    unittest.main()