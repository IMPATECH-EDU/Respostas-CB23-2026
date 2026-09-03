A operação de desenfileirar na estrutura de fila baseada em duas pilhas possui **complexidade de tempo amortizada $O(1)$**, apesar de algumas vezes apresentar um custo individual de $O(N)$ no pior caso. Na análise amortizada o custo médio é estimado para cada operação ao longo de toda a sequência de chamadas para mostrar que operações caras e pouco frequentes são cobertas por uma sequência de operações baratas.

**O Mecanismo de Funcionamento**

A fila gerencia o fluxo de dados dividindo o trabalho entre duas pilhas encadeadas: a pilha de `entrada` e a pilha de `saida`.

* **Enfileirar (`enfileirar`):** Insere o elemento no topo da pilha de `entrada` em tempo $O(1)$.
* **Desenfileirar (`desenfileirar`):** Remove o elemento do topo da pilha de `saida`. Se a pilha de `saida` estiver vazia, executa o método `mover_se_necessario()`, que desempilha todos os itens da `entrada` e os empilha na `saida`, invertendo a ordem dos dados para garantir que o primeiro a entrar na lista de entrada, seja o primeiro a sair na lista de saída.

**O Ciclo de Vida de um Elemento**

Para explicar a complexidade amortizada, pode-se analisar quantas operações de pilha cada elemento sofre do momento em que entra na fila até o momento em que é removido:

* **1. Inserção na Entrada:** 1 operação de `push` na pilha de `entrada` (ao enfileirar).
* **2. Desempilhamento da Entrada:** 1 operação de `pop` na pilha de `entrada` (durante a transferência).
* **3. Empilhamento na Saída:** 1 operação de `push` na pilha de `saida` (durante a transferência).
* **4. Remoção Definitiva:** 1 operação de `pop` na pilha de `saida` (ao desenfileirar).

**A Contabilidade do Custo Amortizado**

Cada elemento passa por exatamente **4 operações primitivas de pilha** ao longo de toda a sua permanência na estrutura.

Quando a pilha de `saida` fica vazia e a fila precisa mover $N$ elementos da `entrada` para a `saida`, essa chamada específica de `desenfileirar` executa $2N$ operações e leva tempo $O(N)$. No entanto, essa transferência custosa garante que as próximas $N - 1$ chamadas para `desenfileirar` sejam executadas em tempo direto $O(1)$, pois o elemento da frente já estará pronto no topo da pilha de `saida`.

Ao somar o custo de enfileirar e desenfileirar $N$ elementos, o total de operações de pilha realizadas é $4N$. Dividindo o custo total pelo número de elementos ($4N / N$), obtém-se uma média de 4 operações por item. Como 4 é uma constante independente de $N$, a complexidade amortizada da operação `desenfileirar` é constante: **$O(1)$**.