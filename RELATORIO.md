# Relatório — Arthur Vitorino Ferreira (3462)

## Marco 1

### Ambiente

Execução do aluno em 28/10/2026, no Ubuntu, com o ambiente conda `ambiente_aluno` e matrícula 3462:

```text
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.3 | fornecido 4.0
```

```text
$ which python
/opt/anaconda3/envs/ambiente_aluno/bin/python
```

### R1 — Expressões regulares

Em `PT101extra`, `re.match` encontra o prefixo `PT101`. Já `re.fullmatch` exige que a string termine logo após os dígitos. Com `match`, `valida_tag` aceitaria um identificador com caracteres extras.

### R2 — Linhas inválidas

Guardar a linha original permite investigar o que se perdeu. Se um transmissor passar a enviar datas impossíveis, por exemplo, o gráfico ficará com menos leituras. As linhas descartadas ajudam a distinguir uma falha no relógio do instrumento de uma interrupção da coleta. Nesta execução, foram 2.404 registros válidos e quatro linhas inválidas.

### R3 — Late binding

Na compreensão de lambdas, todas as funções consultam a mesma variável `k` quando são chamadas. Nesse momento o laço terminou e o último fator é 0,1. Por isso 4.095 contagens dão 409,5. Em `criar_conversores`, o parâmetro padrão `fator=fator` guarda o valor de cada iteração. A função de PT102 aplica 600/4095 e devolve 600 kPa.

### R4 — Escala nominal

A escala linear nominal dá 261,97 kPa para uma pressão de referência de 380,00 kPa. O desvio é compatível com um transmissor não linear. Em `fornecido/simulador.py`, `p_real(c)` calcula a pressão com uma senoide e `gerar_log` usa a inversa `c_real(p)` para gerar as contagens de PT102 com ruído. A conversão nominal coincide com a curva nas extremidades, mas subestima a pressão no interior da faixa.

### R5 — Previsão × medição

Nas três branches públicas do fork, as versões do relatório mantêm vazias as previsões de R5 e R6. Não foi localizado um commit de previsões anterior à medição. Sem esse registro, não é possível quantificar a diferença entre previsão e resultado.

| Grandeza | Previsão anterior | Medido no Ubuntu |
| --- | --- | ---: |
| Memória da lista / memória do uint16 | Sem registro anterior | 18,00 |
| Tempo do laço / tempo vetorizado | Sem registro anterior | 36,80 |
| Tempo da compreensão / tempo do laço | Sem registro anterior | 0,93 |

Tempos médios no Ubuntu para um milhão de contagens: laço 39,70 ms, compreensão 37,04 ms, map com lambda 50,55 ms e vetorizado 1,08 ms.

Para um milhão de contagens, a lista ocupa 36.000.056 bytes pelo critério do exercício e o vetor uint16 ocupa 2.000.000. A maior razão medida foi a de tempos: o NumPy executa a multiplicação sobre o vetor inteiro, evitando a iteração em Python. Em uint16, 4095 × 20 = 81900 dá resto 16364 módulo 65536. Para guardar contagens de 12 bits, uint16 basta. Para pressões em kPa, float64 preserva a parte fracionária.

### R6 — Tipos da SerieTemporal

| Expressão | Previsão anterior | Tipo observado na revisão (NumPy 2.3.5) |
| --- | --- | --- |
| `s + s` | Sem registro anterior | SerieTemporal |
| `s[1:]` | Sem registro anterior | SerieTemporal |
| `s * 2` | Sem registro anterior | SerieTemporal |
| `s.sum()` | Sem registro anterior | SerieTemporal |
| `s[0]` | Sem registro anterior | float64 |

A soma de todos os pontos tem um único valor, mas nesta execução o NumPy o devolve como um array de dimensão zero da subclasse SerieTemporal. A indexação s[0] extrai diretamente um escalar NumPy.

### R7 — Issue #4

Para 600 leituras e janela 30, o defeito produzia 570 médias em vez de 571. O teste `test_quantidade_de_janelas` verifica o mesmo erro com 1000 leituras e janela 40. A soma acumulada precisa começar com o total anterior ao primeiro ponto, zero, para que a primeira diferença inclua a primeira janela. Os testes fornecidos verificam tipo, janelas inválidas e preservação da entrada. O teste `test_media_movel_janela_igual_ao_tamanho` também confere a média da única janela possível. Os três testes de regressão falharam com o arquivo original do commit `99affab` e passaram com a versão revisada. No histórico público, o primeiro teste e a correção foram enviados juntos em `f03f224`.

## Marco 2

### Ambiente

Execução de verificação com a matrícula 3462:

```text
=== Etapa 0: ambiente ===
Python 3.12.14 | NumPy 2.3.5 | SciPy 1.17.0 | fornecido 4.0 | matrícula 3462
```

### R8 — Derivada numérica

A diferença adiante usa a inclinação de uma secante para aproximar a tangente. Para passos grandes, domina o erro de truncamento, de ordem h.
Ao reduzir h de 1 para 10⁻⁵, o erro caiu de 1,658 × 10⁻⁵ para 6,224 × 10⁻¹⁰.
Para passos menores, a subtração de pressões quase iguais perde algarismos significativos e a divisão por h amplifica o erro de arredondamento.
Em h = 10⁻¹⁴, o computador representa 1000 + h pelo próprio 1000. A diferença calculada é zero e o erro absoluto é 0,213432888873 kPa/contagem, o módulo da derivada da spline.

### R9 — Issue #7

Os testes `test_pulsos_de_um_decimo` e `test_duas_unidades_apos_dois_elevado_a_53` falharam com o acumulador original.
Como t já guardava a soma arredondada de s e y, recalcular s + y produzia o mesmo número e t − (s + y) zerava a compensação.
Em (t − s) − y, a primeira diferença mede o incremento efetivamente incorporado à soma. A segunda calcula o resíduo que corrige a próxima parcela.
O teste fornecido aceitava o resultado de dez parcelas de 0,1 com `math.isclose`. Essa tolerância admitia também o resultado ingênuo.
Com um milhão de pulsos, a soma ingênua deu 100000,00000133288 L e a compensada deu 100000,0 L.

### R10 — Precisão × exatidão

Após descartar cinco leituras espúrias de PT102, restaram 595. Os desvios amostrais foram 0,531 kPa com a curva linear e 0,532 kPa com a spline: as leituras têm dispersões semelhantes, portanto precisões semelhantes.
Em relação à referência de 380 kPa, os vieses foram −1,842 kPa e −0,012 kPa, respectivamente. A spline foi mais exata neste ponto.
A média de muitas leituras reduz o erro aleatório da média. Como a curva linear subestima a pressão nessa faixa de operação, o deslocamento sistemático persiste na média.
