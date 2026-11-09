"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from elevatoria.acumuladores import AcumuladorKahan
from elevatoria.acumuladores import AcumuladorIngenuo
from fornecido.testes_aceitacao.test_aceitacao_m2 import IDENTIDADE, registros
from elevatoria.medicao import medir

class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).

#Teste de regressão da issue #7: AcumuladorIngenuo não acumula corretamente grandes somas

class TestRegressaoIssue7(unittest.TestCase):
    """Testes de regressão para o defeito numérico (Issue #7)."""

    def test_um_milhao_de_decimos(self):
        """Soma 0,1 um milhão de vezes e exige o resultado exato de 100000.0."""
        acum = AcumuladorKahan()
        for _ in range(1_000_000):
            acum.adicionar(0.1)
        # Falha porque o código original acumula erro e devolve 100000.00000133288
        self.assertEqual(acum.total, 100000.0)

    def test_soma_absorvida(self):
        """Soma parcelas muito pequenas (1e-16) a um valor inicial (1.0)."""
        acum = AcumuladorKahan()
        acum.adicionar(1.0)
        for _ in range(100):
            acum.adicionar(1e-16)
        # O acumulador Kahan correto guarda as frações até formarem um valor que altere o 1.0
        # O código atual perde essas frações, ficando estagnado no 1.0
        self.assertGreater(acum.total, 1.0)

    # Teste para função medir() do módulo elevatoria.medicao.py

    def test_medir_u_sistematica_negativa(self):
        """Garante que levanta ValueError se u_sistematica for menor que zero."""
        regs = registros("PT101", [10, 11, 9, 10, 12])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE, u_sistematica=-1.5)

    def test_medir_mad_zero(self):
        """Garante que levanta ValueError se a MAD for zero (contagens idênticas)."""
        regs = registros("PT101", [10, 10, 10, 10, 10])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE)

if __name__ == "__main__":
    unittest.main()
