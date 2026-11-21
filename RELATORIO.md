# Relatório — Aylan da Silva Reis (3468)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

Trabalhei no Windows, com PowerShell e venv (`$HOME\venvs\prog2-venv`). No lugar de `which python`, usei
`(Get-Command python).Source`, visto que esse comando não existe no Windows:

    C:\Users\Aylan\venvs\prog2-venv\Scripts\python.exe

Etapa 0 do `python marco1.py`:

    === Etapa 0: ambiente ===
    Python 3.13.13 | NumPy 2.5.4 | fornecido 4.0

### R1 — Expressões regulares

Com o padrão de tag `[A-Z]{1,2}\d{1,3}`, a string `"PT1010"` é aceita por `re.match`, que só exige que o começo
da string case com o padrão, mas é rejeitada por `re.fullmatch`, que exige que a string inteira case.
Se `valida_tag` usasse `match`, aceitaria tags inválidas com sobra no fim, como `"PT1010"` (um dígito a mais) ou
`"PT101 "` (um espaço no fim), e assim o teste de aceitação de tags inválidas falharia.

### R2 — Linhas inválidas

Devolver as linhas descartadas permite contabilizar e observar cada uma delas, em vez de perder a informação. No log, 2 das
4 linhas inválidas eram `### falha de comunicacao com a RTU ###`. Se a comunicação com a RTU começasse a falhar
muitas vezes, descartar os dados deixaria ocultos possíveis problemas: o software continuaria mostrando dados como se tudo
estivesse normal, mesmo com danos sérios no resultado. Uma linha truncada (como `2026-10-05 08:20:4`) também poderia ser um
alarme perdido, e somente a contagem de inválidas mostraria que algo foi descartado.

### R3 — Late binding

Na compreensão `{tag: (lambda c: c * k) ...}`, a lambda não guarda o valor de `k`: ela anota só o nome da variável e
procura o valor quando é chamada. Nesse momento, a compreensão já terminou, e `k` ficou com o último fator do
dicionário (0,1, do FT201); por isso, `errados["PT102"](4095)` dá 4095 × 0,1 = 409,5. Na minha `criar_conversores`,
uso `lambda c, f=fator: c * f`: o argumento padrão é avaliado quando cada lambda é criada,
então cada uma guarda o fator da própria tag (PT102 dá 600,0).

### R4 — Escala nominal

Na escala nominal, supomos que o transmissor de pressão é linear (uma reta, c × 600 / 4095), mas isso não é verdade.
A explicação está em `fornecido/simulador.py`, na função `p_real`: a pressão real é 600 · sen(π/2 · c/4095).
As duas curvas coincidem em 0 e em 4095, mas no meio a reta fica abaixo do seno.
Para a média de 1791 contagens, a reta dá ≈ 262 kPa e o seno dá ≈ 380 kPa, igual ao valor de conferência.
O log é gerado com `c_real`, a inversa de `p_real` (com arcsen), e a `tabela_calibracao` indica que a correção virá
por calibração: poderemos usar pontos conhecidos para construir uma conversão, sem depender da reta.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: d836e4a

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ≈ 18 | 18,0 |
| Tempo do laço / tempo vetorizado | ≈ 100 | 27,3 |
| Tempo da compreensão / tempo do laço | ≈ 0,8 | 0,79 |

A maior diferença foi no vetorizado: previ ~100x e medi 27,3x (em outra execução, 20,9x).
A conversão `c * 600 / 4095` cria arrays temporários de 1 milhão de floats (8 MB cada),
e esse custo de memória pesa no tempo. O `uint16` guarda de 0 a 65535; 4095 × 20 = 81900 não cabe e
"dá a volta": o resultado é 81900 − 65536 = 16364, sem aviso. Para contagens (0 a 4095), usaria `uint16`
(2 bytes, 18x menos memória que a lista), convertendo para float antes das contas; para kPa, `float64`,
pois as pressões têm casas decimais e precisam de um tipo de ponto flutuante.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

O único que surpreendeu foi `s.sum()` devolver `SerieTemporal`, e não um número. A soma é uma redução do NumPy,
e o resultado passa pelo mecanismo que preserva a subclasse: vira uma `SerieTemporal` de zero dimensões. Já `s[0]`
acessa um único elemento diretamente e devolve um escalar `float64`. Sabendo disso, no `marco1.py`, usei `float(...)`
para imprimir médias e mínimos.

### R7 — Issue #4

Sintoma: a média móvel de 30 pontos sobre 600 leituras devolvia 570 valores, e não 571 (n − janela + 1).
Testes de regressão: `test_tamanho`, `test_primeiro_valor` e `test_janela_max`.
Causa: com a soma acumulada S, a soma da janela que começa em i é S[i+j−1] − S[i−1]; para i = 0, é preciso S[−1] = 0,
que não existia, então `acumulada[j:] - acumulada[:-j]` começava na segunda janela e perdia a primeira.
Correção: colocar um 0 no início da soma acumulada (`np.concatenate`) e usar `.view(type(self))` para manter o tipo.
Os testes de aceitação só verificavam o tipo e os erros, não o tamanho nem os valores. Eles também não cobrem a
janela igual ao tamanho da série (o código antigo devolvia vazio), caso coberto pelo meu `test_janela_max`.

## Marco 2

### Ambiente

Saída da Etapa 0 do `python marco2.py` (Windows/PowerShell, mesmo venv do Marco 1):

    === Etapa 0: ambiente ===
    Python 3.13.13 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3468

### R8 — Derivada numérica

Para h grande, domina o erro de truncamento: pela série de Taylor, ele é proporcional a h; na tabela, nas 4 primeiras
linhas, o erro cai cerca de 10 vezes a cada passo. Para h pequeno, domina o erro de arredondamento: f(x+h) e f(x) são
muito próximos (cerca de 225 kPa), a subtração perde algarismos significativos e o erro, da ordem de ε·|f|/h (com
ε ≈ 2,2e-16, o épsilon da máquina), cresce quando h diminui. O mínimo ficou em h = 1e-5 (erro de 6,2e-10).
Em h = 1e-14, `1000 + 1e-14 == 1000` é verdadeiro, pois x + h é igual a x em ponto flutuante: o numerador dá zero,
a estimativa da derivada dá zero e o erro é a própria derivada (0,2134).

### R9 — Issue #7

Testes de regressão: `test_dez_decimos` (10 × 0,1 deve dar 1,0; o código antigo dava `0.9999999999999999`) e
`test_comparacao_kahan_ingenuo` (o erro do Kahan deve ser menor que o do ingênuo; os dois davam 1,88e-8).
Motivo: t já é o resultado arredondado de soma + y; a expressão `t − (soma + y)` refaz a mesma conta, obtém o mesmo
valor arredondado e dá t − t = 0, então a correção nunca era guardada. Na matemática, (t − soma) − y = t − (soma + y),
mas, em ponto flutuante, t − soma mede o que de fato entrou na soma, e subtrair y isola o que se perdeu.
Os testes de aceitação não capturaram o defeito porque o `test_acumuladores` passou com o código antigo, em que o
Kahan se comportava como a soma ingênua: ele não usa nenhum caso em que a soma ingênua erra além da sua tolerância
e, por isso, não distingue um Kahan que compensa de um que não compensa.

### R10 — Precisão × exatidão

Precisão é o quanto as leituras se espalham (desvio). Exatidão é o quanto a média se aproxima do valor verdadeiro (viés).
Para PT102, as duas curvas têm a mesma precisão (desvio de 0,527 e 0,528 kPa),
mas a spline é exata (380,0 kPa, viés 0,000) e a linear não (378,2 kPa, viés −1,830).
A média de ~595 leituras reduz o erro aleatório (o erro padrão fica em torno de 0,527/√595 ≈ 0,02 kPa),
mas o viés da linear é sistemático: vem do erro de interpolação da curva (até 2,88 kPa na Etapa 1(a)),
que é o mesmo em todas as leituras próximas de 1790 contagens e, por isso, não se cancela na média.

## Marco 3

### R11 — Bissecção × Newton

A bissecção divide o intervalo ao meio a cada iteração, usando apenas o sinal de f (e não o tamanho dos valores); por
isso, a quantidade de iterações depende somente da largura inicial do intervalo e da tolerância (≈ log2((b − a)/tol)).
Como esses dois são os mesmos para todos os Reynolds da Etapa 2(a), a bissecção gasta sempre 44 iterações.
Ordem de convergência 2 significa e_{k+1} ≈ C·e_k²: em Re = 10⁴, os erros do Newton foram 2,9 → 5,0e-2 → 2,3e-5 → 5,0e-12,
e o expoente quase dobra a cada passo (o número de dígitos corretos dobra); a ordem estimada foi 2,00.
O Newton falha quando a derivada é nula ou muito pequena, ou quando o passo sai do intervalo. Aqui, a curva da bomba
não extrapola, e um passo para fora de [0, 100] L/s interromperia o Newton, enquanto a bissecção fica sempre dentro
do intervalo, com a troca de sinal garantida.

### R12 — Issue #9

Testes de regressão: `test_iteracoes_raiz_de_2` (no máximo 5 iterações para √2; o código antigo gastava 8)
e `test_erro_apos_tres_iteracoes` (erro menor que 1e-10 após 3 iterações; o antigo ainda errava 7,9e-6).
Com a derivada fixa d = f'(x₀), x_{k+1} = x_k − f(x_k)/d dá e_{k+1} ≈ (1 − f'(r)/d)·e_k:
o erro é multiplicado por uma constante, e a convergência é linear (para √2, o fator é próximo de 0,057).
Recalculando f'(x_k) a cada passo, esse fator vai a zero e e_{k+1} ≈ C·e_k².
Em Re = 10⁴, o Newton passou de 10 para 5 iterações. Os testes de aceitação não capturaram o defeito porque ele não
muda a raiz encontrada, só a velocidade: o `test_metodos_de_raiz` passou com o código antigo, pois não confere o
número de iterações nem a rapidez da queda do erro.

## Marco 4

### R13 — Integração e descontinuidade

As ordens 2 (trapézio) e 4 (Simpson) valem para integrandos suaves: o erro vem das derivadas da função, que
precisam existir e ser limitadas no intervalo. O custo tem a tarifa descontínua em 18 h e 21 h; integrando o dia de
uma vez, com n subintervalos iguais, o salto cai no meio de um subintervalo, e esse único subintervalo erra uma
quantidade proporcional a h. Esse erro O(h) domina, e a ordem observada cai para 1,00 no trapézio e 0,65 no
Simpson. Integrando cada faixa separadamente, a tarifa é constante dentro de cada uma, o integrando volta a ser
suave e as ordens voltam a 2,00 e 4,00.

### R14 — Issue #11

Testes de regressão: `test_constante_malha_irregular` (a integral de 1 com pontos 0, 1 e 3 deve dar 3; o código
antigo dava 2) e `test_linear_malha_irregular` (a de x com pontos 0, 2 e 3 deve dar 4,5; o antigo dava 7). Causa:
`integrar_tabela` usava a largura do primeiro intervalo, x[1] − x[0], para todos os trapézios; com leituras
perdidas, há intervalos de 15 e de 30 min, e o volume do dia deu 7103 m³ contra 3888 m³ (com a correção,
3885,1 m³). O `test_integradores` passou com o código antigo, ou seja, não usa uma tabela com espaçamento não
uniforme, o único caso em que o defeito aparece. O Simpson não serve porque exige pontos igualmente espaçados.