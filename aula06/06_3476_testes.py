import unittest
import importlib

modulo = importlib.import_module("06_3476_pilha_encadeada")
PilhaEncadeada = modulo.PilhaEncadeada
modulo2 = importlib.import_module("06_3476_fila_encadeada")
FilaEncadeada = modulo2.FilaEncadeada


class TestPilhaEncadeada(unittest.TestCase):

    def test_ordem_lifo(self):
        pilha = PilhaEncadeada()
        itens = [1, 2, 3, 4]
        for item in itens:
            pilha.push(item)

        removidos = [pilha.pop() for _ in range(len(itens))]
        self.assertEqual(removidos, [4, 3, 2, 1])

    def test_excecao_pilha_vazia(self):
        pilha = PilhaEncadeada()
        with self.assertRaises(IndexError):
            pilha.pop()
        with self.assertRaises(IndexError):
            pilha.topo()

    def test_coerencia_len(self):
        pilha = PilhaEncadeada()
        self.assertEqual(len(pilha), 0)
        pilha.push("A")
        self.assertEqual(len(pilha), 1)
        pilha.push("B")
        self.assertEqual(len(pilha), 2)
        pilha.pop()
        self.assertEqual(len(pilha), 1)
        pilha.pop()
        self.assertEqual(len(pilha), 0)

    def test_alternancia_operacoes(self):
        pilha = PilhaEncadeada()
        pilha.push(10)
        self.assertEqual(pilha.topo(), 10)
        pilha.push(20)
        self.assertEqual(pilha.pop(), 20)
        pilha.push(30)
        self.assertEqual(pilha.pop(), 30)
        self.assertEqual(pilha.pop(), 10)
        self.assertTrue(pilha.esta_vazia())

    def test_tipos_diversos_duplicados_e_none(self):
        pilha = PilhaEncadeada()
        pilha.push(100)
        pilha.push("texto")
        pilha.push(None)
        pilha.push(None)
        pilha.push(100)

        self.assertEqual(pilha.pop(), 100)
        self.assertIsNone(pilha.pop())
        self.assertIsNone(pilha.pop())
        self.assertEqual(pilha.pop(), "texto")
        self.assertEqual(pilha.pop(), 100)


class TestFilaEncadeada(unittest.TestCase):

    def test_ordem_fifo(self):
        fila = FilaEncadeada()
        itens = ["A", "B", "C", "D"]
        for item in itens:
            fila.enfileirar(item)

        removidos = [fila.desenfileirar() for _ in range(len(itens))]
        self.assertEqual(removidos, ["A", "B", "C", "D"])

    def test_intercalacao_operacoes(self):
        fila = FilaEncadeada()
        fila.enfileirar(1)
        fila.enfileirar(2)
        self.assertEqual(fila.desenfileirar(), 1)

        fila.enfileirar(3)
        self.assertEqual(fila.frente(), 2)
        self.assertEqual(fila.desenfileirar(), 2)
        self.assertEqual(fila.desenfileirar(), 3)
        self.assertTrue(fila.esta_vazia())

    def test_esvaziar_e_reutilizar(self):
        fila = FilaEncadeada()
        fila.enfileirar("X")
        fila.enfileirar("Y")
        fila.desenfileirar()
        fila.desenfileirar()
        self.assertTrue(fila.esta_vazia())

        fila.enfileirar("Z")
        self.assertEqual(fila.frente(), "Z")
        self.assertEqual(len(fila), 1)
        self.assertEqual(fila.desenfileirar(), "Z")

    def test_excecao_fila_vazia(self):
        fila = FilaEncadeada()
        with self.assertRaises(IndexError):
            fila.desenfileirar()
        with self.assertRaises(IndexError):
            fila.frente()

    def test_coerencia_len(self):
        fila = FilaEncadeada()
        self.assertEqual(len(fila), 0)
        fila.enfileirar(10)
        fila.enfileirar(20)
        self.assertEqual(len(fila), 2)
        fila.desenfileirar()
        self.assertEqual(len(fila), 1)
        fila.desenfileirar()
        self.assertEqual(len(fila), 0)


if __name__ == "__main__":
    unittest.main()