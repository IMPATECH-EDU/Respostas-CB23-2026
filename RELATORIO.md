# Relatório — Oigres Leal Brandão (3489)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

```
$ which python
/opt/anaconda3/envs/ambiente_aluno/bin/python

=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.2 | fornecido 4.0
```

### R1 — Expressões regulares

String: `"PT1234"`
| Comando | Saída |
| --- | --- |
| `re.match("[A-Z]{1,2}\d{1,3}", "PT1234")` | `<re.Match object; span=(0, 5), match='PT123'>` |
| `re.fullmatch("[A-Z]{1,2}\d{1,3}", "PT1234")` | `None` |

`valida_tag` utiliza re.fullmatch, logo a string dada não passaria, pois não é aceita no padrão de tag `[A-Z]{1,2}\d{1,3}`. Mas o re.match só verifica se os primeiros caracteres se encaixam no padrão, isto é, re.match veria que `"PT123"` passa e ignoraria o 4. Essa tag não existiria no sistema por ter mais de 3 digitos finais, implicando numa validação inválida por parte do sistema.

### R2 — Linhas inválidas

`ler_log` devolve as linhas descartadas para informar quantas foram perdidas, por que foram perdidas e se os registros válidos representam o log inteiro. Se um sensor desregulado passasse a escrever as linhas em outro formato, `ler_log` descartaria todas elas e o volume bombeado ficaria menor que o real, mas os números pareceriam normais. Com `invalidas`, a lista cresceria de poucas linhas para muitas, todas parecidas e da mesma tag, o que apontaria o problema.

### R3 — Late binding

Em `errados`, `lambda c: c * k` não guarda o valor de `k`, só uma referência ao nome. `k` é consultado quando a lambda é chamada, e nesse momento o laço já terminou e `k` vale 0,1 (escala de `FT201`). Por isso `errados["PT102"](4095)` dá 4095 × 0,1 = 409,5, em vez de 600. Isso é late binding. Em `criar_conversores`, `lambda c, k=fator: c * k` fixa o valor na criação da lambda (early binding), então cada tag mantém o seu próprio `k`.

### R4 — Escala nominal

A diferença (> 100 kPa) entre a pressão calculada com a escala nominal e o valor de `verdade["pressao_recalque"]` pode ocorrer porque a escala nominal assume uma resposta linear do transmissor `(p = c × 600 / 4095)`, mas a resposta real do sensor é não-linear. A explicação está em `fornecido/simulador.py`, nas funções `p_real` e `c_real` mostrando que a resposta verdadeiramente é senoidal.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 14fba7d

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 18 |
| Tempo do laço / tempo vetorizado | 30 | 34,77 |
| Tempo da compreensão / tempo do laço | 0,73 | 0,92 |

A maior diferença (proporcional) foi em `Tempo da compreensão / tempo do laço`: previ uma vantagem um pouco maior, mas o custo principal estava nas operações aritméticas e não no overhead do laço. `uint16 * 20` dá overflow, pois `uint16` vai só de `0` a `65535` e `4095 * 20 = 81900 > 65535`, então o resultado é `81900 % 65536 = 16364`. Para contagens (0 a 4095), escolheria `np.uint16`, o menor inteiro que comporta o máximo. Para kPa, `np.float64`, pela precisão em contas posteriores.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

O que mais me surpreendeu foi o `s.sum()` ser `SerieTemporal` e não `float64`. Acreditei que `s.sum()` pegaria os termos internos que são `float64` e retornaria a soma de floats em `float64`, mas o que o `s.sum()` realmente faz é pegar a `SerieTemporal` (subclasse de `ndarray`) que ele recebe e retorna um resultado de uma dimensão menor e não um `float64`. Isso ocorre porque, nas reduções, o NumPy preserva a subclasse e devolve um array 0-d da SerieTemporal, em vez de um escalar.

### R7 — Issue #4

- **Sintoma:** para 600 leituras de `PT102` e janela 30, `media_movel(30)` devolvia 570 valores, mas a docstring exigia `n - janela + 1 = 571`.
- **Testes de regressão:** `test_quantidade_de_medias`, `test_media_movel_valores` e `test_media_movel_janela_1` falhavam com o código original.
- **Causa:** `np.cumsum(self)` sem o zero inicial. Com um vetor de `n` posições, as fatias `acumulada[janela:]` e `acumulada[:-janela]` produziam `n - janela` médias, e a média da primeira janela ficava de fora.
- **Correção:** concatenei `[0.0]` antes do `cumsum`, gerando `n + 1` posições e, portanto, `n - janela + 1` médias.
- **Por que os testes de aceitação não pegaram:** eles só verificavam o tipo e os `ValueError`, não o comprimento nem os valores.
- **Outro caso não coberto:** o valor da primeira janela. `test_media_movel_valores` cobre isso: espera `[1.5, 2.5, 3.5, 4.5]`, e o código original devolve `[2.5, 3.5, 4.5]`.

## Marco 2

### Ambiente

```
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.5 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3489 
```

### R8 — Derivada numérica

De h = 1 até 1e-5 domina o erro de truncamento da diferença finita, proporcional a h: o erro cai 10x a cada passo (1,66e-5 em h = 1 até 6,2e-10 em h = 1e-5, o mínimo). Abaixo disso domina o erro de arredondamento: f(c+h) e f(c) ficam quase iguais, a subtração cancela os dígitos e a divisão por um h pequeno amplifica o ruído (2,6e-3 em h = 1e-11). Em h = 1e-14, `1000 + 1e-14 == 1000` retorna `True` (o passo entre números vizinhos perto de 1000 é cerca de 1e-13), então f(c+h) == f(c), a derivada numérica dá 0 e o erro é a própria derivada exata, 0,2134 kPa/contagem.

### R9 — Issue #7

Testes de regressão: `test_total_exato` e `test_kahan_e_ingenuo` (classe `TestAcumuladorKahan`). Antes da
correção os dois falhavam: o total dava 100000.00000133288, com erro de 1,33e-6, igual ao do ingênuo.
Causa: `t` já é o `float` arredondado de `s + y`; recalcular `s + y` repete a mesma operação com os
mesmos operandos e d git config --global user.email "you@example.com"á o mesmo `t`, então `t - (s + y)` é `t - t = 0` e a correção nunca guarda o
resíduo. Em aritmética exata `t - (s + y)` e `(t - s) - y` valem o mesmo, mas em ponto flutuante só
`(t - s) - y` recupera o que o arredondamento descartou. Os testes de aceitação somam só 10 parcelas de
0,1 e comparam com `math.isclose` (tolerância relativa 1e-9): nesse tamanho o erro do ingênuo é da
ordem de 1e-16, então o defeito passa despercebido e só aparece com muitas parcelas.

### R10 — Precisão × exatidão

Precisão é o quanto as leituras se agrupam (o desvio) e exatidão é o quanto a média chega perto do
valor verdadeiro (o viés). Em PT102 o desvio é praticamente o mesmo nas duas curvas (0,557 na linear e
0,558 na spline), então a precisão é igual; o viés, porém, é -1,841 kPa na linear (média 378,2) e
-0,012 kPa na spline (média 380,0), ou seja, a spline é muito mais exata. Tirar a média de quase 600
leituras só reduz o erro aleatório (erro padrão ≈ 0,557/√595 ≈ 0,02 kPa), mas o viés da linear vem de
um erro sistemático do modelo da curva, que desloca todas as leituras no mesmo sentido e não se
cancela na média. Esse viés de 1,84 kPa é maior que a incerteza declarada de ±1,5, que vem da
`u_sistematica` e não enxerga o erro da curva.

## Marco 3

### R11 — Bissecção × Newton

A bissecção realiza sempre 44 iterações porque a quantidade depende da largura do intervalo inicial e da tolerância, que permanecem iguais para os três números de Reynolds. A ordem de convergência 2 significa que o erro seguinte é aproximadamente proporcional ao quadrado do erro atual, fazendo com que os dígitos corretos dobrem a cada iteração. O Newton pode falhar quando a derivada é nula na aproximação inicial, como em \(f(x)=x^3+0.1\), partindo de \(x_0=0\). Nesse caso, a bissecção ainda consegue encontrar a raiz no intervalo \([-1,1]\), pois há troca de sinal nos extremos.

### R12 — Issue #9

Testes de regressão: `test_recalcula_derivada_analitica` e `test_convergencia_com_derivada_numerica` (classe `TestRegressaoNewton`). Calcular a derivada apenas uma vez mantém o denominador fixo nas iterações, fazendo o método apresentar convergência linear, em vez de quadrática. Ao recalcular a derivada em cada aproximação, recuperamos a convergência quadrática, na qual o erro aproximadamente se eleva ao quadrado a cada iteração. Os testes de aceitação não detectaram o defeito porque verificavam a precisão do resultado, mas não a quantidade de iterações nem o recálculo da derivada.

## Marco 4

### R13 — Integração e descontinuidade

Integrar o custo do dia de uma vez atravessa as mudanças bruscas de tarifa (18 h e 21 h), violando a hipótese de suavidade das regras e reduzindo a ordem observada para aproximadamente 1. Ao integrar cada faixa separadamente, a tarifa fica constante e o integrando é suave em cada intervalo; assim, o trapézio recupera ordem 2 e Simpson, ordem 4.

### R14 — Issue #11

Testes de regressão: `test_integral_de_funcao_linear_em_malha_irregular` e `test_integral_de_funcao_quadratica_em_malha_irregular` (classe `TestIntegracaoTrapezioMalhaIrregular`). O defeito era usar uma única largura entre pontos, embora as falhas do SCADA gerassem uma malha não uniforme. Os testes de aceitação não o detectaram porque não cobria o caso em que o espaçamento é irregular; Simpson não serve porque exige espaçamento uniforme, enquanto o registro do SCADA possui intervalos de 15 ou 30 minutos devido às 8 leituras perdidas.
