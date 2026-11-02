# Relatório — <Stella Ventura> (<3493>)

# Relatório — Projeto Elevatória

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

Output de `which python`:
/home/usuario/venvs/prog2-venv/bin/python

Output da Etapa 0 do `python marco1.py`:
=== Etapa 0: ambiente ===
Python 3.10.12 | NumPy 1.26.4 | fornecido 4.0

### R1 — Expressões regulares

String aceita por `re.match` e rejeitada por `re.fullmatch`: `"PT101 extra"`.
Se `valida_tag` utilizasse `re.match`, tags com sufixos inválidos (como `"PT1010"` ou `"PT101 "`) seriam incorretamente validadas, pois `match` valida apenas o início da cadeia de caracteres.

### R2 — Linhas inválidas

A função `ler_log` retorna as linhas descartadas para possibilitar auditoria, métricas de integridade de sinal e identificação de falhas de hardware ou comunicação no barramento SCADA.
Em operação real, o descarte em silêncio ocultaria interferências elétricas ou falhas recorrentes em transmissores, impedindo a manutenção preventiva da infraestrutura.

### R3 — Late binding

No dicionário `errados`, a variável `k` na lambda é capturada por referência no escopo externo e avaliada tardiamente ao invocar a função, assumindo o valor do último par iterado (`0.1`). Por isso, `4095 * 0.1 = 409.5`.
A função `criar_conversores` resolve o problema usando um argumento com valor padrão (`fator=k`), congelando o parâmetro na assinatura da lambda no instante da sua criação.

### R4 — Escala nominal

A discrepância ocorre porque a conversão nominal assume uma resposta linear do transmissor de pressão (600 / 4095), enquanto a resposta física real simulada possui característica senoidal não linear.
A equação exata da física encontra-se no módulo `fornecido/simulador.py`, na função `p_real(c)`.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: commit inicial de previsões

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 20.00x | 20.44x |
| Tempo do laço / tempo vetorizado | 25.00x | 32.15x |
| Tempo da compreensão / tempo do laço | 0.60x | 0.65x |

A maior diferença de memória se deve ao overhead de ponteiros e estruturas de objeto do CPython em listas genéricas.
A operação `uint16 * 20` estoura a capacidade de 16 bits sem sinal (4095 * 20 = 81900; 81900 mod 65536 = 16364).
Para contagens brutas A/D, o tipo adequado é `uint16`; para valores de pressão em kPa, deve-se utilizar `float64` para garantir a precisão decimal necessária.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float64 | float64 |
| `s[0]` | float64 | float64 |

Surpreendeu o fato de `s.sum()` e `s[0]` retornarem `numpy.float64` em vez da subclasse `SerieTemporal`, pois operações que reduzem a dimensionalidade para um único escalar convertem a subclasse do NumPy para o tipo numérico primitivo correspondente.

### R7 — Issue #4

- **Sintoma:** O método `media_movel(30)` aplicado a uma série de 600 pontos gerava 570 elementos em vez dos 571 esperados.
- **Teste de regressão:** `test_media_movel_tamanho_correto`.
- **Causa:** A fórmula `acumulada[janela:] - acumulada[:-janela]` não considerava o termo base zero inicial do somatório.
- **Correção:** Adicionou-se o padding constante zero no início da soma acumulada via `np.pad`.
- **Testes de aceitação:** Não checavam a relação de tamanho N - K + 1 para arrays genéricos.
- **Caso não coberto:** A exatidão numérica dos primeiros elementos da janela em vetores pequenos (`test_media_movel_valores_exatos`).
