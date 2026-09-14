import unittest
import importlib

pe = importlib.import_module("06_3484_pilha_encadeada")
fe = importlib.import_module("06_3484_fila_encadeada")


class TestPilha(unittest.TestCase):

    def setUp(self):
        """Executado antes de cada método de teste."""
        self.pilha = pe.PilhaEncadeada()

    def test_ordem_lifo(self):
        """Garante a ordem LIFO (Last In, First Out) na sequência de push e pop."""
        elementos = [10, 20, 30, 40]
        for elem in elementos:
            self.pilha.push(elem)

        # Deve desempilhar na ordem inversa da inserção
        for elem_esperado in reversed(elementos):
            self.assertEqual(self.pilha.pop(), elem_esperado)

    def test_operacoes_em_pilha_vazia(self):
        """Verifica se pop() e topo() lançam exceção (IndexError) em pilha vazia."""
        self.assertTrue(self.pilha.esta_vazia())

        with self.assertRaises(IndexError):
            self.pilha.pop()

        with self.assertRaises(IndexError):
            self.pilha.topo()

    def test_coerencia_len(self):
        """Testa se len() reflete com precisão o tamanho após inserções e remoções."""
        self.assertEqual(len(self.pilha), 0)

        # Adicionando elementos
        self.pilha.push("A")
        self.assertEqual(len(self.pilha), 1)

        self.pilha.push("B")
        self.assertEqual(len(self.pilha), 2)

        # Removendo elemento
        self.pilha.pop()
        self.assertEqual(len(self.pilha), 1)

        # Removendo até esvaziar
        self.pilha.pop()
        self.assertEqual(len(self.pilha), 0)

    def test_alternancia_operacoes(self):
        """Verifica o comportamento com chamadas intercaladas de push, pop e topo."""
        self.pilha.push(1)
        self.assertEqual(self.pilha.topo(), 1)

        self.pilha.push(2)
        self.assertEqual(self.pilha.topo(), 2)

        # Remove o 2, o topo volta a ser 1
        self.assertEqual(self.pilha.pop(), 2)
        self.assertEqual(self.pilha.topo(), 1)

        self.pilha.push(3)
        self.assertEqual(len(self.pilha), 2)
        self.assertEqual(self.pilha.pop(), 3)
        self.assertEqual(self.pilha.pop(), 1)

        self.assertTrue(self.pilha.esta_vazia())

    def test_tipos_diferentes_repetidos_e_none(self):
        """Garante que a pilha armazena tipos variados, elementos repetidos e None."""
        elementos = [
            42,
            "texto",
            42,  # Repetido
            None,  # Valor None
            [1, 2],  # Lista (mutável)
            None,  # None repetido
            {"chave": "valor"},
        ]

        for elem in elementos:
            self.pilha.push(elem)

        self.assertEqual(len(self.pilha), len(elementos))

        # Confirma que os itens saem exatamente na ordem inversa e mantêm o tipo/valor
        for elem_esperado in reversed(elementos):
            self.assertEqual(self.pilha.pop(), elem_esperado)


import unittest



class TestFila(unittest.TestCase):

    def setUp(self):
        """Executado antes de cada método de teste."""
        self.fila = fe.FilaEncadeada()

    def test_ordem_fifo(self):
        """Garante a ordem FIFO (First In, First Out): o primeiro que entra é o primeiro que sai."""
        elementos = ["primeiro", "segundo", "terceiro", "quarto"]
        for elem in elementos:
            self.fila.enfileirar(elem)

        # Deve desenfileirar exatamente na mesma ordem em que os itens foram inseridos
        for elem_esperado in elementos:
            self.assertEqual(self.fila.desenfileirar(), elem_esperado)

    def test_intercalacao_operacoes(self):
        """Verifica o comportamento com chamadas intercaladas de enfileirar, desenfileirar e frente."""
        self.fila.enfileirar(10)
        self.assertEqual(self.fila.frente(), 10)

        self.fila.enfileirar(20)
        self.assertEqual(self.fila.frente(), 10)  # O elemento da frente continua sendo 10

        # Remove o 10; agora a frente deve ser 20
        self.assertEqual(self.fila.desenfileirar(), 10)
        self.assertEqual(self.fila.frente(), 20)

        self.fila.enfileirar(30)
        self.assertEqual(len(self.fila), 2)
        
        self.assertEqual(self.fila.desenfileirar(), 20)
        self.assertEqual(self.fila.desenfileirar(), 30)

        self.assertTrue(self.fila.esta_vazia())

    def test_esvaziar_e_reutilizar_instancia(self):
        """Testa o esvaziamento completo e se a mesma instância volta a funcionar normalmente."""
        # 1ª Rodada: Insere e esvazia completamente
        self.fila.enfileirar("A")
        self.fila.enfileirar("B")
        self.assertEqual(self.fila.desenfileirar(), "A")
        self.assertEqual(self.fila.desenfileirar(), "B")
        self.assertTrue(self.fila.esta_vazia())

        # 2ª Rodada: Reutiliza a mesma instância
        self.fila.enfileirar("C")
        self.fila.enfileirar("D")
        self.assertEqual(len(self.fila), 2)
        self.assertEqual(self.fila.frente(), "C")
        self.assertEqual(self.fila.desenfileirar(), "C")
        self.assertEqual(self.fila.desenfileirar(), "D")
        self.assertTrue(self.fila.esta_vazia())

    def test_operacoes_em_fila_vazia(self):
        """Verifica se desenfileirar() e frente() lançam exceção (IndexError) em fila vazia."""
        self.assertTrue(self.fila.esta_vazia())

        with self.assertRaises(IndexError):
            self.fila.desenfileirar()

        with self.assertRaises(IndexError):
            self.fila.frente()

    def test_coerencia_len(self):
        """Testa se len() reflete com precisão o tamanho após inserções e remoções."""
        self.assertEqual(len(self.fila), 0)

        # Adicionando elementos
        self.fila.enfileirar(1)
        self.assertEqual(len(self.fila), 1)

        self.fila.enfileirar(2)
        self.assertEqual(len(self.fila), 2)

        # Removendo um elemento
        self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 1)

        # Removendo o último elemento até esvaziar
        self.fila.desenfileirar()
        self.assertEqual(len(self.fila), 0)


if __name__ == "__main__":
    unittest.main()