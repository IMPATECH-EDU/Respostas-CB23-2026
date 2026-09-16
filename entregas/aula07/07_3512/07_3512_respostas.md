# Aula 7 - Busca em Labirintos

## Questão 2 - Discussão da solução

Para encontrar o caminho entre a posição inicial `(1,1)` e o queijo, utilizei uma busca em profundidade (DFS) iterativa.

A DFS foi implementada utilizando uma pilha, evitando o uso de chamadas recursivas. A posição inicial é inserida na pilha e, a cada passo, uma posição é retirada e seus vizinhos acessíveis que ainda não foram visitados são adicionados para serem explorados.

Durante a busca, foi utilizado um dicionário para armazenar a posição anterior de cada célula visitada. Quando o queijo é encontrado, essas informações permitem reconstruir o caminho percorrido do queijo até a posição inicial.

Escolhi a DFS porque o objetivo da atividade é encontrar um caminho válido até o queijo. O `maze_builder.py` gera um labirinto perfeito, no qual existe exatamente um caminho entre quaisquer dois pontos. Dessa forma, não é necessário utilizar uma busca em largura (BFS) para escolher entre diferentes caminhos mínimos: basta encontrar o caminho existente.

Para a exibição, o labirinto é copiado e as posições pertencentes ao caminho encontrado são marcadas com `.`. A posição inicial é representada por `S` e o queijo permanece representado por `*`.
