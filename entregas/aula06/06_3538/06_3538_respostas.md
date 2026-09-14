### Justificativa: Complexidade Amortizada O(1) do método `desenfileirar`

A operação `desenfileirar` possui complexidade de tempo **O(1) amortizada** porque cada elemento passa por um número fixo e constante de operações durante todo o seu ciclo de vida na estrutura. 

Analisando o fluxo de um único item, ele sofre, no máximo, 4 operações básicas:
1. Um `push` na `pilha_entrada` (quando é enfileirado).
2. Um `pop` da `pilha_entrada` (durante a transferência).
3. Um `push` na `pilha_saida` (durante a transferência).
4. Um `pop` da `pilha_saida` (quando é finalmente desenfileirado e removido).

Embora uma chamada específica do `desenfileirar` possa disparar o laço `while` e levar tempo O(n) para transferir os itens (o pior caso isolado), esse custo pesado ocorre apenas quando a `pilha_saida` esvazia. O esforço dessa transferência é distribuído (amortizado) entre as operações subsequentes de `desenfileirar`, que acontecerão em tempo imediato O(1). Como o custo total de manipulação por elemento nunca passa de 4 operações, a complexidade média a longo prazo se mantém constante em O(1).