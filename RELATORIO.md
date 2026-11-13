# Relatório — Stella (3493)

Resultados do Marco 1 para a matrícula 3493.

## Marco 1

### Ambiente

Ambiente usado nesta execução:

```text
$ which python
/opt/anaconda3/envs/ambiente_aluno/bin/python
$ python marco1.py
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.3 | fornecido 4.0
```

### R1 — Expressões regulares

Com o padrão `[A-Z]{1,2}[0-9]{1,3}`, `re.match` aceita o começo de `PT101texto`,
mas `re.fullmatch` rejeita porque sobra texto depois da tag.
Se `valida_tag` usasse `match`, poderia aceitar identificadores inválidos como esse.

### R2 — Linhas inválidas

As linhas descartadas permitem conferir quais dados foram perdidos e investigar a causa.
Nesta execução, foram 2404 registros válidos e 4 linhas inválidas.
Se uma falha de comunicação interrompesse as leituras de pressão, descartar as linhas
sem avisar poderia esconder o problema e fazer os dados parecerem completos.

### R3 — Late binding

As lambdas da versão errada consultam a mesma variável `k` quando são chamadas.
Ao terminar a compreensão, `k` vale 0,1, o último fator, de FT201; por isso 4095 vira 409,5.
Em `criar_conversores`, o argumento padrão `fator=fator` guarda o fator de cada lambda
no momento em que ela é criada. Assim, PT102 usa 600/4095 e devolve 600,0.

### R4 — Escala nominal

A escala nominal deu 261,95 kPa, enquanto a referência é 380,00 kPa.
Isso indica que a relação entre contagens e pressão não é linear.
A explicação está em `p_real`, em `fornecido/simulador.py`: a resposta usa uma função seno,
e não a reta `c * 600 / 4095`. A escala nominal não representa essa curva.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: `721df08`.

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | aproximadamente 18 | 18,000028 |
| Tempo do laço / tempo vetorizado | aproximadamente 20 | aproximadamente 34,51 |
| Tempo da compreensão / tempo do laço | aproximadamente 0,8 | aproximadamente 0,92 |

A maior diferença foi a aceleração vetorizada: 34,51 vezes, acima da previsão de 20.
O NumPy faz as operações em código compilado; os tempos também dependem do ambiente.
Nesta execução, laço, compreensão e vetorização levaram 40,578, 37,348 e 1,176 ms.
A lista ocupou 36.000.056 bytes e o `uint16`, 2.000.000 bytes.
Em `uint16`, 81900 ultrapassa 65535 e vira 81900 módulo 65536 = 16364.
Para contagens de 0 a 4095, usaria `uint16`; para pressões em kPa, `float64`.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `SerieTemporal` | `SerieTemporal` |
| `s[0]` | `float64` | `float64` |

O caso menos intuitivo é `s.sum()`: apesar de representar um único valor, o resultado
mantém a subclasse `SerieTemporal` como um array de dimensão zero.
Já `s[0]` devolve um escalar NumPy `float64`. Nesta execução, os tipos coincidiram
com as previsões registradas.

### R7 — Issue #4

A média móvel de 600 leituras com janela 30 devolvia 570 valores, em vez de 571.
Os testes `test_primeira_janela` e `test_janela_do_tamanho_da_serie` falharam antes da correção.
Faltava o zero inicial na soma acumulada, por isso a subtração pulava a primeira janela.
A correção insere esse zero e mantém o retorno como `SerieTemporal`, sem alterar a série.
Os testes de aceitação verificavam tipo e erros, mas não os valores nem o tamanho da média.
Outro caso não coberto era log sem chave=valor, verificado por `test_rejeita_linha_sem_pares`.
