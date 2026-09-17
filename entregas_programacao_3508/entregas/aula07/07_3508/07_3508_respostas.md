# Aula 7 - Respostas

Na questão 2 eu usei busca em profundidade (DFS) de forma iterativa.

A busca começa na posição `(1, 1)` e usa uma pilha para guardar as próximas posições que devem ser visitadas. Para evitar visitar a mesma posição várias vezes, também é mantido um conjunto de posições já visitadas. Além disso, para cada posição visitada é guardada a posição anterior. Quando o queijo é encontrado, essas referências são usadas para reconstruir o caminho desde o queijo até o início.

Escolhi DFS porque o labirinto gerado é um labirinto perfeito, ou seja, existe apenas um caminho entre dois pontos. Nesse caso, não é necessário usar BFS para procurar um caminho menor, já que o caminho entre a entrada e o queijo é único. A DFS também mantém a mesma ideia usada na geração do labirinto da questão 1.
