import unittest
import importlib

modulo_pilha = importlib.import_module("06_3538_pilha_encadeada")
PilhaEncadeada = modulo_pilha.PilhaEncadeada

modulo_fila = importlib.import_module("06_3538_fila_encadeada")
FilaEncadeada = modulo_fila.FilaEncadeada

class TestesPilhaEncadeada(unittest.TestCase):
    
    def test_ordem_lifo_push_pop(self):
        pilha = PilhaEncadeada()
        pilha.push(10)
        pilha.push(20)
        pilha.push(30)
        
        # O último a entrar (30) deve ser o primeiro a sair
        self.assertEqual(pilha.pop(), 30)
        self.assertEqual(pilha.pop(), 20)
        self.assertEqual(pilha.pop(), 10)

    def test_erro_pilha_vazia(self):
        pilha = PilhaEncadeada()
        # 2. Agora, dizemos ao Python qual erro estamos esperando que aconteça
        with self.assertRaises(IndexError):
            pilha.pop()

        with self.assertRaises(IndexError):
            pilha.topo()

    def test_coerencia_tamanho(self):
        pilha = PilhaEncadeada()
        self.assertEqual(len(pilha), 0)
        pilha.push(30)
        pilha.push(20)
        self.assertEqual(len(pilha), 2)
        pilha.pop()
        self.assertEqual(len(pilha), 1)

    def test_tipos_diferentes_e_alternancia(self):
        pilha = PilhaEncadeada()
        
        # Adicionando tipos variados
        pilha.push(100)
        pilha.push("Python")
        pilha.push(None)
        
        # Testando se o topo (último a entrar) sai correto
        self.assertEqual(pilha.pop(), None)
        
        # Alternando: coloco mais um e já tiro
        pilha.push(999)
        self.assertEqual(pilha.pop(), 999)
        
        # Tirando o resto para ver se a ordem LIFO se manteve intacta
        self.assertEqual(pilha.pop(), "Python")
        self.assertEqual(pilha.pop(), 100)

    def test_valores_repetidos(self):
        pilha = PilhaEncadeada()
        # Inserindo valores idênticos
        pilha.push(7)
        pilha.push(7)
        pilha.push(7)
        
        self.assertEqual(len(pilha), 3)
        self.assertEqual(pilha.pop(), 7)
        self.assertEqual(pilha.pop(), 7)
        self.assertEqual(pilha.pop(), 7)
        self.assertTrue(pilha.esta_vazia())


class TestesFilaEncadeada(unittest.TestCase):
    
    def test_ordem_fifo(self):
        fila = FilaEncadeada()
        fila.enfileirar(10)
        fila.enfileirar(20)
        fila.enfileirar(30)

        self.assertEqual(fila.desenfileirar(), 10)
        self.assertEqual(fila.desenfileirar(), 20)
        self.assertEqual(fila.desenfileirar(), 30)

    def test_erro_fila_vazia(self):
        fila = FilaEncadeada()
        # 2. Agora, dizemos ao Python qual erro estamos esperando que aconteça
        with self.assertRaises(IndexError):
            fila.desenfileirar()

        with self.assertRaises(IndexError):
            fila.frente()

    def test_alternancia_e_tamanho(self):
        fila = FilaEncadeada()
        
        self.assertEqual(len(fila), 0)
        
        fila.enfileirar("A")
        fila.enfileirar("B")
        self.assertEqual(len(fila), 2)
        
        self.assertEqual(fila.desenfileirar(), "A")
        self.assertEqual(len(fila), 1)
        
        fila.enfileirar("C")
        self.assertEqual(len(fila), 2)
        
        self.assertEqual(fila.desenfileirar(), "B")
        self.assertEqual(fila.desenfileirar(), "C")
        self.assertEqual(len(fila), 0)

        # Continuação do teste: Esvaziar e voltar a usar a mesma instância
        fila.enfileirar("D")
        self.assertEqual(len(fila), 1)
        self.assertEqual(fila.desenfileirar(), "D")

    def test_frente_nao_remove_elemento(self):
        fila = FilaEncadeada()
        fila.enfileirar("Primeiro")
        fila.enfileirar("Segundo")
        
        # O método frente deve retornar "Primeiro"
        self.assertEqual(fila.frente(), "Primeiro")
        
        # O tamanho deve continuar sendo 2 (pois frente() não remove)
        self.assertEqual(len(fila), 2)
        
        # Ao desenfileirar, o valor deve continuar sendo "Primeiro"
        self.assertEqual(fila.desenfileirar(), "Primeiro")


if __name__ == "__main__":
    unittest.main()