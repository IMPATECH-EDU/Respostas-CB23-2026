import unittest
from P06_3547_fila_encadeada import FilaEncadeada
from P06_3547_pilha_encadeada import PilhaEncadeada

class TestPilhaEncadeada(unittest.TestCase):
    def test_push(self):
        pilha = PilhaEncadeada()

        pilha.push(1)
        pilha.push(2)
        pilha.push(3)

        self.assertEqual(len(pilha), 3)
        self.assertEqual(pilha.topo(),3)
    def test_pop(self):
        pilha = PilhaEncadeada()

        pilha.push(1)
        pilha.push(2)
        pilha.push(3)

        self.assertEqual(pilha.pop(), 3)
        self.assertEqual(pilha.pop(), 2)
        self.assertEqual(len(pilha),1)
    def test_pop(self):
        pilha = PilhaEncadeada()

        with self.assertRaises(IndexError):
            pilha.pop()

        with self.assertRaises(IndexError):
            pilha.topo()
    def test_pushandpop(self):
        pilha = PilhaEncadeada()

        pilha.push("a")
        pilha.push(2)
        pilha.push(5)

        self.assertEqual(len(pilha),3)
        self.assertEqual(pilha.pop(),5)
        self.assertEqual(len(pilha),2)
        self.assertEqual(pilha.pop(),2)
        self.assertEqual(pilha.pop(),"a")
class TestFilaEncadeada(unittest.TestCase):
    def test_enfileirardesenfileirar(self):
        fila = FilaEncadeada()

        fila.enfileirar(1)
        fila.enfileirar(2)
        fila.enfileirar(3)

        self.assertEqual(fila.desenfileirar(),1)
        self.assertEqual(len(fila), 2)
        self.assertEqual(fila.desenfileirar(),2)
    def test_esvaziar(self):
        fila = FilaEncadeada()

        fila.enfileirar(1)
        fila.desenfileirar()

        self.assertEqual(len(fila),0)
        fila.enfileirar(2)
        self.assertEqual(len(fila),1)
        self.assertEqual(fila.desenfileirar(),2)
    def test_filavazia(self):
        fila = FilaEncadeada()
        with self.assertRaises(IndexError):
            fila.desenfileirar()
        with self.assertRaises(IndexError):
            fila.frente()
if __name__ == '__main__':
    unittest.main()