A função desenfileirar pode custar complexidade O(n) no caso em que a pilha exit está vazia e entrance não,
fazendo necessário mover todos os elementos de entrance para exit. Contudo, um elemento é transferido entre
duas pilhas somente um máximo de uma vez ao longo de sua vida na estrutura, e como sempre que houver elementos em exit o custo é O(1), frequentemente o custo será O(1), tornando assim a complexidade da função O(n) no pior caso mas O(1) amortizada.
