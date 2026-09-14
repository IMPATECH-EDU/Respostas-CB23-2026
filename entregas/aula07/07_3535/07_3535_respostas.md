# Discussão Teórica — Questão 2

Para encontrar o caminho até o queijo, escolhi fazer uma **Busca em Profundidade (DFS)** de forma iterativa, utilizando uma pilha manual. Baseando minha decisão nos seguintes pontos:

* **Só existe um caminho possível:** Como o labirinto gerado é "perfeito", não existem atalhos, rotas alternativas ou ciclos, logo não seria necessário procurar entre varias opções, que é onde o BFS se destaca.

* **A pilha já me entrega o caminho pronto:** A dinâmica da pilha (`stack`) facilitou muito o rastreamento da rota:
  * Conforme fui avançando, empilhei cada coordenada percorrida.
  * Quando bati em um beco sem saída, voltei removendo a posição do topo com `.pop()`.
  * No momento em que alcancei o queijo, o conteúdo mantido na pilha era **exatamente a rota final limpa**, do ponto inicial até o objetivo, sem que eu precisasse criar estruturas extras de histórico.

* **Economia de memória:** A DFS gasta muito menos memória porque só preciso guardar o caminho atual em exploração.

* **Segurança na execução:** Optei por usar uma pilha manual dentro de um loop `while` (em vez de recursão de função) para garantir que meu código resolva labirintos de qualquer tamanho sem o risco de estourar o limite de pilha do Python (`RecursionError`).