import P06_3461_pilha_encadeada as _pilha
import P06_3461_fila_encadeada as _fila
import unittest

class TestPilhaEncadeada(unittest.TestCase):
    def setUp(self):
        self.pilha = _pilha.PilhaEncadeada()

    def test_ordem_lifo(self):
        """Ordem LIFO em sequência de push/pop"""
        self.pilha.push("Primeiro")
        self.pilha.push("Segundo")
        self.pilha.push("Terceiro")
        self.assertEqual(self.pilha.pop(), "Terceiro")
        self.assertEqual(self.pilha.pop(), "Segundo")
        self.assertEqual(self.pilha.pop(), "Primeiro")

    def test_excecao_pilha_vazia(self):
        """pop e topo em pilha vazia"""
        with self.assertRaises(IndexError):
            self.pilha.pop()
        with self.assertRaises(IndexError):
            self.pilha.topo()

    def test_coerencia_len(self):
        """Coerência de len após inserções e remoções"""
        self.assertEqual(self.pilha.len(), 0)
        self.pilha.push("A")
        self.assertEqual(self.pilha.len(), 1)
        self.pilha.push("B")
        self.assertEqual(self.pilha.len(), 2)
        self.pilha.pop()
        self.assertEqual(self.pilha.len(), 1)
        self.pilha.pop()
        self.assertEqual(self.pilha.len(), 0)

    def test_alternancia_operacoes(self):
        """Alternância de operações"""
        self.pilha.push(1)
        self.assertEqual(self.pilha.pop(), 1)
        self.pilha.push(2)
        self.pilha.push(3)
        self.assertEqual(self.pilha.pop(), 3)
        self.pilha.push(4)
        self.assertEqual(self.pilha.pop(), 4)
        self.assertEqual(self.pilha.pop(), 2)

    def test_tipos_diferentes_repetidos_none(self):
        """Armazenamento de itens de tipos diferentes, repetidos e None"""
        self.pilha.push(100)           # Inteiro
        self.pilha.push("Texto")       # String
        self.pilha.push(100)           # Repetido
        self.pilha.push(None)          # None
        
        self.assertIsNone(self.pilha.pop())
        self.assertEqual(self.pilha.pop(), 100)
        self.assertEqual(self.pilha.pop(), "Texto")
        self.assertEqual(self.pilha.pop(), 100)

class TestFilaEncadeada(unittest.TestCase):
    def setUp(self):
        self.fila = _fila.FilaEncadeada()

    def test_ordem_fifo(self):
        """Ordem FIFO"""
        self.fila.enfileirar("A")
        self.fila.enfileirar("B")
        self.fila.enfileirar("C")
        self.assertEqual(self.fila.desenfileirar(), "A")
        self.assertEqual(self.fila.desenfileirar(), "B")
        self.assertEqual(self.fila.desenfileirar(), "C")

    def test_intercalacao_operacoes(self):
        """Intercalação de enfileirar e desenfileirar"""
        self.fila.enfileirar(1)
        self.assertEqual(self.fila.desenfileirar(), 1)
        self.fila.enfileirar(2)
        self.fila.enfileirar(3)
        self.assertEqual(self.fila.desenfileirar(), 2)
        self.fila.enfileirar(4)
        self.assertEqual(self.fila.desenfileirar(), 3)
        self.assertEqual(self.fila.desenfileirar(), 4)

    def test_esvaziar_e_reutilizar(self):
        """Esvaziar e voltar a usar a mesma instância"""
        # Esvazia a fila
        self.fila.enfileirar("X")
        self.fila.enfileirar("Y")
        self.fila.desenfileirar()
        self.fila.desenfileirar()
        
        self.assertTrue(self.fila.esta_vazia())
        
        # Volta a usar
        self.fila.enfileirar("Z")
        self.assertEqual(self.fila.len(), 1)
        self.assertEqual(self.fila.desenfileirar(), "Z")

    def test_excecao_fila_vazia(self):
        """Desenfileirar e frente em fila vazia"""
        with self.assertRaises(IndexError):
            self.fila.desenfileirar()
        with self.assertRaises(IndexError):
            self.fila.frente()

    def test_coerencia_len(self):
        """Coerência de len"""
        self.assertEqual(self.fila.len(), 0)
        self.fila.enfileirar(10)
        self.assertEqual(self.fila.len(), 1)
        self.fila.enfileirar(20)
        self.assertEqual(self.fila.len(), 2)
        self.fila.desenfileirar()
        self.assertEqual(self.fila.len(), 1)
        self.fila.desenfileirar()
        self.assertEqual(self.fila.len(), 0)

if __name__ == "__main__":
    unittest.main()