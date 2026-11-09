# Relatório — Eduardo Costa de Souza (3465)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

Python instalado no sistema (Windows), sem ambiente virtual.

```text
$ which python
/c/dev/languages/Python/Python312/python

$ python marco1.py   # Etapa 0
=== Etapa 0: ambiente ===
Python 3.12.1 | NumPy 1.26.3 | fornecido 4.0
```

### R1 — Expressões regulares

A string `PT1010` é aceita por `re.match` e rejeitada por `re.fullmatch` com o padrão de tag, porque o `re.match` precisa que somente o *início* seja igual, já o `re.fullmatch` necessita que a string satisfaça do início ao fim.
Se `valida_tag` usasse `match`, então seriam aprovadas tags inválidas, tais quais `PT1010` e `PT101`.

### R2 — Linhas inválidas

`ler_log` devolve as linhas descartadas porque isso permite analisar o que foi perdido e apurar o motivo de serem inválidas, além de poder determinar o que era aquela informação.
Na operação da estação, descartá-las em silêncio esconderia um problema quando houvesse em alguma dessas linhas uma falha que seria omitida por ser um log inválido.

### R3 — Late binding

`errados["PT102"](4095)` dá 409,5 porque a função lambda guarda a variável `k` e não o valor dessa variável, ou seja, é passado por referência e vale o último fator, no caso `0,1`.
A minha `criar_conversores` não tem o problema porque a cada chamada de `_multiplicador(fator)` um novo escopo é criado e a função lambda fica presa nesse escopo.

### R4 — Escala nominal

A escala nominal deu 262,0 kPa, e o valor de conferência é 380,0 kPa.
Minha hipótese para a diferença é que a resposta do transmissor não é linear, de forma que a reta dada subestima a pressão nessa faixa.
A explicação está em `p_real`, no arquivo `fornecido/simulador.py`, onde ela calcula `600 * sen(π/2 * c/4095)` que é uma senoidal, com `c` próximo de `1790` que aproxima bem melhor o valor esperado.

### R5 — Previsão × medição (Etapa 3)

Previsões: não houve commit separado de previsões. Como previsão para esta máquina, usei as razões medidas numa execução anterior em outra máquina (Python 3.13.15, NumPy 2.5.2), registradas depois da medição.

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18,0× | 18,0× (36 000 056 B / 2 000 000 B) |
| Tempo do laço / tempo vetorizado | 34,7× | 14,4× (108,59 ms / 7,53 ms) |
| Tempo da compreensão / tempo do laço | 0,91× | 0,92× (99,80 ms / 108,59 ms) |

A maior diferença entre previsão e medição foi na razão laço / vetorizado: previ 34,7× e medi 14,4×, porque o tempo depende da máquina, e as duas partes mudam de jeitos diferentes. O laço em Python ficou cerca de 3,4× mais lento (31,75 → 108,59 ms), já o vetorizado ficou cerca de 8× mais lento (0,91 → 7,53 ms) e oscilou entre 4,9 e 10 ms em execuções seguidas. Uma operação de poucos milissegundos sofre mais com a carga do sistema e com a versão do NumPy (1.26 aqui, 2.5 na outra máquina). A memória não muda (18,0× nas duas), porque só depende do tamanho dos objetos, e a razão compreensão / laço também quase não muda (0,91× e 0,92×), porque as duas implementações rodam no mesmo interpretador.
`uint16` vezes 20 dá 16364 porque o resultado continua `uint16`, que só guarda de 0 a 65535: 4095 · 20 = 81900 estoura e o valor é tomado módulo 2¹⁶, ou seja, 81900 − 65536 = 16364, sem aviso nenhum.
Para guardar contagens, eu escolheria `uint16`, porque 0 a 4095 cabe em 12 bits e cada contagem ocupa 2 bytes, 18 vezes menos que na lista (só é preciso converter para `float` antes de fazer contas, como em `converter_vetorizado`).
Para guardar pressões em kPa, eu escolheria `float64`, porque é o tipo padrão do NumPy e das contas que vêm depois (médias, desvios, incertezas), evitando arredondamentos acumulados do `float32`, e a memória extra (8 MB por milhão) é irrelevante aqui.

### R6 — Tipos da SerieTemporal (Etapa 4d)

Como no R5, a coluna "previsto" vem da execução anterior em outra máquina. Os tipos não dependem da máquina, e as duas execuções coincidem.

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `SerieTemporal` | `SerieTemporal` |
| `s[0]` | `float64` | `float64` |

O resultado que mais me surpreendeu foi `s.sum()`, porque uma redução devolve um único número, e o natural seria um `float64`; mas o NumPy preserva a subclasse e devolve uma `SerieTemporal` de dimensão 0. Já `s[0]` indexa um elemento e devolve o escalar `numpy.float64`. Por isso o `marco1.py` usa `float(s.mean())` antes de formatar.

### R7 — Issue #4

**Sintoma:** `media_movel(30)` da série de 600 leituras de PT102 devolvia 570 valores, e não os `n − janela + 1 = 571` da docstring; o valor que faltava era a média da primeira janela, `s[0:30]`.
**Teste de regressão:** `test_tamanho_do_relato` e `test_primeira_janela_presente` (além de `test_janela_do_tamanho_da_serie` e `test_janela_unitaria`); os quatro falham com o código original.
**Causa:** em termos da soma acumulada, `acumulada[i] = s[0] + ... + s[i]`, então `acumulada[i + janela] − acumulada[i]` é a soma de `s[i+1 : i+janela+1]`; a soma da primeira janela, `s[0:janela]`, é `acumulada[janela−1] − 0`, e esse "0" não existia no vetor. A subtração produzia só `n − janela` diferenças.
**Correção:** inserir um zero no início antes de acumular, `np.cumsum(np.insert(self, 0, 0.0))`: o vetor passa a ter `n + 1` somas parciais e as `n − janela + 1` diferenças incluem a primeira janela. `np.insert` devolve uma cópia, então `self` não é modificado, e o resultado continua `SerieTemporal`.
**Por que os testes de aceitação não pegaram:** `test_media_movel_tipo_e_erros` só confere o tipo do resultado e os `ValueError` das janelas 0 e 6; nenhum teste de aceitação confere o tamanho nem os valores da média móvel.
**Outro caso que eles não cobrem:** `janela == len(s)`, que deveria devolver um único valor (a média da série) e devolvia um vetor vazio, coberto pelo meu teste `test_janela_do_tamanho_da_serie`.

## Marco 2

### Ambiente

```text
$ python marco2.py   # Etapa 0
=== Etapa 0: ambiente ===
Python 3.12.1 | NumPy 1.26.3 | SciPy 1.16.3 | fornecido 4.0 | matrícula 3465
```

### R8 — Derivada numérica

De h = 1 (erro 1,7e-5) até h = 1e-5 (erro 6,2e-10), o erro cai 10 vezes a cada década de h: domina o erro de **truncamento** da diferença adiante, proporcional a h (ordem 1).
Abaixo disso domina o erro de **arredondamento**: f(x+h) e f(x) são quase iguais, a subtração cancela os dígitos significativos e o erro relativo de ~1e-16 de cada valor (~224 kPa) é dividido por h, crescendo como 1/h (2,8e-6 em h = 1e-8, 1,4e-2 em h = 1e-12).
Em h = 1e-14, `1000 + 1e-14 == 1000` é `True`: x + h é o próprio x em ponto flutuante, então f(x+h) − f(x) = 0, a estimativa é 0 e o erro é exatamente a derivada, 0,2134.

### R9 — Issue #7

Testes de regressão: `test_milhao_de_decimos`, `test_parcela_pequena_nao_se_perde` e `test_igual_a_fsum`; os três falhavam com o código original.
Causa: `t` já é o resultado arredondado de `soma + y`; calcular `soma + y` de novo arredonda do mesmo jeito e dá o mesmo `t`, então `t − (soma + y)` é sempre 0 e a correção nunca é aplicada (o Kahan virava a soma ingênua). Algebricamente é igual a `(t − soma) − y`, mas só nessa ordem a conta recupera o que se perdeu: `t − soma` é exato e vale a parte de `y` que de fato entrou na soma; subtrair `y` dá o resto perdido. A correção foi só reordenar os parênteses.
Os testes de aceitação somam apenas dez parcelas de 0,1 e comparam com `math.isclose` (tolerância relativa de 1e-9): o erro da soma ingênua é muito menor que isso, então os dois acumuladores passavam.

### R10 — Precisão × exatidão

Para PT102, o desvio é 0,536 kPa com a linear e 0,537 kPa com a spline: a **precisão** (dispersão das leituras em torno da própria média) é a mesma, porque vem do ruído do transmissor. Já o viés é −1,835 kPa com a linear e −0,006 kPa com a spline: a **exatidão** (distância da média ao valor verdadeiro) é bem diferente.
A média de ~595 leituras reduz o erro aleatório (o erro padrão cai com √n), mas o erro da curva linear é sistemático: perto de 1790 contagens a reta entre os pontos da tabela fica sempre abaixo da resposta senoidal, e toda leitura é convertida com o mesmo erro. A média converge para o valor enviesado, não para o verdadeiro.

## Marco 3

### R11 — Bissecção × Newton

A bissecção divide o intervalo ao meio a cada iteração, sem olhar para a forma de f: para sair de [2, 15] (largura 13) e chegar a uma largura menor que 1e-12, precisa de ⌈log2(13 / 1e-12)⌉ = ⌈43,56⌉ = 44 iterações, para qualquer Reynolds.
Ordem 2 significa e_{k+1} ≈ C·e_k²: o número de dígitos corretos dobra a cada passo. Em Re = 1e4, os erros do Newton foram 5,0e-2 → 2,3e-5 → 5,0e-12 (2, 5 e 11 dígitos), e a ordem estimada foi 2,00.
O Newton falha se a derivada se anula ou se o ponto inicial está longe da raiz: em f(x) = x³ − 2x + 2 a partir de x0 = 0 ele fica oscilando entre 0 e 1 para sempre; a bissecção em [−2, 0] converge, porque só precisa da troca de sinal.

### R12 — Issue #9

Testes de regressão: `test_colebrook_em_poucas_iteracoes`, `test_raiz_de_dois_em_poucas_iteracoes` e `test_digitos_dobram`; os três falhavam com o código original (10 e 32 iterações).
Com a derivada calculada uma vez só, em x0, o método vira o das cordas: x_{k+1} = x_k − f(x_k)/f'(x0). Perto da raiz, e_{k+1} ≈ (1 − f'(r)/f'(x0))·e_k, ou seja, o erro só é multiplicado por uma constante a cada passo: convergência linear. O Newton precisa da derivada no ponto atual para que esse fator também vá a zero.
Os testes de aceitação só conferem se o resultado converge e se a raiz está certa, com `max_iter = 100`: o método lento chega à mesma raiz, só que gastando mais iterações, e nenhum teste conferia o número de iterações.

## Marco 4

### R13 — Integração e descontinuidade

As regras compostas só têm ordem 2 (trapézio) e 4 (Simpson) se o integrando for suave em cada subintervalo. Integrando o custo de uma vez, a tarifa salta às 18 h e às 21 h, e esses instantes caem no meio de um subintervalo: ali a regra aproxima um degrau por um polinômio, com erro proporcional ao salto vezes h. Esse erro O(h) domina os demais, e a ordem observada cai para 1,00 (trapézio) e 0,65 (Simpson).
Integrando faixa por faixa, os saltos ficam nos extremos dos intervalos de integração, a tarifa é constante em cada faixa e a potência é suave: voltam as ordens 2,00 e 4,00 (erro de 8e-8 com Simpson em n = 110).

### R14 — Issue #11

Testes de regressão: `test_reta_em_malha_irregular`, `test_constante_com_leitura_perdida` e `test_registro_do_dia_com_falhas`; os três falhavam com o código original.
Causa: `integrar_tabela` do trapézio usava um único passo `h = x[1] − x[0]` (15 min) para todos os trapézios. Onde o SCADA perdeu leituras, intervalos de 30 e 45 min eram contados como 15, e o volume do dia saía 3584,8 m³ em vez de 3888,0 m³ (7,8% abaixo). A correção usa a largura de cada trapézio, `np.diff(x)`.
Os testes de aceitação só usam malhas uniformes (`linspace` e passos de 1,5 h), em que as duas fórmulas coincidem.
Simpson não serve porque exige pontos igualmente espaçados e um número par de subintervalos; o registro do dia tem passos de 15, 30 e 45 min, e a própria `Simpson.integrar_tabela` recusa a tabela.
