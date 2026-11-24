# Relatório — Gabriel Cypreste (3517)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente
(prog2-venv) Gabriels-MacBook-Air:Respostas-CB23-2026 ogabrielcypreste$ python marco1.py 2>&1 | head -3
=== Etapa 0: ambiente ===
Python 3.9.6 | NumPy 2.0.2 | fornecido 4.0

### R1 — Expressões regulares

Com o padrão de tag, a string "PT1010" é aceita por re.match e rejeitada por re.fullmatch. O match só exige que o começo da string case (PT101) e ignora o 0 que sobra, enquanto o fullmatch exige que a string inteira case. Se valida_tag usasse match, ela devolveria True para "PT1010", que não é uma tag válida.

### R2 — Linhas inválidas

ler_log devolve as linhas descartadas para que quem opera a estação possa contá-las e olhar o que veio corrompido, em vez de perdê-las sem aviso. Aqui foram 4 em 2404. Se derrepente centenas de linhas viessem corrompidas, seria sinal de falha de comunicação com a RTU, e descartar em silêncio deixaria lacunas nas séries de pressão sem que ninguém notasse.

### R3 — Late binding

A lambda c: c * k não guarda o valor de k, e sim uma referência à variável. Ela só lê k quando é chamada, e nessa hora o laço já terminou e k vale 0.1, o fator do FT201. A minha criar_conversores chama uma função auxiliar, _conversor(fator), que cria um escopo novo a cada chamada, então cada lambda guarda o fator da sua própria tag.

### R4 — Escala nominal

A escala nominal supõe que a pressão cresce em linha reta com a contagem ((c * 600) / 4095), mas o transmissor não responde assim. Em fornecido/simulador.py, a função p_real calcula 600 * sin((π/2) * (c/4095)), uma curva de seno. Na região perto de 1790 contagens, a curva real está bem acima da reta, por isso a conta linear dá cerca de 262 kPa e o valor de conferência é 380 kPa. Confirme olhando p_real e c_real antes de escrever.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` |18|17.8|
| Tempo do laço / tempo vetorizado |10|49.9|
| Tempo da compreensão / tempo do laço |1|1.4|

A maior diferença foi no laço contra o vetorizado: previ 10 vezes e medi 49.9. Subestimei o custo do interpretador: no laço, cada um dos 1 milhão de elementos passa por instruções do Python e por objetos int e float criados a cada volta, enquanto o NumPy faz o mesmo laço em C, sobre memória contígua. O uint16 * 20 dá 16364 porque o uint16 só vai até 65535 e 4095 * 20 = 81900, então o valor dá a volta e faz 81900 − 65536 = 16364. Eu guardaria as contagens em uint16 (cabem em 2 bytes) e as pressões em kPa em float64 (ou float32, se a memória importar mais), porque têm casas decimais.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` |SerieTemporal|SerieTemporal|
| `s[1:]` |SerieTemporal|SerieTemporal|
| `s * 2` |SerieTemporal|SerieTemporal|
| `s.sum()` |Float|SerieTemporal|
| `s[0]` |float64|float64|

O resultado que mais me surpreendeu foi s.sum(), que devolve uma SerieTemporal de 0 dimensões e não um float. Eu achava que somar uma série daria um número comum. A soma continua correta, mas o NumPy mantém a subclasse até em resultados de um único valor, enquanto s[0] já volta como float64.

### R7 — Issue #4

O sintoma era a média móvel de 30 pontos de uma série de 600 devolver um valor a menos. Escrevi test_tamanho_do_resultado e test_valores_incluem_a_primeira_janela, que falhavam antes da correção. Isso porque np.cumsum não começa com um zero, então a soma da primeira janela (acumulada[janela-1] não tem um "antes" para subtrair e a diferença só produz as janelas seguintes. A correção foi colocar um 0.0 na frente da soma acumulada. Os testes de aceitação só conferem o tipo e os erros, nunca o tamanho nem os valores. Outro caso que eles não cobrem é a janela igual ao tamanho da série, que deve dar um único valor, e é coberto pelo meu test_janela_igual_ao_tamanho.