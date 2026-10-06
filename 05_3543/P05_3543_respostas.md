### QUESTÃO 1

`Funcioário` herda de `Pessoa` *nome* e *idade*, assim como `Gerente`, `Chefe de cozinha` e `Garçom` herdam de `Funcionário` tando *nome* e *idade*, quanto *salario* e *carga_horaria*.

- Pessoa
    - Funcionário (herda nome, idade)
        - Gerente (herda nome, idade, salario, carga_horaria)
        - Chefe de cozinha (herda nome, idade, salario, carga_horaria)
        - Garçom (herda nome, idade, salario, carga_horario)

`Pizzaria` herda de `Restaurante` *nome*, *endereco* e *telefone*, visto que é uma especificação de um tipo de restaurante.

- Restaurante
    - Pizzaria (herda nome, endereco, telefone)

Por fim, `Bolo` e `Pizza` herdariam *nome*, *preco* de `Iguaria`, pois são tipos de iguarias.

- Iguaria
    - Bolo (herda nome, preco)
    - Pizza (herda nome, preco)



## QUESTÃO 2

A relação de `Restaurante` e `Iguaria` foi estabelecida através de uma nova classe `Menu`, possuindo as funções *+adiciona_iguaria(list(Iguaria))* e *+remove_iguaria(list(Iguaria))*. `Menu` possui uma relação de composição com `Restaurante` e de agregação com `Iguaria`.



## QUESTÃO 3

#### argumento1
Uma instância da classe `Iguaria`, já que só precisa do nome e preço. Assim, a função `anotar_pedido` poderia retornar uma lista de instâncias de `Iguaria`.

#### argumento2
Uma lista de instâncias de `Iguaria` ( `list(Iguaria)` ), como a lista retornada por `anotar_pedido`. Desse modo, uma lista permite que várias iguarias sejam preparadas ao mesmo tempo, evitendo que a função seja chamada repetidas vezes.

#### argumento3
A função `demitir` do gerente precisa receber a classe Funcionário, visto que engloba instâncias de `Garçom`, `Chefe de cozinha` e `Gerente`.