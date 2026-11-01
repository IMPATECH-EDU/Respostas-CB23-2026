# Relatório — Maria Leticia Lins Nunes (3478)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

```
/home/leticia/venvs/prog2-venv/bin/python
=== Etapa 0: ambiente ===
Python 3.12.3 | NumPy 2.5.4 | fornecido 1.0
```

### R1 — Expressões regulares

O padrão de tag é `[A-Z]{1,2}\d{1,3}`. A string `"PT1010"` é aceita por `re.match`, que só exige que o começo combine (`PT101`) e ignora o `0` que sobra, mas é rejeitada por `re.fullmatch`, que exige a string inteira. O mesmo vale para `"PT101 "` (espaço no fim). Se `valida_tag` usasse `match`, ela devolveria `True` para essas duas tags inválidas.

### R2 — Linhas inválidas

`ler_log` devolve as linhas descartadas para que quem chamou possa contá-las, conferi-las e investigá-las. No meu log, 4 das 2408 linhas estavam corrompidas, e o `assert` do script confere esse número. Se elas fossem descartadas em silêncio, uma falha de comunicação com a RTU (as linhas `### falha de comunicacao ###`) passaria despercebida: um instrumento ficaria sem registrar durante minutos e o volume bombeado ou a pressão média seriam calculados com dados faltando, sem ninguém saber.

### R3 — Late binding

Em `{tag: (lambda c: c * k) for tag, k in escalas.items()}`, a lambda não guarda o valor de `k`, guarda a variável `k`. Ela só consulta o valor quando é chamada, e nesse momento o laço já terminou e `k` vale o último fator (0,1, do `FT201`). Por isso `errados["PT102"](4095)` dá 4095 × 0,1 = 409,5. A minha `criar_conversores` chama a função auxiliar `_fazer_conversor(fator)` para cada tag: cada chamada cria o seu próprio `fator`, que a lambda guarda e que nunca muda.

### R4 — Escala nominal

A escala nominal (600/4095) supõe que o transmissor é linear, isto é, que a pressão é proporcional às contagens. Minha hipótese é que ele não é linear. No `fornecido/simulador.py`, a função `p_real` mostra que a resposta verdadeira é `600 * sin(0,5 * pi * c / 4095)`. Para a contagem média normal de PT102 (cerca de 1788), a escala nominal dá 262,0 kPa, enquanto `p_real` dá 380,02 kPa, igual ao valor de conferência. A função `tabela_calibracao`, com 9 pontos, indica que o próximo passo é usar a calibração em vez da escala linear.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 063aa63

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 vezes | 18 vezes |
| Tempo do laço / tempo vetorizado | 100 vezes | 32 vezes |
| Tempo da compreensão / tempo do laço | 0,7 | 0,71 |

A maior diferença foi no tempo: previ ~100 vezes e medi 32. Minha hipótese é que subestimei o custo do NumPy: `contagens * 600 / 4095` percorre 1 milhão de elementos duas vezes e cria vetores temporários. `uint16 * 20` dá 16364 porque 81900 não cabe em 16 bits (máximo 65535) e o NumPy "dá a volta" sem avisar: 81900 − 65536 = 16364. Escolheria `uint16` para contagens e `float32` para kPa (`float64` se forem encadear muitos cálculos).

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

O que mais me surpreendeu foi `s.sum()` devolver uma `SerieTemporal` (um array de dimensão 0) e não um número comum. A subclasse de `ndarray` mantém o seu tipo até nas reduções, enquanto `s[0]` devolve um escalar `float64`. Para ter um número simples preciso converter, como em `int(...)` ou `float(...)`, que usei na Etapa 1(c).

### R7 — Issue #4

Sintoma: 600 leituras e janela 30 davam 570 valores, não 571. Regressão: `test_tamanho_de_600_com_janela_30` e `test_primeira_media_inclui_o_inicio_da_serie`, que falhavam antes da correção. Causa: `cumsum[i]` já inclui o elemento `i`, então `acumulada[janela:] - acumulada[:-janela]` somava `self[i+1 : i+janela+1]`: a primeira janela (`self[0:janela]`) se perdia. Correção: um `0` na frente da soma acumulada. Os de aceitação só conferem o tipo de retorno e os erros de janela (0 e 6) de `media_movel`, nunca o tamanho nem os valores; com o defeito, todos passavam. Caso não coberto: janela igual a `len(s)` (dava zero valores), coberto por `test_janela_igual_ao_tamanho`.

## Marco 2

### Ambiente

```
Python 3.12.3 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3478
```

### R8 — Derivada numérica

De h = 1 até h = 1e-5 o erro cai de 1,7e-05 para 6,2e-10 (o menor da tabela está em h = 1e-5): domina o erro de truncamento da diferença adiante, que é proporcional a h (termo f''·h/2 da série de Taylor). Para h menor, domina o erro de arredondamento: f(x+h) e f(x) ficam quase iguais, a subtração cancela algarismos e o erro cresce como ε·|f|/h. Em h = 1e-14, `1000 + 1e-14 == 1000` (o passo é menor que o espaçamento entre números perto de 1000), então f(x+h) − f(x) = 0, a derivada calculada é 0 e o erro é |0 − exata| = a própria derivada (0,2134 kPa/contagem).

### R9 — Issue #7

Testes de regressão: `test_um_milhao_de_decimos_de_litro`, `test_kahan_bem_melhor_que_o_ingenuo`, `test_parcelas_menores_que_o_arredondamento` e `test_valores_variados_contra_math_fsum`; todos falhavam antes da correção. Causa: `t = s + y` e depois `t - (s + y)`: a segunda soma repete a mesma conta com os mesmos operandos e dá exatamente o mesmo `t`, então o resultado é sempre 0 e a correção nunca guarda nada. Algebricamente é igual a `(t - s) - y`, mas em ponto flutuante não: `t - s` recupera o que realmente entrou em `t`, e subtrair `y` deixa o que se perdeu. Correção: `(t - self._soma) - y`. Os testes de aceitação somam só 10 parcelas de 0,1 e comparam com `math.isclose`; com tão poucas parcelas o ingênuo e o Kahan dão praticamente o mesmo total, e o defeito não aparece.

### R10 — Precisão × exatidão

Os desvios são praticamente iguais (linear 0,569 kPa, spline 0,571 kPa): a precisão, isto é, a dispersão das leituras em torno da própria média, não depende da curva. Já o viés (média menos 380 kPa) é -1,812 kPa na linear e 0,018 kPa na spline: a exatidão, isto é, a proximidade do valor verdadeiro, é bem pior na linear. O erro padrão da média é só cerca de 0,023 kPa (desvio/√595), então a média de quase 600 leituras reduz o erro aleatório, mas não o viés: ele vem da interpolação linear (erro máximo de 2,88 kPa), é sistemático e igual em todas as leituras, e por isso não se cancela ao tirar a média.

## Marco 3

### R11 — Bissecção × Newton

A bissecção gasta sempre 44 iterações porque o intervalo inicial é o mesmo ([2, 15], largura 13) e cada iteração o divide ao meio: o número de passos é ⌈log2(13/tol)⌉ = 44 para tol = 1e-12, e não depende de f nem do Reynolds. Ordem de convergência 2 significa e_{k+1} ≈ C·e_k²: o número de dígitos corretos dobra a cada iteração. Com Re = 1e4, os erros foram 2,9e+00 → 5,0e-02 → 2,3e-05 → 5,0e-12 e a ordem estimada deu 2,00. O Newton falha e a bissecção não quando a derivada é zero (ou quase) em alguma aproximação, ou quando o ponto inicial é ruim e as iterações divergem, como em f(x) = x^(1/3), de raiz 0, em que cada passo dobra a distância. A bissecção só precisa da troca de sinal em [a, b] e sempre converge.

### R12 — Issue #9

Testes de regressão: `test_poucas_iteracoes_para_a_raiz_de_dois`, `test_derivada_recalculada_a_cada_iteracao`, `test_erro_cai_com_o_quadrado_a_cada_passo` e `test_colebrook_re_1e4_com_cinco_ou_seis_iteracoes`; os quatro falhavam antes da correção. Com a derivada calculada só no ponto inicial, a iteração vira `x ← x − f(x)/f'(x0)` (método da corda): o erro é multiplicado a cada passo por um fator constante, ≈ |1 − f'(raiz)/f'(x0)|, que não é zero, então a convergência é linear. Recalculando f'(x_k), esse fator tende a zero e o erro passa a cair com o quadrado do anterior. Os testes de aceitação só conferem se a raiz sai certa (a corda também chega, com mais passos) e não contam iterações nem medem a ordem; no Colebrook com Re = 1e4 são 5 iterações após a correção, contra 10 antes. Correção: mover `derivada = self._derivada(f, x)` para dentro do laço.
