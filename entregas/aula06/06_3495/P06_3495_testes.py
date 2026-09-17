import unittest as u
from P06_3495_pilha_encadeada import PilhaEncadeada as P
from P06_3495_fila_encadeada import FilaEncadeada as F

class TestePilha(u.TestCase):

    def teste_push(self):
        pilha = P()
        pilha.push("a")
        pilha.push("b")
        pilha.push("c")
        pilha.push("d")
        self.assertEqual(str(pilha), "d\nc\nb\na")

    def teste_pop(self):
        pilha = P()
        pilha.push("a")
        pilha.push("b")
        pilha.push("c")
        pilha.push("d")
        pilha.pop()
        self.assertEqual(str(pilha), "c\nb\na")

    def teste_pop_em_pilha_vazia(self):
        pilha_vazia = P()
        with self.assertRaises(IndexError):
            pilha_vazia.pop()    

    def teste_topo_em_pilha_vazia(self):
        pilha_vazia = P()
        with self.assertRaises(IndexError):
            pilha_vazia.topo()

    def teste_len(self):
        pilha = P()
        pilha.push("a")
        pilha.push("b")
        pilha.push("c")
        pilha.push("d")
        self.assertEqual(len(pilha), 4)
    def teste_len_apos_remocao(self):
        pilha = P()
        pilha.push("a")
        pilha.push("b")
        pilha.push("c")
        pilha.pop()
        pilha.push("d")
        pilha.pop()
        self.assertEqual(len(pilha), 2)

    def teste_alternancia_operacao(self):
        pilha = P()
        pilha.push("a")
        pilha.push("b")
        pilha.push("c")
        pilha.pop()
        pilha.push("d")
        pilha.pop()
        pilha.push("g")
        pilha.push("h")
        pilha.pop()
        x = len(pilha)
        y = pilha.esta_vazia()
        z = str(pilha)
        pilha.push("i")
        pilha.push("j")
        pilha.pop()
        self.assertEqual(str(pilha), "i\ng\nb\na")

    def teste_arm_tipos_diferentes(self):
        pilha = P()
        pilha.push("a")
        pilha.push("a")
        pilha.push(4)
        pilha.push(4)
        pilha.push(None)
        pilha.push(7.5)
        pilha.push(True)
        self.assertEqual(str(pilha), "True\n7.5\nNone\n4\n4\na\na")

class TesteFila(u.TestCase):

    def teste_enfileirar(self):
        fila = F()
        fila.enfileirar("a")
        fila.enfileirar("b")
        fila.enfileirar("c")
        fila.enfileirar("d")
        self.assertEqual(str(fila), "a\nb\nc\nd")

    def teste_desenfileirar(self):
        fila = F()
        fila.enfileirar("a")
        fila.enfileirar("b")
        fila.enfileirar("c")
        fila.enfileirar("d")
        fila.desenfileirar()
        self.assertEqual(str(fila), "b\nc\nd")

    def teste_intercalacao(self):
        fila = F()
        fila.enfileirar("a")
        fila.enfileirar("b")
        fila.desenfileirar()
        fila.enfileirar("c")
        fila.enfileirar("d")
        fila.enfileirar("e")
        fila.desenfileirar()
        fila.enfileirar("f")
        fila.desenfileirar()
        self.assertEqual(str(fila), "d\ne\nf")

    def teste_esvaziar_e_voltar_a_usar(self):
        fila = F()
        fila.enfileirar("a")
        fila.enfileirar("b")
        fila.enfileirar("c")
        fila.enfileirar("d")
        fila.desenfileirar()
        fila.desenfileirar()
        fila.desenfileirar()
        fila.desenfileirar()
        fila.enfileirar("e")
        fila.enfileirar("f")
        fila.enfileirar("g")
        self.assertEqual(str(fila), "e\nf\ng")

    def teste_desenfileirar_em_fila_vazia(self):
        fila_vazia = F()
        with self.assertRaises(IndexError):
            fila_vazia.desenfileirar()  

    def teste_frente_em_fila_vazia(self):
        fila_vazia = F()
        with self.assertRaises(IndexError):
            fila_vazia.frente()

    def teste_len(self):
        fila = F()
        fila.enfileirar("a")
        fila.enfileirar("b")
        fila.enfileirar("c")
        fila.enfileirar("d")
        self.assertEqual(len(fila), 4)

    def teste_len_apos_remocao(self):
        fila = F()
        fila.enfileirar("a")
        fila.enfileirar("b")
        fila.enfileirar("c")
        fila.desenfileirar()
        fila.enfileirar("d")
        fila.desenfileirar()
        fila.enfileirar("e")
        self.assertEqual(len(fila), 3)

if __name__ == '__main__':
    u.main()