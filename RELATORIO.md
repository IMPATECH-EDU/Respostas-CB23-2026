# Relatório — Lucas Rafael Barbosa (3503)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

/home/lucas/venvs/prog2-venv/bin/python

=== Etapa 0: ambiente ===
Python 3.12.3 | NumPy 1.26.4 | fornecido 3.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

"PT1010", pois, com o padrão [A-Z]{1,2}\d{1,3}, apenas a correspondência inicial é exigida pelo re.match, enquanto re.fullmatch exige que a string inteira case. Se vlaida_tag usasse match, ela diria que tags como "PT1011" passariam e os assert da 1(d) falhariam.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

Para quem chama ler_log possa contar, registrar e investigar, porque ignorar em silêncio apagaria a evidência. No log da hora vieram 4 linhas corrompidas (falhas de comunicação com a RTU e linhas truncadas). Se a RTU de uma bomba comçasse a falhar e as linhas fossem jogadas foram sem aviso, o operador só iria ver uma série com buracos, sem saber que a comunicação está caindo.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

Errados é um dicinário de lambdas que usam a váriavel k do laço de compreensão. A lambda não gaurda o valor de k, só a variável. Quando ela é chamada, o laço já terminou e k vale o último fator, 0,1 (do FT201). Então errados["PT102"](4095) = 4095 * 0,1 = 409.5. Na criar_conversoes, cada lambda é criado dentro de _conversor(fator), e cada chamada tem seu próprio fator, que não muda depois (cada tag usa o fator da sua entrada), o que não gera o problema. 

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

O transmissor não responder linearmente às contagens, e a escala nomial (600/4095) supõe uma reta. Indo para fornecido/simulador.py, p_real(c) = 600*sin(0,5*pi*c/4095) não é linear. Para c ~1800 (média das contagens normais de PT102) a reta dá ~ 260 kPa e a curva verdadeira dá ~ 380 kPa. A escala nomial só acerta nos extremos (o e 600) e subestima no meio da faixa. (Usei o simulador só para entender a diferença, não para calcular).

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 16ceca0

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 36,000,056/2,000,000 = 18 |
| Tempo do laço / tempo vetorizado | 30 | 67.06/1.08 = 62 |
| Tempo da compreensão / tempo do laço | 0,8 | 63.37/67.06 = 0,94  |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

A maior diferença foi o tempo laço/vetorizado: foi quase o dobro. O vetorizado foi mais rápido do que eu esperava. o laço roda no interpretador, elemento por elmento, criando um float a cada conta, mas o numpy faz o laço em memória contígua. (add: estava testando o código e passar uma lista no lugar do ndarray para o vetorizado fazia o tempo ser 33x maior!). 
O uint16 guarda de 0 a 65535 e 4095 * 20 = 81900 passa, mas o numpy não avisa e pega o módulo (65536), que é 16364. Com o int do python dá certo. Assim, para contagens o uint16, e para pressão o float64.


### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | Serie Temporal | SerieTemporal |
| `s * 2` | Serie Temporal | SerieTemporal|
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

<!-- Explique o resultado que mais surpreendeu você. -->

O que mais me surpreendeu foi o s.sum(). Esperava que o tipo fosse um número simples do python, e não uma SerieTemporal de zero dimensões (um ponto?). Operações e reduções do numpy usam a classe do array original para criar o resultado, e a subclasse se mantém. Para usar o total como um número comum faço float(s.sum()).

### R7 — Issue #4

Quando fazíamos media_movel(30) ao invés de 571 = 600 - 30 + 1 valores, obtíamos só 570. Isso acontecia porque a soma acumulada estava começando do índice 0, e não no valor 0, então acumulada[janela:] - acumulada[:-janela] perde a primeira janela. Então, foi
colocado um 0 no começo e retorno como SerieTemporal. Os testes estavam pegando porque estavam conferindo só tipos, erros, sem ver o tamanho dos intervalos. Um caso legal é
que a janela igual a 1 deve ser do tamanho da série, e é coberto pelo teste teste_janela_igual_ao_tamanho.

## Marco 2

### Ambiente

Saída inicial do Marco 2

=== Etapa 0: ambiente ===
Python 3.12.3 | NumPy 1.26.4 | SciPy 1.11.4 | fornecido 4.0 | matrícula3503

=== Etapa 1: calibração ===
(a) linear  erro máximo = 2.8752 kPa
(a) spline  erro máximo = 0.0247 kPa
(b) derivada exata em c = 1000: 0.213432888873 kPa/contagem
      k        h         erro
      0    1e+00    1.658e-05
      1    1e-01    1.657e-06
      2    1e-02    1.657e-07
      3    1e-03    1.654e-08
      4    1e-04    1.651e-09
      5    1e-05    6.224e-10
      6    1e-06    2.336e-08
      7    1e-07    6.191e-08
      8    1e-08    6.191e-08
      9    1e-09    1.415e-05
     10    1e-10    2.984e-04
     11    1e-11    2.572e-03
     12    1e-12    1.394e-02
     13    1e-13    3.550e-01
     14    1e-14    2.134e-01
    menor erro: h = 1e-5, erro = 6.224e-10

=== Etapa 2: totalizador de pulsos ===
(a) acumulador                           total    erro (L)  tempo (ms)
    AcumuladorIngenuo       100000.00000133288   1.333e-06          66
    AcumuladorKahan         100000.00000133288   1.333e-06         111
    AcumuladorInteiro                 100000.0   0.000e+00         146
Traceback (most recent call last):
  File "/home/lucas/PROG2_Marcos/Respostas-CB23-2026/marco2.py", line 129, in <module>
    main()
  File "/home/lucas/PROG2_Marcos/Respostas-CB23-2026/marco2.py", line 123, in main
    etapa2()
  File "/home/lucas/PROG2_Marcos/Respostas-CB23-2026/marco2.py", line 83, in etapa2
    assert erros["AcumuladorKahan"] <= erros["AcumuladorIngenuo"] / 1000, \
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: o AcumuladorKahan não está compensando o arredondamento(issue #7)


### R8 — Derivada numérica

Para h grande (1 até 1e-4) domina o erro de truncamento: a diferença adiante só aproxima a derivada e o erro cai junto com h (1,7e-5 em h=1; 1,7e-9 em h=1e-4).
O mínimo vai ficar em h = 1e-5 (6,2e-10). Abaixo disso vai domiinar o erro de arredondamento: f(x+h) - f(x) subtrai números quase iguais e perde dígitos,
e dividir por um h minúsculo vai amplificar o erro (cresce como 1/h: 2,3e-8 em h=1e-6 e 1,4e-2 em h=1e-12).
Em h = 1e-14, 1000 + 1e-14 == 1000, porque h é menor que o espaçamento dos float perto de 1000. Então f(x+h) = f(x), a diferença dá 0
e o erro é |0 - exata| = 0,2134, que é a derivada.

### R9 — Issue #7

Testes de regressão: test_dez_parcelas_de_0_1_somam_exatamente_1, test_um_milhao_de_pulsos, test_parcela_pequena_nao_some_perto_de_numero_grande e test_kahan_fica_mais_perto_do_exato_que_o_ingenuo.
Causa: a correção era o t - (soma + y). Como t já é um float arredondado de soma + y, calcular a soma + y denovo vai dar o mesmo float e a conta dá sempre 0:
nada é compensado e o Kahan vai virar a soma ingênua (100000.00000133288). Em (t - soma) - y, a subtração t - soma é exata e subtrair y deixa o que o arredondamento perdeu.
Os testes de aceitação só vão somar 10 parcelas de 0,1 e comparam com math.isclose (tolerância), que a soma ingênua também passa.

### R10 — Precisão × exatidão

Precisão é o espalhamento das leituras (o desvio); exatidão é a distância até o valor verdadeiro (o viés). Os desvios são quase iguais (0,539 linear e 0,541 spline): mesma precisão.
Mas o viés de PT102 é -1,844 kPa na linear e -0,015 na spline: a linear é precisa, mas é pouco exata.
A média de 595 leituras só reduz o erro aleatório (erro padrão ~ 0,54/raiz(595) ~ 0,02 kPa). O viés vem da própria curva (erro máximo de 2,9 kPa na Etapa 1(a)),
é igual em todas as leituras e, por isso, não some na média.
