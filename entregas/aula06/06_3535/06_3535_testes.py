import unittest
import importlib

pilha_module = importlib.import_module("06_3535_pilha_encadeada")
PilhaEncadeada = pilha_module.PilhaEncadeada
fila_modules = importlib.import_module("06_3535_fila_encadeada")
FilaEncadeada = fila_modules.FilaEncadeada

class TestPilhaEncadeada(unittest.TestCase):

    def setUp(self):
        """Garante que antes de cada teste, a pilha esteja vazia."""

        self.pilha = PilhaEncadeada()

    def test_ordem_lifo_sequencia_push_pop(self):
        """Verifica se o push e pop funcionam na ordem LIFO"""

        elementos = [10, 20, 30, 40, 50]
        for elem in elementos:
            self.pilha.push(elem)
        
        desempilhados = []
        while not self.pilha.esta_vazia():
            desempilhados.append(self.pilha.pop())

        self.assertEqual(desempilhados, [50, 40, 30, 20, 10])

    def test_pop_e_topo_em_pilha_vazia(self):
        """Garante que caso a pilha esteja vazia retorne True, 
        e que se for usado pop ou topo em Pilha vazia levanta erro"""

        self.assertTrue(self.pilha.esta_vazia())
        
        with self.assertRaises(IndexError):
            self.pilha.pop()

        with self.assertRaises(IndexError):
            self.pilha.topo()

    def test_coerencia_do_len(self):
        """Testa se o len funciona ao adicionar item por item e ao remover também"""

        self.assertEqual(len(self.pilha), 0)

        for i in range(1, 6):
            self.pilha.push(i)
            self.assertEqual(len(self.pilha), i)

        self.assertEqual(self.pilha.topo(), 5)

        for i in range(5, 0, -1):
            self.assertEqual(len(self.pilha), i)
            self.pilha.pop()

        self.assertEqual(len(self.pilha), 0)
        self.assertTrue(self.pilha.esta_vazia())

    def test_alternancia_de_operacoes(self):
        """Testa operações alternadas, incluindo push, pop, len e esta_vazia."""

        self.pilha.push(1)
        self.pilha.push(2)
        self.assertEqual(self.pilha.pop(), 2)
        
        self.pilha.push(3)
        self.assertEqual(self.pilha.topo(), 3)
        self.assertEqual(len(self.pilha), 2)

        self.assertEqual(self.pilha.pop(), 3)
        self.assertEqual(self.pilha.pop(), 1)
        self.assertTrue(self.pilha.esta_vazia())

    def test_tipos_diferentes_repetidos_e_none(self):
        """Testa diferentes tipos de itens, incluindo None, str, int, list."""

        itens = ["texto", 42, None, 3.14, True, None, "texto", [1, 2]]
        
        for item in itens:
            self.pilha.push(item)

        self.assertEqual(len(self.pilha), len(itens))

        desempilhados = []
        while not self.pilha.esta_vazia():
            desempilhados.append(self.pilha.pop())

        self.assertEqual(desempilhados, list(reversed(itens)))


class TestFilaEncadeada(unittest.TestCase):
    def setUp(self):
        """Garante que antes de cada teste, a Fila esteja vazia."""

        self.fila = FilaEncadeada()

    def test_ordem_fifo(self):
        """Verifica se o enfileirar e desenfileirar funcionam na ordem FIFO."""

        elementos = ["A", "B", "C", "D"]
        for elem in elementos:
            self.fila.enfileirar(elem)

        desenfileirados = []
        while not self.fila.esta_vazia():
            desenfileirados.append(self.fila.desenfileirar())

        self.assertEqual(desenfileirados, elementos)

    def test_intercalar_enfileirar_e_desenfileirar(self):
        """Testa enfileirar e desenfileirar de forma intercalada."""

        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.assertEqual(self.fila.desenfileirar(), 1)

        self.fila.enfileirar(3)
        self.assertEqual(self.fila.frente(), 2)

        self.assertEqual(self.fila.desenfileirar(), 2)
        self.assertEqual(self.fila.desenfileirar(), 3)
        self.assertTrue(self.fila.esta_vazia())

    def test_esvaziar_e_voltar_a_usar(self):
        """Testa esvaziar a fila completamente e voltar a usar a mesma instância."""

        self.fila.enfileirar("Ciclo 1 - Item 1")
        self.fila.enfileirar("Ciclo 1 - Item 2")
        self.assertEqual(self.fila.desenfileirar(), "Ciclo 1 - Item 1")
        self.assertEqual(self.fila.desenfileirar(), "Ciclo 1 - Item 2")
        self.assertTrue(self.fila.esta_vazia())

        self.fila.enfileirar("Ciclo 2 - Item 1")
        self.assertEqual(self.fila.frente(), "Ciclo 2 - Item 1")
        self.assertEqual(len(self.fila), 1)
        self.assertEqual(self.fila.desenfileirar(), "Ciclo 2 - Item 1")
        self.assertTrue(self.fila.esta_vazia())

    def test_desenfileirar_e_frente_em_fila_vazia(self):
        """Garante que esta_vazia retorna True em uma fila vazia,
        aleḿ de levantar erro ao usar desenfileirar e frente."""

        self.assertTrue(self.fila.esta_vazia())

        with self.assertRaises(IndexError):
            self.fila.desenfileirar()

        with self.assertRaises(IndexError):
            self.fila.frente()

    def test_coerencia_de_len(self):
        """Testa a coerência de len durante diferentes tipos de manipulações."""

        self.assertEqual(len(self.fila), 0)

        for i in range(1, 4):
            self.fila.enfileirar(i)
            self.assertEqual(len(self.fila), i)

        self.assertEqual(self.fila.frente(), 1)
        self.assertEqual(len(self.fila), 3)

        self.fila.enfileirar(4)
        self.assertEqual(len(self.fila), 4)

        resultados = []
        while not self.fila.esta_vazia():
            resultados.append(self.fila.desenfileirar())

        self.assertEqual(resultados, [1, 2, 3, 4])
        self.assertEqual(len(self.fila), 0)


if __name__ == "__main__":
    unittest.main()