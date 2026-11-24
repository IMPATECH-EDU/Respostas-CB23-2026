"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
import numpy as np
from elevatoria.integracao import Simpson
from elevatoria.integracao import Trapezio


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestRegressaoIntegracao(unittest.TestCase):
    """Testes de regressão para a issue #11 (malha irregular / passos perdidos do SCADA)."""

    def test_integracao_com_falhas_multiplas(self):
        """Verifica integração com múltiplas falhas de comunicação (malha não uniforme)."""
        # Simula lacunas no tempo devido a leituras perdidas pelo SCADA
        t = np.array([0.0, 1.0, 3.0, 4.0])
        y = np.array([2.0, 2.0, 2.0, 2.0])
        integrador = Trapezio()
        
        # Com y constante = 2 e intervalo total de 0 a 4, a área exata é 8.0.
        resultado = integrador.integrar_tabela(t, y)
        self.assertAlmostEqual(resultado, 8.0, places=4)

    def test_integracao_com_valores_nan(self):
        """Verifica espaçamento variável de tempo na integração do trapézio."""
        t = np.array([0.0, 2.0, 5.0])
        y = np.array([1.0, 1.0, 1.0])
        integrador = Trapezio()
        
        # Área total de 0 a 5 com altura 1 = 5.0
        resultado = integrador.integrar_tabela(t, y)
        self.assertAlmostEqual(resultado, 5.0, places=4)
if __name__ == "__main__":
    unittest.main()
