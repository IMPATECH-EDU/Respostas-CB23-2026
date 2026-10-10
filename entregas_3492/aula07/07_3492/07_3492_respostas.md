# Discussão teórica — Questão 2

## Método utilizado

Para encontrar o caminho partindo da posição `(1,1)` até o queijo, foi utilizada uma **busca em profundidade (DFS)**.

## Justificativa da escolha da DFS

A escolha da DFS é adequada porque o objetivo da questão é **encontrar um caminho** entre `(1,1)` e o queijo, sem exigir que seja encontrado o caminho com a menor quantidade de movimentos.

O labirinto gerado pelo código anterior é um **labirinto perfeito**, ou seja, existe exatamente um caminho entre quaisquer duas salas. Consequentemente, existe apenas um caminho possível entre a posição inicial e o queijo. Assim, uma busca em profundidade e uma busca em largura encontrarão o mesmo caminho final, embora possam explorar as posições do labirinto em ordens diferentes antes de chegar ao queijo.

A busca em largura (BFS) teria como principal vantagem, garantir o menor caminho em número de movimentos. Essa propriedade não é necessária neste problema, pois o labirinto já possui um único caminho entre o início e o queijo.

Por esse motivo, foi escolhida a DFS, que atende diretamente ao objetivo proposto e utiliza uma pilha para controlar a exploração das posições.

E já que ambas chegavam na mesma resposta, foi utilizada a mais simples de implementar
