# Relatório — Madson dos Santos Silva (3533)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

Python 3.13.7

=== Etapa 0: ambiente ===
Python 3.13.7 | NumPy 2.5.4 | fornecido 2.0

### R1 — Expressões regulares

Uma string como `"PT101 "` (com espaço no final) ou `"PT101X"` começa com o padrão da tag, sendo aceita pelo `re.match` no início da palavra. No entanto, ela possui lixo residual, sendo rejeitada pelo `re.fullmatch`. A consequência para `valida_tag` é que usar `fullmatch` nos protege de falsos positivos, garantindo rigorosamente que a string inteira é válida, sem caracteres ocultos no final.

### R2 — Linhas inválidas

A função `ler_log` devolve as linhas descartadas para viabilizar auditorias na qualidade dos dados. Se descartássemos as falhas em silêncio, uma pane grave (ex: formato de data do SCADA desconfigurado ou sensor retornando letras) passaria despercebida. O sistema processaria menos dados sem gerar alertas, causando análises incompletas e baseando decisões de engenharia em dados corrompidos.

### R3 — Late binding

A falha ocorre porque a `lambda` no laço do código original cria uma referência à variável iteradora `k`, e não ao seu valor. Ao fim do laço, `k` é `0.1` (referente ao último sensor, FT201), fazendo todos os conversores usarem esse fator (`4095 * 0.1 = 409.5`). O script não tem esse problema porque o `criar_conversores` usa um escopo fechado (seja por um argumento default `k=k` ou factory) que "congela" o valor isolado por tag.

### R4 — Escala nominal

A hipótese principal é que o sensor real instalado no campo sofreu degradação ou possui calibração com desvio (erro de offset ou de ganho), não acompanhando a escala puramente teórica nominal fornecida pela fábrica. No código-base, a explicação dessa diferença encontra-se no módulo da simulação (`fornecido/simulador.py`), onde ruídos e distorções na conversão analógica são inseridos intencionalmente.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: "Adiciona previsoes no relatorio"

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 18.0x |
| Tempo do laço / tempo vetorizado | 50 | 20.8x |
| Tempo da compreensão / tempo do laço | 0.7 | 0.93x |

A diferença expressiva no tempo vetorizado ocorreu porque previu-se um ganho teórico alto, porém operações no NumPy têm um custo fixo de inicialização que limita o ganho em arrays menores. O `uint16 * 20` dá `16364` devido a overflow (81900 extrapola o teto de 65535, sobrando o resto de `81900 % 65536 = 16364`). Para as variáveis, eu escolheria `uint16` para contagens e `float32` para pressões.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal  |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

O resultado que mais surpreende é `s.sum()` resultar em uma `SerieTemporal` em vez de um número simples (`float64`). Isso se explica porque operações de redução do NumPy priorizam preservar o tipo retornado das classes-filhas de `ndarray` por meio do método interno `__array_wrap__`, envelopando equivocadamente o escalar de volta para a classe da série.

### R7 — Issue #4

**Sintoma**: A média móvel retornava um ponto menos (Erro "off-by-one"), com `n=570` ao invés de `571`. **Teste**: Faltava um caso cobrindo janelas extremas (como `test_tamanho_media_movel`). **Causa**: Fatiar matrizes de `cumsum` descartava a primeiríssima janela temporal. **Correção**: Inserir um `0` artificial no início da matriz via `np.insert()` antes da soma cumulativa. Os testes de aceitação originais usavam blocos onde essa falta não era fatal, camuflando o desvio.