# Questões

## Questão 1
As classes apresentadas organizam-se em três árvores principais de herança.

* Hierarquia de pessoa: a classe Pessoa serve de base para Funcionário. Esta, por sua vez, é herdada pelas classes especializadas Gerente, Chefe de cozinha e Garçom.
Pessoa
├── Funcionário
    ├── Gerente
    ├── Chefe de cozinha
    └── Garçom

Hierarquia de Restaurante: A classe Restaurante serve como superclasse para Pizzaria.
Restaurante
└── Pizzaria

Hierarquia de Iguaria: A classe Iguaria atua como base para as classes Pizza e Bolo.
Iguaria
├── Pizza
└── Bolo


## Questão 2
A relação entre as classes Restaurante e Iguaria deve ser representada por meio de composição ou associação, e não por herança, visto que um restaurante "possui" iguarias.

Para modelar isso de forma eficiente, a classe Restaurante conterá um atributo (como uma lista ou dicionário) para armazenar os objetos da classe Iguaria que compõe o seu cardápio. Para associar os preços a cada item sem acoplar o valor diretamente à iguaria, pode-se criar uma classe ItemCardapio, que conterá uma referência para o objeto Iguaria e um atributo específico para o preço correspondente.


## Questão 3
* argumento 1: tipo primitivo __str__, pois o garçom anota apenas um único pedido duma vez. Como não há previamente uma classe cliente, a string é o tipo de dado que melhor modela a relação cliente-pedido.
* argumento 2: instância da classe __Iguaria__, pois o chefe só pode preparar um pedido por vez e só pode cozinhar (analogia a instanciar) uma iguaria que o restaurante de fato ofereça.
* argumento 3: lista contendo instâncias da classe Funcionário, pois o gerente pode demitir mais de uma única instância da classe Funcionário por vez.