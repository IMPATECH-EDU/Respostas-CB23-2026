# Relatório — Maria Eduarda Teixeira de Araujo Dantas (3476)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->
Usei Windows, então no lugar de `which python` usei `(Get-Command python).Source`.
CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Application     python.exe                                         3.14.41... C:\Users\dudad\venvs\prog2-venv\Scripts\python.exe
Python 3.14.4 | NumPy 2.5.4 | fornecido 3.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
Uma string que re.match aceita e re.fullmatch rejeita é "PT1010". O match só exige que o começo case, então aceita PT101 e ignora o 0 que sobra. Se valida_tag usasse match, aceitaria "PT1010" e "PT101 ", que estão na lista de inválidas do enunciado.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Eu tive 4 inválidas em 2408 linhas. Devolvê-las permite contar e auditar a falha. Situação possível: se um transmissor ou a comunicação falhar por vários minutos, todas as linhas dele chegam corrompidas, e descartar em silêncio esconderia o instrumento morto.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Na compreensão, cada lambda guarda a variável k, não o valor dela. Quando as lambdas são chamadas, k já terminou o laço valendo 0,1 (a escala de FT201, a última do dicionário), e por isso errados["PT102"](4095) dá 4095 × 0,1 = 409,5. A minha criar_conversores usa f=fator como argumento padrão, que é avaliado na criação de cada lambda e fixa o fator de cada tag.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. --> 
Hipótese: o transmissor não responde linearmente. A escala nominal assume pressão = contagens * 600 / 4095 (uma reta), mas a curva real é curvada, e no meio da faixa ela dá valores maiores que a reta. A média de PT102 (cerca de 1791 contagens) dá 262 kPa pela escala nominal e 380 kPa de conferência.
Onde está: em fornecido/simulador.py, na função p_real, que calcula 600 * sin(0.5 * pi * c / 4095). A função tabela_calibracao() fornece justamente pontos dessa curva, o que sugere que, no mundo real, a conversão deveria usar a calibração (por exemplo, interpolando) em vez da escala nominal.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 2ee94cd

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ~18x | 18,0x (36.000.056 / 2.000.000) |
| Tempo do laço / tempo vetorizado | ~100x | 12,5x (94,10 ms / 7,53 ms) |
| Tempo da compreensão / tempo do laço | ~0,8 | 0,83 (77,88 ms / 94,10 ms) |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->
A maior diferença foi no tempo vetorizado: previsto ~100x, medido 12,5x. A memória bateu: a lista usa 36 B por elemento, 8 B do ponteiro + 28 B do objeto int, contra 2 B do uint16, o que dá 18x. O vetorizado ganhou menos que o esperado porque a conta c * 600 / 4095 é muito simples, então o laço já gasta pouco por elemento, e o vetorizado ainda paga a conversão com astype e cria arrays temporários, provavelmente. A compreensão ficou perto do laço (0,83) porque as duas fazem a mesma conta em Python, e a compreensão só evita o append. O map com lambda foi o mais lento (106 ms) porque chama uma função Python por elemento.
uint16 * 20 dá 16364 porque 4095 * 20 = 81900 não cabe em 16 bits (máximo 65535), e o NumPy dá a volta: 81900 - 65536 = 16364. Para contagens eu escolheria uint16 (0 a 4095, 2 B por valor). Para pressões em kPa eu escolheria float64: uso float32 só se a memória for um problema, porque a precisão dele é menor e pode se acumular em somas longas.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | numpy.float64 | SerieTemporal |
| `s[0]` | numpy.float64 | numpy.float64 |

<!-- Explique o resultado que mais surpreendeu você. -->
O que mais me surpreendeu foi o s.sum() devolver uma SerieTemporal e não um número comum. É por isso que o marco1.py usa float(...) ao imprimir, já o s[0] volta como float64, um escalar do NumPy.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
- Sintoma: media_movel(30) sobre PT102 (600 leituras) devolvia 570 valores; a docstring prevê 571.
- Testes de regressão: test_media_movel_quantidade_de_valores (3 != 4), test_media_movel_janela_igual_ao_tamanho (0 != 1), test_media_movel_valores e test_media_movel_janela_1_devolve_a_propria_serie.
- Causa: acumulada[i] inclui self[i]. A soma da janela i é acumulada[i+janela-1] − acumulada[i-1], mas o código usava acumulada[i+janela] − acumulada[i], deslocando tudo um ponto e perdendo a primeira janela.
- Correção: um 0 no início da soma acumulada (faz o papel de acumulada[-1]) e .view(SerieTemporal), porque o concatenate devolve ndarray.
- Por que a aceitação não pegou: test_media_movel_tipo_e_erros só confere o tipo e os ValueError (janela 0 e 6); o outro uso só confere que self não muda. Nenhum confere tamanho nem valores.
- Caso não coberto: janela == len(serie) (devolvia 0 valores); coberto por test_media_movel_janela_igual_ao_tamanho.