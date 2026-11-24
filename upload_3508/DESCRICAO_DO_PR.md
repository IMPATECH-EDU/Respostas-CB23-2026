## Marco 1
Resolve as issues #1 a #5 do enunciado.

### O que mudou
- `elevatoria/dados.py`: `LINHA` com `re.VERBOSE` e grupos nomeados; `valida_tag` com `fullmatch`; `ler_log` delega cada linha a `_interpretar_linha`, que levanta `ValueError` com o motivo, e a linha descartada vai para `invalidas` sem alteração; `contagem_por_tag` com compreensão de dicionário sobre compreensão de conjunto; `serie` recusa chaves com valores textuais.
- `criar_conversores` (#2): cada lambda nasce em `_multiplicador(fator)`, num escopo próprio, sem *late binding*.
- `medir_memoria`, as quatro conversões e `medir_tempos` (#3). `converter_vetorizado` passa para `float64` antes da conta.
- `SerieTemporal.media_movel` (#4): faltava o termo 0 antes da soma acumulada, e a primeira janela era pulada (570 valores em vez de 571).
- `SerieTemporal.reamostrar` (#5): `reshape` sobre a fatia `len // k * k`; a sobra do fim é descartada.
- `marco1.py` com a matrícula 3508 e todas as impressões; nenhum `assert` foi alterado.

### Como testei
- `python -m unittest discover -v`: 108 testes, todos passando (50 de aceitação e 58 meus; 22 deles em `testes/test_dados.py`)
- `python marco1.py`: todos os assert passam
- Testes de regressão da #4 (`TestRegressaoMediaMovel`, 4 testes) commitados antes da correção. Rodados contra o `media_movel` original, os 4 falham.

### Pontos de atenção para o revisor
- `converter_vetorizado`: sem a conversão para `float64`, um `ndarray` em `uint16` estouraria em `c * 600` (há um teste para isso).
- `medir_memoria` também recusa contagens fora de 0 a 4095 (o `array('H')` não aceitaria negativos). Isso foi acrescentado à docstring.
- A correção da #4 usa `np.concatenate` só no termo subtraído, para o resultado continuar `SerieTemporal` (o `concatenate` sozinho devolveria `ndarray`).

## Marco 2
Resolve as issues #6 e #7 do enunciado.

### O que mudou
- `elevatoria/medicao.py` (#6): `medir` encadeia `serie` (Marco 1), a `CurvaCalibracao`, o z robusto com a MAD (`_separar_espurias`), `scipy.stats.sem` e `Medida`; `altura_manometrica` faz toda a conta com `Medida`, inclusive a incerteza de ρ.
- `elevatoria/acumuladores.py` (#7): a correção de Kahan passa a ser `(t - soma) - y`. A forma antiga, `t - (soma + y)`, recalculava a mesma soma arredondada e dava sempre 0.

### Como testei
- `python -m unittest discover -v`: 108 testes, todos passando (12 em `testes/test_medicao.py`)
- `python marco1.py` e `python marco2.py`: todos os assert passam
- Testes de regressão da #7 (`TestRegressaoKahan`, 4 testes) commitados antes da correção. Rodados contra o código original, os 4 falham.

### Pontos de atenção para o revisor
- O `ValueError` da curva (contagem fora do domínio) não é capturado em `medir`: sobe para quem chamou, como diz o contrato (há um teste para isso).
- Os índices de `espurias` são posições na série da tag, e não no log inteiro (há um teste com outras tags e um alarme intercalados).

## Marco 3
Resolve as issues #8 e #9 do enunciado.

### O que mudou
- `elevatoria/operacao.py` (#8): `ponto_operacao` confere o intervalo e o domínio da bomba, resolve `bomba(Q) - altura_sistema(Q) = 0` e recusa um resultado que não convergiu; `ordem_convergencia` usa os três últimos erros acima do piso.
- `elevatoria/raizes.py` (#9): o Newton recalcula a derivada a cada iteração. Com a derivada fixa no ponto inicial, ele virava o método da corda, com convergência linear (10 iterações em Re = 1e4; agora são 5, com ordem 2,00).

### Como testei
- `python -m unittest discover -v`: 108 testes, todos passando (12 em `testes/test_operacao.py`)
- `python marco3.py`: todos os assert passam
- Testes de regressão da #9 (`TestRegressaoNewton`, 3 testes) commitados antes da correção. Rodados contra o código original, os 3 falham.

### Pontos de atenção para o revisor
- `ponto_operacao` também recusa uma raiz fora de `[a, b]`: o Newton não fica preso ao intervalo e, em `[10, 40]`, escapava para Q ≈ 65 L/s. Isso foi acrescentado à docstring.
- `ordem_convergencia` levanta `ValueError` (e não `ZeroDivisionError`) quando dois erros seguidos são iguais.

## Marco 4
Resolve as issues #10 e #11 do enunciado.

### O que mudou
- `elevatoria/dia.py` (#10): `ajustar_polinomio` pela fatoração QR da matriz de Vandermonde (`np.linalg.qr` e `scipy.linalg.solve_triangular`); `dia_de_operacao` calcula a potência em cada instante e integra o volume, a energia e o custo faixa por faixa, só com os pontos de cada faixa.
- `elevatoria/integracao.py` (#11): `Trapezio.integrar_tabela` usa a largura de cada intervalo (`np.diff(x)`). Antes, supunha passo constante de 15 min, e o volume do dia com falhas saía 8,8% abaixo; agora o erro é de 0,05%.

### Como testei
- `python -m unittest discover -v`: 108 testes, todos passando (12 em `testes/test_dia.py`)
- `python marco4.py`: todos os assert passam
- Testes de regressão da #11 (`TestRegressaoTrapezioTabela`, 3 testes) commitados antes da correção. Rodados contra o código original, os 3 falham.

### Pontos de atenção para o revisor
- Método de mínimos quadrados: escolhi a QR porque ela não forma `VᵀV` (as equações normais), que eleva ao quadrado o número de condição da Vandermonde. O resultado bate com `np.polyfit` (teste de aceitação). Ela também detecta `x` distintos insuficientes pela diagonal de `R` e levanta `ValueError`.
- O custo de cada faixa é integrado só com os instantes `início ≤ t ≤ fim`, para a regra não atravessar o salto da tarifa (Etapa 1(b): de uma vez, a ordem cai para cerca de 1).
