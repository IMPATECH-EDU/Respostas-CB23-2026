import unittest
from P06_3521_pilha_encadeada import PilhaEncadeada
from P06_3521_fila_encadeada import FilaEncadeada
 
 
# Testes da PilhaEncadeada
 
class TestPilhaEncadeadaLIFO(unittest.TestCase):
    """Verifica se a ordem de saída dos elementos é LIFO (Last In, First Out)."""
 
    def test_ordem_lifo_sequencia_push_pop(self):
        pilha = PilhaEncadeada()
        pilha.push(10)
        pilha.push(20)
        pilha.push(30)
 
        # O último a entrar deve ser o primeiro a sair.
        self.assertEqual(pilha.pop(), 30)
        self.assertEqual(pilha.pop(), 20)
        self.assertEqual(pilha.pop(), 10)
 
    def test_ordem_lifo_com_topo(self):
        pilha = PilhaEncadeada()
        pilha.push(1)
        pilha.push(2)
        pilha.push(3)
 
        # topo() não deve remover o elemento.
        self.assertEqual(pilha.topo(), 3)
        self.assertEqual(pilha.topo(), 3)
 
        self.assertEqual(pilha.pop(), 3)
        self.assertEqual(pilha.topo(), 2)
 
 
class TestPilhaEncadeadaVazia(unittest.TestCase):
    """Verifica o comportamento de pop() e topo() quando a pilha está vazia."""
 
    def test_pop_pilha_vazia_levanta_excecao(self):
        pilha = PilhaEncadeada()
        with self.assertRaises(IndexError):
            pilha.pop()
 
    def test_topo_pilha_vazia_levanta_excecao(self):
        pilha = PilhaEncadeada()
        with self.assertRaises(IndexError):
            pilha.topo()
 
    def test_esta_vazia_no_inicio(self):
        pilha = PilhaEncadeada()
        self.assertTrue(pilha.esta_vazia())
 
 
class TestPilhaEncadeadaLen(unittest.TestCase):
    """Verifica a coerência de len() após inserções e remoções."""
 
    def test_len_apos_insercoes_e_remocoes(self):
        pilha = PilhaEncadeada()
        self.assertEqual(len(pilha), 0)
 
        pilha.push(10)
        self.assertEqual(len(pilha), 1)
 
        pilha.pop()
        self.assertEqual(len(pilha), 0)
 
    def test_len_com_varias_insercoes(self):
        pilha = PilhaEncadeada()
        for i in range(5):
            pilha.push(i)
        self.assertEqual(len(pilha), 5)
 
        pilha.pop()
        pilha.pop()
        self.assertEqual(len(pilha), 3)
 
 
class TestPilhaEncadeadaAlternancia(unittest.TestCase):
    """Verifica a alternância entre push e pop, incluindo esta_vazia()."""
 
    def test_alternancia_push_pop(self):
        pilha = PilhaEncadeada()
        self.assertTrue(pilha.esta_vazia())
 
        pilha.push(10)
        pilha.push(30)
        pilha.push(20)
        self.assertEqual(len(pilha), 3)
        self.assertFalse(pilha.esta_vazia())
 
        self.assertEqual(pilha.pop(), 20)
        self.assertEqual(len(pilha), 2)
 
        self.assertEqual(pilha.pop(), 30)
        self.assertEqual(len(pilha), 1)
 
        pilha.push(50)
        self.assertEqual(len(pilha), 2)
        self.assertEqual(pilha.topo(), 50)
 
        self.assertFalse(pilha.esta_vazia())
 
    def test_esvaziar_e_reutilizar(self):
        pilha = PilhaEncadeada()
        pilha.push(1)
        pilha.push(2)
        pilha.pop()
        pilha.pop()
        self.assertTrue(pilha.esta_vazia())
 
        # Reutiliza a mesma instância após esvaziar.
        pilha.push(99)
        self.assertEqual(pilha.topo(), 99)
        self.assertEqual(len(pilha), 1)
 
 
class TestPilhaEncadeadaTiposDiferentes(unittest.TestCase):
    """Verifica o armazenamento de itens de tipos diferentes, repetidos e None."""
 
    def test_tipos_diferentes(self):
        pilha = PilhaEncadeada()
        pilha.push("ABC")
        pilha.push(10)
        pilha.push(True)
        pilha.push(10.0)
 
        self.assertEqual(len(pilha), 4)
        self.assertEqual(pilha.pop(), 10.0)
        self.assertEqual(pilha.pop(), True)
        self.assertEqual(pilha.pop(), 10)
        self.assertEqual(pilha.pop(), "ABC")
 
    def test_valores_repetidos(self):
        pilha = PilhaEncadeada()
        pilha.push(7)
        pilha.push(7)
        pilha.push(7)
 
        self.assertEqual(len(pilha), 3)
        self.assertEqual(pilha.pop(), 7)
        self.assertEqual(pilha.pop(), 7)
        self.assertEqual(pilha.pop(), 7)
        self.assertTrue(pilha.esta_vazia())
 
    def test_valor_none(self):
        pilha = PilhaEncadeada()
        pilha.push(None)
        pilha.push(1)
 
        self.assertEqual(len(pilha), 2)
        self.assertEqual(pilha.pop(), 1)
        # None é um valor de dado legítimo, diferente de uma pilha vazia.
        self.assertFalse(pilha.esta_vazia())
        self.assertIsNone(pilha.pop())
        self.assertTrue(pilha.esta_vazia())
 
 
# Testes da FilaEncadeada
 
class TestFilaEncadeadaFIFO(unittest.TestCase):
    """Verifica se a ordem de saída dos elementos é FIFO (First In, First Out)."""
 
    def test_ordem_fifo_sequencia_enfileirar_desenfileirar(self):
        fila = FilaEncadeada()
        fila.enfileirar(10)
        fila.enfileirar(20)
        fila.enfileirar(30)
 
        # O primeiro a entrar deve ser o primeiro a sair.
        self.assertEqual(fila.desenfileirar(), 10)
        self.assertEqual(fila.desenfileirar(), 20)
        self.assertEqual(fila.desenfileirar(), 30)
 
    def test_ordem_fifo_com_frente(self):
        fila = FilaEncadeada()
        fila.enfileirar(1)
        fila.enfileirar(2)
        fila.enfileirar(3)
 
        # frente() não deve remover o elemento.
        self.assertEqual(fila.frente(), 1)
        self.assertEqual(fila.frente(), 1)
 
        self.assertEqual(fila.desenfileirar(), 1)
        self.assertEqual(fila.frente(), 2)
 
 
class TestFilaEncadeadaIntercalacao(unittest.TestCase):
    """Verifica a intercalação de enfileirar e desenfileirar, inclusive após a
    pilha de saída já ter sido preenchida (para exercitar o caminho em que
    desenfileirar() não precisa repassar a pilha de entrada)."""
 
    def test_intercalacao_operacoes(self):
        fila = FilaEncadeada()
        fila.enfileirar(10)
        fila.enfileirar(30)
        self.assertEqual(fila.desenfileirar(), 10)  # força o repasse entrada -> saída
 
        fila.enfileirar(20)
        self.assertEqual(len(fila), 2)
 
        self.assertEqual(fila.desenfileirar(), 30)  # consome direto da pilha de saída
        self.assertEqual(fila.desenfileirar(), 20)  # repassa de novo, pois saída esvaziou
        self.assertTrue(fila.esta_vazia())
 
    def test_intercalacao_com_frente(self):
        fila = FilaEncadeada()
        fila.enfileirar("a")
        self.assertEqual(fila.frente(), "a")  # repassa entrada -> saída
 
        fila.enfileirar("b")
        self.assertEqual(fila.frente(), "a")  # "a" continua na frente
        self.assertEqual(fila.desenfileirar(), "a")
        self.assertEqual(fila.frente(), "b")
 
 
class TestFilaEncadeadaEsvaziarEReutilizar(unittest.TestCase):
    """Verifica esvaziar a fila e voltar a usar a mesma instância."""
 
    def test_esvaziar_e_reutilizar(self):
        fila = FilaEncadeada()
        fila.enfileirar(10)
        fila.enfileirar(30)
        fila.enfileirar(20)
 
        self.assertEqual(fila.desenfileirar(), 10)
        self.assertEqual(fila.desenfileirar(), 30)
        self.assertEqual(fila.desenfileirar(), 20)
        self.assertTrue(fila.esta_vazia())
 
        # Reutiliza a mesma instância após esvaziar.
        fila.enfileirar("10")
        self.assertEqual(len(fila), 1)
        self.assertEqual(fila.frente(), "10")
 
 
class TestFilaEncadeadaVazia(unittest.TestCase):
    """Verifica o comportamento de desenfileirar() e frente() quando a fila está vazia."""
 
    def test_desenfileirar_fila_vazia_levanta_excecao(self):
        fila = FilaEncadeada()
        with self.assertRaises(IndexError):
            fila.desenfileirar()
 
    def test_frente_fila_vazia_levanta_excecao(self):
        fila = FilaEncadeada()
        with self.assertRaises(IndexError):
            fila.frente()
 
    def test_esta_vazia_no_inicio(self):
        fila = FilaEncadeada()
        self.assertTrue(fila.esta_vazia())
 
 
class TestFilaEncadeadaLen(unittest.TestCase):
    """Verifica a coerência de len() após inserções e remoções."""
 
    def test_len_apos_insercoes_e_remocoes(self):
        fila = FilaEncadeada()
        self.assertEqual(len(fila), 0)
 
        fila.enfileirar(10)
        self.assertEqual(len(fila), 1)
 
        fila.enfileirar(30)
        self.assertEqual(len(fila), 2)
 
        fila.enfileirar(20)
        self.assertEqual(len(fila), 3)
 
        fila.desenfileirar()
        self.assertEqual(len(fila), 2)
 
    def test_len_com_varias_insercoes(self):
        fila = FilaEncadeada()
        for i in range(5):
            fila.enfileirar(i)
        self.assertEqual(len(fila), 5)
 
        fila.desenfileirar()
        fila.desenfileirar()
        self.assertEqual(len(fila), 3)
 
 
if __name__ == "__main__":
    unittest.main()