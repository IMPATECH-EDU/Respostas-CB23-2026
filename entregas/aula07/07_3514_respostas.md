# Justificativa questão 2

* A escolha adotada na questão dois se baseia na implementação de um algoritmo de dfs (Depth First Search) e backtracking, no qual o mesmo é implementado pelo uso de pilhas.

* O motivo da escolha desse algoritmo se deve ao fato do labirinto ser perfeito, ou seja, não existir outro caminho de um vértice a até o vértice b, dessa forma, optei pelo uso do algoritmo pois minimiza o uso da memória, visto que utiliza de pilhas em sua implementação.

* Embora a utilização de um algoritmo bfs (Breadth First Search) possa ser mais rápida e encontrar caminhos melhores ainda optei pelo dfs pois como já mencionado antes, o caminho é único, portanto o mesmo sempre será o melhor. Dessa forma achei mais viável trocar velocidade por menos uso de memória, pois torna o programa mais viável e acessível para uma matriz de tamanho maior.