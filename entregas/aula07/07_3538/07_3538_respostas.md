# Respostas - Aula 07: Resolução de Labirintos

## Questão 2: Discussão Teórica sobre a Escolha do Algoritmo de Busca

Para encontrar o caminho da posição inicial até o queijo, utilizei a **Busca em Largura (BFS - Breadth-First Search)**.

### Motivos da Escolha:

1. **Garantia de Caminho Mínimo:** A Busca em Largura explora o grafo em "camadas" concentradas a partir do ponto de origem. Em estruturas de custo uniforme (onde cada passo entre salas adjacentes tem peso 1), a BFS garante matematicamente que a primeira vez que o nó objetivo é alcançado, ele corresponde ao caminho com o **menor número de passos**.
2. **Evita Aprofundamento Desnecessário:** A Busca em Profundidade (DFS) poderia seguir por um ramo longo e sem saída antes de avaliar uma solução mais curta que estivesse próxima ao ponto inicial.
3. **Comportamento em Labirintos Perfeitos:** Labirintos "perfeitos" possuem exatamente um caminho único entre quaisquer dois pontos (estrutura de árvore geradora). A BFS percorre essa estrutura sem risco de estourar a pilha de execução, utilizando uma fila FIFO.