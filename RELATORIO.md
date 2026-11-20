# Relatório — <seu nome> (<sua matrícula>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

Path do python e Etapa 0:

No linux do IMPATECH.
``` 
-> which python                               
/home/al.souza.pedro/venvs/prog2-venv/bin/python
```
``` 
-> python marco1.py
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.4 | fornecido 4.0
``` 
No meu windows pessoal.
``` 
-> (Get-Command python).Path
C:\Users\pedro\venvs\prog2-venv\Scripts\python.exe
```
```
-> python marco1.py
=== Etapa 0: ambiente ===
Python 3.13.5 | NumPy 2.4.6 | fornecido 4.0
```

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
re.match aceita 'PT103weubcwo9ien\n\nscv658212r5', mas re.fullmatch rejeita. Usar re.match permite falsos positivos, já todos os positivos de fullmatch está contido em todos os positivos de match (O contrário não vale).

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Ainda que uma linha não seja útil para as medições, o sensor pode comunicar um erro por mensagem. Essa linha é corrompida do ponto de vista do tratamento dos dados, mas contém informação relevante. Basta ver uma das linhas corrompidas "### Falha de comunicação com o RTU ###" de exemplo.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Ao definirmos uma função lambda, criamos um escopo onde podemos definir variáveis. Errados define a variável de entrada, mas usa diretamente o k definido no escopo do for in line. Então quando chamamos a função, ela tenta usar uma variável que não existe no seu escopo e segue procurando nos escopos que contêm a função. No escopo do for in line, k refere-se ao último valor acessado. Na nossa função, k é definido no escopo de lambda.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
Nossa função de conversão é linear, mas a conversão real se dá pela expressão c = 4095 · (2/π) · arcsin(p / 600), como pode ser visto em c_real em simulador.py.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: abaa37e <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 36000056/2000000 ~ 18.000028 | 18.000028 |
| Tempo do laço / tempo vetorizado  | ~35 | 34.54 | 
| Tempo da compreensão / tempo do laço  | ~0.71 | 1/1.07 = 0.93|

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->
Tinha colocado a previsão na coluna errada, mas corrigi. A memória deu exata pois .tolist() cria uma lista com allocated = ob_size. Então o tamanho da lista será 56 + 8*N + 28*N (tamanho dos ponteiros + tamanho de um int). Já uint16 ocupa 2 bytes/elemento. Os tempos de laço/vetorizado deram consistentes, não há como encontrar o valor exato, mas usei dis.dis pra ver os processos de um laço, estimei o tempo de cada ação em unidades genéricas. Considerei que o vetorizado levava uma unidade/elemento. O compr/laço deu bastante diferente. Eu achei que ia ser bem mais rápido por não usar nenhum CALL, mas acho que superestimei. Também: 4095 * 20 = 81900 > 2**16. O NumPy tira o mod. Por isso seria mais apropriado usar int64. Em dados.py, linha 245 tomamos cuidado para converter para float64 antes de multiplicar. 

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | SerieTemporal (0-d) | SerieTemporal (0-d, `ndim == 0`) |
| `s[0]` | float64 | float64 |

<!-- Explique o resultado que mais surpreendeu você. -->
Previsões no commit 92f6ee2. O que mais chama atenção é `s.sum()`: o resultado é um número, mas continua sendo `SerieTemporal` (com `ndim == 0`). A soma é uma redução de ufunc (`np.add.reduce`), e o NumPy devolve o resultado passando pelo `__array_wrap__` da subclasse, que mantém o tipo mesmo sem dimensão. Já `s[0]` é indexação de um elemento só, que devolve um escalar do NumPy (`float64`), e não uma view. Por isso o `marco1.py` usa `float(...)` antes de comparar ou formatar médias e somas: senão estaríamos passando uma "série" de zero dimensões.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
Sintoma: com a série de PT102 (600 leituras) e janela 30, `media_movel` devolvia 570 valores, e não 571. Teste de regressão: `TestRegressaoMediaMovel.test_quantidade_de_valores` (falhava com `570 != 571`), junto com mais três da mesma classe. Causa: `np.cumsum` dá `A[i] = s[0] + ... + s[i]`, então `A[j+w] - A[j]` é a soma de `s[j+1 .. j+w]`. A primeira janela, `s[0:w]`, precisaria de um "A[-1] = 0" que não existe: ela some, e todas as médias ficam deslocadas um ponto para frente. Correção: colocar um 0 na frente da soma acumulada (`np.insert(np.cumsum(self), 0, 0.0)`), daí `A[j+w] - A[j]` passa a ser exatamente a soma de `s[j : j+w]`.
Os testes de aceitação só conferiam o tipo do retorno e o `ValueError` para janelas 0 e 6, nunca o tamanho nem os valores. Outro caso que eles não cobrem: janela igual ao tamanho da série, que deve dar um único valor (a média de tudo); o código antigo devolvia uma série vazia. Coberto por `test_janela_igual_ao_tamanho`.
