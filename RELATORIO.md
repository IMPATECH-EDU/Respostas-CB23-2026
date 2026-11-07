# Relatório — <Josué Rubem dos Santos Sousa> (<3540>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

- <b>Saída do which python</b>: /c/Users/josue/OneDrive/Documentos/Projeto Prog 2/Respostas-CB23-2026/.venv/Scripts/python
- <b>Saída da Etapa 0</b>: Python 3.14.3 | NumPy 2.5.4 | fornecido 1.0

### R1 — Expressões regulares

"PT1012". Passa no re.match porque pode-se formar uma tag correta usando do primeiro ao penúltimo caractere ("PT101"), já que o último é ignorado pelo re.match; mas re.fullmatch verificaria a linha toda e indicaria que a string não é uma tag válida. Isso torna a função valida_tag muito mais segura e rígida. Erros como um espaço em "PT101 " não são desconsiderados por usar re.fullmatch.

### R2 — Linhas inválidas

Para que se possa avaliar quais instrumentos falharam nas verificações e realizar correções. Se um deles estivesse com defeito e a função ler_log não retornasse as linhas inválidas, um diagnóstico de um problema na estação seria dificultado.

### R3 — Late binding

errados["PT102"](4095) dá 409,5 porque a funções só são avaliadas após a compreensão do dicionário, quando só há acesso ao fator de conversão da última tag ("FT201"), que é 0.1. A minha função não tem esse problema a implementação especifica para cada função qual é o fator a ser utilizado através de um argumento: `{tag: (lambda c, fator=fator: c * fator) for tag, fator in escalas.items()}`. <b>fator=fator</b> deixa claro para a função que a cada avaliação de tag há um fator diferente.

### R4 — Escala nominal

Há uma grande diferença entre a pressão nominal e a pressão real (maior que 100) porque na conversão é realizada apenas uma regra de três simples, multiplicando c por 600/4095, enquanto o valor real é gerado por um arcoseno multiplicado por uma constante. A conversão supõe que a conversão é linear, mas ela não é.
O valor real é definido da seguinte forma no arquivo simulador.py:\
`def c_real(p):`\
&emsp;`    """Contagens do A/D (12 bits) que correspondem à pressão p (kPa)."""`\
&emsp;`    return 4095.0 * (2.0 / np.pi) * np.arcsin(np.asarray(p, dtype=float) / 600.0)`

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 1934c57

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 36_000_000 bytes / 2_000_000 bytes = 18 | 36000056 bytes / 2000000 bytes = 18.000028 |
| Tempo do laço / tempo vetorizado | 200 ms / 20 ms = 10 | 0.093 ms / 0.006 ms = 15.5 |
| Tempo da compreensão / tempo do laço | 200 ms / 50 ms = 4 | 0.093 ms / 0.082 ms = 1.134 |

Como tanto compreensão como o laço `for` iteram em bytecode Python (um elemento de cada vez), a diferença de tempo entre elas não é tão grande quanto previsto, apesar do ganho de desempenho da compreensão por evitar o método `.append()`. O vetorizado, por outro lado, roda em **C compilado**, o que o torna ainda mais rápido do que o previsto. A previsão de memória foi bem acurada. O valor `uint16 * 20` resulta em 16364 devido ao *overflow* modular de 16 bits (81900 mod 65536). Para contagens, usaria `uint16` para economia de memória; para kPa, usaria `float32`, por ser eficiente com ponto flutuante.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | | |
| `s[1:]` | | |
| `s * 2` | | |
| `s.sum()` | | |
| `s[0]` | | |

<!-- Explique o resultado que mais surpreendeu você. -->

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

- **Sintoma:** A função media_movel devolvia $n - j$ valores ao invés de $n - j + 1$ (por exemplo, 570 ao invés de 571, como no relato); 
- **Teste de Regressão:** `test_media_movel_janela_2`;
- **Causa:** O fatiamento original `acumulada[janela:] - acumulada[:-janela]` ignorava o índice `janela - 1` (soma da primeira janela), começando em `janela`. Como não havia um elemento na posição anterior ao início do vetor para subtrair, a primeira janela era descartada.
- **Correção:** Inserção do valor `0.0` no início do vetor (`np.insert(np.cumsum(self), 0, 0.0)`). Isso permitiu que a fatiação `acumulada[janela:] - acumulada[:-janela]` funcionasse para a primeira janela e a função pudesse retornar $n - j +1$ valores.
- **Por que não foi detectado pelos testes:** Os testes não checavam o tamanho (`len()`) da SerieTemporal retornada.
- **Caso extra não coberto:** O comportamento de `media_movel` quando a janela é unitária (`janela = 1`), que deve retornar uma cópia idêntica da série original em tamanho e valores, coberto pelo meu teste `test_media_movel_janela_1`.
