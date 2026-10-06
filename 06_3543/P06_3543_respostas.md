# Aula 06 - Análise de Complexidade 

## Complexidade Amortizada para `desenfileirar()`

A operação `desenfileirar()` na fila encadeada pode custar $O(N)$ no pior caso em uma chamada isolada, isto ocorre quando a *pilha de saída* está vazia e há $N$ elementos acumulados na *pilha de entrada*, exigindo a transferência de todos os itens de uma pilha para a outra para inverter a ordem.
No entanto, o custo amortizado (caso médio por operação) é $O(1)$, pois cada elemento passa por operações de custo constante $O(1)$ ao longo de toda a sua permanência na fila, em especial quando é execultado `desenfileirar()`, o elemento do topo da *pilha de saida* é o primeiro elemento da fila, requisitando apenas uma operação de custo $O(1)$