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

import os
import sys
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if raiz not in sys.path:
    sys.path.append(raiz)

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
      """Mede a grandeza registrada pela `tag` no log.

      Passos:

      1. obtém as contagens da `tag` (chave `"contagens"`) com `serie`, do Marco 1;
      2. converte as contagens com a `curva`;
      3. descarta as leituras espúrias pelo z robusto: `z = (x - mediana) / MAD`, com a MAD
      calculada por `scipy.stats.median_abs_deviation(x, scale="normal")`; uma leitura é
      espúria se `|z| > limiar`. Os índices em `espurias` são posições na série da tag
      (a primeira leitura da tag tem índice 0);
      4. com as leituras válidas, calcula a média, o desvio padrão amostral (`ddof=1`) e o erro
      padrão da média (`scipy.stats.sem`);
      5. devolve uma `Medicao` cuja `medida` é `Medida(média, u)`, com
      `u = sqrt(erro_padrao² + u_sistematica²)`.

      `u_sistematica` é a incerteza do instrumento, que não diminui com o número de leituras.

      Levanta `ValueError` se `u_sistematica < 0`, se a tag tiver menos de 2 leituras, se a MAD
      for zero ou se sobrarem menos de 2 leituras válidas. Um `ValueError` da curva (contagem
      fora do domínio) não é tratado: ele chega a quem chamou `medir`.
      """

      # Levantamos ValueError se u_sistematica for menor que 0
      if u_sistematica<0:
         raise ValueError(f"valor inválido para u_sistematica: {u_sistematica}")

      nuem=serie(registros, tag, "contagens")  # SerieTemporal com o valor de chave dos registros da `tag` que têm essa chave
      
      if nuem.size<2:       # Verifico se a tag teve menos de 2 leituras
          raise ValueError(f"Tag possui menos de 2 leituras")
      
      conts=curva(nuem)                                        # Valores calibrados por meio de curva
      medana=np.median(conts)                                  # Cáculo da mediana dos valores
      mad= stats.median_abs_deviation(conts, scale="normal")   # Cálculo da MAD dos valores já calibrados
      
      # Verificação se o MAD é nulo
      if mad == 0:
          raise ValueError(f"valor de MAD é nulo.")
      
      # np.ndarray com os valores de espurias
      zsco=(conts-medana)/mad

      # Indicies dos espurias que são maiors que o limiar, usamos operações vetorizadas para realizar essa comparação
      lisa=np.where(np.abs(zsco)>limiar)[0].tolist() 

      # Calculamos a quantidade de valores válidos e vemos se restam no mínimo 2 medições
      n_validas=nuem.size - len(lisa)
      if n_validas<2:
         raise ValueError(f"Restaram menos de 2 valores: {n_validas}")

      # Vamos usar a ideia de Mascara Booleana do NumPy
      mascara = np.ones(conts.size, dtype=bool)
      mascara[lisa] = False
      validos = conts[mascara]

      # Agora calculamos os dados apenas com os valores válidos
      media=validos.mean()
      desvio=np.std(validos, ddof=1)
      erro=stats.sem(validos)
      u = np.sqrt(erro**2 + u_sistematica**2)
      medid_fin = Medida(media, u)
      
      # Retornamos a medição como sendo da clase Medicao
      return Medicao(tag, medid_fin, desvio, n_validas, lisa)

      raise NotImplementedError("issue #6: medir")


def altura_manometrica(registros: list[Registro], curva: CurvaCalibracao,
                       u_sistematica: float = 1.5) -> Medida:
    """Altura manométrica da bomba, em metros, com a sua incerteza.

    `H = (P_PT102 - P_PT101) * 1000 / (MASSA_ESPECIFICA * GRAVIDADE)`, em que `P_PT101` e
    `P_PT102` são as `medida`s de `medir` para as duas tags, em kPa (o fator 1000 converte
    para Pa), ambas com a incerteza sistemática `u_sistematica`. Todas as contas são feitas
    com `Medida`, que propaga as incertezas.
    """

    # Através da função definida medir() realizamos a medida da pressão para PT101 e para PT102
    m_1=medir(registros, "PT101", curva, u_sistematica)
    m_2=medir(registros, "PT102", curva, u_sistematica)

    # Realizamos o cálculo mediante a fórmula dada na dcstring da função
    return ((m_2.medida-m_1.medida)*1000)/(MASSA_ESPECIFICA*GRAVIDADE)

    raise NotImplementedError("issue #6: altura_manometrica")