Respostas:

O código das duas questões está em P07_3487_labirinto.py:

python P07_3487_labirinto.py              # labirinto 10x14 com semente aleatória
python P07_3487_labirinto.py 15 30 42     # 15x30 com semente 42
python P07_3487_labirinto.py testes       # testes que usei nas respostas abaixo

A geração e a busca usam só a biblioteca padrão. O maze_builder.py só entra nos testes que comparam com a versão recursiva, e precisa estar na mesma pasta do P07_3487_labirinto.py. 
Se não estiver, o import falha, esses testes são pulados e o resto roda normal.

Questão 1:
Na dfs do maze_builder.py, quem guarda "onde eu estava" é a pilha de chamadas do Python. Cada chamada dfs(x, y) deixa guardada a sala e até que ponto o for das direções já foi. 
Na versão iterativa (dfs_iterativo) eu faço isso na mão, com uma lista pilha em que cada item é [x, y, ordem, k].

O visita(x, y) faz o que o começo da dfs(x, y) fazia: abre a sala, embaralha as direções e empilha a sala com k = 0. O while olha sempre o topo da pilha. 
Se k já passou pelas 4 direções, desempilha, que é o mesmo que o return. Se não, testa a direção k; se o vizinho ainda for parede, derruba a parede do meio e chama visita no vizinho, 
que é o equivalente à chamada recursiva.

Como o topo da pilha é sempre a sala mais recente que ainda tem direção para testar, a ordem das salas é a mesma da recursão. Para conferir, deixei a opção igual_ao_original=True 
(explico abaixo por que ela existe) e comparei com o generate_maze original usando a mesma semente. Comparei só as paredes, 
porque o queijo muda de lugar por causa da correção do problema 2. Em 352 comparações com tamanhos aleatórios os labirintos saíram idênticos. 
Outros 148 sorteios foram pulados porque o original deu erro (também é o problema 2).

Fiz iterativo por causa do limite de recursão do Python, que por padrão é de 1000 chamadas. A dfs faz corredores bem compridos antes de voltar, 
então a pilha fica muito alta (medi uma altura máxima média de 467 no 30x30 (900 salas) e de 1134 no 50x50 (2500 salas)). Por isso, no teste 3, 
o original já deu RecursionError no 50x50, enquanto a versão iterativa gerou um 200x200 em menos de 0,1 s.

Testando, encontrei dois problemas no maze_builder.py.

1. A lista directions é a mesma para todas as chamadas. O random.shuffle(directions) embaralha a lista que o for das chamadas de cima ainda está percorrendo. 
Quando uma chamada volta da recursão, o for dela continua do índice onde tinha parado, só que numa lista que foi embaralhada de novo lá embaixo. 
Aí ela pode testar uma direção duas vezes e pular outra. Se o vizinho pulado não for alcançado por outro lado, 
a sala fica fechada (aparece como um bloco de parede 3x3) e o labirinto deixa de ser "perfeito" como diz o comentário do arquivo. 
Em 3000 labirintos de tamanhos aleatórios isso aconteceu em 567, quase 19%.

Na minha versão, cada item da pilha guarda a sua própria cópia embaralhada (directions[:]), e nenhum dos 3000 labirintos teve sala fechada. 
Conferi também que todos tinham exatamente m*n - 1 paredes derrubadas, que é o número de arestas de uma árvore com m*n vértices, ou seja, 
o labirinto é mesmo uma árvore que passa por todas as salas. Uso essa versão por padrão. A opção igual_ao_original=True só serve para o teste de comparação.

2. A coluna do queijo é sorteada com 2 * m. A linha j = int(random.uniform(0, 2 * m)) deveria usar 2 * n. Com m < n o queijo nunca cai na parte da direita 
(no exemplo 10x14 do arquivo ele nunca passa da coluna 19, de 29), e com m > n pode sair uma coluna que não existe e o programa quebra com IndexError. 
Na minha versão já está 2 * n.

Questão 2:
Pensei no labirinto como um grafo: cada célula que não é parede é um vértice, ligado às células abertas logo acima, abaixo, à esquerda e à direita. 
A busca começa em (1, 1) e para quando chega na célula do queijo. Durante a busca, guardo num dicionário veio_de de qual célula cada uma foi descoberta. 
Quando acho o queijo, volto pelo veio_de até (1, 1) e inverto a lista (monta_caminho).

A função mostra_labirinto desenha o resultado no terminal. Exemplo com python P07_3487_labirinto.py 8 12 42:
Labirinto 8x12 gerado com a dfs iterativa (semente 42)

##################################################
##R ##    Q o o o o         ##o o o o o         ##
##o ##########  ##o ##  ######o ######o ######  ##
##o o o o o ##  ##o ##  ##o o o ##  ##o o o ##  ##
##########o ##  ##o ######o ######  ######o ######
##  ##o o o ##  ##o o o o o             ##o o o ##
##  ##o ######################################o ##
##  ##o ##    o o o o o o o ##o o o o o o o ##o ##
##  ##o ######o ##########o ##o ##########o ##o ##
##  ##o ##o o o ##o o o o o ##o o o ##o o o ##o ##
##  ##o ##o ######o ##############o ##o ######o ##
##  ##o ##o o o ##o o o o o o o o o ##o ##o o o ##
##  ##o ##  ##o ######################o ##o ######
##o o o ##  ##o o o ##  ##      ##o o o ##o o o ##
##o ##############o ##  ##  ##  ##o ##########o ##
##o o o o o o o o o ##      ##    o o o o o o o ##
##################################################

R = rato em (1, 1)   Q = queijo   o = caminho   ## = parede
Queijo na posição (1, 5), caminho com 140 passos
Células visitadas pela BFS: 185 (a DFS, só para comparar, visitaria 163)

Por que busca em largura (BFS):
Usei BFS, com um deque como fila (busca_largura). A BFS visita as células em ordem de distância até o início: primeiro todas a 1 passo, depois todas a 2 passos, e assim por diante. 
Então a primeira vez que ela chega no queijo é por um caminho mais curto possível, em qualquer labirinto.

Mas nesse gerador isso não faz diferença, e eu quis ver isso nos números. Como o labirinto é uma árvore, só existe um caminho entre (1, 1) e o queijo, 
e qualquer busca que não repete célula acha esse mesmo caminho. Implementei também a versão com pilha (busca_profundidade) e comparei as duas em 1000 labirintos de cada tamanho (teste 4):

tamanho	 passos em média  visitadas pela BFS (média)  visitadas pela DFS (média)  quem visitou menos
10x14	 98,4	          138,7	                      137,9	                  DFS em 648, BFS em 208
30x30	 547,1	          938,1	                      919,3	                  DFS em 728, BFS em 251

As duas acharam exatamente o mesmo caminho nos 2000 labirintos, e a DFS visitou menos células na maioria das vezes. 
A BFS precisa passar por todas as células que estão mais perto do rato do que o queijo, em todas as direções. Já a DFS segue um corredor até o fim e, 
quando escolhe o corredor certo, chega sem olhar o resto. Na média as duas ficaram quase iguais, porque quando a DFS escolhe o corredor errado ela percorre o galho inteiro antes de voltar.

Para esse gerador, então, a DFS também serviria. O que me fez ficar com a BFS foi o teste 5. Nele abri algumas paredes a mais (10% do número de salas) para o labirinto ter ciclos, 
e aí passa a existir mais de um caminho até o queijo:

tamanho	passos em média (BFS)	passos em média (DFS)	DFS achou caminho mais longo
10x14	40,9	                79,2	                em 414 de 500
30x30	102,6	                393,5	                em 481 de 500

A DFS continua achando um caminho, mas é o primeiro que ela encontra seguindo os corredores, e ele pode ser bem mais longo. A BFS continua devolvendo o menor. 
No labirinto perfeito a BFS visitou no máximo uns 2% de células a mais que a DFS, na média. Como esse custo extra é pequeno, 
preferi a busca que garante o caminho mais curto sem depender de o labirinto ser uma árvore.

Nas duas buscas cada célula é expandida uma vez só e tem no máximo 4 vizinhas, então tanto o tempo quanto a memória ficam O(m·n).