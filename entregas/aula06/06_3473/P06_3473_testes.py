import unittest

import P06_3473_pilha_encadeada 
import P06_3473_fila_encadeada

class TestPilhaEncadeada(unittest.TestCase):

    def setUp(self):
        self.pilha = P06_3473_pilha_encadeada.PilhaEncadeada()

    def test_ordem_lifo(self):
        """Verifica se a pilha segue a ordem LIFO."""
        self.pilha.push(10)
        self.pilha.push(20)
        self.pilha.push(30)

        self.assertEqual(self.pilha.pop(), 30)
        self.assertEqual(self.pilha.pop(), 20)
        self.assertEqual(self.pilha.pop(), 10)

    def test_pop_pilha_vazia(self):
        """Verifica se pop levanta IndexError em pilha vazia."""
        with self.assertRaises(IndexError):
            self.pilha.pop()

    def test_topo_pilha_vazia(self):
        """Verifica se topo levanta IndexError em pilha vazia."""
        with self.assertRaises(IndexError):
            self.pilha.topo()

    def test_len(self):
        """Verifica se o tamanho é atualizado corretamente."""
        self.assertEqual(len(self.pilha), 0)

        self.pilha.push(10)
        self.assertEqual(len(self.pilha), 1)

        self.pilha.push(20)
        self.assertEqual(len(self.pilha), 2)

        self.pilha.push(30)
        self.assertEqual(len(self.pilha), 3)

        self.pilha.pop()
        self.assertEqual(len(self.pilha), 2)

        self.pilha.pop()
        self.assertEqual(len(self.pilha), 1)

        self.pilha.pop()
        self.assertEqual(len(self.pilha), 0)

    def test_esta_vazia(self):
        """Verifica o comportamento de esta_vazia."""
        self.assertTrue(self.pilha.esta_vazia())

        self.pilha.push(10)

        self.assertFalse(self.pilha.esta_vazia())

        self.pilha.pop()

        self.assertTrue(self.pilha.esta_vazia())

    def test_alternancia_de_operacoes(self):
        """Verifica uma sequência alternada de push e pop."""
        self.pilha.push(10)
        self.assertEqual(self.pilha.pop(), 10)

        self.pilha.push(20)
        self.pilha.push(30)
        self.assertEqual(self.pilha.pop(), 30)

        self.pilha.push(40)
        self.assertEqual(self.pilha.topo(), 40)

        self.assertEqual(self.pilha.pop(), 40)
        self.assertEqual(self.pilha.pop(), 20)

        self.assertTrue(self.pilha.esta_vazia())

    def test_tipos_diferentes_valores_repetidos_e_none(self):
        """Verifica diferentes tipos, valores repetidos e None."""
        self.pilha.push(10)
        self.pilha.push("Python")
        self.pilha.push(None)
        self.pilha.push(10)
        self.pilha.push(3.14)

        self.assertEqual(self.pilha.pop(), 3.14)
        self.assertEqual(self.pilha.pop(), 10)
        self.assertIsNone(self.pilha.pop())
        self.assertEqual(self.pilha.pop(), "Python")
        self.assertEqual(self.pilha.pop(), 10)

        self.assertTrue(self.pilha.esta_vazia())

    def test_topo_nao_remove(self):
        """Verifica se topo apenas consulta o elemento."""
        self.pilha.push(10)
        self.pilha.push(20)

        self.assertEqual(self.pilha.topo(), 20)
        self.assertEqual(len(self.pilha), 2)
        self.assertEqual(self.pilha.topo(), 20)


class TestFilaEncadeada(unittest.TestCase):

    def setUp(self):
        self.fila = P06_3473_fila_encadeada.FilaEncadeada()

    def test_ordem_fifo(self):
        """Verifica se a fila segue a ordem FIFO."""
        self.fila.enfileirar(10)
        self.fila.enfileirar(20)
        self.fila.enfileirar(30)

        self.assertEqual(self.fila.desenfileirar(), 10)
        self.assertEqual(self.fila.desenfileirar(), 20)
        self.assertEqual(self.fila.desenfileirar(), 30)

    def test_intercalacao_enfileirar_desenfileirar(self):
        """Verifica operações intercaladas."""
        self.fila.enfileirar(10)
        self.fila.enfileirar(20)

        self.assertEqual(self.fila.desenfileirar(), 10)

        self.fila.enfileirar(30)
        self.fila.enfileirar(40)

        self.assertEqual(self.fila.desenfileirar(), 20)
        self.assertEqual(self.fila.desenfileirar(), 30)

        self.fila.enfileirar(50)

        self.assertEqual(self.fila.desenfileirar(), 40)
        self.assertEqual(self.fila.desenfileirar(), 50)

    def test_esvaziar_e_reutilizar(self):
        """Verifica se a mesma fila pode ser reutilizada após esvaziar."""
        self.fila.enfileirar(10)
        self.fila.enfileirar(20)

        self.assertEqual(self.fila.desenfileirar(), 10)
        self.assertEqual(self.fila.desenfileirar(), 20)

        self.assertTrue(self.fila.esta_vazia())

        self.fila.enfileirar(30)
        self.fila.enfileirar(40)

        self.assertEqual(self.fila.desenfileirar(), 30)
        self.assertEqual(self.fila.desenfileirar(), 40)

        self.assertTrue(self.fila.esta_vazia())

    def test_desenfileirar_fila_vazia(self):
        """Verifica se desenfileirar levanta IndexError em fila vazia."""
        with self.assertRaises(IndexError):
            self.fila.desenfileirar()

    def test_frente_fila_vazia(self):
        """Verifica se frente levanta IndexError em fila vazia."""
        with self.assertRaises(IndexError):
            self.fila.frente()

    def test_frente_nao_remove(self):
        """Verifica se frente apenas consulta o primeiro elemento."""
        self.fila.enfileirar(10)
        self.fila.enfileirar(20)
        self.fila.enfileirar(30)

        self.assertEqual(self.fila.frente(), 10)
        self.assertEqual(self.fila.frente(), 10)
        self.assertEqual(len(self.fila), 3)

        self.assertEqual(self.fila.desenfileirar(), 10)

    def test_len(self):
        """Verifica se o tamanho da fila é atualizado corretamente."""
        self.assertEqual(len(self.fila), 0)

        self.fila.enfileirar(10)
        self.assertEqual(len(self.fila), 1)

        self.fila.enfileirar(20)
        self.assertEqual(len(self.fila), 2)

        self.fila.enfileirar(30)
        self.assertEqual(len(self.fila), 3)

        self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 2)

        self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 1)

        self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 0)

    def test_esta_vazia(self):
        """Verifica o comportamento de esta_vazia."""
        self.assertTrue(self.fila.esta_vazia())

        self.fila.enfileirar(10)

        self.assertFalse(self.fila.esta_vazia())

        self.fila.desenfileirar()

        self.assertTrue(self.fila.esta_vazia())

    def test_frente_depois_de_intercalacao(self):
        """Verifica frente após operações em ambas as pilhas."""
        self.fila.enfileirar(10)
        self.fila.enfileirar(20)
        self.fila.enfileirar(30)

        self.assertEqual(self.fila.desenfileirar(), 10)

        self.fila.enfileirar(40)
        self.fila.enfileirar(50)

        self.assertEqual(self.fila.frente(), 20)
        self.assertEqual(len(self.fila), 4)

        self.assertEqual(self.fila.desenfileirar(), 20)
        self.assertEqual(self.fila.frente(), 30)


if __name__ == "__main__":
    unittest.main()