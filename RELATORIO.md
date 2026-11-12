# Relatório — Mariana Medeiros de Oliveira (3515)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

/home/al.mariana.medeiros/venvs/prog2-venv/bin/python

=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.4 | fornecido 4.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

Com PT101abc, re.match encontra PT101 no início da string. re.fullmatch exige que a string inteira siga o padrão e rejeita a entrada por causa do sufixo abc. Se valida_tag usasse match, aceitaria essa tag inválida.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

A função `ler_log` devolve as linhas inválidas para que seja possível conferir o que foi descartado e investigar por quê. Por exemplo, se uma falha de comunicação cortar várias linhas de leitura de pressão, descartá-las em silêncio faria parecer que não houve leituras naquele intervalo. Com as linhas originais em mãos, dá para ver que chegaram dados, mas que eles estavam incompletos.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Na versão errados, as lambdas consultam a mesma variável fator quando são chamadas. Nesse momento, ela já tem o último fator da compreensão, 0,1, que pertence a FT201. Por isso, errados["PT102"](4095) calcula 4095 × 0,1 = 409,5. Em criar_conversores, o argumento padrão fator=fator guarda o valor de cada tag no momento em que a lambda é criada.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
A escala nominal de 600 / 4095 kPa por contagem deu 262,0 kPa, enquanto o valor de conferência foi 380,0 kPa. A diferença vem da relação usada pelo simulador para gerar as contagens. Na linha 61 de fornecido/simulador.py, as leituras de PT102 são geradas com c_real(PRESSAO_RECALQUE), com ruído e arredondamento. Como c_real segue outra relação entre pressão e contagem, aplicar a escala nominal a essas leituras resulta em um valor diferente da pressão usada pelo simulador.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` |Cerca de 18×|18.00×|
| Tempo do laço / tempo vetorizado |Cerca de 10×|19.45×|
| Tempo da compreensão / tempo do laço |Cerca de 0,8×|0.91×|

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->
A maior diferença foi no tempo do laço em relação ao NumPy. Previ cerca de 10× e medi 19,45×. O NumPy opera sobre o array inteiro em código compilado, enquanto o laço executa a conversão elemento por elemento em Python. Em uint16, 4095 × 20 dá 16364 porque o resultado exato, 81900, excede 65535 e sobra 81900 − 65536. Eu usaria uint16 para as contagens de 0 a 4095 e float64 para as pressões em kPa, que podem ter casas decimais.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal| |
| `s[1:]` | SerieTemporal| |
| `s * 2` | SerieTemporal| |
| `s.sum()` | SerieTemporal de dimensão 0| |
| `s[0]` |numpy.float64 | |

<!-- Explique o resultado que mais surpreendeu você. -->

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
Para 600 pontos e uma janela de 30, media_movel devolvia 570 médias em vez de 571. Os testes test_inclui_a_primeira_janela e test_janela_do_tamanho_da_serie reproduziram o problema. A soma acumulada começava no primeiro valor da série, então as diferenças entre as fatias pulavam a primeira janela. Acrescentei um zero no início da soma acumulada, e os dois testes passaram.