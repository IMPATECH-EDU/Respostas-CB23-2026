# Relatório — Marco Antonio Smiguel Dacoregio (3537)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

/home/marco/venvs/prog2-venv/bin/python

=== Etapa 0: ambiente ===
Python 3.12.3 | NumPy 2.5.4 | fornecido 2.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

`"FT201     "` (possui 5 espaços a mais no final). E tomando um padrão igual ao usado em valida_tag: `TAG: re.Pattern = re.compile(r"[A-Z]{1,2}\d{1,3}")`.

O `re.match` verifica se o padrão se cumpre a partir do inicio da string e ignora oque sobrar. Nesse caso o `re.match` SIM aceita a string, pois ignora os 5 espaços a mais.

O `re.fullmatch` verifica se o padrão se cumpre em toda a string. Nesse caso o `re.fullmatch` NAO aceita a string, pois existem espaços a mais.

Se `valida_tag` usasse `re.match` ele iria retornar True para strings que deveria barrar, como: `"PT101 "` (sobra de caracteres).

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

O `ler_log` devolve as linhas descartadas para que quem o chamou possa contá-las e conferi-las, em vez de perdê-las. 
No meu log foram 2404 registros válidos e 4 linhas inválidas. Se, num dia ruim, uma falha de comunicação com os instrumentos deixasse centenas de linhas inválidas e elas fossem ignoradas em silêncio, as médias ainda pareceriam normais, mas a estação ficaria horas sem alguns instrumentos e ninguém seria avisado.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

A lambda `lambda c: c * k` não guarda o valor de `k`: ela lê a variável `k` só no momento em que é chamada. Quando chamo `errados["PT102"](4095)`, o laço já terminou e `k` vale 0,1 (o fator de `FT201`, o último do dicionário), então o resultado é 4095 × 0,1 = 409,5. Na minha `criar_conversores`, cada tag chama `_com_fator(fator)`, e cada chamada tem o seu próprio `fator`, que a lambda de dentro guarda. Por isso `certos["PT102"](4095)` dá 600,0.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

A escala nominal (600/4095) supõe que a pressão é proporcional às contagens. Por ela, a média normal de PT102 dá 261,9 kPa, contra 380 kPa de conferência. 
Minha hipótese é que o transmissor simulado não responde de forma linear, e a reta subestima a pressão. No código da base, em `fornecido/simulador.py`, a função `p_real` calcula `600 * sin(0,5 * pi * c / 4095)`, e `c_real` faz a conta inversa com `arcsin`. Com contagens perto de 1790, essa curva dá cerca de 380 kPa.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 2993572

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | cerca de 1,2 | 18,0 |
| Tempo do laço / tempo vetorizado | cerca de 2 | 43,1 |
| Tempo da compreensão / tempo do laço | cerca de 1 (iguais) | 0,78 |


<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

A maior diferença foi no tempo: previ 2 vezes e deu 43,1 (laço 92 ms, vetorizado 2 ms), porque o laço roda um milhão de voltas no Python e o NumPy faz tudo de uma vez, em código compilado. Na memória previ 1,2 e deu 18,0: cada item da lista ocupa 36 bytes, e no `uint16` são 2.
`uint16 * 20` dá 16364 porque o `uint16` só vai até 65535 e 4095 × 20 = 81900; o valor estoura e recomeça do zero (81900 − 65536 = 16364). Usaria `uint16` para contagens (0 a 4095) e `float64` para kPa, que têm casas decimais.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | ndarray | SerieTemporal |
| `s[1:]` | ndarray | SerieTemporal |
| `s * 2` | ndarray | SerieTemporal |
| `s.sum()` | ndarray | SerieTemporal |
| `s[0]` | ndarray | float64 |

<!-- Explique o resultado que mais surpreendeu você. -->

Previ `ndarray` para tudo e errei: `s + s`, `s[1:]` e `s * 2` devolveram `SerieTemporal`, porque a classe herda de `np.ndarray` e o NumPy mantém o tipo da subclasse nessas operações. O que mais me surpreendeu foi `s.sum()`, que também devolveu `SerieTemporal` e não um número simples, embora seja um valor só. Já `s[0]` devolveu `float64`: um elemento sozinho é um número, e não uma série.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

Sintoma: `media_movel(30)` em 600 pontos devolvia 570 valores, e não 571. Testes de regressão: `test_tamanho_do_resultado` e mais quatro da classe `TestMediaMovelRegressao`, que davam FAIL antes da correção. Causa: o `np.cumsum` não começa em zero, então a diferença `acumulada[janela:] - acumulada[:-janela]` perde a primeira janela. Correção: pôr `0.0` no início da soma acumulada (`np.concatenate`) e devolver `SerieTemporal` com `.view`. Os testes de aceitação só conferem o tipo, as janelas inválidas e que a série não muda, não o tamanho nem os valores. Outro caso não coberto: janela igual ao tamanho da série (dava 0 valores), coberto por `test_janela_igual_ao_tamanho`.

## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->

=== Etapa 0: ambiente ===
Python 3.12.3 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3537

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->

Para h grande domina o erro de **truncamento** (Taylor cortado, ~|f''|·h/2): o erro cai 10× a cada passo, de 1,658e-05 (h = 1, previsto 1,65e-05) a 1,651e-09 (h = 1e-4). 
Para h pequeno domina o **arredondamento**: f(x+h) e f(x) (~225 kPa) quase se cancelam e o erro ~1e-16 de cada um é dividido por h (cresce ~1/h: 1,4e-05 em 1e-9, 1,4e-02 em 1e-12); o equilíbrio dá o mínimo, 6,2e-10 em h = 1e-5.
Em h = 1e-14, `1000 + 1e-14 == 1000` é `True` (o espaçamento dos floats perto de 1000 é ~1,1e-13), então f(x+h) − f(x) = 0 e o erro é |0 − 0,2134|, a própria derivada.

### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->

Testes de regressão: `test_com_100_000_parcelas`, `test_com_10_000_000_parcelas` (dava 999999.9998389754), `test_parcelas_pequenas_nao_somem` (dava 1.0 em vez de 1.000000000000001) e `test_parcelas_diferentes` (dava 600.0000000000113 em vez de 600.0); os quatro falhavam antes da correção.
Causa: `t = s + y` já é arredondado, e calcular `s + y` de novo repete o mesmo arredondamento, então `t - (s + y)` é sempre 0 e o Kahan virava a soma ingênua; em `(t - s) - y`, `t - s` é exato e o resultado é o que se perdeu (a Etapa 2 passa a dar 100000.0, com erro 0).
Os testes de aceitação não pegaram o defeito porque usam `math.isclose`, que aceita 0.9999999999999999 como 1.0.

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->

Precisão é a dispersão das leituras (o desvio) e exatidão é a proximidade do valor verdadeiro (o viés): para PT102, as duas curvas são igualmente precisas (desvio 0,498 na linear e 0,499 na spline), mas só a spline é exata (viés de −0,038 kPa, contra −1,868 kPa da linear).
O desvio vem do ruído do transmissor, que é o mesmo nas duas curvas; o viés vem da reta, que não acompanha a resposta não linear do sensor (erro máximo de 2,88 kPa, contra 0,025 kPa da spline).
A média de 595 leituras reduz só o erro aleatório (o erro padrão cai para 0,498/√595 ≈ 0,02 kPa), mas a reta erra do mesmo jeito em todas as leituras, e esse erro sistemático, cerca de 90 vezes maior, não se cancela.

## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->

A bissecção usa só o sinal de f e corta o intervalo [2, 15] ao meio a cada iteração até a largura ficar menor que `tol = 1e-12`: são log₂(13 / 1e-12) ≈ 43,6, ou seja, sempre 44 iterações, qualquer que seja o Reynolds (a função não influencia).
Ordem 2 (convergência quadrática) quer dizer e_{k+1} ≈ C·e_k²: o número de dígitos corretos dobra a cada passo. Em Re = 1e4 os erros do Newton foram 5,0e-02 → 2,3e-05 → 5,0e-12 (o expoente vai de 2 a 5 e a 12), e a ordem estimada foi 2,00.
O Newton falha quando a derivada é nula ou quase nula, ou quando o ponto inicial está longe da raiz: em f(x) = arctan(x) no intervalo [−2, 8], ele começa em x = 3 e diverge (3 → −9,5 → 5,2 → −8,6 → …), enquanto a bissecção encontra a raiz x = 0, porque só precisa da troca de sinal.

### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->

Testes de regressão: `test_ordem_colebrook_re_10_000`, `test_ordem_colebrook_re_100_000` e `test_ordem_raiz_de_2` (ordem ≈ 1,0 antes da correção, ≈ 2,0 depois).
Com a derivada fixa d, o erro cai sempre na mesma proporção, e_{k+1} ≈ (1 − g'(raiz)/d)·e_k: linear.
Como Colebrook é quase uma reta, esse fator é pequeno (0,039 em Re = 1e4), e o método ainda converge, mas em 10 iterações em vez de 5. Os testes de aceitação só conferem `convergiu` e a raiz, e não as iterações nem a ordem: o resultado sai certo, só que mais devagar.

## Marco 4

### R13 — Integração e descontinuidade

<!-- Na Etapa 1(b), integrando o custo do dia de uma vez, a ordem observada cai para cerca
de 1, no trapézio e no Simpson; integrando cada faixa separadamente, voltam as ordens 2 e 4.
Por quê? -->

### R14 — Issue #11

<!-- Os nomes dos seus testes de regressão; a causa do defeito; por que os testes de
aceitação não o pegaram; por que a regra de Simpson não serve para o registro do dia. -->
```