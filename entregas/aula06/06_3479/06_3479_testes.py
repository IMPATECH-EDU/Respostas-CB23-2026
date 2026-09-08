import unittest
import importlib

_pilha_mod = importlib.import_module("06_3479_pilha_encadeada")
PilhaEncadeada = _pilha_mod.PilhaEncadeada 
_fila_mod = importlib.import_module("06_3479_fila_encadeada")
FilaEncadeada = _fila_mod.FilaEncadeada
# from pilhaenc import PilhaEncadeada
# from filaenc import FilaEncadeada

class TestandoPilha(unittest.TestCase):
    def testelifo_push_pop_len_topo(self):
        '''Testa o LIFO da pilha com os métodos básicos que foram implementados.'''
        p = PilhaEncadeada()
        p.push(10)
        p.push(20)
        self.assertEqual(len(p), 2)
        self.assertEqual(p.topo(), 20)
        self.assertEqual(p.pop(), 20)
        self.assertEqual(p.pop(), 10)
        self.assertTrue(p.esta_vazia())

    def testando_qnd_ta_vazia(self):
        '''Verifica se há o levantamento de IndexError quando a pilha está vazia.'''
        p = PilhaEncadeada()
        with self.assertRaises(IndexError):
            p.pop()
        with self.assertRaises(IndexError):
            p.topo()

    def testando_coerencia_len(self): 
        '''Verifica se o método len funciona após push e pop alternados.'''
        p = PilhaEncadeada()
        self.assertEqual(len(p), 0) 
        p.push(1) 
        self.assertEqual(len(p), 1) 
        p.pop() 
        self.assertEqual(len(p), 0)
        p.push(2) 
        self.assertEqual(len(p), 1)

    def testando_None_e_type(self):
        '''Verifica se a pilha aceita valores de diferentes tipos, incluindo None.'''
        p = PilhaEncadeada()
        p.push("Texto")
        p.push(None)
        p.push(9.98)
        self.assertEqual(p.pop(), 9.98)
        self.assertIsNone(p.pop()) 

    def testede_alternancia_e_valores_repetidos(self):
        '''Verifica se a pilha funciona corretamente com alternância de push e pop, incluindo valores repetidos.'''
        p = PilhaEncadeada()
        p.push(10)
        p.push(10) 
        self.assertEqual(p.pop(), 10)
        p.push(20) 
        self.assertEqual(p.pop(), 20)
        self.assertEqual(p.pop(), 10)
# um extra p verificar se o método próprio de repr está funcionando corretamente. 

    def testando_repr(self):
        '''Verifica se o método próprio de repr está funcionando corretamente.'''
        p = PilhaEncadeada()
        p.push("mas estou testando")
        p.push("Não sei se dá certo")
        self.assertEqual(repr(p), "PilhaEncadeada(['Não sei se dá certo', 'mas estou testando'])")

class TestFilaEncadeada(unittest.TestCase):
    def testando_enfileirar_e_desenfileirar(self):
        '''Testa o FIFO da fila com os métodos básicos que foram implementados.'''
        f = FilaEncadeada() 
        f.enfileirar(20) 
        f.enfileirar(26) 
        self.assertEqual(len(f), 2)
        self.assertEqual(f.frente(), 20) 
        self.assertEqual(f.desenfileirar(), 20) 
        self.assertEqual(f.desenfileirar(),26) 
        self.assertTrue(f.esta_vazia())

    def testando_qnd_ta_vazia(self):
        '''Verifica se há o levantamento de IndexError quando a fila está vazia.'''
        f = FilaEncadeada()
        with self.assertRaises(IndexError):
            f.desenfileirar()
        with self.assertRaises(IndexError):
            f.frente()

    def test_esvazia_e_volta(self):
        '''Verifica se a fila funciona após esvaziar e adicionar elementos.''' 
        f = FilaEncadeada() 
        f.enfileirar(1) 
        f.enfileirar(2) 
        self.assertEqual(f.desenfileirar(),1) 
        self.assertEqual(f.desenfileirar(), 2)
        self.assertTrue(f.esta_vazia()) 
        f.enfileirar(3) 
        self.assertEqual(f.desenfileirar(), 3)

    def testando_coerencia_len_fila(self): 
        '''Verifica se o método len funciona após enfileirar e desenfileirar alternados.'''
        f = FilaEncadeada()
        self.assertEqual(len(f), 0) 
        f.enfileirar(1) 
        self.assertEqual(len(f), 1) 
        f.enfileirar(2) 
        self.assertEqual(len(f), 2)
        f.desenfileirar() 
        self.assertEqual(len(f), 1)
        f.desenfileirar() 
        self.assertEqual(len(f), 0)
# teste extra para verfificar se o método próprio de repr da fila está funcionando corretamente. 
    def testando_repr_fila(self):
        '''Verifica se o método próprio de repr está funcionando corretamente.'''
        fila = FilaEncadeada() 
        fila.enfileirar("testando") 
        fila.enfileirar("código") 
        self.assertEqual(repr(fila), "FilaEncadeada(['testando', 'código'])")

if __name__ == "__main__":
    unittest.main()