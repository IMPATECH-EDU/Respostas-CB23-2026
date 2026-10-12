# Relatório — <seu nome> (<sua matrícula>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->
/opt/anaconda3/envs/ambiente_aluno/bin/python

=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.3 | fornecido 1.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
A string "EX248!" é aceita por re.match, uma vez que sua forma satisfaz a regra de começar com uma ou duas letras maiúsculas seguidas por 1,2 ou 3 números. No entanto, re.full.match a rejeitaria, pois possui um caractere "!" que está além das regras.
Como consequência, vê-se que re.fullmatch é mais restritivo e garante a padronização de tags, enquanto que re.match permitiria adições aleatórias no final e comprometeria a organização interna ao não garantir o padrão esperado.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
ler_log devolve as linhas descartadas para que seja possível analisar defeitos de comunicação ou dados corrompidos no monitoramento do sistema. Um exemplo realista em que isso é pertinente seria o caso de uma unidade perder contato com o sistema e passar a não conseguir produzir respostas válidas.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
O resultado final é 409,5 porque a função lambda só é chamada posteriormente, utilizando como fator de multiplicação do argumento c não pelo fator associado a cada item de "escalas", mas pelo último com que terminou o ciclo de criação de "errados": 0,1.

A implementação resolve o problema utilizando um argumento padrão que avalia e liga o valor de `fator` no momento exato da definição da função, preservando o fator individual de cada tag.
### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
A discrepância surge pela diferença entre a escala senoidal do medidor real e a linear utilizada no cálculo da nominal

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 18.000028 |
| Tempo do laço / tempo vetorizado | 20 | 19.20 |
| Tempo da compreensão / tempo do laço | 0.7 | 0.86 |

2351a64
<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->
A multiplicação direta de $4095 \times 20$ dá $81900$, que excede o limite máximo suportado. Quando ocorre um estouro no NumPy, o valor equivale a tirar o resto da divisão por $65536$, retornando $16364$.
O tipo a ser escolhido deve ser o uint16, pois os valores utilizados encontram-se dentre do intervalo de 0 a 4095, dentro dos limites do uint16 sem desperdiçar memória.

Não houve uma grande discrepância entre o previsto e o obtido, mas a maior, que foi a razão de tempo da compressão pelo tempo do laço, mas podem ser explicadas por processos computacionais internos. A discrepância na memória pode ser explicada pela necessidade de ocupar memória para outros processos além de somente os ponteiros e dados da lista, como o cabeçalho e outros dados da estrutura interna da lista. As discrepâncias nas razões dos tempos, por outro lado, são um pouco maiores por dercorreram de chutes menos precisos, baseados apenas no conhecimento teórico da otimização de cada implementação, mas passíveis de alteração devido à natureza dinâmica e inconstante do tempo de execução.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | Float64 | SerieTemporal |
| `s[0]` | Float64 | Float64 |

<!-- Explique o resultado que mais surpreendeu você. -->
O fato de que s.sum() é do tipo SerieTemporal e não float64. 

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
O sintoma era que media_movel(30) retornava 570 valores para uma série de 600 pontos, quando deveria retornar 571. O teste de regressão test_media_movel_quantidade_correta detecta esse erro. A causa era o uso de acumulada[janela:] - acumulada[:-janela], que descartava uma média válida. Corrigi o problema acrescentando zero ao início da soma acumulada e usando acumulada[janela-1:] no primeiro termo da subtração. Os testes de aceitação não detectaram o defeito porque não cobriam esse caso: detectam se há tipo de retorno adequado, se levanta ValueError em caso de janela maior do que o tamanho da lista e se algumas operações mantêm o tipo SerieTemporal. Além disso, testei uma janela igual a 1 (test_media_movel_janela_um) e uma janela igual ao tamanho da série (test_media_movel_janela_igual_tamanho), casos que verificam os limites da operação.
