import unittest
from P06_3531_fila_encadeada import FilaEncadeada
from P06_3531_pilha_encadeada import PilhaEncadeada


class TestPilhaEncadeada(unittest.TestCase):

    def setUp(self):
        """Garante uma pilha limpa antes de cada teste."""
        self.pilha = PilhaEncadeada()

    def test_inicializacao_e_esta_vazia(self):
        """Testa o estado inicial e o comportamento do método esta_vazia()."""
        self.assertIsNone(self.pilha.cabeca)
        self.assertEqual(len(self.pilha), 0)
        self.assertTrue(self.pilha.esta_vazia())

        self.pilha.push(10)
        self.assertFalse(self.pilha.esta_vazia())

        self.pilha.pop()
        self.assertTrue(self.pilha.esta_vazia())

    def test_ordem_lifo_e_coerencia_len(self):
        """Testa a ordem LIFO e a coerência do len após inserções e remoções seguidas."""
        elementos = [10, 20, 30, 40]
        
        
        for i, val in enumerate(elementos, start=1):
            self.pilha.push(val)
            self.assertEqual(len(self.pilha), i)
            self.assertEqual(self.pilha.topo(), val)

      
        for i, val in enumerate(reversed(elementos), start=1):
            self.assertEqual(self.pilha.pop(), val)
            self.assertEqual(len(self.pilha), len(elementos) - i)

    def test_erros_pilha_vazia(self):
        """Garante que pop e topo em pilha vazia levantam IndexError."""
        with self.assertRaises(IndexError) as ctx_pop:
            self.pilha.pop()
        self.assertEqual(str(ctx_pop.exception), "A pilha está vazia.")

        with self.assertRaises(IndexError) as ctx_topo:
            self.pilha.topo()
        self.assertEqual(str(ctx_topo.exception), "A pilha está vazia.")

    def test_alternancia_operacoes(self):
        """Testa a alternância contínua entre empilhar, consultar topo e desempilhar."""
        self.pilha.push("A")
        self.assertEqual(self.pilha.topo(), "A")
        
        self.pilha.push("B")
        self.assertEqual(self.pilha.pop(), "B")
        self.assertEqual(len(self.pilha), 1)

        self.pilha.push("C")
        self.assertEqual(self.pilha.topo(), "C")
        self.assertEqual(len(self.pilha), 2)

        self.assertEqual(self.pilha.pop(), "C")
        self.assertEqual(self.pilha.pop(), "A")
        self.assertEqual(len(self.pilha), 0)

    def test_tipos_diferentes_repetidos_e_none(self):
        """Testa o armazenamento de tipos mistos, valores duplicados e None."""
        itens = [10, "texto", 10, None, 3.14, None]

        for item in itens:
            self.pilha.push(item)

        self.assertEqual(len(self.pilha), len(itens))


        for item_esperado in reversed(itens):
            self.assertEqual(self.pilha.pop(), item_esperado)

    def test_repr(self):
        """Testa a representação em string para pilha vazia e com elementos."""
        self.assertEqual(repr(self.pilha), "PilhaEncadeada(Pilha Vazia)")

        self.pilha.push(10)
        self.pilha.push(20)
        self.assertEqual(repr(self.pilha), "PilhaEncadeada(20 -> 10)")

class TestFilaEncadeada(unittest.TestCase):

    def setUp(self):
        """Garante uma fila limpa antes de cada teste."""
        self.fila = FilaEncadeada()

    def test_ordem_fifo_e_coerencia_len(self):
        """Testa a ordem FIFO (First-In, First-Out) e a variação do len."""
        elementos = [10, 20, 30, 40]

        
        for i, val in enumerate(elementos, start=1):
            self.fila.enfileirar(val)
            self.assertEqual(len(self.fila), i)

        self.assertEqual(self.fila.frente(), 10)

     
        for i, val_esperado in enumerate(elementos, start=1):
            self.assertEqual(self.fila.desenfileirar(), val_esperado)
            self.assertEqual(len(self.fila), len(elementos) - i)

    def test_intercalacao_enfileirar_e_desenfileirar(self):
        """Testa a alternância contínua entre enfileirar e desenfileirar."""
        self.fila.enfileirar("A")
        self.fila.enfileirar("B")
        self.assertEqual(self.fila.desenfileirar(), "A")  
        self.assertEqual(len(self.fila), 1)

        self.fila.enfileirar("C")
        self.fila.enfileirar("D")
        self.assertEqual(len(self.fila), 3)

        self.assertEqual(self.fila.frente(), "B")
        self.assertEqual(self.fila.desenfileirar(), "B") 
        self.assertEqual(self.fila.desenfileirar(), "C")  
        self.assertEqual(len(self.fila), 1)

        self.assertEqual(self.fila.desenfileirar(), "D")
        self.assertEqual(len(self.fila), 0)

    def test_esvaziar_e_reutilizar_instancia(self):
        """Testa esvaziar completamente a fila e voltar a usá-la na mesma instância."""
   
        self.fila.enfileirar(1)
        self.fila.enfileirar(2)
        self.assertEqual(self.fila.desenfileirar(), 1)
        self.assertEqual(self.fila.desenfileirar(), 2)

     
        self.assertEqual(len(self.fila), 0)
        self.assertTrue(self.fila.esta_vazia())

     
        self.fila.enfileirar(100)
        self.fila.enfileirar(200)
        self.assertFalse(self.fila.esta_vazia())
        self.assertEqual(len(self.fila), 2)
        self.assertEqual(self.fila.frente(), 100)

        self.assertEqual(self.fila.desenfileirar(), 100)
        self.assertEqual(self.fila.desenfileirar(), 200)
        self.assertEqual(len(self.fila), 0)

    def test_erros_fila_vazia(self):
        """Garante que desenfileirar e frente em fila vazia levantam IndexError."""
        with self.assertRaises(IndexError) as ctx_desenfileirar:
            self.fila.desenfileirar()
        self.assertEqual(str(ctx_desenfileirar.exception), "A fila está vazia.")

        with self.assertRaises(IndexError) as ctx_frente:
            self.fila.frente()
        self.assertEqual(str(ctx_frente.exception), "A fila está vazia.")


    def test_repr(self):
        """Testa a representação em string para fila vazia e com elementos, garantindo ausência de efeitos colaterais."""
       
        self.assertEqual(repr(self.fila), "FilaEncadeada(Fila Vazia)")

     
        self.fila.enfileirar(10)
        self.fila.enfileirar(20)
        self.assertEqual(repr(self.fila), "FilaEncadeada(10 -> 20)")

    
        self.assertEqual(self.fila.frente(), 10)  
        self.fila.enfileirar(30)                  
        self.assertEqual(repr(self.fila), "FilaEncadeada(10 -> 20 -> 30)")

 
        self.assertEqual(len(self.fila), 3)
        self.assertEqual(self.fila.desenfileirar(), 10)
        self.assertEqual(self.fila.desenfileirar(), 20)
        self.assertEqual(self.fila.desenfileirar(), 30)
        self.assertEqual(len(self.fila), 0)



if __name__ == "__main__":
    unittest.main()


    
