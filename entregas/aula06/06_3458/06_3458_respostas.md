ANÁLISE DE COMPLEXIDADE AMORTIZADA — FILA COM DUAS PILHAS

1. PIOR CASO ISOLADO: O(N)
   - Ocorre quando a pilha de saída está vazia e a de entrada contém N itens.
   - A operação precisa mover todos os N elementos da entrada para a saída.
   - Custo: N remoções + N inserções = 2N operações de pilha -> O(N).

2. CICLO DE VIDA DO ELEMENTO (O que fundamenta a análise amortizada)
   Cada elemento passa por exatamente 4 operações de pilha em toda a sua vida:
   - 1x push (inserção na pilha de entrada ao enfileirar)
   - 1x pop  (remoção da pilha de entrada durante o transporte)
   - 1x push (inserção na pilha de saída durante o transporte)
   - 1x pop  (remoção da pilha de saída ao desenfileirar)

   * Nota: A transferência (pop + push) ocorre UMA ÚNICA VEZ por elemento.

3. COMPLEXIDADE AMORTIZADA: O(1)
   - Em uma sequência de N enfileiramentos e N desenfileiramentos, executam-se
     no máximo 4N operações internas no total.
   - Custo médio por operação: 4N / 2N = 2 operações de pilha.
   - Como 2 é uma constante, a complexidade amortizada de desenfileirar() é O(1).