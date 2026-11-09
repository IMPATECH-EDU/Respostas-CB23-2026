# Relatório — <seu nome> (<sua matrícula>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

where pyhton:
C:\Users\bruno\AppData\Local\Microsoft\WindowsApps\python.exe
<!-- Isso mesmo eu fiz no WINDOWS, na minha visão o sistema operacional não importa. (Até ir trabalhar com servidores, aí importa, Linux vira o Goat) -->

=== Etapa 0: ambiente ===
Python 3.11.9 | NumPy 2.4.4 | fornecido 4.0

=== Etapa 1: leitura do log ===
Registros por nível: {'ALARME': 2, 'WARN': 1, 'INFO': 2401}
Total de pulsos: 2334531
Volume bombeado: 233453.1 litros

=== Etapa 2: lambda e compreensões ===
Pressão nominal: 261.98 kPa
Pressão de referência: 380.00 kPa

=== Etapa 3: memória e tempo ===
estrutura     B/elem    bytes totais  razão vs lista
list           36.00      36,000,056           1.000
array('H')      2.00       2,000,000           0.056
uint16          2.00       2,000,000           0.056
int32           4.00       4,000,000           0.111
int64           8.00       8,000,000           0.222
float32         4.00       4,000,000           0.111
float64         8.00       8,000,000           0.222
versão          tempo (ms)  aceleração vs laço
laço                 56.80                 1.0x
compreensão          51.45                 1.1x
map+lambda           68.97                 0.8x
vetorizado            4.80                11.8x

=== Etapa 4: a série de pressão ===
s + s      -> SerieTemporal
s[1:]      -> SerieTemporal
s * 2      -> SerieTemporal
s.sum()    -> SerieTemporal
s[0]       -> float64

Marco 1: todos os assert passaram.

### R1 — Expressões regulares

O re.match verifica apenas o início da string, enquanto re.fullmatch exige que ela inteira corresponda ao padrão. Por exemplo, "PT101XYZ" pode ser aceita pelo match, pois começa com uma tag válida, mas é rejeitada pelo fullmatch. Se valida_tag usasse match, poderia aceitar tags com caracteres extras no final, contrariando a regra de validar a string inteira.

### R2 — Linhas inválidas

A função ler_log devolve as linhas descartadas para que a perda de dados não passe despercebida. Se elas fossem ignoradas sem contabilização, poderíamos deixar de perceber falhas na comunicação com os sensores, por exemplo. Isso poderia esconder a ausência de leituras de pressão ou vazão e comprometer a análise do funcionamento da elevatória.

### R3 — Late binding

O problema acontece porque as funções lambda criadas dentro do laço não guardam o valor de fator daquele momento, elas acabam usando o último valor atribuído à variável, que corresponde ao fator 0,1 do FT201. Na função criar_conversores, o problema é evitado ao associar o fator correto a cada função no momento de sua criação, garantindo que cada instrumento use sua própria escala.

### R4 — Escala nominal

A diferença ocorre porque a escala nominal usada na conversão é linear, enquanto o transmissor do simulador possui uma resposta não linear. Portanto, faz com que a pressão estimada seja diferente da pressão de referência de 380 kPa. Sendo mais específico, o ponto está em `p_real()` --> `fornecido/simulador.py`, que utiliza uma função seno para relacionar as contagens à pressão.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 1ddb294

|                Grandeza                 | Previsão | Medido |
|                  ---                    |    ---   |   ---  |
| Memória da lista / memória do `uint16`  |    18x   |   18x  |
| Tempo do laço / tempo vetorizado        |    20x   |  11,8x |
| Tempo da compreensão / tempo do laço    |   0,85   |   0,91 |


1. O ganho previsto era de 20x, mas foi de 11,8x (40% abaixo). A diferença pode ser explicada pelos custos da vetorização do NumPy e pela variação entre medições.
2. O `uint16` suporta até 65535, ao ultrapassar esse limite, o valor volta ao início. Assim, 81900 − 65536 =  16364.
3. Para contagens, usaria `int32` ou `int64`, pois `uint16` não suporta 2.334.531 pulsos. Para kPa, usaria `float32`, que oferece precisão suficiente e consome metade da memória do `float64`.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto  | Tipo observado |
|    ---    |      ---       |      ---       |
| `s + s`   | `SerieTemporal`|`SerieTemporal` |
| `s[1:]`   | `SerieTemporal`|`SerieTemporal` |
| `s * 2`   | `SerieTemporal`|`SerieTemporal` |
| `s.sum()` |    `float64`   |`SerieTemporal` |
| `s[0]`    |    `float64`   |   `float64`    |

1. O resultado que mais me surpreendeu foi o s.sum(), pois esperava um float64, mas recebi uma SerieTemporal. Isso mostra que a classe possui um comportamento personalizado para a soma, diferente do esperado para um tipo numérico comum.

### R7 — Issue #4

1. Sintoma, o defeito fazia `media_movel(30)` retornar 570 valores em vez de 571.
2. O teste de regressão `test_quantidade_de_valores` verifica essa quantidade.
3. A causa era a soma acumulada não incluir o zero inicial, omitindo a primeira janela.
4. A correção foi adicionar `0.0` ao início da soma acumulada com `np.concatenate`.
5. Os testes de aceitação não detectaram o erro porque não verificavam esse caso.
6. O teste `test_primeiro_valor_e_media_da_primeira_janela` cobre outro caso que não era testado.
