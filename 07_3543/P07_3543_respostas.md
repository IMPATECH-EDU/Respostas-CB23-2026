# Aula 07 - Respostas

## Questão 1

Foi implementada uma versão iterativa da busca em profundidade (DFS).

A implementação utiliza uma pilha para armazenar as posições que ainda
precisam ser exploradas. A cada iteração, uma posição é retirada do topo
da pilha e seus vizinhos são analisados.

Para evitar que o algoritmo visite a mesma posição várias vezes, foi
utilizado um conjunto chamado `visitados`.

Também foi utilizado um dicionário chamado `anteriores`, que armazena
qual posição levou até cada posição visitada. Essa estrutura permite
reconstruir posteriormente o caminho encontrado.

A versão é iterativa porque não utiliza chamadas recursivas da função
`dfs_iterativo`.

## Questão 2

Para encontrar o caminho entre a posição `(1, 1)` e o queijo, foi
utilizada uma busca em profundidade (DFS) iterativa.

A escolha da DFS ocorreu porque o objetivo da atividade é encontrar um
caminho válido entre dois pontos do labirinto, e a DFS é adequada para
percorrer estruturas representadas como grafos. O labirinto pode ser
interpretado como um grafo, no qual cada posição livre representa um
vértice e cada movimento possível entre posições vizinhas representa
uma aresta.

A utilização de uma pilha permite realizar a busca de maneira
iterativa. Quando uma posição é visitada, seus vizinhos possíveis são
adicionados à pilha. O algoritmo continua explorando as posições até
encontrar o queijo ou até que não existam mais posições para visitar.

Durante a busca, o dicionário `anteriores` registra a posição que
precedeu cada posição visitada. Quando o queijo é encontrado, esse
registro é percorrido de trás para frente para reconstruir o caminho
desde o queijo até a posição inicial. Depois, o caminho é invertido
para obter a ordem correta, partindo de `(1, 1)`.

A DFS não garante que o caminho encontrado seja o menor caminho
possível. Entretanto, para o objetivo desta atividade, ela é suficiente
para encontrar um caminho válido até o queijo e permite demonstrar a
aplicação de busca em grafos de forma iterativa.