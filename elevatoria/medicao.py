"""Medição de pressão a partir do log: calibração, estatística e incerteza (issue #6).

Este módulo junta peças que já existem na base:

- `serie` (de `elevatoria/dados.py`, o seu Marco 1): as contagens de uma tag no log;
- `CurvaCalibracao` (de `elevatoria/calibracao.py`, escrita por um colega): contagens -> kPa;
- `scipy.stats`: mediana, MAD e erro padrão;
- `Medida` (de `fornecido/medida.py`, da equipe de metrologia): valor ± incerteza.

As funções marcadas com `NotImplementedError` são a issue #6; as docstrings descrevem o
contrato. Não mude nomes nem assinaturas públicas: o `marco2.py` e os testes dependem deles.
Funções auxiliares privadas (`_nome`) são permitidas.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro, serie
from fornecido.medida import Medida

#: Massa específica da água (kg/m³), com a sua incerteza.
MASSA_ESPECIFICA = Medida(998.0, 1.0)

#: Aceleração da gravidade (m/s²), considerada exata.
GRAVIDADE = 9.81


@dataclass(frozen=True)
class Medicao:
    """Resultado da medição de uma grandeza a partir do log."""

    tag: str
    medida: Medida        # média das leituras válidas, com a incerteza total
    desvio: float         # desvio padrão amostral (ddof=1) das leituras válidas: a precisão
    n_validas: int        # número de leituras válidas (sem as espúrias)
    espurias: list[int]   # índices das leituras descartadas, em ordem crescente


def medir(registros: list[Registro], tag: str, curva: CurvaCalibracao,
          u_sistematica: float = 0.0, limiar: float = 6.0) -> Medicao:
      """
        Converte as leituras da tag e filtra valores espúrios usando Z-score robusto (MAD).

        Parâmetros:
            registros: Lista de registros do log.
            tag: Identificador do sensor.
            curva: Função de calibração (contagens para grandeza física).
            u_sistematica: Incerteza do instrumento (não diminui com mais leituras).
            limiar: Limite do Z-score para corte de espúrias.

        Retorna um objeto Medicao com a média, incerteza propagada, desvio e filtro.
        Levanta ValueError se os dados forem insuficientes ou inválidos.
        """
      if u_sistematica < 0.0:
          raise ValueError(f"u_sistematica deve ser não negativa; recebi {u_sistematica!r}")
      
      contagens = serie(registros, tag, chave="contagens")

      if len(contagens) < 2:
          raise ValueError(f"Menos de 2 leituras para a tag {tag!r}: {len(contagens)}")

      pressoes_kpa = curva(contagens)


      mad = stats.median_abs_deviation(pressoes_kpa, scale="normal")

      if mad == 0.0:
          raise ValueError(f"MAD = 0 para a tag {tag!r}: {pressoes_kpa}")

      z = (pressoes_kpa - np.median(pressoes_kpa)) / mad

      espurias = list(np.where(np.abs(z) > limiar)[0])

      validas = np.delete(pressoes_kpa, espurias)

      if len(validas) < 2:
          raise ValueError(f"Menos de 2 leituras válidas para a tag {tag!r}: {len(validas)}")
      
      media = np.mean(validas)

      desvio = np.std(validas, ddof=1)

      erro_padrao = stats.sem(validas)

      incerteza_total = (erro_padrao ** 2 + u_sistematica ** 2) ** 0.5

      return Medicao(tag=tag, medida=Medida(media, incerteza_total), desvio=desvio, n_validas=len(validas),espurias=espurias)


    


def altura_manometrica(registros: list[Registro], curva: CurvaCalibracao,
                       u_sistematica: float = 1.5) -> Medida:
    
    """
    Calcula a diferença de pressão na bomba e propaga a incerteza estatística.
    
        Parâmetros:
            medicao_succao: Medição consolidada da entrada (sucção).
            medicao_recalque: Medição consolidada da saída (recalque).
    
        Retorna um objeto Medida contendo o ganho de pressão (recalque - sucção) 
            e a raiz da soma dos quadrados das incertezas individuais.
    """        


    pressao_PT101 = medir(registros, "PT101", curva, u_sistematica)

    pressao_PT102 = medir(registros, "PT102", curva, u_sistematica)

    return (pressao_PT102.medida - pressao_PT101.medida) * 1000 / (MASSA_ESPECIFICA * GRAVIDADE)



      
