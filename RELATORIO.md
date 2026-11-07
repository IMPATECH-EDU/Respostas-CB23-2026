# Relatório — Diogo Ismael Ferreira da Silva (3459)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

```
$ which python
<COLE AQUI a saída de `which python` (ou `where python` no Windows) com o ambiente ativo>

=== Etapa 0: ambiente ===
Python 3.13.18 | NumPy 2.5.3 | fornecido 4.0
```

### R1 — Expressões regulares

Com o padrão de tag `[A-Z]{1,2}\d{1,3}`, a string `"PT1010"` passa no `re.match`, porque ele
só exige que o começo case (casa `"PT101"` e ignora o último `0`), mas falha no `re.fullmatch`,
que exige a string inteira. O mesmo acontece com `"PT101 "`, que tem um espaço sobrando. Se eu
tivesse usado `match` em `valida_tag`, essas duas tags inválidas seriam aceitas.

### R2 — Linhas inválidas

Devolver as linhas descartadas permite contá-las, registrá-las e gerar um alerta: no meu log
foram 4 de 2408 (≈ 0,17 %). Se elas fossem ignoradas em silêncio, uma RTU com falhas
frequentes passaria despercebida. Por exemplo, se a comunicação cair justamente durante um
alarme de pressão alta, as leituras desse trecho somem, a média continua parecendo normal e
ninguém fica sabendo que faltam dados exatamente no momento mais importante.

### R3 — Late binding

Na versão errada, a lambda `lambda c: c * k` não guarda o valor de `k`, e sim uma referência à
variável `k` da compreensão. Ela só é lida quando a função é chamada, e aí a compreensão já
acabou e `k` ficou com o último fator, 0,1 (do `FT201`); por isso 4095 · 0,1 = 409,5. Na minha
`criar_conversores` usei `lambda c, fator=fator: c * fator`: o valor padrão é calculado no
momento em que cada lambda é criada, então cada tag fica com o seu próprio fator.

### R4 — Escala nominal

Minha hipótese é que o transmissor não é linear. A escala nominal é uma reta (600 kPa em 4095
contagens), mas em `fornecido/simulador.py` a função `p_real` mostra que a resposta verdadeira
é `600·sin(π/2 · c/4095)`, uma curva côncava, que fica acima da reta no meio da faixa. Com a
média de ≈ 1791 contagens, a reta dá 262,0 kPa e a curva dá 380 kPa. Por isso o Marco 2 usa
a tabela de calibração (`tabela_calibracao`) em vez da escala nominal.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: d604fd0

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ≈ 18× (8 B de ponteiro + 28 B de `int` por elemento, contra 2 B) | 18,0× (36 000 056 B / 2 000 000 B) |
| Tempo do laço / tempo vetorizado | ≈ 50× | 45,6× (53,82 ms / 1,18 ms) |
| Tempo da compreensão / tempo do laço | ≈ 0,7 (a compreensão evita o `append`) | 1,02 (54,72 ms / 53,82 ms) |

A maior diferença foi na compreensão: eu esperava uns 30 % de ganho e ela saiu praticamente
igual ao laço. No Python 3.13 o `append` dentro do laço ficou barato (o interpretador
especializa essa chamada), e quase todo o tempo vai na conta `c * 600 / 4095`, que as duas
fazem do mesmo jeito. O `uint16` só vai até 65535: 4095 · 20 = 81900 estoura e volta do zero,
81900 − 65536 = 16364, sem nenhum aviso. Para contagens eu usaria `uint16` (cabe e ocupa 2 B),
convertendo para float antes de fazer contas; para kPa, `float64`, pela precisão.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float64` | `SerieTemporal` |
| `s[0]` | `float64` | `float64` |

O que me surpreendeu foi `s.sum()`. Eu esperava um número, mas a soma é feita por uma redução
de ufunc (`np.add.reduce`), e o NumPy devolve o resultado embrulhado na subclasse, como uma
`SerieTemporal` de dimensão 0. Já `s[0]` pega um único elemento e devolve um escalar
`float64`, sem passar pela subclasse. Para usar a soma como número, é preciso `float(s.sum())`.

### R7 — Issue #4

O sintoma era `media_movel(30)` devolver 570 valores para 600 pontos, em vez de 571. Os testes
de regressão são `TestMediaMovelRegressao.test_quantidade_de_valores` e
`test_primeira_janela_presente`. A causa: `acumulada[i]` é a soma de `x[0]` até `x[i]`, então
`acumulada[janela:] - acumulada[:-janela]` só dá as janelas que começam em 1, 2, ...; a que
começa em 0 ficava de fora. Corrigi colocando um zero antes da soma acumulada. Os testes de
aceitação só checavam o tipo e as janelas inválidas, nunca o tamanho nem os valores. Outro
caso não coberto: janela do tamanho da série dava vetor vazio (`test_janela_do_tamanho_da_serie`).

## Marco 2

### Ambiente

```
=== Etapa 0: ambiente ===
Python 3.13.18 | NumPy 2.5.3 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3459
```

### R8 — Derivada numérica

De h = 1 até h = 1e-5 o erro cai 10 vezes a cada década (de 1,66e-5 para 1,65e-9), porque
domina o erro de truncamento da diferença adiante, que é proporcional a h (≈ h·|f''|/2). Abaixo
de 1e-5 domina o arredondamento, que cresce como ε·|f|/h: f(x+h) e f(x) ficam quase iguais, a
subtração perde dígitos e a divisão por h amplia o erro. O melhor foi h = 1e-5 (erro 6,2e-10).
Em h = 1e-14, `1000 + 1e-14 == 1000` dá `True` (perto de 1000 os floats estão a ≈ 1,1e-13 um do
outro), então f(x+h) − f(x) = 0 e o erro é a própria derivada, 0,2134.

### R9 — Issue #7

Os testes de regressão são `TestKahanRegressao.test_dez_decimos_dao_exatamente_um`,
`test_parcelas_menores_que_o_ulp_nao_se_perdem` e `test_erro_muito_menor_que_o_ingenuo`. A
causa: `t = soma + y` já é o valor arredondado, e calcular `soma + y` de novo arredonda para o
mesmo float, então `t - (soma + y)` dá sempre zero e a correção nunca acontece. Escrevendo
`(t - soma) - y`, a conta `t - soma` é exata e mostra quanto de `y` realmente entrou; tirando
`y`, sobra o que se perdeu. Os testes de aceitação só somavam 10 × 0,1 com `math.isclose`, que
aceita o erro de 1e-16 da soma ingênua.

### R10 — Precisão × exatidão

Precisão é o quanto as leituras se espalham; exatidão é o quanto a média se afasta do valor
verdadeiro. Em PT102, as duas curvas têm quase o mesmo desvio (0,540 kPa na linear e 0,542 na
spline), que é o ruído do transmissor, mas o viés é −1,840 kPa na linear e só −0,010 na spline.
A média das 595 leituras válidas reduz o erro aleatório (erro padrão ≈ 0,542/√595 ≈ 0,02 kPa),
mas não o viés: a reta entre os pontos da tabela fica abaixo da curva verdadeira, e toda leitura
é convertida com o mesmo erro sistemático, que não se cancela na média.

## Marco 3

### R11 — Bissecção × Newton

A bissecção só olha o sinal de g e corta o intervalo ao meio a cada passo, então o número de
iterações depende só de (b − a)/tol = 13/1e-12: ⌈log2(1,3e13)⌉ = 44, seja qual for o Reynolds.
Ordem 2 significa e_{k+1} ≈ C·e_k². Em Re = 10⁴, os erros do Newton foram 5,0e-2 → 2,3e-5 →
5,0e-12, e os dígitos corretos (1, 5, 11) quase dobram a cada passo (ordem estimada 2,00). Um
caso em que o Newton falha e a bissecção não: `atan(x)` começando em |x0| > 1,39, onde os passos
crescem e divergem, enquanto a bissecção em [−2, 3] sempre converge.

### R12 — Issue #9

Os testes de regressão são `TestNewtonRegressao.test_raiz_de_dois_em_poucas_iteracoes`,
`test_colebrook_re_1e4`, `test_derivada_avaliada_a_cada_iteracao` e
`test_erros_caem_quadraticamente`. Com a derivada fixa em x0, o método vira o método da corda:
e_{k+1} ≈ (1 − f'(r)/f'(x0))·e_k, ou seja, o erro cai por um fator constante (convergência
linear). Só com f'(x_k) atualizada esse termo de primeira ordem some e sobra o termo em e_k².
Os testes de aceitação só verificavam se convergia e se a raiz estava certa, não o número de
iterações nem a ordem.

## Marco 4

### R13 — Integração e descontinuidade

As ordens 2 e 4 só valem se a função for suave (com f'' ou f⁽⁴⁾ limitada) em cada
subintervalo. O custo dá um salto às 18 h e às 21 h por causa da tarifa, e com n = 30 a 110 os
nós quase nunca caem nesses horários. O subintervalo que contém o salto erra da ordem de h·salto,
e esse erro domina: a ordem cai para ≈ 1 (trapézio 1,00 e Simpson 0,65). Integrando cada faixa
separadamente, a função é a potência (suave) vezes uma constante, e as ordens voltam a 2,00 e
4,00 (erro em n = 110 de 6,3e-4 e 8,1e-8).

### R14 — Issue #11

Os testes de regressão são `TestTrapezioTabelaRegressao.test_reta_em_malha_irregular_e_exata`,
`test_constante_da_comprimento_total` e `test_registro_com_falhas_igual_ao_np_trapezoid`. A
causa: `integrar_tabela` usava o mesmo passo `h = x[1] - x[0]` (15 min) em todos os trapézios;
onde faltava uma leitura, o intervalo real era de 30 min, mas entrava com metade da largura. Com
a minha matrícula, o volume dava 3545,2 m³ contra 3888,0 m³ (−8,8 %); corrigido, dá 3905,2 m³
(0,44 %). Os testes de aceitação só usavam malhas uniformes. Simpson não serve porque exige
pontos igualmente espaçados e em número ímpar, e o registro tem intervalos de 15 e 30 min.
