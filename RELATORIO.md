# Relatório — Kauã Medeiros de Melo Oliveira (3464)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente
which python:
C:\Users\Kaua\AppData\Local\Programs\Python\Python313\python.exe
C:\Users\Kaua\AppData\Local\Microsoft\WindowsApps\python.exe
python marco1.py:
Python 3.13.2 | NumPy 2.4.4 | fornecido 4.0

### R1 — Expressões regulares
Um exemplo seria uma string como "PT3141". Como o re.match se preocupa que os primeiros caracteres com o padrão sejam satisfeitos, ele "ignoraria" o último '1'.
Já o re.fullmatch exige que todo esse segmento esteja no padrão perfeito, e então retornaria um erro.
Se usássemos re.match no valida_tag, strings inválidas passariam despercebidos durante a log do sistema.

### R2 — Linhas inválidas
ler_log devolve as linhas descartadas porque isso é importante para descobrirmos os problemas por trás dessas logs erradas. Idealmente o formato das logs
já adequa todas as informações e possíveis problemas a um log ideal, mas se, por exemplo, tivermos uma falha em algum hardware, pode ser que logs importantes
sejam perdidas. Nesse caso, coisas ainda piores podem acontecer, pois esse erro silencioso não permitiria medir adequadamente o nível das águas, por exemplo.

### R3 — Late binding
O problema que ocorre é justamente o late binding. De forma simplificada, se não realizarmos nenhuma operação ou acesso com as funções lambdas criadas, elas só
determinam suas variáveis no momento de execução. Por conta disso, o errados["PT102"](4095) processa todos os dados com o último fator, ao invés do adequado em cada
tag. Ao definir escalas[tag] como valor padrão de fator na lambda function, garantimos que escalas[tag] será acessada no momento da criação da função, e então
impedimos o late binding de ocorrer.

### R4 — Escala nominal
Pelo que verifiquei no código base, o motivo dessa diferença está na suposição de que as contagens seguem uma relação linear. O código atual assume que
o número de contagens cresce linearmente com a pressão, o que não é verdade ao olhar as funções p_real e c_real em simulador.py.
Assim, em cada etapa da simulação, a diferença entre a pressão medida e a real é de mais de 100kPA quando a pressão real (PRESSAO_RECALQUE) é grande.
<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | |
| Tempo do laço / tempo vetorizado | 30 | |
| Tempo da compreensão / tempo do laço | 0.8 | |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | |
| `s[1:]` | np.ndarray | |
| `s * 2` | SerieTemporal | |
| `s.sum()` | float | |
| `s[0]` | float | |

<!-- Explique o resultado que mais surpreendeu você. -->

### R7 — Issue #4
O sintoma é que o primeiro ponto da média móvel não é calculado. Isso acontece porque, no código original, ao calcular acumulada[janela:] e acumulada[:-janela],
o primeiro termo é ignorado, pois acumulada[janela] ignora o termo na posição janela-1, que corresponde à soma de 0 até janela-1.
Corrigimos isso adicionando um termo 0 à frente dos outros no vetor 'acumulada'.
Os testes de aceitação não pegaram o defeito porque verificavam apenas o tipo da lista e se a função não levantava erros, mas não fazia um teste numérico.
O teste que fiz inclui um teste de tamanho da lista, além de um teste com o primeiro valor calculado, para garantir que a função calcula esse primeiro termo.