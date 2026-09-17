# Aula 7 — Busca em Grafos e Resolução de Labirintos

## Questão 1 — DFS iterativo

A busca em profundidade (DFS) foi implementada de forma iterativa utilizando uma pilha (`stack`). No código original, a geração do labirinto utiliza chamadas recursivas para explorar as salas e realizar o retrocesso (backtracking).

Na versão iterativa, a pilha armazena as posições que ainda precisam ser exploradas. Enquanto houver posições na pilha, o algoritmo verifica os vizinhos disponíveis. Quando encontra uma sala não visitada, derruba a parede entre as duas salas, marca a nova sala como visitada e adiciona sua posição à pilha. Quando não existem mais vizinhos disponíveis, a posição é removida da pilha, realizando o retrocesso.

Essa abordagem reproduz o comportamento da busca em profundidade recursiva, mas sem depender da pilha de chamadas do Python.

## Questão 2 — Resolução do labirinto

Para encontrar o caminho da posição `(1,1)` até o queijo, foi utilizada a busca em profundidade iterativa (DFS).

O algoritmo começa na posição `(1,1)` e utiliza uma pilha para explorar as posições acessíveis do labirinto. Cada posição visitada é registrada em um conjunto chamado `visited`, evitando que a mesma posição seja explorada várias vezes.

Além disso, foi utilizado um dicionário chamado `parent`, que armazena a posição anterior de cada célula visitada. Dessa forma, quando o algoritmo encontra o queijo, é possível reconstruir o caminho percorrendo os pais de cada posição até retornar à posição inicial.

Depois da reconstrução, o caminho é exibido no terminal, utilizando o símbolo `*` para representar as posições percorridas.

## Escolha entre busca em profundidade e busca em largura

A busca em profundidade foi escolhida porque a atividade tem como objetivo consolidar os conceitos de DFS e sua implementação iterativa. Além disso, o labirinto utilizado é gerado por DFS com retrocesso, tornando essa estratégia coerente com a forma de geração do labirinto.

A DFS utiliza uma pilha e explora um caminho até não conseguir avançar, realizando o retrocesso quando necessário. Essa característica permite encontrar um caminho entre o início e o queijo sem precisar explorar todas as posições antes de encontrar o objetivo.

Entretanto, a DFS não garante encontrar o menor caminho em um grafo geral. Se o objetivo fosse encontrar o caminho com menor número de passos em um labirinto sem pesos, a busca em largura (BFS) seria uma alternativa adequada, pois explora as posições por níveis de distância a partir da origem.

Neste trabalho, a DFS foi escolhida principalmente pela relação com o conteúdo da aula e pela simplicidade de implementação utilizando uma pilha.

## Conclusão

A implementação realizada utiliza uma versão iterativa da busca em profundidade para gerar o labirinto e também para encontrar o caminho até o queijo. O uso da pilha substitui a recursão, enquanto o registro dos pais permite reconstruir e exibir o caminho encontrado no terminal.
