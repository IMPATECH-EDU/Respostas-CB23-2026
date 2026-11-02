# Relatório — Mickael Eleakim dos Santos Oliveira Almeida (3492)

Relatório do projeto, preenchido na branch do aluno. Cada marco acrescenta a sua seção.

## Marco 1

### Ambiente

`which python`: `/home/al.mickael.eleakim/venvs/prog2-venv/bin/python`

Etapa 0 de `python marco1.py`: `Python 3.14.4 | NumPy 2.3.5 | fornecido 4.0`.

### R1 — Expressões regulares

A string `PT1010` é aceita por `re.match(r"[A-Z]{1,2}\d{1,3}", ...)`, pois `match` só precisa encontrar um prefixo compatível (`PT101`). `re.fullmatch` rejeita a string porque sobra um quarto dígito. Se `valida_tag` usasse `match`, aceitaria incorretamente essa tag inválida.

### R2 — Linhas inválidas

`ler_log` devolve as linhas descartadas, exatamente como apareceram, para que os erros possam ser investigados e contabilizados; linhas vazias são ignoradas. Por exemplo, se uma falha de comunicação truncar mensagens do transmissor PT102, descartá-las silenciosamente esconderia uma falha da RTU e dificultaria perceber que faltam leituras.

### R3 — Late binding

As lambdas de `errados` fecham sobre a variável `k`, que é consultada quando a função é chamada, e não quando é criada. Ao fim do laço, `k` vale `0,1`, o fator de `FT201`; por isso `errados["PT102"](4095)` resulta em `409,5`. Em `criar_conversores`, o argumento padrão `fator=escalas[tag]` guarda o fator correspondente a cada tag no momento da criação da lambda.

### R4 — Escala nominal

A conversão nominal `c * 600 / 4095` pressupõe uma relação linear entre contagens e pressão, mas o simulador modela o transmissor de forma não linear. Em `fornecido/simulador.py`, `p_real(c)` usa `600 * sin(0.5 * pi * c / 4095)` e `c_real(p)` usa a inversa com `arcsin`; assim, contagens próximas de 1790 correspondem a 380 kPa verdadeiros, mas a escala linear indica cerca de 262 kPa.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: `9ed72f0`.

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ≈ 18× (cerca de 36 MB contra 2 MB) | 18,0× (36.000.056 B / 2.000.000 B) |
| Tempo do laço / tempo vetorizado | ≈ 30 a 40× (laço perto de 0,1 s; vetorizado perto de 3 ms) | 63,1× (37,8 ms / 0,6 ms) |
| Tempo da compreensão / tempo do laço | ≈ 0,8× (compreensão um pouco mais rápida) | ≈ 0,89× (33,6 ms / 37,8 ms) |

A maior diferença foi a aceleração do método vetorizado: 63,1× em vez dos 30–40× previstos. Nesta execução, tanto o laço (37,8 ms, abaixo de 0,1 s) quanto a operação vetorizada (0,6 ms, abaixo de 3 ms) demoraram menos que o estimado; os tempos também variam com a máquina, as versões das bibliotecas e a carga do sistema. `uint16` representa valores de 0 a 65.535: como `4095 * 20 = 81.900`, o resultado sofre redução módulo `2^16` e vira 16.364; inteiros Python não têm esse overflow fixo. Escolheria `uint16` para contagens de 0 a 4095, por ocupar 2 bytes, e `float64` para pressões em kPa, para preservar precisão nas conversões e estatísticas.

### R6 — Tipos da `SerieTemporal` (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `SerieTemporal` (0-d, a subclasse costuma ser mantida) | `SerieTemporal` |
| `s[0]` | `np.float64` | `float64` |

O resultado mais surpreendente é `s.sum()`: embora a soma reduza a série a um único valor, o NumPy mantém a subclasse e devolve um objeto `SerieTemporal` de dimensão zero. Já `s[0]` é um escalar NumPy (`float64`), não uma série.

### R7 — Issue #4

Com 600 leituras e janela 30, `media_movel` devolvia 570 valores, mas o contrato exige `600 - 30 + 1 = 571`. O teste de regressão `test_tamanho_com_600_leituras_e_janela_30` verifica esse tamanho; também cobri o caso-limite em `test_janela_igual_ao_tamanho_da_serie`. A versão defeituosa subtraía `acumulada[:-janela]` de `acumulada[janela:]`, deixando de calcular a primeira janela; corrigi os índices para começar em `acumulada[janela-1:]` e acrescentei zero ao início do vetor de somas acumuladas deslocado. Os testes de aceitação só verificavam o tipo de retorno e as janelas inválidas, não o comprimento nem os valores calculados; `test_primeiro_valor_e_a_media_dos_primeiros_pontos` também verifica as médias esperadas, e `test_janela_1_devolve_a_propria_serie` cobre a janela 1.

## Marco 2

### Ambiente

`Python 3.13.15 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3492`

### R8 — Derivada numérica

O erro cai de `1.658e-05` (`h=1`) até `6.224e-10` (`h=1e-5`) porque o erro de truncamento da diferença adiante diminui com `h`.
Para passos ainda menores, o arredondamento de ponto flutuante e o cancelamento numérico dominam, fazendo o erro crescer.
Em `h=1e-14`, `1000 + 1e-14 == 1000`; a diferença adiante fica zero e o erro absoluto é `|0 - 0.213432888873|`, igual à derivada exata.

### R9 — Issue #7

Os testes de regressão são `test_um_milhao_de_pulsos` e `test_erro_do_kahan_e_bem_menor_que_o_do_ingenuo`.
Como `t = s + y`, `t - (s + y)` repete a mesma soma arredondada e subtrai valores iguais, resultando em zero; `(t - s) - y` preserva a informação do arredondamento.
Os testes de aceitação somavam apenas dez parcelas de `0.1`, caso em que `math.isclose` aceita o resultado; eles não revelavam o erro acumulado em somas longas.

### R10 — Precisão × exatidão

Para PT102, os desvios são quase iguais: `0.541 kPa` (linear) e `0.543 kPa` (spline), indicando dispersão e precisão semelhantes.
Os vieses diferem: `-1.841 kPa` na curva linear e `-0.011 kPa` na spline; a média spline (`380.0 kPa`) fica muito mais próxima do valor verdadeiro do que a linear (`378.2 kPa`).
Mesmo com 595 leituras válidas, a média reduz a variação aleatória, mas não elimina o viés sistemático causado pela curva linear.

## Marco 3

### R11 — Bissecção × Newton

A bissecção usa sempre o intervalo `[2, 15]` e tolerância `1e-12` para resolver Colebrook; como reduz a largura pela metade a cada iteração, precisa de 44 iterações, independentemente de `Re`.
Newton precisou de 5, 4 e 3 iterações para `Re = 10⁴`, `10⁵` e `10⁶`, com ordens estimadas de `2.00`, `1.98` e `2.00`.
Ordem 2 significa que, perto da raiz, o erro seguinte é aproximadamente proporcional ao quadrado do erro atual, fazendo os dígitos corretos tenderem a dobrar a cada iteração.
Por exemplo, para `f(x) = x³` em `[-1, 1]`, Newton começa em `x = 0` e falha porque `f′(0) = 0`; a bissecção encontra a raiz `0` imediatamente.

### R12 — Issue #9

Os testes de regressão são `test_newton_recalcula_derivada` e `test_newton_converge_em_poucas_iteracoes`.
Calcular a derivada apenas no ponto inicial mantém a inclinação fixa nas iterações seguintes; em geral, isso perde a convergência quadrática de Newton e resulta em convergência linear perto da raiz.
Os testes de aceitação verificavam principalmente a correção da raiz/fator calculado, mas não impunham um limite de iterações nem verificavam a ordem de convergência, então o resultado correto escondia a lentidão.

## Marco 4

### R13 — Integração e descontinuidade

Na Etapa 1(b), o custo integrado de uma vez atravessa os saltos da tarifa às 18 h e às 21 h, deixando o integrando descontínuo; por isso a ordem observada cai para 1,00 no trapézio e 0,65 no Simpson.
Separando a integral por faixa tarifária, cada trecho tem tarifa constante e os saltos ficam nos limites dos trechos. Assim, as ordens voltam a 2,00 para o trapézio e 4,00 para Simpson.
Para `n = 110`, os erros por faixa foram `6.3e-04` (trapézio) e `8.1e-08` (Simpson).

### R14 — Issue #11

Os testes de regressão são `test_exato_para_afim_com_tabela_irregular` e `test_exato_para_constante_com_tabela_irregular`; ambos verificam integrais conhecidas em malhas irregulares.
O defeito usava apenas o primeiro passo, `x[1] - x[0]`, para todos os trapézios. A correção usa a largura individual de cada intervalo, `np.diff(x)`, e soma as áreas correspondentes.
Os testes de aceitação usavam malhas uniformes (`np.linspace` ou intervalos de 1,5 h), nas quais todos os passos são iguais; por isso não revelavam o defeito.
O registro real tem 89 leituras para 97 esperadas e intervalos de 15, 30 e 45 minutos. Simpson exige pontos igualmente espaçados, então não serve para essa tabela irregular e corretamente levanta `ValueError`.
