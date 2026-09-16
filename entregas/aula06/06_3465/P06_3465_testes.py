from .P06_3465_pilha_encadeada import PilhaEncadeada
from .P06_3465_fila_encadeada import FilaEncadeada

import unittest


class TestePilhaEncadeada(unittest.TestCase):
    def setUp(self):
        self.pilha = PilhaEncadeada()

    def testar_lifo(self):
        m = 5
        for i in range(m):
            self.pilha.push(i)
            self.assertEqual(self.pilha.topo, i)

        self.assertEqual(self.pilha.pop(), m - 1)
        self.pilha.push(m - 1)

        m -= 1
        while not self.pilha.esta_vazia():
            self.assertEqual(self.pilha.pop(), m)
            m -= 1

    def testar_excecoes_pilha_vazia(self):
        with self.assertRaises(IndexError):
            self.pilha.topo
        with self.assertRaises(IndexError):
            self.pilha.pop()

    def testar_coerencia_len(self):
        m, n, l = 10, 5, 0

        self.assertEqual(len(self.pilha), l)

        for _ in range(m):
            self.pilha.push(m)
            l += 1
            self.assertEqual(len(self.pilha), l)

        for _ in range(n):
            self.pilha.pop()
            l -= 1
            self.assertEqual(len(self.pilha), l)

        for i in range(n):
            self.pilha.push(i)
            l += 1
            self.assertEqual(len(self.pilha), l)

        for _ in range(m):
            self.pilha.pop()
            l -= 1
            self.assertEqual(len(self.pilha), l)

    def testar_alternancia_operacoes(self):
        self.pilha.push(3)
        self.pilha.push(5)
        self.assertEqual(self.pilha.topo, 5)
        self.assertEqual(self.pilha.pop(), 5)
        self.assertFalse(self.pilha.esta_vazia())
        self.assertEqual(self.pilha.pop(), 3)
        self.assertTrue(self.pilha.esta_vazia())
        self.pilha.push(4)
        self.assertEqual(self.pilha.topo, 4)

    def testar_itens_de_tipos_diversos(self):
        self.pilha.push(4)
        self.pilha.push(4)
        self.pilha.push(None)
        self.pilha.push(None)
        self.pilha.push("Str teste")
        self.pilha.push("Str teste")
        self.pilha.push("Str teste")
        self.assertEqual(len(self.pilha), 7)
        self.assertEqual(self.pilha.pop(), "Str teste")
        self.assertEqual(self.pilha.pop(), "Str teste")
        self.assertEqual(len(self.pilha), 5)
        self.assertEqual(self.pilha.pop(), "Str teste")
        self.assertEqual(len(self.pilha), 4)
        self.pilha.push(None)
        self.pilha.push(4)
        self.assertEqual(len(self.pilha), 6)
        self.assertEqual(self.pilha.pop(), 4)
        self.assertEqual(len(self.pilha), 5)
        self.assertEqual(self.pilha.pop(), None)
        self.assertEqual(len(self.pilha), 4)
        self.assertIsNone(self.pilha.topo)


class TesteFilaEncadeada(unittest.TestCase):
    def setUp(self):
        self.fila = FilaEncadeada()

    def testar_fifo(self):
        for i in range(4):
            self.fila.enfileirar(i)

        self.assertEqual(self.fila.desenfileirar(), 0)
        self.assertEqual(self.fila.desenfileirar(), 1)
        self.fila.enfileirar(0)
        self.fila.enfileirar(1)
        self.assertEqual(self.fila.desenfileirar(), 2)
        self.assertEqual(self.fila.desenfileirar(), 3)
        self.fila.enfileirar(2)
        self.fila.enfileirar(3)
        
        for i in range(4):
            self.assertEqual(self.fila.frente, i)
            self.assertEqual(self.fila.desenfileirar(), i)
            
        self.assertTrue(self.fila.esta_vazia())

    def testar_excecoes_fila_vazia(self):
        with self.assertRaises(IndexError):
            self.fila.desenfileirar()
        with self.assertRaises(IndexError):
            self.fila.frente

    def testar_esvaziar_e_reutilizar(self):
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.fila.desenfileirar()
        self.fila.desenfileirar()
        self.assertTrue(self.fila.esta_vazia())
        
        self.fila.enfileirar(3)
        self.fila.enfileirar(4)
        self.assertFalse(self.fila.esta_vazia())
        self.assertEqual(self.fila.frente, 3)

    def testar_coerencia_len(self):
        m, n, l = 10, 5, 0

        self.assertEqual(len(self.fila), l)

        for _ in range(m):
            self.fila.enfileirar(m)
            l += 1
            self.assertEqual(len(self.fila), l)

        for _ in range(n):
            self.fila.desenfileirar()
            l -= 1
            self.assertEqual(len(self.fila), l)

        for i in range(n):
            self.fila.enfileirar(i)
            l += 1
            self.assertEqual(len(self.fila), l)

        for _ in range(m):
            self.fila.desenfileirar()
            l -= 1
            self.assertEqual(len(self.fila), l)


if __name__ == '__main__':
    unittest.main()
