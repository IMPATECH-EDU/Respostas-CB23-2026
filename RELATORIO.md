# Relatório — Oigres Leal Brandão (3489)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

```
$ which python
/opt/anaconda3/envs/ambiente_aluno/bin/python

=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.2 | fornecido 4.0
```

### R1 — Expressões regulares

String: `"PT1234"`
| Comando | Saída |
| --- | --- |
| `re.match("[A-Z]{1,2}\d{1,3}", "PT1234")` | `<re.Match object; span=(0, 5), match='PT123'>` |
| `re.fullmatch("[A-Z]{1,2}\d{1,3}", "PT1234")` | `None` |

`valida_tag` utiliza re.fullmatch, logo a string dada não passaria, pois não é aceita no padrão de tag `[A-Z]{1,2}\d{1,3}`. Mas o re.match só verifica se os primeiros caracteres se encaixam no padrão, isto é, re.match veria que `"PT123"` passa e ignoraria o 4. Essa tag não existiria no sistema por ter mais de 3 digitos finais, implicando numa validação inválida por parte do sistema.

### R2 — Linhas inválidas

`ler_log` devolve as linhas descartadas para informar quantas foram perdidas, por que foram perdidas e se os registros válidos representam o log inteiro. Se um sensor desregulado passasse a escrever as linhas em outro formato, `ler_log` descartaria todas elas e o volume bombeado ficaria menor que o real, mas os números pareceriam normais. Com `invalidas`, a lista cresceria de poucas linhas para muitas, todas parecidas e da mesma tag, o que apontaria o problema.

### R3 — Late binding

Em `errados`, `lambda c: c * k` não guarda o valor de `k`, só uma referência ao nome. `k` é consultado quando a lambda é chamada, e nesse momento o laço já terminou e `k` vale 0,1 (escala de `FT201`). Por isso `errados["PT102"](4095)` dá 4095 × 0,1 = 409,5, em vez de 600. Isso é late binding. Em `criar_conversores`, `lambda c, k=fator: c * k` fixa o valor na criação da lambda (early binding), então cada tag mantém o seu próprio `k`.

### R4 — Escala nominal

A diferença (> 100 kPa) entre a pressão calculada com a escala nominal e o valor de `verdade["pressao_recalque"]` pode ocorrer porque a escala nominal assume uma resposta linear do transmissor `(p = c × 600 / 4095)`, mas a resposta real do sensor é não-linear. A explicação está em `fornecido/simulador.py`, nas funções `p_real` e `c_real` mostrando que a resposta verdadeiramente é senoidal.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 14fba7d

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 18 |
| Tempo do laço / tempo vetorizado | 30 | 34,77 |
| Tempo da compreensão / tempo do laço | 0,73 | 0,92 |

A maior diferença (proporcional) foi em `Tempo da compreensão / tempo do laço`: previ uma vantagem um pouco maior, mas o custo principal estava nas operações aritméticas e não no overhead do laço. `uint16 * 20` dá overflow, pois `uint16` vai só de `0` a `65535` e `4095 * 20 = 81900 > 65535`, então o resultado é `81900 % 65536 = 16364`. Para contagens (0 a 4095), escolheria `np.uint16`, o menor inteiro que comporta o máximo. Para kPa, `np.float64`, pela precisão em contas posteriores.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

O que mais me surpreendeu foi o `s.sum()` ser `SerieTemporal` e não `float64`. Acreditei que `s.sum()` pegaria os termos internos que são `float64` e retornaria a soma de floats em `float64`, mas o que o `s.sum()` realmente faz é pegar a `SerieTemporal` (subclasse de `ndarray`) que ele recebe e retorna um resultado de uma dimensão menor e não um `float64`. Isso ocorre porque, nas reduções, o NumPy preserva a subclasse e devolve um array 0-d da SerieTemporal, em vez de um escalar.

### R7 — Issue #4

- **Sintoma:** para 600 leituras de `PT102` e janela 30, `media_movel(30)` devolvia 570 valores, mas a docstring exigia `n - janela + 1 = 571`.
- **Testes de regressão:** `test_quantidade_de_medias`, `test_media_movel_valores` e `test_media_movel_janela_1` falhavam com o código original.
- **Causa:** `np.cumsum(self)` sem o zero inicial. Com um vetor de `n` posições, as fatias `acumulada[janela:]` e `acumulada[:-janela]` produziam `n - janela` médias, e a média da primeira janela ficava de fora.
- **Correção:** concatenei `[0.0]` antes do `cumsum`, gerando `n + 1` posições e, portanto, `n - janela + 1` médias.
- **Por que os testes de aceitação não pegaram:** eles só verificavam o tipo e os `ValueError`, não o comprimento nem os valores.
- **Outro caso não coberto:** o valor da primeira janela. `test_media_movel_valores` cobre isso: espera `[1.5, 2.5, 3.5, 4.5]`, e o código original devolve `[2.5, 3.5, 4.5]`.