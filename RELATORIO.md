# Relatório — Matheus Ferreira Lucena (3548)

## Marco 1

### Ambiente

/home/matheus/venvs/prog2-venv/bin/python
=== Etapa 0: ambiente ===
Python 3.13.13 | NumPy 2.5.3 | fornecido 1.0

### R1 — Expressões regulares

`re.match` aceita o prefixo `PT101` da string `PT1010`, enquanto `re.fullmatch` rejeita a string inteira; caso `valida_tag` usasse `match`, consideraria válida uma entrada que tem caracteres excedentes.


### R2 — Linhas inválidas

Devolver linhas descartadas possibilita a contagem de falhas e a investigação de sua origem a partir do conteúdo original.
Por exemplo, uma falha de comunicação com a RTU poderia interromper as leituras de pressão de PT102; ignorar essas linhas esconderia a perda de monitoramento da estação.

### R3 — Late binding

As lambdas de `errados` consultam `k` quando são chamadas. Ao terminar a compreensão, essa variável contém o fator 0.1, por isso retorna 409,5 que é resultado de `4095 * 0.1`.
Em `criar_conversores`, `fator=fator` é avaliado na criação de cada lambda, preservando o fator da tag.

### R4 — Escala nominal

Uma hipótese inicial seria que a escala nominal não representa a resposta real do transmissor.
Em `fornecido/simulador.py`, encontrei `p_real(c) = 600*sin(0.5*pi*c/4095)` e sua inversa, `c_real`.
O simulador gera PT102 com essa curva, mas a conversão nominal usa a relação linear `c*600/4095`.
A diferença entre essas relações explica os aproximadamente 262 kPa nominais diante dos 380 kPa de conferência.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: d9bcd37

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 18,000028 |
| Tempo do laço / tempo vetorizado | 20 | 55,118618 |
| Tempo da compreensão / tempo do laço | 0,8 | 0,830354 |

A maior diferença foi laço/vetorizado: medi aproximadamente 55,12, contra a previsão de 20.
A execução das operações NumPy em código compilado evita a iteração Python por elemento, ajudando a explicar essa aceleração.
Em `uint16`, `4095*20 = 81900` excede os 16 bits e resulta em `81900 % 65536 = 16364`.
Escolheria `uint16` para contagens de 0 a 4095 e `float64` para representar pressões fracionárias, mantendo a precisão usada pela `SerieTemporal`.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `numpy.float64` | `SerieTemporal` |
| `s[0]` | `numpy.float64` | `float64` |

Um resultado interessante é `s.sum()`: eu previa `numpy.float64`, mas observei `SerieTemporal`.
Nesse caso, a redução herdada do NumPy conserva a subclasse, produzindo um array de dimensão zero.
Já `s[0]` devolve um escalar `numpy.float64`, exibido pelo script como `float64`.

### R7 — Issue #4

Com 600 leituras e janela 30, `media_movel` retornava 570 valores em vez de 571.
`test_media_movel_inclui_primeira_janela` detectou a ausência da primeira janela.
Faltava o zero inicial na soma acumulada, fazendo as diferenças começarem na segunda janela.
A correção insere esse zero antes de `np.cumsum` e mantém `SerieTemporal`, sem modificar `self`.
A aceitação conferia tipo, limites inválidos e imutabilidade, mas não tamanho e valores das médias.
A janela igual ao tamanho também não era coberta; `test_media_movel_janela_igual_ao_tamanho` verifica o resultado `[11.0]`.

## Marco 2

### Ambiente

```text
=== Etapa 0: ambiente ===
Python 3.13.13 | NumPy 2.5.3 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3548
```

### R8 — Derivada numérica

O erro diminuiu de 1,658e-5 em h = 1 para 6,224e-10 em h = 1e-5, quando atingiu o mínimo.
Para passos maiores, o erro de truncamento da diferença adiante dominou, na ordem de O(h).
Para menores, o arredondamento e o cancelamento na subtração de valores próximos dominam e a divisão por h amplifica o erro.
Em h = 1e-14, `1000 + 1e-14 == 1000`: o incremento não é representável nessa escala.
As duas avaliações da spline ficam iguais, a derivada aproximada vira zero e o erro é a própria derivada que é cerca de 0,213432888873 kPa/contagem.

### R9 — Issue #7

As regressões `test_kahan_um_milhao_de_decimos` e `test_kahan_recupera_unidades_entre_valores_grandes` falharam antes da correção e passaram depois.
Como `t` já guarda a soma arredondada `s + y`, `t - (s + y)` subtrai dois resultados idênticos e zera.
Com `(t - s) - y`, a ordem das operações permite recuperar o resíduo perdido. A aritmética de ponto flutuante não é associativa.
No milhão de pulsos, a soma ingênua deu 100000,00000133288 L, com erro de aproximadamente 1,333e-6 L; Kahan deu 100000,0 L.
A aceitação somava apenas dez parcelas e usava `math.isclose`, que aceita o resultado 0,9999999999999999; por isso o defeito passava despercebido.

### R10 — Precisão × exatidão

Para PT102, os desvios foram 0,536 kPa com a curva linear e 0,537 kPa com a spline: as duas têm precisão semelhante.
Os viéses foram -1,806 kPa e +0,024 kPa, respectivamente. A spline ficou mais próxima dos 380 kPa de referência e foi mais exata.
Depois de descartar cinco espúrias, a média usa 595 leituras, o que reduz o erro aleatório da média, mas não elimina o viés da curva de calibração.
O erro da interpolação linear se repete nas conversões e permanece mesmo ao aumentar o número de leituras.

## Marco 3

### R11 — Bissecção × Newton

Nos três casos, a bissecção usa [2,15] e tol=1e-12, e a largura é 13/2^k depois de k divisões.
São necessárias 44 divisões para ficar abaixo da tolerância, independentemente do Reynolds nesses casos.
Newton usou 5, 4 e 3 iterações, com ordens estimadas 2,00, 1,98 e 2,00.
Para Re=10⁴, os erros 5,0e-2 → 2,3e-5 → 5,0e-12 ilustram e_{k+1}≈C·e_k².
Essa ordem quadrática significa aproximadamente dobrar os dígitos corretos por passo, perto da raiz.
Para x³−1 em [-2,2], Newton com df=3x² começa com derivada nula em zero. A bissecção encontra a raiz 1.

### R12 — Issue #9

As regressões são test_colebrook_converge_em_ate_seis_iteracoes
e test_ordem_quadratica_com_derivada_analitica, commitadas em 10c0db1 antes da correção 1b69838.
A derivada ficava fixa no ponto inicial, embora as aproximações mudassem a cada passo.
Em geral, isso mantém um termo linear no erro, e_{k+1}≈c·e_k, produzindo ordem próxima de 1.
Recalculá-la em cada aproximação restaurou a ordem próxima de 2 observada na execução.
A aceitação conferia os resultados finais, sem exigir rapidez nem ordem do histórico real de Newton.

## Marco 4

### R13 — Integração e descontinuidade

A tarifa tem saltos às 18h e às 21h, tornando o custo descontínuo no dia inteiro.
Nos intervalos dos saltos, o erro pode ser O(h), dominando o erro da parte suave.
Integrando de uma vez, observei ordens de 1,00 no trapézio e 0,65 em Simpson.
Por faixas, a tarifa fica constante e a potência integrada é suave, recuperando as hipóteses dos métodos, assim o trapézio voltou pra ordem 2,00 e Simpson pra ordem 4,00.
Na função suave, as ordens observadas já eram 2,01 e 4,06, próximas das teóricas.

### R14 — Issue #11

As regressões são test_trapezio_constante_malha_irregular
e test_trapezio_reta_malha_irregular, commitadas em f08882b antes da correção 9fbe756.
A fórmula antiga usava a largura do primeiro intervalo para toda a tabela.
A correção soma as áreas usando cada largura real, calculada por np.diff(x).
A aceitação usava malhas uniformes para o trapézio, nas quais o defeito não aparecia.
Simpson exige espaçamento uniforme, mas o registro tem intervalos de 15 e 30 minutos.