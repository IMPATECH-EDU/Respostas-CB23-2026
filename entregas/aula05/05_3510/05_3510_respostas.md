### Questão 1

Todo funcionário possui os atributos definidos em `Pessoa` (nome e idade), com acréscimo de salário e carga horária, logo, `Funcionário` é uma especialização de `Pessoa`. Da mesma forma, `Garçom`, `Chefe de cozinha` e `Gerente` são todas especializações separadas de `Funcionário`, pois compartilham dos atributos definidos em `Funcionário` (nome, idade, salário e carga horária), mas possuem operações próprias (`anotar_pedido`, `preparar` e `demitir`). 

- Pessoa
    - Funcionário (herda nome e idade)
        - Garçom (herda nome, idade, salário e carga horária)
        - Chefe de cozinha (herda nome, idade, salário e carga horária)
        - Gerente (herda nome, idade, salário e carga horária)

Pizzarias possuem os mesmos atributos definidos em `Restaurante`, além do  atributo `rodizio`, logo, `Pizzaria` pode herdar esses atributos de `Restaurante`

- Restaurante
    - Pizzaria (herda nome, endereço e telefone)

Da mesma forma, `Pizza` e `Bolo` ambos têm nome e preço, como instâncias de `Iguaria`, mas possuem atributos específicos, logo, são ambos especializações de `Iguaria`

- Iguaria (comida)
    - Pizza (herda nome e preço)
    - Bolo (herda nome e preço)



### Questão 2

É possível adicionar um atributo `+cardapio: dict` à classe Restaurante, implementando instâncias da classe Iguaria em um dicionário, utilizando `iguaria.nome` como chave e `iguaria.preco` como valor.  
Por exemplo:

```
restaurante.cardapio = {
    iguaria.nome: iguaria.preco
}
```

### Questão 3

#### argumento1
Uma instância da classe `Iguaria`, já que só precisa do nome e preço (instâncias de `Pizza` e `Bolo` também podem ser recebidas, já que são filhas de `Iguaria`). Assim, a função `anotar_pedido` poderia retornar uma lista de instâncias de `Iguaria` a serem usadas de argumento pela função `preparar` do chefe.

#### argumento2
Uma lista de instâncias de `Iguaria` ( `list[Iguaria]` ), como a lista retornada por `anotar_pedido`. Uma lista permite que várias iguarias sejam preparadas de uma vez, evitando que a função precise ser chamada várias vezes por pedido.

#### argumento3
Um gerente precisa poder demitir funcionários independentemente de sua função específica, logo, a função `demitir` precisa receber a classe Funcionário, que engloba instâncias de `Garçom`, `Chefe de cozinha` e `Gerente`.
