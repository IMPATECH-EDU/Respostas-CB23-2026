<<<<<<< HEAD
# Relatório — Wilian Martins da Silva (3551)
=======
# Relatório — <Wilian Martins da Silva> (3551)
>>>>>>> da03db36e70bcda7d3abf5944ceec2b439d1deda

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

/usr/bin/python3
Python 3.14.4 | NumPy 2.3.5 | fornecido 3.0

### R1 — Expressões regulares

O `re.match` procura correspondência apenas no início, aceitando "PT101 " (com um espaço no fim). O `re.fullmatch` exige que a string inteira corresponda ao padrão. Se usássemos `match` em `valida_tag`, as strings com lixo ou espaços extra no final seriam aceites indevidamente como tags válidas, o que iria corromper a filtragem dos dados.

### R2 — Linhas inválidas

Devolver as linhas descartadas permite que o sistema seja auditado. Se o `ler_log` as ignorasse em silêncio, a equipa não conseguiria distinguir entre um período sem eventos e uma falha crítica, como uma perda de pacotes de rede ou um sensor avariado a enviar dados truncados que precisaria de intervenção de manutenção.

### R3 — Late binding

A versão `errados["PT102"](4095)` dá 409.5 porque o Python avalia a variável `k` apenas quando a lambda é chamada (*late binding*), usando o último valor assumido no laço (0.1)[cite: 15]. A nossa `criar_conversores` resolve isto com um argumento padrão (`fator=fator`), forçando a avaliação imediata (*early binding*) na criação da lambda.

### R4 — Escala nominal

A escala nominal resulta em 261.99 kPa contra os 380.00 kPa de referência[cite: 7, 14]. A diferença deve-se ao facto do instrumento `PT102` estar a simular um desvio real (ruído ou falta de calibração) face à equação ideal. A explicação codificada para esta perturbação nos dados encontra-se no ficheiro da base `fornecido/simulador.py`[cite: 15].

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | [Sua Previsão] | ~ 18.0x (36.000.056 / 2.000.000) |
| Tempo do laço / tempo vetorizado | [Sua Previsão] | ~ 33.7x (37.33 ms / 1.11 ms) |
| Tempo da compreensão / tempo do laço | [Sua Previsão] | ~ 1.0x (37.61 ms / 37.33 ms) |

A maior diferença reside na aceleração da versão vetorizada face ao laço (33.7x)[cite: 7], pois o NumPy roda as operações em C compilado, ignorando o *overhead* do interpretador Python. O valor `16364` surge porque 81900 excede o limite do `uint16` (65535), causando um *overflow* ($81900 \pmod{65536} = 16364$)[cite: 7]. Escolheria `uint16` para as contagens A/D e `float32` ou `float64` para pressões em kPa.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | [Sua Previsão] | `SerieTemporal` |
| `s[1:]` | [Sua Previsão] | `SerieTemporal` |
| `s * 2` | [Sua Previsão] | `SerieTemporal` |
| `s.sum()` | [Sua Previsão] | `float` |
| `s[0]` | [Sua Previsão] | `float` |

O resultado que mais me surpreendeu foi que `s.sum()` e o acesso ao índice `s[0]` devolvem o tipo primitivo `float` do Python[cite: 7, 14], em vez de retornarem uma série unitária ou um tipo nativo do NumPy (como `numpy.float64`).

### R7 — Issue #4

O sintoma era que o tamanho da série resultante na `media_movel` tinha um valor a menos do que o tamanho matematicamente correto[cite: 15]. O meu teste de regressão é o `test_tamanho_media_movel`. A causa era o uso de `len() - w` no limite do `range`, que exclui a última iteração. A correção foi alterar o iterador para `len(self._valores) - w + 1`[cite: 13]. Os testes de aceitação não falharam porque não faziam validação ao tamanho da lista[cite: 15]. Outro caso que não cobriam era passar um tamanho de janela inválido (ex: `w <= 0`), algo que eu cobri no `test_media_movel_w_invalido`.
