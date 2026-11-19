# Relatório — Nicholas Joseph Ali (3487)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

```
$ which python
/root/venvs/prog2-venv/bin/python
$ python marco1.py
=== Etapa 0: ambiente ===
Python 3.13.18 | NumPy 2.5.5 | fornecido 4.0
```

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

Com o padrão de tag `[A-Z]{1,2}[0-9]{1,3}`, `re.match` aceita `"PT1010"`: casa `"PT101"` no começo da
string e ignora o `0` que sobra. `re.fullmatch` exige a string inteira e devolve `None`. Com `match`,
`valida_tag` aceitaria `"PT1010"` e `"PT101 "`, dois dos cinco casos inválidos da docstring. Pôr `$` no
fim não basta: `re.match(padrao + "$", "PT101\n")` ainda casa, porque o `$` aceita uma quebra de linha
no final. No padrão usei `[0-9]` em vez de `\d`: num padrão `str`, `\d` casa qualquer dígito Unicode,
e o `strptime` aceita "２０２６" como ano (é o caso de `test_digitos_de_largura_total`).

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

Se `ler_log` só pulasse as linhas ruins, quem usa os registros não teria como saber quanto do log se
perdeu. No meu log foram 4: duas falhas de comunicação com a RTU e duas linhas cortadas
(`2026-10-05 08:03` e `2026-10-05 08:20:4`). Uma linha cortada pode ter sido um alarme de pressão alta
do PT102; descartada em silêncio, o alarme some e ninguém fica sabendo. Com o volume é igual: cada
leitura perdida do FT201 tira uns 390 L da hora sem deixar rastro. Com a lista dá para contar as
falhas por hora e avisar quando a taxa subir, sinal de problema na comunicação com a RTU.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

As lambdas de `errados` não guardam o valor de `k`, guardam a variável `k` da compreensão, e o valor
só é lido na hora da chamada. Quando `errados["PT102"]` roda, a compreensão já terminou com `k = 0.1`,
o fator do FT201 (último do dicionário), e `4095 * 0.1 = 409.5`. Na minha versão cada lambda nasce
dentro de uma chamada de `_multiplica_por(fator)`, e cada chamada tem o seu próprio `fator`, que
ninguém reatribui. O truque `lambda c, k=k: c * k` também resolveria, mas deixa um segundo parâmetro
aberto: `conv["PT101"](10, 5)` daria 50 sem erro nenhum.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

A escala nominal trata o transmissor como linear, `p = c * 600 / 4095`. A média das contagens normais
do PT102 foi 1788,2, o que dá 262,0 kPa contra 380 kPa de conferência. Minha hipótese é que a resposta
do transmissor é curva. Em `fornecido/simulador.py`, `p_real(c)` vale `600 * sin(pi/2 * c / 4095)`:
reta e senoide coincidem em 0 e em 4095, mas no meio a senoide passa bem acima, e `p_real(1788.2)` dá
380,0 kPa. A `tabela_calibracao()` sai dessa mesma função, e é ela que a `CurvaCalibracao` do Marco 2
interpola.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 503b68c

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ≈ 18 | 18,00 |
| Tempo do laço / tempo vetorizado | ≈ 30 | 29,6 |
| Tempo da compreensão / tempo do laço | ≈ 0,7 | 0,79 |

Conta por trás da previsão: na lista, cada contagem custa um ponteiro de 8 bytes mais um `int`
de 28 bytes, contra 2 bytes no `uint16`. Para o tempo, chutei uns 60 ns por volta do laço
contra 2 ns por elemento no NumPy.

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

Memória e vetorizado bateram; a maior diferença foi a compreensão, 0,79 contra 0,7. Ela só poupa a
busca de `kpa.append` e a chamada do método, e o resto (a conta e um `float` novo por elemento) pesa
mais. `uint16 * 20` dá 16364 porque 81900 não cabe em 16 bits: o NumPy mantém o dtype e guarda
81900 - 65536 = 16364, sem erro nem aviso. Para contagens eu usaria `uint16` (os 12 bits do A/D cabem
em 2 bytes), convertendo antes de fazer conta, como o `converter_vetorizado`. Para kPa, `float64`: o
`float32` tem uns 7 dígitos e já perderia centésimos de kPa na soma acumulada da `media_movel`.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float` | `SerieTemporal` |
| `s[0]` | `float` | `float64` |

<!-- Explique o resultado que mais surpreendeu você. -->

O que me pegou foi `s.sum()`: devolve uma `SerieTemporal` de zero dimensões (`shape == ()`), e não um
número. A soma é uma redução de ufunc (`np.add.reduce`), e o NumPy embrulha o resultado na classe da
entrada mesmo sem dimensão nenhuma. Já `s[0]` é indexação por inteiro, que extrai o elemento como o
escalar `float64` do NumPy. Ele herda de `float`, então `isinstance(s[0], float)` dá `True`, enquanto
`isinstance(s.sum(), float)` dá `False`. Agora entendo por que a `amplitude()` faz `float(...)`.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

`media_movel(30)` em 600 leituras dava 570 valores, e não 571. Testes de regressão: os três de
`TestMediaMovelRegressao`, a começar por `test_tamanho_do_relato`. Com `S = cumsum(x)`, a janela que
começa em i soma `S[i+janela-1] - S[i-1]`, com `S[-1] = 0`; o código fazia `S[janela:] - S[:-janela]`,
que são as janelas a partir de i = 1, e a de i = 0 sumia. Corrigi com `somas = S[janela-1:].copy()` e
`somas[1:] -= S[:-janela]`. A aceitação só olha tipo e erros, nunca o tamanho, e não tenta janela =
`len(s)`, que voltava vazia: `test_janela_do_tamanho_da_serie` cobre esse caso.

## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->

```
$ python marco2.py
=== Etapa 0: ambiente ===
Python 3.13.18 | NumPy 2.5.5 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3487
```

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->

De h = 1 até 1e-4 o erro cai dez vezes por década (1,66e-5 até 1,65e-9): é o truncamento da
diferença adiante, cerca de `h * |f''| / 2`. Abaixo de 1e-5 manda o arredondamento: cada valor de
`f` (uns 224,6 kPa em c = 1000) erra na ordem de `eps * 224`, e a divisão por h amplia esse erro,
que cresce como `eps * |f| / h`. O equilíbrio fica perto de `sqrt(eps * |f| / |f''|)`, uns 4e-5, e o
menor erro da tabela saiu em h = 1e-5. Em h = 1e-14, `1000 + 1e-14 == 1000` (o ulp de 1000 é
1,1e-13), `f(x+h) - f(x)` dá 0 e o erro é a própria derivada, 0,2134.

### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->

Testes: `test_milhao_de_decimos` e `test_parcelas_menores_que_o_ulp`, em `TestKahanRegressao`. Com
`t = s + y` já arredondado, `t - (s + y)` calcula `s + y` de novo, com os mesmos operandos e o mesmo
arredondamento: dá o mesmo `t`, e `t - t = 0`. Em `(t - s) - y`, `t` e `s` são próximos e `t - s`
sai exato; é a parte de `y` que entrou na soma, e tirando `y` sobra o que o arredondamento comeu. A
aceitação soma 0,1 dez vezes e usa `math.isclose(total, 1.0)`: o erro do ingênuo ali é 1,1e-16,
longe do `rel_tol` de 1e-9, e o Kahan quebrado passava.

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->

Precisão é o quanto as leituras se repetem; exatidão, o quanto o resultado chega perto do
verdadeiro. No PT102 as duas curvas têm o mesmo desvio (0,526 e 0,527 kPa): ele vem do ruído do A/D,
e perto de 1788 contagens as duas inclinações quase coincidem (0,178 kPa por contagem). O viés é
outra história, -1,800 kPa na linear e 0,030 na spline. A reta liga nós a cada 512 contagens e passa
por baixo da senoide côncava, por isso erra para menos em toda leitura. A média de 595 leituras só
encolhe a parte aleatória (erro padrão 0,526/√595 ≈ 0,02 kPa); o erro repetido fica inteiro.

## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->

A bissecção só olha o sinal de `g`: corta [2, 15] ao meio a cada iteração e para quando a largura
`13 / 2**k` fica abaixo de 1e-12, o que pede k = 44 (`2**43` ≈ 8,8e12 não basta). O Reynolds muda a
raiz, não a largura do intervalo. Ordem 2 quer dizer `e_{k+1} ≈ C * e_k**2`, e os dígitos certos
mais ou menos dobram por passo: em Re = 1e4 os erros foram 5,0e-2, 2,3e-5 e 5,0e-12, com
`e_{k+1} / e_k**2` igual a 0,0094 e 0,0093. O Newton falha em `x**3 - 2*x + 2` com [-2, 2]: sai de
0, vai a 1, volta a 0 e fica no ciclo até `max_iter`; a bissecção acha -1,7693 em 42 iterações, só
com a troca de sinal.

### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->

Testes: `test_colebrook_com_re_1e4` e `test_erro_cai_ao_quadrado`, em `TestNewtonRegressao`. Com a
derivada `d` congelada no ponto inicial, `x - f(x) / d` é uma iteração de ponto fixo, e perto da
raiz cada passo multiplica o erro por `1 - f'(r) / d`. Como `d` não é `f'(r)`, o fator não zera e a
convergência é linear: em `x**2 - 2`, saindo de 1, ele vale `1 - 2.83 / 2 ≈ -0,41`. Recalculando
`d = f'(x_k)`, o fator vai a zero e o erro cai ao quadrado. A aceitação só confere se o método chega
ao valor certo, e com a derivada fixa ele chega, só que devagar (10 iterações contra 5 em Re = 1e4).
