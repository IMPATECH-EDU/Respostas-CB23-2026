import unittest
import importlib

modulo_pilha = importlib.import_module("06_3467_pilha_encadeada")
PilhaEncadeada = modulo_pilha.PilhaEncadeada

modulo_fila = importlib.import_module("06_3467_fila_encadeada")
FilaEncadeada = modulo_fila.FilaEncadeada


class TestPilhaEncadeada(unittest.TestCase):

    def test_ordem_lifo(self):
        p = PilhaEncadeada()
        p.push(1)
        p.push(2)
        p.push(3)
        self.assertEqual(p.pop(), 3)
        self.assertEqual(p.pop(), 2)
        self.assertEqual(p.pop(), 1)

    def test_pop_pilha_vazia_levanta_erro(self):
        p = PilhaEncadeada()
        with self.assertRaises(IndexError):
            p.pop()

    def test_topo_pilha_vazia_levanta_erro(self):
        p = PilhaEncadeada()
        with self.assertRaises(IndexError):
            p.topo()

    def test_len_apos_insercoes_e_remocoes(self):
        p = PilhaEncadeada()
        self.assertEqual(len(p), 0)
        p.push('a')
        p.push('b')
        self.assertEqual(len(p), 2)
        p.pop()
        self.assertEqual(len(p), 1)

    def test_alternancia_push_pop(self):
        p = PilhaEncadeada()
        p.push(1)
        p.push(2)
        self.assertEqual(p.pop(), 2)
        p.push(3)
        self.assertEqual(p.pop(), 3)
        self.assertEqual(p.pop(), 1)

    def test_tipos_diferentes_incluindo_none(self):
        p = PilhaEncadeada()
        p.push(None)
        p.push(True)
        p.push('texto')
        p.push(3.14)
        self.assertEqual(p.pop(), 3.14)
        self.assertEqual(p.pop(), 'texto')
        self.assertEqual(p.pop(), True)
        self.assertEqual(p.pop(), None)

    def test_valores_repetidos(self):
        p = PilhaEncadeada()
        p.push(5)
        p.push(5)
        p.push(5)
        self.assertEqual(len(p), 3)
        self.assertEqual(p.pop(), 5)
        self.assertEqual(p.pop(), 5)
        self.assertEqual(len(p), 1)
        self.assertEqual(p.pop(), 5)
        self.assertTrue(p.esta_vazia())


class TestFilaEncadeada(unittest.TestCase):

    def test_ordem_fifo(self):
        f = FilaEncadeada()
        f.enfileirar(1)
        f.enfileirar(2)
        f.enfileirar(3)
        self.assertEqual(f.desenfileirar(), 1)  # primeiro que entrou, primeiro que sai
        self.assertEqual(f.desenfileirar(), 2)
        self.assertEqual(f.desenfileirar(), 3)

    def test_intercalar_enfileirar_desenfileirar(self):
        f = FilaEncadeada()
        f.enfileirar(1)
        f.enfileirar(2)
        self.assertEqual(f.desenfileirar(), 1)
        f.enfileirar(3)
        self.assertEqual(f.desenfileirar(), 2)
        self.assertEqual(f.desenfileirar(), 3)

    def test_esvaziar_e_reusar(self):
        f = FilaEncadeada()
        f.enfileirar(1)
        f.desenfileirar()
        self.assertTrue(f.esta_vazia())
        f.enfileirar(2)
        self.assertEqual(f.desenfileirar(), 2)

    def test_desenfileirar_fila_vazia_levanta_erro(self):
        f = FilaEncadeada()
        with self.assertRaises(IndexError):
            f.desenfileirar()

    def test_frente_fila_vazia_levanta_erro(self):
        f = FilaEncadeada()
        with self.assertRaises(IndexError):
            f.frente()

    def test_len_coerente(self):
        f = FilaEncadeada()
        self.assertEqual(len(f), 0)
        f.enfileirar('a')
        f.enfileirar('b')
        self.assertEqual(len(f), 2)
        f.desenfileirar()
        self.assertEqual(len(f), 1)

if __name__ == '__main__':
    unittest.main()