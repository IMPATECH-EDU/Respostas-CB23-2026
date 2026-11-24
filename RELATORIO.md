# Relatório — <seu nome> (<sua matrícula>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->
which python: /home/zanata/Respostas-CB23-2026/.prog2/bin/python
etapa 0: Python 3.14.6 | NumPy 2.5.4 | fornecido 4.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
A string `"PT101 extra"` (ou `"PT101 "`) é aceita por `re.match(r"[A-Z]{1,2}\d{1,3}", s)` porque `match` verifica apenas o início da string e ignora caracteres excedentes, enquanto `re.fullmatch` exige que a string inteira case com o padrão e a rejeita. Se `valida_tag` usasse `match`, tags corrompidas com sufixos inválidos (como `"PT1010"` ou `"PT101 "`) seriam aceitas como válidas, permitindo a entrada de identificadores malformados no sistema.


### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
`ler_log` devolve as linhas descartadas para permitir auditoria, diagnóstico de falhas de comunicação e contagem de perda de dados sem mascarar problemas de telemetria. Se o sistema descartasse linhas em silêncio, uma falha intermitente na RTU ou um sensor enviando leituras corrompidas continuamente passaria despercebido, fazendo o operador acreditar que a estação está estável quando na verdade há perda severa de visibilidade operacional.


### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Na compreensão `{tag: (lambda c: c * k) for tag, k in escalas.items()}`, todas as lambdas capturam por referência a mesma variável de escopo `k`, que ao final do laço vale `0.1` (fator de `FT201`), fazendo `errados["PT102"](4095)` retornar `4095 * 0.1 = 409.5`. Em `criar_conversores`, o valor de `escalas[tag]` é fixado como argumento padrão (`lambda x, fator=escalas[tag]: x * fator`), ligando cada função ao seu próprio fator no momento da criação.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
A escala nominal assume resposta linear (`p = c * 600 / 4095`), gerando cerca de `262 kPa` para `PT102`, enquanto a pressão real de recalque é `380 kPa`. Isso ocorre porque a curva física do transmissor de pressão é não linear (senoidal), conforme definido na função `p_real(c) = 600.0 * np.sin(0.5 * np.pi * c / 4095.0)` em `fornecido/simulador.py` e interpolada pela `CurvaCalibracao` em `elevatoria/calibracao.py`.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18,0× (`3,6e7 / 2e6`) | 18,00× (`35.999.176 / 2.000.000` B) |
| Tempo do laço / tempo vetorizado | ~30× | <!-- cole a razão medida na sua máquina (ex.: ~45×) --> |
| Tempo da compreensão / tempo do laço | ~0,7× | <!-- cole a razão medida na sua máquina (ex.: ~0,75×) --> |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->


A maior diferença ocorre na aceleração do código vetorizado frente ao laço Python, pois o NumPy executa a aritmética em C sobre buffers contíguos sem overhead de bytecode ou boxing de objetos `float`. Em `uint16`, `4095 * 20 = 81900` excede `65535` (`2^16 - 1`), causando overflow modular: `81900 mod 65536 = 16364`. Para contagens de 12 bits (0 a 4095), `uint16` é ideal pela economia de memória; para pressões em kPa, `float64` (ou `float32`) evita truncamento e overflow.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float64` | `float64` |
| `s[0]` | `float64` | `float64` |

<!-- Explique o resultado que mais surpreendeu você. -->
O comportamento que mais me surpreendeu é que operações aritméticas (`s + s`, `s * 2`) e fatiamentos (`s[1:]`) preservam automaticamente a subclasse `SerieTemporal` graças à herança de `numpy.ndarray`, enquanto reduções (`s.sum()`) e indexação escalar (`s[0]`) retornam o escalar NumPy `float64` em vez de um objeto `SerieTemporal` de dimensão zero.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

O sintoma era `s.media_movel(30)` devolver `570` pontos em vez de `571` para uma série de `600` leituras (`test_media_movel_tamanho_600_janela_30` e `test_media_movel_valores_e_janela_1`). A causa era subtrair `acumulada[janela-1:] - acumulada[:-janela+1]` sem prefixar `0.0` na soma acumulada, omitindo a primeira janela (`self[0:janela]`) e quebrando `janela=1`. Corrigiu-se prefixando `0.0` em `np.cumsum` e fazendo `(acumulada[janela:] - acumulada[:-janela]) / janela`. Os testes de aceitação só checavam `isinstance(..., SerieTemporal)` e `ValueError`, sem verificar o comprimento nem os valores da média móvel.

## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->
Python 3.14.6 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3530

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->
De h = 1 até h = 1e-5, o erro cai linearmente com h (1.658e-05 para 6.224e-10) porque domina o erro de truncamento da série de Taylor, que é $O(h)$. Para h < 1e-5, o erro volta a crescer porque domina o erro de arredondamento por cancelamento catastrófico ao subtrair f(x + h) - f(x) muito próximos e dividir por um h minúsculo. Em h = 1e-14, 1000.0 + 1e-14 == 1000.0 na precisão IEEE 754 (float64), então o numerador zera e o erro |0 - f'(1000)| = 0.2134 iguala exatamente a própria derivada.

### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->
Testes de regressão: test_kahan_um_milhao_de_decimos e test_kahan_parcelas_pequenas_apos_grande. Em ponto flutuante, t = s + y já descarta os bits baixos de y no arredondamento; recalcular s + y em t - (s + y) repete o mesmo t e sempre zera, enquanto (t - s) - y isola a parcela realmente somada antes de subtrair y. Os testes de aceitação somavam só 10 parcelas de 0.1, insuficientes para o erro superar math.isclose.

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->

Em PT102 (referência 380.00 kPa), linear e spline têm quase o mesmo desvio (0.531 vs 0.532 kPa), ou seja, a mesma precisão (dispersão). Já a exatidão difere muito: a linear tem viés de -1.824 kPa (378.18 ± 1.50 kPa), enquanto a spline tem +0.006 kPa (380.01 ± 1.50 kPa). A média de ~600 leituras reduz apenas o ruído aleatório (s/sqrt{n}), mas não corrige o erro sistemático da curva linear.

## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->

A bissecção corta [2, 15] ao meio até largura < 1e-12, exigindo sempre teto(log_2(13/ 10^{-12})) = 44 passos, independentemente de Re. Ordem 2 no Newton significa |e_{k+1}|se aproxima de  C(|e_k|)², dobrando os dígitos corretos por passo (2.9e+00 -> 5.0e-02 -> 2.3e-05 -> 5.0e-12). O Newton falha se f'(x_k) = 0 ou divergir de um chute ruim, enquanto a bissecção sempre converge quando f(a)f(b) < 0$.

### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->
Testes de regressão: test_newton_converge_em_poucas_iteracoes_colebrook e test_newton_ordem_quadratica_em_funcao_nao_linear. Avaliar f'(x_0) uma única vez transforma Newton no método da corda fixa (x_{k+1} = x_k - f(x_k)/f'(x_0)), cujo fator assintótico 1 - f'(x^*)/f'(x_0) != 0 reduz a convergência para linear (ordem 1). Os testes de aceitação só conferiam a raiz final, sem checar iterações ou ordem.

## Marco 4

### R13 — Integração e descontinuidade

<!-- Na Etapa 1(b), integrando o custo do dia de uma vez, a ordem observada cai para cerca
de 1, no trapézio e no Simpson; integrando cada faixa separadamente, voltam as ordens 2 e 4.
Por quê? -->
As ordens 2 (trapézio) e 4 (Simpson) exigem integrando suave (C² e C⁴). Como a tarifa salta de 0,50 para 1,50 R$/kWh às 18 h e volta a 0,50 às 21 h, a descontinuidade de salto faz o erro ser dominado pelo subintervalo que cruza a quebra (O(h), ordem ~1.00 e ~0.65). Integrando cada faixa separadamente, o integrando é contínuo em cada trecho e recupera as ordens 2.00 e 4.00.

### R14 — Issue #11

<!-- Os nomes dos seus testes de regressão; a causa do defeito; por que os testes de
aceitação não o pegaram; por que a regra de Simpson não serve para o registro do dia. -->
Testes de regressão: test_trapezio_tabela_malha_nao_uniforme_constante e test_trapezio_tabela_malha_nao_uniforme_linear. O defeito em Trapezio.integrar_tabela usava passo fixo x[1] - x[0] (15 min) em vez de np.diff(x), subestimando o volume quando faltam leituras (3562,4 vs 3876,4 m³). Os testes de aceitação só usavam malha uniforme. Simpson exige malha igualmente espaçada e número ímpar de pontos, recusando o registro real.