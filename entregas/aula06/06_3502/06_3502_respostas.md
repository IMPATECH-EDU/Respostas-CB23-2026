Assuma n como o comprimento da fila/pilha 

Classe Pilha: 

    Todas as funções fazem busca, O(1).

    Função push:
        Cria Nó, O(1);
        Muda ponteiro, O(1);
        Soma 1 ao comprimento, O(1).

    Função pop:
        Faz comparação, O(1);
        Muda ponteiro, O(1);
        Subtrai 1 do comprimento, O(1).

    Função topo:
        Faz comparação, O(1).

    Função esta_vazia:
        Faz comparação, O(1).

    Função len:
        Faz busca, O(1).

    Função repr:
        Percorre toda a lista fazendo:
            Comparação, O(1);
            Criando string, O(1);
            Mudando ponteiro, O(1).

        Portanto possui complexidade O(n).

Classe FilaEncadeada: 

    Todas as funções fazem busca, O(1).

    Função enfileirar:
        Chama função push, O(1);
        Soma 1 ao comprimento, O(1).

    Função transferir:
        Percorre toda a atual lista entrada fazendo:
            Chamando esta_vazia, O(1);
            Comparação, O(1);
            Chamando push e pop, O(1).

        Portanto possui complexidade O(comprimento da lista entrada) = O(n).
        
    Função desenfileirar:
        Faz comparação, O(1);
        Subtrai 1 do comprimento, O(1);
        Chama a função pop, O(1);
        Caso esteja vazia, chama a função transferir, O(comprimento da lista entrada) = O(n).

        Possui complexidade O(1) amortizado pois chama a função transferir somente quando está vazia e porqu todo elemento é transferido uma única vez.

    Função frente:
        Faz comparação, O(1);
        Caso esteja vazia, chama a função transferir, O(comprimento da lista entrada) = O(n).

        Possui complexidade O(1) amortizado pois chama a função transferir somente quando está vazia e porque todo elemento é transferido uma única vez.

    Função esta_vazia:
        Faz comparação, O(1).

    Função len:
        Faz busca, O(1).

    Função repr:
        Faz multiplos laços, entretanto, a complexidade do interior de cada laço é sempre O(1), portanto possui complexidade O(n)