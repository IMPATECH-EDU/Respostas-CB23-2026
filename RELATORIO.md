# Relatório — Gabryel Rodrigues Ferreira (3547)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

~/venvs/prog2-venv/bin/python
=== Etapa 0: ambiente ===
Python 3.14.7 | NumPy 2.5.4 | fornecido 3.0


### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

s = "BO1234"
Vai ser aceito pelo match e nao será aceito pelo fullmatch.
pois o fullmatch só aceita se a palavra toda seguir o padrão.
já o match corresponde ao inicio da string.



### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Para que a equipe possa reconhecer erros de leituras de pressão etc..
por exemplo, uma falha pode causar que uma leitura de pressão não seja registrada.


### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Porque foi usada a compreensão para criar aas conversões, isso faz com que todas acabem usando o mesmo fator.
Na minha implementação eu usei funções lambdas, evitando esse problema.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
Essa diferença provavelmente veio devido a uma diferença entre a escala nominal do transmitor e a calibração utilizada para gerar os dados de referencia.


### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 874246b5479ac8811b3240530c30f8b7e43cb976 <!-- cole o hash curto do commit de previsões -->
###

(prog2-venv) gabryel@Gabryel:~/Documentos/Respostas-CB23-2026$ python3 -c 'import numpy as np; from elevatoria.dados import medir_memoria, medir_tempos; c = np.random.default_rng(1).integers(0, 4096, 1_000_000); print("MEMÓRIA:", medir_memoria(c)); print("TEMPOS:", medir_tempos(c, k=10))'
MEMÓRIA: {'list': 36000056, "array('H')": 2000000, 'uint16': 2000000, 'int32': 4000000, 'int64': 8000000, 'float32': 4000000, 'float64': 8000000}
TEMPOS: {'laço': 0.14117228409886592, 'compreensão': 0.12800499930090153, 'map+lambda': 0.14699144629994407, 'vetorizado': 0.00287036209992948}
(prog2-venv) gabryel@Gabryel:~/Documentos/Respostas-CB23-2026$

###

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | A lista vai ocupar mais memória que o array uint16.|A lista ocupou 36.000.056 bytes, enquanto array uint16 ocupou 2.000.000 bytes (18 vezes a mais).|
| Tempo do laço / tempo vetorizado |Espero que a vetorização seja mais rápida em muitos casos. |O laço levou 141ms, enquanto a vetorizada levou 2.87ms, a vetorizada foi muito mais rapida(~=49 vezes mais rápido). |
| Tempo da compreensão / tempo do laço | Acho que a compreensão será muito mais rápida do que laço. | O tempo de compreesão foi 128ms já o laço levou 141ms, acho que essa diferença foi muito menor do que eu esperava (0.90) |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->


### R6 — Tipos da SerieTemporal (Etapa 4d)
###
(prog2-venv) gabryel@Gabryel:~/Documentos/Respostas-CB23-2026$ python3 -c 'from elevatoria.serie import SerieTemporal; s = SerieTemporal.de_lista([1, 2, 3]); print("s + s:", type(s + s).__name__); print("s[1:]:", type(s[1:]).__name__); print("s * 2:", type(s * 2).__name__); print("s.sum():", type(s.sum()).__name__); print("s[0]:", type(s[0]).__name__)'
s + s: SerieTemporal
s[1:]: SerieTemporal
s * 2: SerieTemporal
s.sum(): SerieTemporal
s[0]: float64
###

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` |SerieTemporal|SerieTemporal|
| `s[1:]` |SerieTemporal|SerieTemporal|
| `s * 2` |SerieTemporal|SerieTemporal|
| `s.sum()` |Float|SerieTemporal|
| `s[0]` |Float|float64|

<!-- Explique o resultado que mais surpreendeu você. -->
Acho que o que me mais me surpreendeu fooi o s.sum() ser serieTemporal. Pelo que entendi isso acontece porquea classe herda numpy e o numpy pode preservar a subclasse(ndarray) em operações como sum(), dependendo de como estão implementadas.
### R7 — Issue #4
O sintoma é que a media movel retorna 570 invés de 571.
O teste de regressão (test_media_move) avalia se a função retorna a quantidade correta.
A causa foi que uso de acumulada[janela:] descartava um valor da soma acumulada, reduzindo em um a quantidade de resultados. Além disso, a primeira janela precisa ser tratada separadamente, pois não existe uma soma anterior a subtrair.
Para corrigir isso utilizei acumulada[janela - 1:].copy() e subtraí as somas acumuladas anteriores apenas das posições seguintes. A solução não utiliza laços, não modifica a série original e retorna uma SerieTemporal.