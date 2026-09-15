import unittest
# Certifique-se de que o arquivo original está na mesma pasta ou importe corretamente
from P06_3458_fila_encadeada import PilhaEncadeada, FilaEncadeada


class TestPilhaEncadeada(unittest.TestCase):
    """Bateria de testes unitários para a classe PilhaEncadeada."""

    def setUp(self):
        self.pilha = PilhaEncadeada()

    def test_ordem_lifo(self):
        """Verifica se os elementos são desempilhados na ordem LIFO (último a entrar, primeiro a sair)."""
        elementos = [10, 20, 30, 40]
        for elem in elementos:
            self.pilha.push(elem)

        removidos = []
        while not self.pilha.esta_vazia():
            removidos.append(self.pilha.pop())

        self.assertEqual(removidos, [40, 30, 20, 10])

    def test_pilha_vazia_excecoes(self):
        """Garante que pop() e topo() em pilha vazia levantam IndexError."""
        self.assertTrue(self.pilha.esta_vazia())
        with self.assertRaises(IndexError):
            self.pilha.pop()

        with self.assertRaises(IndexError):
            self.pilha.topo()

    def test_coerencia_len(self):
        """Verifica a coerência do tamanho (len) após várias inserções e remoções."""
        self.assertEqual(len(self.pilha), 0)
        self.pilha.push("A")
        self.assertEqual(len(self.pilha), 1)
        self.pilha.push("B")
        self.assertEqual(len(self.pilha), 2)
        self.pilha.pop()
        self.assertEqual(len(self.pilha), 1)
        self.pilha.pop()
        self.assertEqual(len(self.pilha), 0)

    def test_alternancia_operacoes(self):
        """Testa o comportamento alternando push, topo e pop."""
        self.pilha.push(1)
        self.assertEqual(self.pilha.topo(), 1)
        self.pilha.push(2)
        self.assertEqual(self.pilha.pop(), 2)
        self.pilha.push(3)
        self.assertEqual(self.pilha.topo(), 3)
        self.assertEqual(self.pilha.pop(), 3)
        self.assertEqual(self.pilha.pop(), 1)
        self.assertTrue(self.pilha.esta_vazia())

    def test_tipos_diferentes_e_none(self):
        """Verifica o suporte a tipos de dados variados, incluindo None e duplicados."""
        itens = [42, "texto", None, [1, 2], None, 42]
        for item in itens:
            self.pilha.push(item)

        desempilhados = []
        while not self.pilha.esta_vazia():
            desempilhados.append(self.pilha.pop())

        self.assertEqual(desempilhados, list(reversed(itens)))

    def test_repr(self):
        """Testa a representação em string da pilha."""
        self.pilha.push(1)
        self.pilha.push(2)
        self.assertEqual(repr(self.pilha), "[2, 1]")


class TestFilaEncadeada(unittest.TestCase):
    """Bateria de testes unitários para a classe FilaEncadeada."""

    def setUp(self):
        self.fila = FilaEncadeada()

    def test_ordem_fifo(self):
        """Verifica se a fila respeita rigorosamente a ordem FIFO (primeiro a entrar, primeiro a sair)."""
        elementos = ["primeiro", "segundo", "terceiro"]
        for elem in elementos:
            self.fila.enfileirar(elem)

        removidos = []
        while not self.fila.esta_vazia():
            removidos.append(self.fila.desenfileirar())

        self.assertEqual(removidos, elementos)

    def test_intercalacao(self):
        """Testa intercalação entre enfileirar, desenfileirar e consultar a frente."""
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.assertEqual(self.fila.desenfileirar(), 1)
        self.fila.enfileirar(3)
        self.assertEqual(self.fila.frente(), 2)
        self.assertEqual(self.fila.desenfileirar(), 2)
        self.assertEqual(self.fila.desenfileirar(), 3)
        self.assertTrue(self.fila.esta_vazia())

    def test_esvaziar_e_reutilizar(self):
        """Verifica se a fila pode ser totalmente esvaziada e depois reutilizada sem problemas."""
        for i in range(5):
            self.fila.enfileirar(i)
        for i in range(5):
            self.assertEqual(self.fila.desenfileirar(), i)

        self.assertTrue(self.fila.esta_vazia())
        self.assertEqual(len(self.fila), 0)

        # Reutilização
        self.fila.enfileirar("novo")
        self.assertEqual(self.fila.frente(), "novo")
        self.assertEqual(self.fila.desenfileirar(), "novo")

    def test_fila_vazia_excecoes(self):
        """Garante que desenfileirar() e frente() em fila vazia levantam IndexError."""
        self.assertTrue(self.fila.esta_vazia())
        with self.assertRaises(IndexError):
            self.fila.desenfileirar()

        with self.assertRaises(IndexError):
            self.fila.frente()

    def test_coerencia_len(self):
        """Verifica a coerência do tamanho da fila ao longo das inserções e remoções."""
        self.assertEqual(len(self.fila), 0)
        for i in range(10):
            self.fila.enfileirar(i)
            self.assertEqual(len(self.fila), i + 1)
        for i in range(10):
            self.assertEqual(len(self.fila), 10 - i)
            self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 0)

    def test_repr(self):
        """Testa a representação textual legível da fila."""
        self.fila.enfileirar(10)
        self.fila.enfileirar(20)
        self.assertEqual(repr(self.fila), "[10, 20]")
        self.assertEqual(self.fila.desenfileirar(), 10)
        self.assertEqual(repr(self.fila), "[20]")


if __name__ == "__main__":
    unittest.main()