# Respostas - Aula 07: Resolução de Labirintos

## Questão 1

Substituí a busca em profundidade (DFS) recursiva utilizada no código `maze_builder.py` por uma versão iterativa utilizando uma pilha. Enquanto existe uma célula vizinha que ainda não foi visitada, ela é adicionada à pilha e passa a ser explorada. Quando não existem mais vizinhos disponíveis, a célula é removida da pilha com `pop()`, realizando o retrocesso (backtracking).

Dessa forma, a pilha utilizada na implementação iterativa assume o papel que seria desempenhado pelas chamadas recursivas da função `dfs`, mantendo o funcionamento da busca em profundidade sem utilizar recursão.

## Questão 2

Para encontrar o caminho entre a posição inicial `(1,1)` e o queijo, utilizei uma busca em profundidade (DFS) iterativa, também utilizando uma pilha.

A escolha da DFS é adequada porque o código `maze_builder.py` gera um labirinto perfeito. Nesse tipo de labirinto existe exatamente um caminho entre quaisquer dois pontos. Portanto, depois que a DFS encontra o queijo, o caminho encontrado é necessariamente o único caminho existente entre o início e o objetivo e, consequentemente, também é o menor caminho possível.

Além disso, a DFS é suficiente para este problema porque não é necessário explorar vários caminhos diferentes para escolher o menor deles: no labirinto gerado pelo professor, não existem caminhos alternativos entre duas posições.

Se o labirinto possuísse ciclos ou diferentes caminhos entre o início e o queijo, a situação seria diferente. Nesse caso, eu escolheria a busca em largura (BFS) caso o objetivo fosse garantir o caminho com o menor número de movimentos, pois a BFS explora o grafo por níveis e encontra o menor caminho em um grafo não ponderado.
