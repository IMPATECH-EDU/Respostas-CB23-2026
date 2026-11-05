"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime, timedelta

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.medicao import medir
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro


def registros_pressao(contagens):
    """Cria registros de pressão com a estrutura esperada por `medir`."""
    instante = datetime(2026, 1, 1)
    return [
        Registro(instante + timedelta(seconds=i), "INFO", "pressao",
                 {"contagens": contagem})
        for i, contagem in enumerate(contagens)
    ]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestAcumuladorKahan(unittest.TestCase):
    """Testes de regressão da issue #7."""
    
    def test_soma_1000x1e_6(self): # não deixam usar "-" no nome de função, então usei "_"
        """Soma 1000 parcelas de 1e-6 com AcumuladorKahan e compara com o resultado exato."""
        acumulador = AcumuladorKahan()
        for _ in range(1000):
            acumulador.adicionar(1e-6)
        self.assertAlmostEqual(acumulador.total, 1e-3, places=10)

    def test_soma_um_milhao_de_decimos(self):
        """Soma um milhão de parcelas de 0,1 e verifica a compensação do erro."""
        acumulador = AcumuladorKahan()
        for _ in range(1_000_000):
            acumulador.adicionar(0.1)
        self.assertAlmostEqual(acumulador.total, 100_000.0, places=9)

    def test_soma_dez_mil_de_decimos(self):
        """Soma dez mil parcelas de 0,1 e detecta erro de arredondamento acumulado."""
        acumulador = AcumuladorKahan()
        for _ in range(10_000):
            acumulador.adicionar(0.1)
        self.assertAlmostEqual(acumulador.total, 1_000.0, places=12)

class TestMedida(unittest.TestCase):
    """Testes de medição e tratamento de dados inválidos da issue #6."""

    def test_u_sistematica_negativa(self):
        """Rejeita incerteza sistemática negativa com registros e curva válidos."""
        registros = registros_pressao([1000, 2000, 3000])
        curva = CurvaCalibracao([1000, 2000, 3000], [10, 20, 30], metodo="linear")
        with self.assertRaises(ValueError):
            medir(registros, "pressao", curva, u_sistematica=-1.0)

    def test_menos_de_duas_validas(self):
        """Levanta ValueError quando o filtro robusto deixa apenas uma leitura válida."""
        registros = registros_pressao([1000, 2000, 3000])
        curva = CurvaCalibracao([1000, 2000, 3000], [10, 20, 30], metodo="linear")
        with self.assertRaises(ValueError):
            medir(registros, "pressao", curva, u_sistematica=1.0, limiar=0.1)

    def test_mad_zero(self):
        """Levanta ValueError quando todas as leituras são iguais e a MAD é zero."""
        registros = registros_pressao([2000, 2000, 2000])
        curva = CurvaCalibracao([1000, 2000, 3000], [10, 20, 30], metodo="linear")
        with self.assertRaises(ValueError):
            medir(registros, "pressao", curva)

    def test_contagem_fora_do_dominio_da_curva(self):
        """Propaga ValueError quando uma contagem está fora do domínio de calibração."""
        registros = registros_pressao([1000, 2000, 4000])
        curva = CurvaCalibracao([1000, 2000, 3000], [10, 20, 30], metodo="linear")
        with self.assertRaises(ValueError):
            medir(registros, "pressao", curva)

class TestComportamentoDerivada(unittest.TestCase):
    """Testando o comportamento da derivada para h pequeno"""

    def test_derivada_h_pequeno(self):
        """Verifica se 1000 + 1e-14 == 1000"""
        self.assertEqual(1000 + 1e-14, 1000)

if __name__ == "__main__":
    unittest.main()
