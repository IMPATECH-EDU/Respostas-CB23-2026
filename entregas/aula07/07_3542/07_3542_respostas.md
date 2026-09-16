\# Resolução de Labirintos e Busca em Grafos - Aula 07

\*\*Matrícula:\*\* 3542



\---



\## Discussão Teórica: Algoritmo Utilizado para Encontrar o Caminho



Para a resolução do labirinto (encontrar o caminho da posição inicial `(1,1)` até o queijo `Q`), foi implementado o algoritmo de \*\*Busca em Largura (Breadth-First Search - BFS)\*\*.



\### Justificativa da Escolha da Busca em Largura (BFS)



1\. \*\*Garantia do Caminho Mínimo:\*\*

&#x20;  A BFS explora a grade em "camadas" ou níveis de distância a partir do ponto de partida, utilizando uma fila FIFO (`collections.deque`). Por conta dessa propriedade de expansão uniforme, a BFS garante que o primeiro caminho encontrado até o objetivo seja \*\*estritamente o mais curto\*\* em termos de número de passos.



2\. \*\*Comparação com a Busca em Profundidade (DFS):\*\*

&#x20;  A DFS (Busca em Profundidade) mergulha em um ramo até encontrar um impasse antes de retroceder. Embora encontre um caminho até o destino, esse caminho frequentemente contém desvios desnecessários e laços longos, não garantindo a menor rota possível.



3\. \*\*Conclusão:\*\*

&#x20;  Apesar de a DFS ser perfeita para a \*\*geração\*\* de labirintos perfeitos (criando caminhos longos e ramificados), a \*\*BFS\*\* é a escolha ideal para a \*\*resolução\*\*, pois assegura a rota ótima do ponto inicial até o queijo.

