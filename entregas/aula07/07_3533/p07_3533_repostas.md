# Resolução do Labirinto via DFS com Lista Nativa

## 1. Algoritmo Utilizado
A busca pelo caminho da célula inicial `(1, 1)` até o queijo foi implementada utilizando a **Busca em Profundidade (DFS Iterativa)**. Para gerenciar os nós pendentes, utilizou-se a **`list` nativa do Python operando como uma Pilha (LIFO)** através das operações nativas `append()` e `pop()`, eliminando dependências de módulos externos ou caminhos de diretório.

## 2. Discussão Técnica da Solução

* **Aproveitamento das Listas Nativas do Python:**
  As listas em Python implementam vetores dinâmicos onde a inserção (`append`) e a remoção no final (`pop`) possuem complexidade de tempo **$O(1)$ constante**. Isso garante a mesma eficiência assintótica de uma pilha encadeada sem a complexidade de gerenciar referências de nós no mesmo arquivo.

* **Propriedade do Labirinto Perfeito:**
  Como a estrutura gerada pelo `dfs_iterative` é um labirinto perfeito (uma árvore geradora sem ciclos), existe **exatamente um único caminho simples** conectando a origem `(1, 1)` ao objetivo. Por não existirem caminhos alternativos ou laços fechados, a DFS encontra rigorosamente o mesmo trajeto que seria encontrado por uma busca em largura (BFS).

* **Desempenho e Sobrecarga de Memória:**
  A navegação iterativa evita o limite de recursão da linguagem (`RecursionError`). O dicionário `pais` armazena o histórico do caminho percorrido, permitindo reconstruir a rota exata da chegada até a origem ao término do laço principal.

## 3. Análise de Complexidade

* **Complexidade de Tempo: $\mathcal{O}(V + E)$**
  Onde $V$ é o total de células $(2m+1)(2n+1)$ e $E$ representa as passagens abertas. Cada célula do labirinto é inserida e removida da lista/pilha no máximo uma vez.
* **Complexidade de Espaço: $\mathcal{O}(V)$**
  Alocação necessária para armazenar a pilha de exploração, o conjunto de células visitadas (`set`) e o mapeamento de predecessores (`dict`).