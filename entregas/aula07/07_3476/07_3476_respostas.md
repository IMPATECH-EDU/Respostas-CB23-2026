Discussão da Solução - Questão 2

Algoritmo Utilizado:
Para encontrar o caminho da posição inicial até o queijo foi implementada uma Busca em Largura.
Justificativa:
Garantia de Caminho Mínimo: A busca em largura explora o labirinto em camadas, o que garante encontrar o caminho mais curto em grafos não ponderados. Comportamento em Labirintos Perfeitos: Embora labirintos gerados por DFS possuam uma estrutura de árvore geradora, a BFS realiza uma busca por nível, evitando explorar ramos incorretos do labirinto antes de verificar caminhos mais próximos. Se o algoritmo for aplicado a labirintos não perfeitos, a BFS continuará garantindo a menor quantidade de passos até o objetivo.