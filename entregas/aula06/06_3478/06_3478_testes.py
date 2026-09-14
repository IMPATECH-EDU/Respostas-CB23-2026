import unittest
import importlib

#Importando os módulos dinamicamente devido aos nomes iniciarem com números
mod_pilha = importlib.import_module("06_3478_pilha_encadeada")
PilhaEncadeada = mod_pilha.PilhaEncadeada

mod_fila = importlib.import_module("06_3478_fila_encadeada")
FilaEncadeada = mod_fila.FilaEncadeada

class TestPilhaEncadeada(unittest.TestCase):
    def setUp(self):
        self.pilha = PilhaEncadeada()

    def test_ordem_lifo(self):
        """Testa se a ordem LIFO (Último a Entrar, Primeiro a Sair) é respeitada."""
        self.pilha.push(1)
        self.pilha.push(2)
        self.pilha.push(3)
        self.assertEqual(self.pilha.pop(), 3)
        self.assertEqual(self.pilha.pop(), 2)
        self.assertEqual(self.pilha.pop(), 1)

    def test_pilha_vazia_excecoes(self):
        """Testa se pop e topo levantam IndexError em pilha vazia."""
        with self.assertRaises(IndexError):
            self.pilha.pop()
        with self.assertRaises(IndexError):
            self.pilha.topo()

    def test_coerencia_len(self):
        """Testa a coerência do tamanho após inserções e remoções."""
        self.assertEqual(len(self.pilha), 0)
        self.pilha.push(10)
        self.assertEqual(len(self.pilha), 1)
        self.pilha.push(20)
        self.assertEqual(len(self.pilha), 2)
        self.pilha.pop()
        self.assertEqual(len(self.pilha), 1)
        self.pilha.pop()
        self.assertEqual(len(self.pilha), 0)

    def test_alternancia_operacoes(self):
        """Testa a alternância de operações (push e pop intercalados)."""
        self.pilha.push(1)
        self.assertEqual(self.pilha.pop(), 1)
        self.pilha.push(2)
        self.pilha.push(3)
        self.assertEqual(self.pilha.pop(), 3)
        self.pilha.push(4)
        self.assertEqual(self.pilha.pop(), 4)
        self.assertEqual(self.pilha.pop(), 2)

    def test_tipos_diferentes_e_repetidos(self):
        """Testa armazenamento de itens de tipos diferentes, valores repetidos e None."""
        self.pilha.push("texto")
        self.pilha.push(None)
        self.pilha.push(3.14)
        self.pilha.push(3.14)
        
        self.assertEqual(self.pilha.pop(), 3.14)
        self.assertEqual(self.pilha.pop(), 3.14)
        self.assertIsNone(self.pilha.pop())
        self.assertEqual(self.pilha.pop(), "texto")


class TestFilaEncadeada(unittest.TestCase):
    def setUp(self):
        self.fila = FilaEncadeada()

    def test_ordem_fifo(self):
        """Testa se a ordem FIFO (Primeiro a Entrar, Primeiro a Sair) é respeitada."""
        self.fila.enfileirar("A")
        self.fila.enfileirar("B")
        self.fila.enfileirar("C")
        self.assertEqual(self.fila.desenfileirar(), "A")
        self.assertEqual(self.fila.desenfileirar(), "B")
        self.assertEqual(self.fila.desenfileirar(), "C")

    def test_intercalacao_operacoes(self):
        """Testa a intercalação de enfileirar e desenfileirar."""
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.assertEqual(self.fila.desenfileirar(), 1)
        self.fila.enfileirar(3)
        self.assertEqual(self.fila.desenfileirar(), 2)
        self.assertEqual(self.fila.desenfileirar(), 3)

    def test_esvaziar_e_reusar(self):
        """Testa esvaziar e voltar a usar a mesma instância."""
        self.fila.enfileirar(10)
        self.fila.enfileirar(20)
        self.fila.desenfileirar()
        self.fila.desenfileirar()
        self.assertTrue(self.fila.esta_vazia())
        
        #Reutilizando
        self.fila.enfileirar(30)
        self.assertEqual(self.fila.desenfileirar(), 30)

    def test_fila_vazia_excecoes(self):
        """Testa se desenfileirar e frente levantam IndexError em fila vazia."""
        with self.assertRaises(IndexError):
            self.fila.desenfileirar()
        with self.assertRaises(IndexError):
            self.fila.frente()

    def test_coerencia_len(self):
        """Testa a coerência do tamanho da fila."""
        self.assertEqual(len(self.fila), 0)
        self.fila.enfileirar(100)
        self.assertEqual(len(self.fila), 1)
        self.fila.enfileirar(200)
        self.assertEqual(len(self.fila), 2)
        self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 1)
        self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 0)

if __name__ == "__main__":
    unittest.main()