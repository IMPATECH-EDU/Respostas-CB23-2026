import unittest


exec(open("06_3459_pilha_encadeada.py", encoding="utf-8").read())

PilhaTestada = PilhaEncadeada

exec(open("06_3459_fila_encadeada.py", encoding="utf-8").read())

FilaTestada = FilaEncadeada


class TestePilhaEncadeada(unittest.TestCase):

    def test_lifo(self):
        pilha = PilhaTestada()

        pilha.push(1)
        pilha.push(2)
        pilha.push(3)

        self.assertEqual(pilha.pop(), 3)
        self.assertEqual(pilha.pop(), 2)
        self.assertEqual(pilha.pop(), 1)

    def test_pilha_vazia(self):
        pilha = PilhaTestada()

        self.assertTrue(pilha.esta_vazia())
        self.assertEqual(len(pilha), 0)

    def test_pop_pilha_vazia(self):
        pilha = PilhaTestada()

        with self.assertRaises(IndexError):
            pilha.pop()

    def test_topo_pilha_vazia(self):
        pilha = PilhaTestada()

        with self.assertRaises(IndexError):
            pilha.topo()

    def test_len_pilha(self):
        pilha = PilhaTestada()

        self.assertEqual(len(pilha), 0)

        pilha.push(10)
        self.assertEqual(len(pilha), 1)

        pilha.push(20)
        self.assertEqual(len(pilha), 2)

        pilha.pop()
        self.assertEqual(len(pilha), 1)

        pilha.pop()
        self.assertEqual(len(pilha), 0)

    def test_alternancia(self):
        pilha = PilhaTestada()

        pilha.push(10)
        self.assertEqual(pilha.topo(), 10)

        pilha.push(20)
        self.assertEqual(pilha.pop(), 20)

        pilha.push(30)
        self.assertEqual(pilha.topo(), 30)

        self.assertEqual(pilha.pop(), 30)
        self.assertEqual(pilha.pop(), 10)

    def test_diferentes_tipos(self):
        pilha = PilhaTestada()

        pilha.push(10)
        pilha.push("texto")
        pilha.push(None)
        pilha.push(10)

        self.assertEqual(pilha.pop(), 10)
        self.assertIsNone(pilha.pop())
        self.assertEqual(pilha.pop(), "texto")
        self.assertEqual(pilha.pop(), 10)

        self.assertTrue(pilha.esta_vazia())


class TesteFilaEncadeada(unittest.TestCase):

    def test_fifo(self):
        fila = FilaTestada()

        fila.enfileirar(1)
        fila.enfileirar(2)
        fila.enfileirar(3)

        self.assertEqual(fila.desenfileirar(), 1)
        self.assertEqual(fila.desenfileirar(), 2)
        self.assertEqual(fila.desenfileirar(), 3)

    def test_frente(self):
        fila = FilaTestada()

        fila.enfileirar(10)
        fila.enfileirar(20)

        self.assertEqual(fila.frente(), 10)
        self.assertEqual(len(fila), 2)

    def test_intercalacao(self):
        fila = FilaTestada()

        fila.enfileirar(1)
        fila.enfileirar(2)

        self.assertEqual(fila.desenfileirar(), 1)

        fila.enfileirar(3)
        fila.enfileirar(4)

        self.assertEqual(fila.desenfileirar(), 2)
        self.assertEqual(fila.desenfileirar(), 3)
        self.assertEqual(fila.desenfileirar(), 4)

    def test_fila_vazia(self):
        fila = FilaTestada()

        self.assertTrue(fila.esta_vazia())
        self.assertEqual(len(fila), 0)

    def test_desenfileirar_fila_vazia(self):
        fila = FilaTestada()

        with self.assertRaises(IndexError):
            fila.desenfileirar()

    def test_frente_fila_vazia(self):
        fila = FilaTestada()

        with self.assertRaises(IndexError):
            fila.frente()

    def test_reutilizacao(self):
        fila = FilaTestada()

        fila.enfileirar(10)
        self.assertEqual(fila.desenfileirar(), 10)
        self.assertTrue(fila.esta_vazia())

        fila.enfileirar(20)
        fila.enfileirar(30)

        self.assertEqual(fila.desenfileirar(), 20)
        self.assertEqual(fila.desenfileirar(), 30)

        self.assertTrue(fila.esta_vazia())

    def test_len_fila(self):
        fila = FilaTestada()

        self.assertEqual(len(fila), 0)

        fila.enfileirar(10)
        self.assertEqual(len(fila), 1)

        fila.enfileirar(20)
        self.assertEqual(len(fila), 2)

        fila.desenfileirar()
        self.assertEqual(len(fila), 1)

        fila.desenfileirar()
        self.assertEqual(len(fila), 0)

    def test_none_e_repetidos(self):
        fila = FilaTestada()

        fila.enfileirar(None)
        fila.enfileirar(5)
        fila.enfileirar(5)
        fila.enfileirar(None)

        self.assertIsNone(fila.desenfileirar())
        self.assertEqual(fila.desenfileirar(), 5)
        self.assertEqual(fila.desenfileirar(), 5)
        self.assertIsNone(fila.desenfileirar())

        self.assertTrue(fila.esta_vazia())


if __name__ == "__main__":
    unittest.main()