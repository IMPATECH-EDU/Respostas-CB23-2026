import unittest

from P06_3515_pilha_encadeada import PilhaEncadeada
from P06_3515_fila_encadeada import FilaEncadeada


class TestPilhaEncadeada(unittest.TestCase):
    """
    Testes da classe PilhaEncadeada.
    """

    def test_ordem_lifo(self):
        pilha = PilhaEncadeada()

        pilha.push(10)
        pilha.push(20)
        pilha.push(30)

        self.assertEqual(pilha.pop(), 30)
        self.assertEqual(pilha.pop(), 20)
        self.assertEqual(pilha.pop(), 10)

    def test_pop_em_pilha_vazia(self):
        pilha = PilhaEncadeada()

        with self.assertRaises(IndexError):
            pilha.pop()

    def test_topo_em_pilha_vazia(self):
        pilha = PilhaEncadeada()

        with self.assertRaises(IndexError):
            pilha.topo()

    def test_tamanho_apos_insercoes_e_remocoes(self):
        pilha = PilhaEncadeada()

        self.assertEqual(pilha.len(), 0)

        pilha.push("A")
        self.assertEqual(pilha.len(), 1)

        pilha.push("B")
        self.assertEqual(pilha.len(), 2)

        pilha.pop()
        self.assertEqual(pilha.len(), 1)

        pilha.pop()
        self.assertEqual(pilha.len(), 0)

    def test_alternancia_de_operacoes(self):
        pilha = PilhaEncadeada()

        pilha.push(1)
        self.assertEqual(pilha.pop(), 1)

        pilha.push(2)
        pilha.push(3)

        self.assertEqual(pilha.topo(), 3)
        self.assertEqual(pilha.pop(), 3)

        pilha.push(4)

        self.assertEqual(pilha.pop(), 4)
        self.assertEqual(pilha.pop(), 2)

    def test_tipos_diferentes_valores_repetidos_e_none(self):
        pilha = PilhaEncadeada()

        pilha.push(10)
        pilha.push("texto")
        pilha.push(None)
        pilha.push(10)

        self.assertEqual(pilha.len(), 4)
        self.assertEqual(pilha.pop(), 10)
        self.assertIsNone(pilha.pop())
        self.assertEqual(pilha.pop(), "texto")
        self.assertEqual(pilha.pop(), 10)

    def test_pilha_vazia(self):
        pilha = PilhaEncadeada()

        self.assertTrue(pilha.esta_vazia())

        pilha.push("item")

        self.assertFalse(pilha.esta_vazia())

        pilha.pop()

        self.assertTrue(pilha.esta_vazia())


class TestFilaEncadeada(unittest.TestCase):
    """
    Testes da classe FilaEncadeada.
    """

    def test_ordem_fifo(self):
        fila = FilaEncadeada()

        fila.enfileirar("A")
        fila.enfileirar("B")
        fila.enfileirar("C")

        self.assertEqual(fila.desenfileirar(), "A")
        self.assertEqual(fila.desenfileirar(), "B")
        self.assertEqual(fila.desenfileirar(), "C")

    def test_intercalacao_de_operacoes(self):
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

        fila.enfileirar("A")
        fila.enfileirar("B")

        self.assertEqual(fila.desenfileirar(), "A")
        self.assertEqual(fila.desenfileirar(), "B")

        self.assertTrue(fila.esta_vazia())

        fila.enfileirar("C")

        self.assertEqual(fila.desenfileirar(), "C")
        self.assertTrue(fila.esta_vazia())

    def test_desenfileirar_em_fila_vazia(self):
        fila = FilaEncadeada()

        with self.assertRaises(IndexError):
            fila.desenfileirar()

    def test_frente_em_fila_vazia(self):
        fila = FilaEncadeada()

        with self.assertRaises(IndexError):
            fila.frente()

    def test_tamanho_da_fila(self):
        fila = FilaEncadeada()

        self.assertEqual(fila.len(), 0)

        fila.enfileirar(1)
        self.assertEqual(fila.len(), 1)

        fila.enfileirar(2)
        self.assertEqual(fila.len(), 2)

        fila.desenfileirar()
        self.assertEqual(fila.len(), 1)

        fila.desenfileirar()
        self.assertEqual(fila.len(), 0)

    def test_frente_sem_remover(self):
        fila = FilaEncadeada()

        fila.enfileirar("primeiro")
        fila.enfileirar("segundo")

        self.assertEqual(fila.frente(), "primeiro")
        self.assertEqual(fila.len(), 2)
        self.assertEqual(fila.desenfileirar(), "primeiro")

    def test_fila_vazia(self):
        fila = FilaEncadeada()

        self.assertTrue(fila.esta_vazia())

        fila.enfileirar("item")

        self.assertFalse(fila.esta_vazia())

        fila.desenfileirar()

        self.assertTrue(fila.esta_vazia())


if __name__ == "__main__":
    unittest.main()