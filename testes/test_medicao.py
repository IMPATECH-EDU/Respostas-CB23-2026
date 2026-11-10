"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest
from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestAcumuladorKahan(unittest.TestCase):
    """Verifica se AcumuladorKahan compensa ou não a precisão."""
    def test_original(self) -> None:
        """Testa se o problema original da compensação de AcumuladorKahan foi ou não resolvido, e se é melhor que o ingênuo."""
        acc_k = AcumuladorKahan()
        acc_n = AcumuladorIngenuo()
        tot = 10**6
        for _ in range(tot):
            acc_k.adicionar(0.1)
            acc_n.adicionar(0.1)
        self.assertAlmostEqual(acc_k.total, 10**5) # padrão de 7 casas decimais
        self.assertLess(acc_k.total, acc_n.total)
        
    def test_alta_precisao(self) -> None:
        """Testa se AcumuladorKahan consegue ou não lidar com adicionar valores ínfimos repetidamente. Utiliza fsum como oráculo."""
        acc_k = AcumuladorKahan()
        acc_k.adicionar(1)
        tot = 10**6
        e = 1e-16
        for _ in range(tot):
            acc_k.adicionar(e)
        self.assertAlmostEqual(acc_k.total, math.fsum([1.0] + [e] * tot), 12)


if __name__ == "__main__":
    unittest.main()
