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
ler_log devolve as linhas descartadas porque isso é importante para descobrirmos os problemas por trás dessas logs erradas. Idealmente o formato das logs já adequa todas as informações e possíveis problemas a um log ideal, mas se, por exemplo, tivermos uma falha em algum hardware, pode ser que logs importantes
sejam perdidas. Nesse caso, coisas ainda piores podem acontecer, pois esse erro silencioso não permitiria medir adequadamente o nível das águas, por exemplo.

### R3 — Late binding
O problema que ocorre é justamente o late binding. De forma simplificada, se não realizarmos nenhuma operação ou acesso com as funções lambdas criadas, elas só determinam suas variáveis no momento de execução. Por conta disso, o errados["PT102"](4095) processa todos os dados com o último fator, ao invés do adequado em cada
tag. Ao definir escalas[tag] como valor padrão de fator na lambda function, garantimos que escalas[tag] será acessada no momento da criação da função, e então
impedimos o late binding de ocorrer.

### R4 — Escala nominal
Pelo que verifiquei no código base, o motivo dessa diferença está na suposição de que as contagens seguem uma relação linear. O código atual assume que o número de contagens cresce linearmente com a pressão, o que não é verdade ao olhar as funções p_real e c_real em simulador.py.
Assim, em cada etapa da simulação, a diferença entre a pressão medida e a real é de mais de 100kPA quando a pressão real (PRESSAO_RECALQUE) é grande.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 6458d6b

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 18.00|
| Tempo do laço / tempo vetorizado | 30  14.56 |
| Tempo da compreensão / tempo do laço | 0.8 | 0.88 |

A maior diferença se deu porque eu não sabia o tempo em média que levaria o laço e o vetorizado. Como eu não tinha certeza dos tempos, tentei perguntar para o Gemini qual seria um tempo razoável, e essa foi a resposta. Eu não sabia avaliar o quão mais rápido o vetorizado seria.
uint16 * 20 dá 16364 por conta do estouro da memória (overflow). Basicamente o uint16 suporta inteiros até 65535, e então qualquer valor adicional causa um estouro da memória, o que faz com que os bits que "saem da memória" sejam ignorados pelo interpretador, e então temos 81900 (mod 65535) = 16364.

Para o número de contagens, eu escolheria uint16. Como os valores só vão até 4095, o uint16 é mais que suficiente. Para kPA eu escolheria float32. Como os dados se dão em kPA, acredito que o espaço ganho ao usar float32 ao invés de float64 vale a pena, pois a precisão ganha não influenciaria nos cálculos.

### R6 — Tipos da SerieTemporal (Etapa 4d)

Previsões registradas no commit: 6458d6b

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | np.ndarray | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float | SerieTemporal |
| `s[0]` | float | float64 |

O resultado que mais me surpreendeu foi o np.ndarray ser uma SerieTemporal. Achei que a operação de slicing do numpy não fosse preservar o tipo original, já que se trata apenas de um vetor. Minha ingenuidade foi que o "cabeçalho" dos vetores do numpy permite que ele apenas troque a posição de início do vetor, e então o tipo original do vetor se conserva.

### R7 — Issue #4
O sintoma é que o primeiro ponto da média móvel não é calculado. Isso acontece porque, no código original, ao calcular acumulada[janela:] e acumulada[:-janela],
o primeiro termo é ignorado, pois acumulada[janela] ignora o termo na posição janela-1, que corresponde à soma de 0 até janela-1.
Corrigimos isso adicionando um termo 0 à frente dos outros no vetor 'acumulada'.
Os testes de aceitação não pegaram o defeito porque verificavam apenas o tipo da lista e se a função não levantava erros, mas não fazia um teste numérico.
O teste que fiz inclui um teste de tamanho da lista, além de um teste com o primeiro valor calculado, para garantir que a função calcula esse primeiro termo.


## Marco 2

### Ambiente

Python 3.13.2 | NumPy 2.4.4 | SciPy 1.17.1 | fornecido 4.0 | matrícula 3464

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->

### R9 — Issue #7

Os nomes dos testes são test_acumulacao_exata_1 e test_acumulacao_exata_2.
t - (s + y) dá sempre zero em ponto flutuante, pois t foi definido anteriormente como s + y. Já (t - s) - y inverte a ordem, e então os pequenos erros de arredondamento conseguem ser capturados, pois forçamos que calcule t - s, e só depois subtraia y.
Os testes de aceitação não pegaram o defeito porque somaram poucos números. Somar 0.1 dez vezes não é suficiente para que o erro de arredondamento do ponto flutuante seja relevante. O método math.isclose() (na documentação) tem tolerância relativa de 10e-9. Somar 0.1 dez vezes retorna 0.9999999999999999, e então math.isclose() não captura essa diferença.

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->