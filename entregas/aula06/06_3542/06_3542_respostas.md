\# Análise de Complexidade e TADs - Aula 06

\*\*Matrícula:\*\* 3542



\---



\## 1. Análise de Complexidade Amortizada da Fila (Dois Stacks)



A classe `FilaEncadeada` foi implementada utilizando o paradigma de composição com duas instâncias do TAD `PilhaEncadeada`:

\* `\_pilha\_entrada`: Armazena os elementos recém-enfileirados (`enfileirar`).

\* `\_pilha\_saida`: Mantém os elementos prontos para desfileirar na ordem correta FIFO (`desenfileirar` / `frente`).



\### Por que `desenfileirar` é O(1) Amortizado (e O(N) no Pior Caso)?



1\. \*\*Pior Caso — O(N):\*\*

&#x20;  Ocorre quando a `\_pilha\_saida` está totalmente vazia e há N elementos acumulados na `\_pilha\_entrada`. Ao chamar `desenfileirar()`, é necessário desempilhar cada um dos N elementos da `\_pilha\_entrada` e empilhá-los na `\_pilha\_saida` para inverter a ordem (de LIFO para FIFO). Esta operação isolada realiza 2N operações de pilha, custando O(N).



2\. \*\*Custo Amortizado — O(1):\*\*

&#x20;  Apesar de um único `desenfileirar` poder custar O(N), cada elemento inserido na fila passa por exatamente o mesmo ciclo de vida:

&#x20;  \* É empilhado na `\_pilha\_entrada` (1 operação O(1));

&#x20;  \* É transferido da `\_pilha\_entrada` para a `\_pilha\_saida` (1 `pop` + 1 `push` = 2 operações O(1));

&#x20;  \* É desempilhado da `\_pilha\_saida` ao ser desenfileirado (1 operação O(1)).



&#x20;  Portanto, ao longo de toda a existência da fila, cada elemento processado gera no máximo \*\*4 operações básicas de pilha\*\*, cada uma custando O(1). 

&#x20;  Dividindo o custo total de uma sequência de N operações por N, o tempo médio por operação é constante:

&#x20;  

&#x20;  Custo Amortizado = O(N) / N = O(1)

