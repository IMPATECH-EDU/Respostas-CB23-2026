# Relatório — Órion Moreira e Pereira (3469)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

Python: C:\Users\orion\AppData\Local\Python\pythoncore-3.14-64\python.exe
=== Etapa 0: ambiente ===
Python 3.14.6 | NumPy 2.4.6 | fornecido 4.0

### R1 — Expressões regulares

`re.match` casa apenas a partir do início da string e aceita caracteres excedentes no final (como `"PT101 "` ou `"PT1010"`), enquanto `re.fullmatch` exige correspondência total de ponta a ponta.
Se `valida_tag` utilizasse `match`, entradas corrompidas com lixo ao final seriam erroneamente validadas como tags corretas, propagando dados inválidos.

### R2 — Linhas inválidas

`ler_log` retorna as linhas inválidas para permitir auditoria, telemetria e detecção precoce de anomalias na comunicação.
Se descartássemos em silêncio, uma falha de hardware na RTU gerando ruído elétrico contínuo passaria despercebida pela supervisão, aparentando falsamente uma operação calma com vazão ou pressão subdimensionada.

### R3 — Late binding

A compreensão captura a variável `k` por referência (*late binding*). Ao final do loop, `k` permanece com o valor do último par (`FT201`, escala 0.1), fazendo `errados["PT102"](4095)` resultar em `4095 * 0.1 = 409.5`.
Nossa função `criar_conversores` usa `k=fator` como argumento padrão da lambda, fixando o valor de cada instrumento no momento em que a função é criada.

### R4 — Escala nominal

A diferença ocorre porque a escala nominal supõe transdutor perfeitamente linear, enquanto o sensor físico PT102 possui resposta não-linear.
A explicação no código da base está em `fornecido/simulador.py` (função interna `_curva_pressao`), que aplica uma característica não linear às contagens de pressão de recalque.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: `cea25e5`

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18.0x | 18.00x |
| Tempo do laço / tempo vetorizado | 40.0x | 24.94x |
| Tempo da compreensão / tempo do laço | 0.65x | 0.91x |

A maior diferença ocorreu no tempo da compreensão em relação ao laço (0.91x vs 0.65x), pois a instanciação de objetos float em Python continua pesada em ambos.
O cálculo `uint16(4095) * 20 = 81900` estoura a capacidade de 16 bits sem sinal ($2^{16} = 65536$), sofrendo overflow modular: $81900 - 65536 = 16364$.
Para contagens de 0 a 4095, escolheria `np.uint16` (econômico, 2 bytes/leitura); para pressões em kPa, escolheria `np.float64` para garantir precisão e suporte a decimais.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

O resultado que mais surpreendeu foi `s.sum()` retornar `SerieTemporal` em vez de um escalar `float64`. Como `SerieTemporal` herda de `np.ndarray`, as ufuncs e reduções padrão do NumPy propagam a própria subclasse quando retornam arrays de dimensão 0.

### R7 — Issue #4

Sintoma: `media_movel(30)` retornava 570 valores em vez de 571 em uma série de 600 pontos.
Testes de regressão: `test_media_movel_tamanho`, `test_media_movel_primeiro_ponto_e_valores` e `test_media_movel_janela_igual_tamanho`.
Causa: `acumulada[janela:] - acumulada[:-janela]` esquecia o primeiro elemento `acumulada[janela - 1]` (que exigiria subtrair zero no índice 0).
Correção: Pré-alocou-se vetor acumulado com `0.0` na primeira posição antes de subtrair as fatias.
Os testes de aceitação originais apenas verificavam o tipo de retorno e exceções, sem validar o comprimento exato nem os valores.
Outro caso não coberto por eles: `janela == len(s)`, em que o código original retornava array vazio e agora retorna a média global (coberto por `test_media_movel_janela_igual_tamanho`).
