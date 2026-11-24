# Relatório — Felipe Brasileiro dos Santos (3508)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

Windows 11, Git Bash, ambiente `venv` em `~/venvs/prog2-venv`, criado fora do repositório.

```
$ which python
/usr/local/bin/python3

$ python marco1.py
=== Etapa 0: ambiente ===
Python 3.13.18 | NumPy 2.5.3 | fornecido 4.0
```

### R1 — Expressões regulares

Com o padrão `[A-Z]{1,2}[0-9]{1,3}`, a string `"PT1010"` passa no `re.match`, porque ele só exige
que o **começo** case: `"PT101"` casa e o `"0"` que sobra é ignorado. O `re.fullmatch` exige que a
string inteira case e rejeita. O mesmo acontece com `"PT101 "`, com o espaço no fim. Se
`valida_tag` usasse `match`, ela aceitaria tags com lixo depois do nome, e um `"PT1010"` digitado
errado seria tratado como o `PT101`, sem nenhum aviso.

### R2 — Linhas inválidas

Uma linha descartada é um dado que se perdeu, e quem usa os registros precisa saber disso para
decidir se confia no resto. No meu log foram 4 de 2408 linhas: duas falhas de comunicação com a
RTU e duas linhas truncadas (`'2026-10-05 08:03'` e `'2026-10-05 08:20:4'`). Se a RTU começasse a
falhar com frequência, um leitor que só ignorasse essas linhas continuaria devolvendo médias com
cara de normais, e ninguém perceberia que o link está caindo. Pior: uma linha truncada pode ser
justamente um `ALARME` de pressão alta que se perdeu.

### R3 — Late binding

Na compreensão `{tag: (lambda c: c * k) ...}`, a lambda não guarda o valor de `k`: ela guarda a
**variável** `k` do escopo da compreensão, e só lê o valor quando é chamada. Quando chamo
`errados["PT102"](4095)`, o laço já terminou e `k` vale o último fator, 0,1 (o do `FT201`): dá
4095 × 0,1 = 409,5. Na minha versão, cada lambda é criada dentro de `_multiplicador(fator)`. Cada
chamada tem o seu próprio escopo, e a lambda fica presa ao `fator` daquela chamada, que nunca muda
depois.

### R4 — Escala nominal

A média das contagens normais de PT102 é 1787,9. A escala nominal supõe que o transmissor é
linear (`p = c · 600/4095`) e dá 262,0 kPa, contra 380 kPa da conferência. Minha hipótese é que a
resposta do transmissor não é linear. A explicação está em `fornecido/simulador.py`, na função
`p_real`: `p = 600 · sin(π/2 · c/4095)`. Com c = 1787,9, ela dá 379,99 kPa. A reta e o seno só
coincidem nas pontas, em 0 e 4095, e no meio da faixa a reta erra mais de 100 kPa. Por isso o
Marco 2 usa uma curva de calibração.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: `HASH_DAS_PREVISOES` ("relatório: cabeçalho e previsões das tabelas R5 e R6 (antes de medir)")

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ≈ 18× (8 B do ponteiro + ≈ 28 B do `int`, contra 2 B) | 18,0× (36 000 056 B / 2 000 000 B) |
| Tempo do laço / tempo vetorizado | ≈ 50× | 23,0× (61,88 ms / 2,69 ms) |
| Tempo da compreensão / tempo do laço | ≈ 0,7 (a compreensão evita o `append`) | 0,81 (50,13 ms / 61,88 ms) |

A maior diferença foi no laço ÷ vetorizado: previ 50× e medi 23×. A versão vetorizada não é só
uma multiplicação. Ela converte o `int64` para `float64` (uma cópia de 8 MB) e cria mais dois
vetores temporários, um em `* 600` e outro em `/ 4095`. Então ela passa três vezes por 8 MB de
memória, e com 1 milhão de elementos a memória limita mais que a conta. `uint16 * 20` dá 16364
porque o NumPy mantém o resultado em `uint16`, que vai até 65535: 81900 dá a volta, e
81900 − 65536 = 16364, sem nenhum aviso. Eu guardaria as contagens em `uint16` (12 bits cabem em
2 B), convertendo para `float64` antes de qualquer conta, e as pressões em kPa em `float64`.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float` | `SerieTemporal` (0-d) |
| `s[0]` | `float` | `float64` |

O que mais me surpreendeu foi `s.sum()` devolver uma `SerieTemporal`, e não um número. A redução
passa pelo mecanismo de subclasse do NumPy, que embrulha o resultado no tipo de `s`, e sai um
array de **dimensão zero** (`ndim == 0`) que ainda é `SerieTemporal`. Já `s[0]` devolve
`np.float64`, um escalar do NumPy, e não o `float` do Python que eu previa. Por isso
`amplitude()` faz `float(...)`, e no `marco1.py` eu converto com `float(s.mean())` antes de
imprimir ou comparar.

### R7 — Issue #4

**Sintoma:** `media_movel(30)` em 600 pontos devolvia 570 valores, e não 571. **Testes**
(`TestRegressaoMediaMovel`): `test_tamanho_do_caso_relatado`,
`test_primeira_media_e_a_da_primeira_janela`, `test_janela_do_tamanho_da_serie` e
`test_janela_um_devolve_a_propria_serie`. Os quatro falhavam antes da correção. **Causa:** com
`S = cumsum(x)`, a soma de `x[i..i+w-1]` é `S[i+w-1] − S[i-1]`, com `S[-1] = 0`. O código fazia
`S[w:] − S[:-w]`, que é a soma de `x[i+1..i+w]`: ele começa na **segunda** janela e perde a
primeira. **Correção:** `S[w-1:] − concatenate([0], S[:-w])`. A aceitação só testava o tipo e os
`ValueError`, nunca o tamanho nem os valores. Ela também não cobre `janela == len(s)`, que deveria
dar um valor e dava zero: é o meu `test_janela_do_tamanho_da_serie`.

## Marco 2

### Ambiente

```
$ python marco2.py
=== Etapa 0: ambiente ===
Python 3.13.18 | NumPy 2.5.3 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3508
```

### R8 — Derivada numérica

De h = 1 até h = 1e-5, o erro cai 10 vezes a cada década (1,7e-5, 1,7e-6, ..., 6,2e-10). Nessa
faixa domina o **erro de truncamento** da diferença adiante, proporcional a h (≈ h·|f''|/2). Abaixo
de 1e-5, domina o **erro de arredondamento**: f(x+h) e f(x) (≈ 225 kPa) ficam quase iguais, a
subtração cancela os dígitos e sobra um erro da ordem de ε·|f|/h, que cresce quando h diminui (em
h = 1e-10 já é 3e-4). Em h = 1e-14, `1000 + 1e-14 == 1000` é `True`, porque o espaçamento entre
doubles perto de 1000 é 1,1e-13. Então f(x+h) − f(x) = 0, a aproximação dá 0, e o erro é a própria
derivada: 0,2134 kPa/contagem.

### R9 — Issue #7

Testes de regressão (`TestRegressaoKahan`): `test_milhao_de_pulsos_da_exatamente_cem_mil`,
`test_parcelas_menores_que_o_espacamento_nao_somem`, `test_dez_decimos_dao_um` e
`test_erro_muito_menor_que_o_da_soma_ingenua`. Os quatro falhavam antes da correção. A causa: `t` já
é `fl(s + y)`, e `t - (s + y)` calcula **de novo** a mesma soma arredondada. Dá `t - t = 0`, e a
correção nunca muda. Em `(t - s) - y`, a subtração `t - s` é exata e devolve a parte de y que
realmente entrou na soma. Tirando y, sobra o que se perdeu. As duas formas só são iguais na
álgebra, porque em ponto flutuante a ordem das contas muda o arredondamento. A aceitação somava dez
décimos e comparava com `math.isclose` (tolerância 1e-9), que aceita 0,9999999999999999.

### R10 — Precisão × exatidão

Para PT102, a linear dá 378,2 kPa, com desvio 0,508 e viés −1,844 kPa. A spline dá 380,0 kPa, com
desvio 0,510 e viés −0,015 kPa. **Precisão** é o quanto as leituras repetidas concordam entre si
(o desvio), e as duas curvas têm a mesma precisão, porque o ruído vem do transmissor, não da curva.
**Exatidão** é a distância até o valor verdadeiro (o viés), e aí a linear perde: entre os nós da
tabela, a reta fica abaixo do seno, que é côncavo, e **toda** leitura sai deslocada para baixo. A
média de 595 leituras reduz o erro aleatório (o erro padrão é 0,508/√595 ≈ 0,021 kPa), mas um erro
que é igual em todas as leituras não se cancela na média: o viés continua lá, quase 90 vezes maior.

## Marco 3

### R11 — Bissecção × Newton

A bissecção não olha para os valores de f, só para o **sinal**. Cada iteração corta o intervalo ao
meio, então depois de k iterações a largura é 13/2^k, a partir de [2, 15]. Ela para quando
13/2^k < 1e-12, isto é, k > log2(1,3e13) ≈ 43,6. São sempre 44 iterações, qualquer que seja o
Reynolds. Ordem 2 quer dizer e_(k+1) ≈ C·e_k², e o número de dígitos corretos dobra a cada passo.
Em Re = 1e4, os erros do Newton foram 5,0e-2, 2,3e-5 e 5,0e-12 (2, 5 e 11 dígitos), e a ordem
estimada foi 2,00. O Newton falha quando a derivada é nula ou muito pequena perto do chute
(divide por zero ou dá um salto enorme). Testei `Newton().encontrar(math.atan, -1, 5)`: começando
em x0 = 2, ele oscila cada vez mais longe, até x ≈ −1,4e10, e para com "derivada nula". A
bissecção no mesmo intervalo acha 0, porque só precisa da troca de sinal.

### R12 — Issue #9

Testes de regressão (`TestRegressaoNewton`): `test_colebrook_re_1e4_em_poucas_iteracoes`,
`test_derivada_exata_tambem_e_reavaliada` e `test_erro_novo_limitado_pelo_quadrado_do_anterior`. Os
três falhavam antes da correção. Com a derivada d0 fixa no ponto inicial, o passo é
`x − f(x)/d0`, e perto da raiz o erro vira e_(k+1) ≈ (1 − f'(r)/d0)·e_k. Esse fator é **constante**,
então a convergência é linear. No relato, o erro caía sempre ≈ 26 vezes (5,0e-2, 1,9e-3, 7,6e-5,
2,9e-6), e por isso foram 10 iterações. Recalculando f'(x_k), o fator vai a zero junto com e_k, e
sai e_(k+1) ∝ e_k². A aceitação só conferia que o método converge para a raiz certa, e o método
da corda também converge, só que mais devagar: ninguém olhava o número de iterações nem a ordem.

## Marco 4

### R13 — Integração e descontinuidade

As ordens 2 e 4 vêm de fórmulas de erro que supõem o integrando suave, com derivadas limitadas,
em cada subintervalo. A tarifa salta de 0,50 para 1,50 às 18 h e volta às 21 h. Com n = 30, 50, 70,
90 e 110 em [0, 24], 18 h e 21 h nunca caem num nó, porque n não é múltiplo de 4. O subintervalo
que contém o salto é aproximado por uma reta (no trapézio) ou por uma parábola (no Simpson) que não
consegue representar o degrau. O erro desse trecho é proporcional a (salto × h), ou seja, O(h), e
ele domina tudo. Medi ordem 1,00 no trapézio e 0,65 no Simpson: o Simpson é mais irregular porque
a constante muda conforme a posição do salto dentro do par de subintervalos. Por faixa, cada
integral é de uma função suave, com os limites nos nós, e voltam 2,00 e 4,00 (erro 6,3e-4 e
8,1e-8 em n = 110).

### R14 — Issue #11

Testes de regressão (`TestRegressaoTrapezioTabela`): `test_reta_em_malha_irregular`,
`test_vazao_constante_no_registro_com_falhas` e `test_tirar_um_ponto_de_uma_reta_nao_muda_nada`. Os
três falhavam antes da correção. A causa: `integrar_tabela` usava `h = x[1] − x[0]` (15 min) em
toda a tabela. Com 8 leituras perdidas, os intervalos de 30 e 45 min entravam como se fossem de
15, e o volume saía 3545,0 m³ contra 3888,0 (−8,82%). Corrigido, deu 3886,0 m³ (0,05%). Os testes
de aceitação só usavam malhas **uniformes** (`linspace`, passo de 1,5 h), em que `x[1] − x[0]`
coincide com todos os passos. O Simpson não serve para o registro do dia porque ajusta uma parábola
a cada **par** de subintervalos iguais: exige malha uniforme e número ímpar de pontos. O registro
tem 89 pontos e passos de 15, 30 e 45 min, e a regra recusa.
