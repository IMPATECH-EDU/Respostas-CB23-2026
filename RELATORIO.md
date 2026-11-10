# Relatório — Matheus Mota de Godoy (3501)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->
C:\python312\python.exe
(usando Windows)
Python 3.12.0 | NumPy 1.26.4 | fornecido 3.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
"PT1010 " com [A-Z]{1,2}\d{1,3} seria aceito por match e rejeitado por fullmatch, já que match por padrão só precisa do começo da string ser igual.
Consequentemente valida_tag precisa de fullmatch para apenas aceitar tags estritamente seguindo o padrão. match também poderia ser usado com alguns truques, mas fullmatch é destinado justamente a isso.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Devolver as linhas descartadas serve de alarme implícito (e.g. número de linhas descartadas aumentando de modo suspeito) e não engole ALARMEs inválidos.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
A função lambda aponta para a variável, não para o valor, que muda e fica com o último valor atribuído, assim dando 409,5 com o último fator de 0,1.
Criar um escopo novo por vez com a função conversor conserta o problema ao criar uma variável que não tem seu valor mudado.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
A escala nominal usada é linear, mas os valores verdadeiros não são. No código (p_real do simulador.py) é usado 600 * sin(0.5 * π * c / 4095).

### R5 — Previsão × medição (Etapa 3)

(Nota: Só fui notar que era para fazer uma previsão no final, e faço 1 commit por marco. De todo modo não consultei os valores medidos para a previsão)
Previsões registradas no commit: Nenhum (ver nota)

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 15 | ~18 |
| Tempo do laço / tempo vetorizado | 10 | 19.75 |
| Tempo da compreensão / tempo do laço | 0.95 | 0.95 |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

Errei a comparação com o tempo vetorizado porque Python é mais lento que o esperado, já que dava para usar a estimativa de 1 segundo por 10^8 operações para o vetorizado mas não tenho uma estimativa assim para Python. uint16*20 dá 16364 por overflow silencioso.
Dado que os valores de contagens ficam abaixo de 2^12, um short (uint16) dá e sobra. Para kPa os valores são reais então float32 é o básico.


### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

<!-- Explique o resultado que mais surpreendeu você. -->
s.sum() retorna SerieTemporal, porque o numpy preserva tipos de subclasse por causa de coisas como matrizes. Achei que esse comportamento não era o padrão, mas é.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
media_movel devolvia 570 valores em vez de 571. Testes foram  TestMediaMovelRegressao.test_tamanho e test_primeira_janela (escritos depois da correção mas verificados contra o código original)
Causa: a soma da janela x[i:i+j] é C[i+j-1] - C[i-1], mas np.cumsum não tem o termo C[-1] = 0. Sem ele, acumulada[j:] - acumulada[:-j] dá as janelas a partir de i = 1: a primeira se perde e sobram n - j valores.
Correção: inserir um 0 no início da soma acumulada (np.insert(np.cumsum(self), 0, 0.0)).
Os testes de aceitação só conferem o tipo de retorno e os ValueError, sem observar o tamanho ou valores.

## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->
Python 3.12.0 | NumPy 1.26.4 | SciPy 1.12.0 | fornecido 4.0 | matrícula 3501

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->
Antes de 1e-5 o erro é dominado por truncamento e diminuí com h. O erro cresce por cancelamento catastrófico, que remove valores significativos e deixa lixo, e a divisão por h que magnifica o valor desse lixo. em h = 1e-14 a diferença relativa vira 0 e logo a diferença adiante vira 0 também, com o erro sendo igual à própria derivada.
### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->
Testes test_original e test_alta_precisao usados para validar AcumuladorKahan. Aritmética de ponto flutuante não é associativa, e como t = s + y ficamos com (s + y) - (s + y) que é sempre 0. Os testes não pegaram o defeito porque não medem especificamente a precisão maior produzida pela soma de Kahan.

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->
desvio 0,543 (linear) x 0,545 (spline), viés −1,829 x 0,001 kPa
A curva linear tem um erro sistemático por estar sempre um pouco abaixo do seno. O número de leituras melhora o desvio de maneira semelhante para ambas as curvas, mas o viés é sistemático.
