# Relatório — FLÁVIA JAKELINE DOS SANTOS AGRA (3479)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

### R4 — Escala nominal

A pressão do recalque com a escala nominal (a reta, c·600/4095) dá 262 kPa, mas o valor de conferência é 380 kPa. A hipótese, então, é de que o transmissor não segue uma reta, mas alguma outra curva que só coincide com a reta em 0 e em 4095 contagens. Em fornecido/simulador.py (funções p_real e c_real), temos que o transmissor não segue uma reta, mas sim uma função seno. Rodando c_real(380), temos cerca de 1788 contagens. Na escala nominal, isso dá 262 kPa, que é diferente de 380, então a reta não representa mesmo o transmissor. 

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 3a0f239

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18x | cerca de 18 vezes |
| Tempo do laço / tempo vetorizado | 40x | cerca de 10,7 vezes |
| Tempo da compreensão / tempo do laço | 68% | 52% |

A maior diferença foi no tempo do laço / tempo vetorizado. Para isso, temos a conta * 600 / 4095,percorrendo e criando um vetor de um milhão de elementos. A versão do Python e a variação entre execuções também são motivos. uint16 * 20 dá 16364 porque 4095 × 20 dá 81900, que passa do máximo (65535) e o valor dá a volta: 81900 − 65536 = 16364. Para as contagens (0 a 4095) escolheria uint16, que ocupa só 2 bytes por número, convertendo para um tipo maior antes de multiplicar, para evitar o overflow. Para os kPa escolheria float64, por guardar mais dígitos.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | np.ndarray | SerieTemporal |
| `s[1:]` | np.ndarray | SerieTemporal |
| `s * 2` | np.ndarray | SerieTemporal |
| `s.sum()` | np.uint64 | SerieTemporal |
| `s[0]` | np.uint16 | float64 |

O que mais me surpreendeu foi o s[0] sair float64. Eu esperava uint16, pois ascontagens são positivas e cabem em 16 bits, mas ler_log converte os números para float e de_lista converte de novo com `dtype=float`, então a série nunca tem inteiros. Eu também errei s + s, s[1:] e s * 2, pensei que seriam np.ndarray, mas agora entendi que o NumPy cria o resultado a partir da própria SerieTemporal, daí a subclasse fica sendo a mesma. Em s.sum(), errei a mesma coisa. Pensei que seria np.uint64 e saiu SerieTemporal, então foi mais por falta de atenção.

### R7 — Issue #4

### R7, Issue #4
1) media_movel(30) na série de 600 pontos deu 570 valores, não 571. 2) test_tamanho_600_janela_30 e test_serie_de_seis. 3) acumulada[i] é a soma até o ponto i. Sem um zero no início, acumulada[i+janela] - acumulada[i] dava a soma de self[i+1 : i+janela+1] e perdia a primeira janela. 4) colocar um zero na frente da soma acumulada, para a diferença ser self[i : i+janela] + 1n - janela + 1. 5) test_media_movel_tipo_e_erros só vê que o retorno é SerieTemporal e que as janelas 0 e 6 levantam ValueError. Sem teste verifica o tamanho ou os valores. 6) o valor da primeira janela. Com [2,4,6,8,10,12] e janela 2, o código antigo devolvia [5,7,9,11], sem o 3 inicial; test_serie_de_seis cobre isso. 
