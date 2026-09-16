import unittest

from P06_3466_pilha_encadeada import PilhaEncadeada
from P06_3466_fila_encadeada import FilaEncadeada


class TestPilhaEncadeada(unittest.TestCase):
    """Testes da pilha encadeada."""

    def test_lifo(self):
        """Verifica o comportamento LIFO."""
        pilha = PilhaEncadeada()

        pilha.push(10)
        pilha.push(20)
        pilha.push(30)

        self.assertEqual(pilha.pop(), 30)
        self.assertEqual(pilha.pop(), 20)
        self.assertEqual(pilha.pop(), 10)

    def test_pop_e_topo_em_pilha_vazia(self):
        """Verifica exceções ao operar sobre pilha vazia."""
        pilha = PilhaEncadeada()

        with self.assertRaises(IndexError):
            pilha.pop()

        with self.assertRaises(IndexError):
            pilha.topo()

    def test_len(self):
        """Verifica a quantidade de elementos."""
        pilha = PilhaEncadeada()

        self.assertEqual(pilha.len(), 0)

        pilha.push("A")
        pilha.push("B")
        self.assertEqual(pilha.len(), 2)

        pilha.pop()
        self.assertEqual(pilha.len(), 1)

        pilha.pop()
        self.assertEqual(pilha.len(), 0)

    def test_operacoes_alternadas(self):
        """Verifica inserções e remoções alternadas."""
        pilha = PilhaEncadeada()

        pilha.push(1)
        self.assertEqual(pilha.pop(), 1)

        pilha.push(2)
        pilha.push(3)
        self.assertEqual(pilha.topo(), 3)

        pilha.push(4)
        self.assertEqual(pilha.pop(), 4)
        self.assertEqual(pilha.pop(), 3)
        self.assertEqual(pilha.pop(), 2)

    def test_diferentes_tipos_e_valores_repetidos(self):
        """Verifica diferentes tipos, valores repetidos e None."""
        pilha = PilhaEncadeada()

        pilha.push(None)
        pilha.push("texto")
        pilha.push(42)
        pilha.push("texto")
        pilha.push(None)

        self.assertEqual(pilha.pop(), None)
        self.assertEqual(pilha.pop(), "texto")
        self.assertEqual(pilha.pop(), 42)
        self.assertEqual(pilha.pop(), "texto")
        self.assertEqual(pilha.pop(), None)

    def test_esta_vazia(self):
        """Verifica o estado de uma pilha vazia e após operações."""
        pilha = PilhaEncadeada()

        self.assertTrue(pilha.esta_vazia())

        pilha.push(1)
        self.assertFalse(pilha.esta_vazia())

        pilha.pop()
        self.assertTrue(pilha.esta_vazia())


class TestFilaEncadeada(unittest.TestCase):
    """Testes da fila encadeada."""

    def test_fifo(self):
        """Verifica o comportamento FIFO."""
        fila = FilaEncadeada()

        fila.enfileirar(10)
        fila.enfileirar(20)
        fila.enfileirar(30)

        self.assertEqual(fila.desenfileirar(), 10)
        self.assertEqual(fila.desenfileirar(), 20)
        self.assertEqual(fila.desenfileirar(), 30)

    def test_operacoes_intercaladas(self):
        """Verifica operações de entrada e saída intercaladas."""
        fila = FilaEncadeada()

        fila.enfileirar("A")
        fila.enfileirar("B")
        self.assertEqual(fila.desenfileirar(), "A")

        fila.enfileirar("C")
        fila.enfileirar("D")

        self.assertEqual(fila.desenfileirar(), "B")
        self.assertEqual(fila.desenfileirar(), "C")

        fila.enfileirar("E")
        self.assertEqual(fila.desenfileirar(), "D")
        self.assertEqual(fila.desenfileirar(), "E")

    def test_fila_vazia_e_reutilizacao(self):
        """Verifica esvaziamento e reutilização da mesma fila."""
        fila = FilaEncadeada()

        self.assertTrue(fila.esta_vazia())

        fila.enfileirar(1)
        fila.enfileirar(2)

        self.assertEqual(fila.desenfileirar(), 1)
        self.assertEqual(fila.desenfileirar(), 2)
        self.assertTrue(fila.esta_vazia())

        fila.enfileirar(3)
        self.assertFalse(fila.esta_vazia())
        self.assertEqual(fila.frente(), 3)
        self.assertEqual(fila.desenfileirar(), 3)

    def test_desinfileirar_e_frente_em_fila_vazia(self):
        """Verifica exceções ao operar sobre fila vazia."""
        fila = FilaEncadeada()

        with self.assertRaises(IndexError):
            fila.desenfileirar()

        with self.assertRaises(IndexError):
            fila.frente()

    def test_len(self):
        """Verifica a quantidade de elementos da fila."""
        fila = FilaEncadeada()

        self.assertEqual(fila.len(), 0)

        fila.enfileirar("A")
        fila.enfileirar("B")
        fila.enfileirar("C")
        self.assertEqual(fila.len(), 3)

        fila.desenfileirar()
        self.assertEqual(fila.len(), 2)

        fila.desenfileirar()
        fila.desenfileirar()
        self.assertEqual(fila.len(), 0)

    def test_frente_sem_remover(self):
        """Verifica que frente não remove o elemento."""
        fila = FilaEncadeada()

        fila.enfileirar(10)
        fila.enfileirar(20)

        self.assertEqual(fila.frente(), 10)
        self.assertEqual(fila.len(), 2)
        self.assertEqual(fila.frente(), 10)

        self.assertEqual(fila.desenfileirar(), 10)
        self.assertEqual(fila.desenfileirar(), 20)


if __name__ == "__main__":
    unittest.main()