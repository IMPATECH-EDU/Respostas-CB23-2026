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
| `s + s` | SerieTemporal| SerieTemporal|
| `s[1:]` | SerieTemporal|SerieTemporal |
| `s * 2` | SerieTemporal| SerieTemporal|
| `s.sum()` | SerieTemporal de dimensão 0|SerieTemporal |
| `s[0]` |numpy.float64 | float64|

<!-- Explique o resultado que mais surpreendeu você. -->
O resultado que mais me surpreendeu foi `s.sum()`. Mesmo resumindo toda a série a um único valor, a soma preservou o tipo `SerieTemporal` em um array de dimensão zero. Já `s[0]` retornou um escalar `float64` ao acessar um único elemento.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
Para 600 pontos e uma janela de 30, media_movel devolvia 570 médias em vez de 571. Os testes test_inclui_a_primeira_janela e test_janela_do_tamanho_da_serie reproduziram o problema. A soma acumulada começava no primeiro valor da série, então as diferenças entre as fatias pulavam a primeira janela. Acrescentei um zero no início da soma acumulada, e os dois testes passaram.


## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3515

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->
Ao reduzir h de 1 até 10⁻⁵, o erro diminuiu de 1,658 × 10⁻⁵ para 6,224 × 10⁻¹⁰, pois diminui o erro de truncamento da diferença adiante. Para passos menores, passam a dominar os erros de arredondamento e a perda de precisão ao subtrair valores próximos. Com h = 10⁻¹⁴, o ponto flutuante representa 1000 + h como 1000. Assim, o numerador da diferença adiante vira zero, a derivada calculada é zero e o erro absoluto coincide com a derivada exata, aproximadamente 0,213432888873.

### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->
Os testes `test_soma_um_milhao_de_decimos` e `test_recupera_duas_parcelas_pequenas` reproduziram o defeito. Como `t` já era o resultado arredondado de `s + y`, calcular `t - (s + y)` sempre dava zero. A correção `(t - s) - y` recupera o erro de arredondamento porque muda a ordem das operações. O teste de aceitação somava apenas dez parcelas de 0,1 e usava `math.isclose`, cuja tolerância aceitava o pequeno erro dessa soma.

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->
Para PT102, as curvas linear e spline tiveram desvios próximos, de 0,540 e 0,541 kPa, indicando precisão semelhante. Porém, os viéses foram −1,823 e 0,006 kPa, respectivamente, mostrando maior exatidão da spline em relação à pressão de referência de 380 kPa. A média de quase 600 leituras reduz a incerteza aleatória da média, mas o erro sistemático da curva linear permanece.

## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->

A bissecção levou 44 iterações porque usa sempre o intervalo [2, 15] e tolerância 10⁻¹²: após 44 divisões, a largura 13/2⁴⁴ fica abaixo da tolerância. O Newton levou 5, 4 e 3 iterações, com ordens estimadas de 2,00, 1,98 e 2,00. Ordem 2 significa que, perto da raiz, o próximo erro é aproximadamente proporcional ao quadrado do atual. Por exemplo, para Re = 10⁴, os erros passaram de 5,0 × 10⁻² para 2,3 × 10⁻⁵ e depois 5,0 × 10⁻¹². Para f(x) = x³ − 1 em [−2, 2], Newton começa em zero e falha por derivada nula, enquanto a bissecção converge.


### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->

Os testes `test_converge_com_derivada_fornecida_em_seis_iteracoes` e `test_converge_com_derivada_numerica_em_seis_iteracoes` reproduziram a lentidão. A derivada era calculada apenas no ponto inicial, fazendo o método usar uma inclinação fixa e ter convergência geralmente linear. Mover esse cálculo para dentro do laço atualiza a derivada a cada aproximação e recupera a convergência quadrática perto de raízes simples. Os testes de aceitação passavam porque o método ainda encontrava a raiz, sem detectar a perda de velocidade.

## Marco 4

### R13 — Integração e descontinuidade

<!-- Na Etapa 1(b), integrando o custo do dia de uma vez, a ordem observada cai para cerca
de 1, no trapézio e no Simpson; integrando cada faixa separadamente, voltam as ordens 2 e 4.
Por quê? -->

### R14 — Issue #11

<!-- Os nomes dos seus testes de regressão; a causa do defeito; por que os testes de
aceitação não o pegaram; por que a regra de Simpson não serve para o registro do dia. -->
Os testes test_constante_em_malha_irregular e test_reta_em_malha_irregular reproduziram o defeito. O trapézio usava o primeiro espaçamento para todos os intervalos, mesmo quando faltavam leituras. Corrigi o cálculo para usar cada largura obtida com np.diff(x). Os testes de aceitação não detectaram o problema porque usavam malhas uniformes. A implementação de Simpson exige espaçamento uniforme, condição que o registro do dia com falhas não atende.