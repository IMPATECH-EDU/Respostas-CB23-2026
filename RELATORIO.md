# Relatório — Adrian (3505)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

Ambiente virtual existente fora do repositório, ativado com `source ~/venvs/prog2-venv/bin/activate`.
Execução da revisão em 10/11/2026, com matrícula 3505:

```text
$ which python
/home/adrian/venvs/prog2-venv/bin/python
=== Etapa 0: ambiente ===
Python 3.11.2 | NumPy 2.4.6 | fornecido 4.0
```
### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
A string "PT101 " é aceita por TAG.match(), pois seu início corresponde ao padrão [A-Z]{1,2}\d{1,3}. Entretanto, TAG.fullmatch() a rejeita porque há um espaço ao final. Se a função valida_tag() utilizasse match() em vez de fullmatch(), poderia aceitar tags inválidas com caracteres adicionais, contrariando o contrato da função
### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
ler_log devolve as linhas descartadas para permitir identificar e investigar erros nos registros, sem perder informações sobre as falhas. Por exemplo, uma falha de comunicação com a RTU poderia produzir registros truncados. Descartá-los silenciosamente esconderia a ocorrência do problema e poderia comprometer a confiabilidade da análise dos dados da estação

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Na versão errada, as lambdas consultam a variável k quando são executadas, após o término da compreensão. Como o último fator é 0.1, todas utilizam esse valor, produzindo 4095 * 0.1 = 409.5. Na implementação correta, lambda c, fator=fator: c * fator captura o fator correspondente a cada tag no momento da criação da lambda, evitando o problema.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

A diferença medida entre 261,99 kPa e 380,00 kPa ocorre porque o transmissor possui uma resposta não linear, enquanto a escala nominal pressupõe linearidade. No arquivo fornecido/simulador.py, a função p_real(c) utiliza uma função seno para converter contagens em pressão, enquanto c_real(p) utiliza a função arco-seno. Portanto, o fator 600/4095 não representa adequadamente a calibração real.

### R5 — Previsão × medição (Etapa 3)

As estimativas abaixo foram propostas retrospectivamente, com auxílio de IA, após a implementação e a medição.
São hipóteses ilustrativas para discutir os resultados, não previsões registradas antes do experimento.

| Grandeza | Previsão (retrospectiva) | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 18,000028 |
| Tempo do laço / tempo vetorizado | 20 | 13,67 |
| Tempo da compreensão / tempo do laço | 0,8 | 0,924 |

Para memória, a estimativa usa 8 bytes por referência e 28 por inteiro Python neste ambiente: `(8 + 28) / 2 = 18`; a lista medida inclui ainda 56 bytes de estrutura.
As hipóteses de tempo são uma aceleração de 20 vezes com NumPy e uma redução de 20% com compreensão; são estimativas aproximadas, não garantias.
A maior diferença relativa é 13,67 contra 20 (31,65% abaixo): alocações, tráfego de memória e custo das operações podem limitar a aceleração vetorizada; esta medição não isola essas causas.
Os tempos médios de 10 repetições foram 151,275 ms (laço), 139,723 ms (compreensão), 197,182 ms (map+lambda) e 11,068 ms (vetorizado); variam entre execuções.
O cálculo `4095 * 20 = 81900` excede o limite 65535 de `uint16`; o resultado modular é `81900 - 65536 = 16364`.
Para armazenar contagens de 0 a 4095, escolheria `uint16`; para pressões em kPa, `float64`, multiplicando em ponto flutuante antes de ocorrer overflow.

### R6 — Tipos da SerieTemporal (Etapa 4d)

Hipóteses retrospectivas: aritmética e fatias preservariam a subclasse, enquanto redução e indexação devolveriam escalares.

| Expressão | Tipo previsto (retrospectivo) | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float64` | `SerieTemporal` |
| `s[0]` | `float64` | `float64` |

Essas hipóteses foram acrescentadas após a execução e não constam do histórico anterior à Etapa 4.
O resultado menos intuitivo é `s.sum()`: a redução preserva a subclasse em um array de dimensão zero, embora represente um único número.
Já `s[0]` extrai um escalar NumPy `float64`; operações aritméticas e fatias preservam `SerieTemporal`.

### R7 — Issue #4

O sintoma era obter 570 médias para 600 leituras com janela 30, em vez das 571 previstas.
`test_media_movel_600_leituras_janela_30` verifica tamanho, valores e tipo; foi incluído em `d201464`, antes da correção `88646ed`.
A soma acumulada original não incluía a soma vazia inicial, perdendo a primeira janela ao subtrair as fatias; inserir zero antes de `np.cumsum` corrige o deslocamento.
A aceitação conferia tipo, erros e imutabilidade, mas não tamanho nem valores das médias.
Ela também não cobre janela igual ao tamanho da série: `test_janela_tamanho_da_serie` exige uma média, e `test_janela_unitaria_preserva_pontos` cobre janela 1.
Na revisão, os três testes falharam com o método original de `upstream/main` e passaram com o atual; os dois últimos foram acrescentados após a correção histórica.

### Validação da revisão

- `python fornecido/simulador.py`: terminou com `simulador.py OK`.
- `python -m unittest fornecido.testes_aceitacao.test_aceitacao_m1 testes.test_dados -v`: 41 testes passaram; 15 próprios além do exemplo, incluindo 3 regressões de média móvel, 3 de reamostragem e 4 regras adicionais de leitura do log.
- `python marco1.py`: todos os asserts passaram; 2.404 registros válidos, 4 inválidos, 571 médias móveis e 60 médias por minuto.
- `git fetch upstream` e `git diff upstream/main --stat -- fornecido/`: nenhuma diferença em `fornecido/`.
- `python -m unittest discover -v`: 69 testes, com 19 erros por `NotImplementedError` nos Marcos 2–4; o Marco 1 passa integralmente. Esses marcos posteriores ainda impedem o checklist global de ficar verde.

### Pendências de processo

O histórico não cumpre a exigência de previsões em commit anterior às Etapas 3 e 4, nem a de dois testes da issue #4 escritos antes da correção: apenas um já existia nessa ordem.
Os novos testes demonstram o defeito original, mas não corrigem retroativamente essa cronologia; os commits existentes foram preservados.
Esta revisão e a complementação do relatório tiveram auxílio de IA. O aluno ainda deve ler, executar e revisar a entrega e escrever as respostas com suas próprias palavras, como exige o enunciado.

## Marco 2

### Ambiente

Execução em 10/11/2026, no mesmo ambiente virtual do Marco 1; o SciPy já estava instalado.

```text
=== Etapa 0: ambiente ===
Python 3.11.2 | NumPy 2.4.6 | SciPy 1.17.1 | fornecido 4.0 | matrícula 3505
```

### R8 — Derivada numérica

O erro caiu de 1,658e-5 em h = 1 para 6,224e-10 em h = 1e-5, o menor valor da tabela.
Nos passos maiores, domina o truncamento da diferença adiante: ela aproxima a derivada por uma secante, com erro de ordem h.
Nos passos muito pequenos, o arredondamento e a subtração de valores próximos dominam; dividir por h amplifica os erros, que voltam a crescer.
Foi confirmado que `1000 + 1e-14 == 1000`: o incremento não é representável nessa escala, e a diferença calculada é zero.
Assim, a derivada numérica é zero e o erro absoluto é o módulo da derivada exata, 0,213432888873 kPa/contagem (2,134e-1 na tabela).

### R9 — Issue #7

Os testes `test_milhao_de_decimos` e `test_parcelas_pequenas_entre_grandes` falharam antes da correção e foram registrados no commit `4b4c163`, anterior a `fd404c4`.
O primeiro encontrou 100000,00000133288 em vez de 100000,0; o segundo perdeu duas unidades entre 1e16 e -1e16, devolvendo 0,0 em vez de 2,0.
Como `t` já contém o resultado arredondado de `s + y`, recalcular `t - (s + y)` subtrai valores idênticos e zera a compensação.
Em `(t - s) - y`, a subtração recupera primeiro a parcela efetivamente somada; compará-la com y registra o arredondamento para a próxima adição, pois ponto flutuante não é associativo.
A correção alterou apenas os parênteses; ambos os testes passaram e o total de um milhão de décimos passou a 100000,0, com erro zero nessa execução.
A aceitação somava apenas dez décimos e usava `math.isclose` com tolerância padrão, que aceita o pequeno erro da soma ingênua nesse caso.

### R10 — Precisão × exatidão

Para PT102, os desvios foram 0,530 kPa (linear) e 0,531 kPa (spline): as leituras têm precisão semelhante, isto é, dispersão semelhante.
Os vieses em relação a 380 kPa foram -1,813 kPa (linear) e +0,017 kPa (spline); a spline apresentou maior exatidão, ficando mais perto da referência.
Após descartar os índices [57, 139, 288, 383, 480], restaram 595 leituras de PT102 em cada curva.
A média reduz o erro aleatório, mas não elimina o viés sistemático de interpolação da curva linear; a incerteza instrumental de 1,5 kPa também não diminui com o número de leituras.
A altura obtida com a spline foi 35,75 ± 0,22 m, compatível com a referência de 35,749 m, com incerteza relativa de 0,61%.

### Validação do Marco 2

- Os dois testes de regressão de Kahan foram executados e falharam antes da alteração em `acumuladores.py`; após a correção, ambos passaram.
- `python -m unittest fornecido.testes_aceitacao.test_aceitacao_m1 fornecido.testes_aceitacao.test_aceitacao_m2 testes.test_dados testes.test_medicao -v`: 60 testes passaram.
- `testes/test_medicao.py` contém 9 testes novos além do exemplo: 2 de Kahan e 7 de regras de medição não cobertas pela aceitação.
- `python marco1.py` e `python marco2.py`: todos os asserts passaram, com matrícula 3505.
- `git fetch upstream` seguido de `git diff upstream/main --stat -- fornecido/ marco2.py`: nenhuma diferença; `calibracao.py` também permaneceu intacto.
- `python -m unittest discover -v`: 78 testes, com 12 erros por `NotImplementedError` dos Marcos 3–4; nenhuma falha dos Marcos 1–2. O checklist global depende da implementação dos marcos posteriores.

As respostas e o código deste marco foram preparados com auxílio de IA e precisam ser lidos e revisados pelo aluno antes da entrega.

## Marco 3

### Ambiente

Execução em 10/11/2026 no ambiente virtual do projeto: Python 3.11.2, NumPy 2.4.6, SciPy 1.17.1, fornecido 4.0 e matrícula 3505.

### R11 — Bissecção × Newton

Colebrook usa sempre [2, 15] e tolerância 1e-12; reduzir a largura 13 pela metade exige 44 iterações, pois `13 / 2**44 < 1e-12`, independentemente de Reynolds nesses casos.
Newton levou 5, 4 e 3 iterações para Re = 1e4, 1e5 e 1e6, com ordens estimadas de 2,00, 1,98 e 2,00.
Ordem 2 significa que, perto de uma raiz simples, o próximo erro é aproximadamente proporcional ao quadrado do anterior, dobrando aproximadamente o número de dígitos corretos.
Em Re = 1e4, os erros caíram de 5,0e-2 para 2,3e-5 e 5,0e-12, antes de atingir o arredondamento.
Para `f(x) = x³ - 1` em [-2, 2], Newton com derivada analítica começa em zero e falha por derivada nula; a bissecção encontra a raiz 1, pois há troca de sinal e a função é contínua.

### R12 — Issue #9

Os testes `test_quadratica_com_derivada_analitica` e `test_colebrook_com_derivada_numerica` exigem convergência em até seis iterações e falharam no código original.
Eles foram registrados em `07ab873`, antes da correção `79e9908`; ambos passaram após mover o cálculo da derivada para dentro do laço de Newton.
Com a derivada fixa em d, a atualização é `x - f(x)/d`; em geral, o erro mantém o termo linear `e_n * (1 - f'(raiz)/d)`.
Recalcular a derivada em cada aproximação elimina esse termo no limite, permitindo convergência quadrática perto de uma raiz simples, com derivada suficientemente precisa.
A aceitação conferia convergência e valor final com até 100 iterações, mas não a velocidade ou a ordem; assim, a versão lenta ainda passava.

### Validação do Marco 3

- `python -m unittest fornecido.testes_aceitacao.test_aceitacao_m3 testes.test_operacao -v`: 16 testes passaram, incluindo 7 próprios além do exemplo.
- `python marco3.py`: todos os asserts passaram; com spline, o ponto foi Q = 65,089 L/s e H = 35,857 m, contra a referência Q = 64,873 L/s e H = 35,741 m.
- Para o ponto de operação, Newton levou 5 iterações e a bissecção 40, tanto com a curva linear quanto com a spline.
- Além das regressões, os testes cobrem intervalos inválidos, domínio da bomba, não convergência e filtragem pelo piso relativo dos erros.

## Marco 4

### Ambiente

Mesmo ambiente e matrícula do Marco 3; não foi necessário instalar dependências.

### R13 — Integração e descontinuidade

Ao integrar o custo de uma vez, a ordem observada foi 1,00 para o trapézio e 0,65 para Simpson; por faixas, foi 2,00 e 4,00, respectivamente.
Os saltos de tarifa às 18 h e 21 h quebram a suavidade exigida pelas estimativas de erro das regras; o erro nos subintervalos que contêm o salto pode dominar e ser proporcional ao passo.
A ordem estimada também depende do alinhamento desses saltos com a malha, por isso não precisa ser exatamente 1 na sequência de tamanhos usada.
Ao separar as faixas, a tarifa fica constante em cada integral e a potência é suave, recuperando as ordens teóricas 2 e 4.
Com n = 110 por faixa, os erros no custo foram 6,3e-4 e 8,1e-8 reais, respectivamente.

### R14 — Issue #11

Os testes `test_constante_em_malha_irregular` e `test_reta_em_malha_irregular` falharam antes da correção: retornavam 4 em vez de 6 e 38 em vez de 42.
Foram registrados em `07ab873`, antes da correção `0b06b50`; ambos passaram após usar `np.diff(x)` como larguras dos trapézios.
O código original multiplicava toda a soma pelo primeiro espaçamento, supondo que nenhuma leitura faltava; em malha irregular, cada área precisa de sua própria largura.
A aceitação só verificava o trapézio com tabela uniforme, na qual o defeito não aparece.
A implementação fornecida de Simpson exige malha uniforme e número ímpar de pontos; o registro tem 89 leituras, mas intervalos de 15 e 30 minutos, então viola a uniformidade.
O volume corrigido foi 3873,07 m³ contra 3888,00 m³ de referência, com erro de 0,38%, dentro do limite de 1,5% do script.

### Ajuste e balanço medidos

Foi usado `np.polynomial.polynomial.polyfit`: resolve o ajuste por mínimos quadrados e já fornece os coeficientes em ordem crescente, compatíveis com `polyval`.
Os ajustes de grau 2 tiveram erros máximos de 0,043 m na altura e 0,0058 no rendimento; a potência foi calculada pela função fornecida e o custo integrado separadamente em cada faixa.

| Grandeza | Calculado | Referência | Erro relativo |
| --- | --- | --- | --- |
| Volume (m³) | 3873,07 | 3888,00 | 0,38% |
| Energia (kWh) | 651,57 | 655,56 | 0,61% |
| Custo (R$) | 413,36 | 416,01 | 0,64% |

Os custos de 0–18 h, 18–21 h e 21–24 h foram R$ 240,05, R$ 131,36 e R$ 41,95. A ponta concentrou 31,8% do custo em 12,5% das horas.

### Validação final dos quatro marcos

- `python -m unittest discover -v`: **93 testes, todos passando**, incluindo os testes de aceitação dos quatro marcos e os testes próprios.
- O Marco 4 tem 8 testes próprios além do exemplo: 2 regressões e 6 testes adicionais de ajuste, limites tarifários, balanço irregular e propagação de erro do rendimento.
- `python marco1.py`, `python marco2.py`, `python marco3.py` e `python marco4.py`: todos os asserts passaram com matrícula 3505.
- Após `git fetch upstream`, a referência `upstream/main` já está contida na branch. `git diff upstream/main --stat -- fornecido/ marco2.py marco3.py marco4.py` não mostrou diferenças.
- Os erros dos Marcos 3–4 registrados nas validações anteriores deste relatório foram resolvidos nesta etapa; aqueles números descrevem as execuções históricas.
- O commit dos testes antecede os commits das correções das issues #9 e #11; as quatro regressões falharam antes e passaram depois.

As implementações e respostas destes marcos tiveram auxílio de IA. Permanecem necessárias a revisão pessoal pelo aluno, a publicação dos commits e a conferência da descrição e do estado do PR antes da entrega; as pendências históricas do Marco 1 continuam documentadas na sua seção.
