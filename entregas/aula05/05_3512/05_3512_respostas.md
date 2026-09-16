# Aula 5 - Orientação a Objetos e UML

## Questão 1 - Relações de herança

As classes podem ser organizadas em uma hierarquia de herança de acordo com a relação "é um".

A classe `Pessoa` pode ser a classe base de `Funcionário`, pois todo funcionário é uma pessoa. Dessa forma, `Funcionário` herda de `Pessoa` os atributos `nome` e `idade` e acrescenta os atributos específicos `salario` e `carga_horaria`.

As classes `Garçom`, `Chefe de Cozinha` e `Gerente` podem herdar de `Funcionário`, pois todas representam tipos específicos de funcionários. Assim, elas herdam os atributos definidos em `Pessoa` e `Funcionário` e acrescentam seus próprios comportamentos:

- `Garçom`: método `anotar_pedido(...)`;
- `Chefe de Cozinha`: método `preparar(...)`;
- `Gerente`: método `demitir(...)`.

A classe `Pizzaria` pode herdar de `Restaurante`, pois uma pizzaria é um tipo específico de restaurante. Ela herda os atributos `nome`, `endereco` e `telefone` e acrescenta o atributo `rodizio`.

A classe `Iguaria` pode ser usada como classe base para `Pizza` e `Bolo`, pois ambos são tipos de comida que podem possuir `nome` e `preco`. Dessa forma:

- `Pizza` herda `nome` e `preco` e acrescenta `borda_recheada`;
- `Bolo` herda `nome` e `preco` e acrescenta `formato`.

## Questão 2 - Relação entre Restaurante e Iguaria

A relação entre `Restaurante` e `Iguaria` pode ser modelada por meio de um `Cardapio`.

Cada restaurante possuiria um cardápio contendo várias iguarias disponíveis. Para isso, pode ser criada a classe `Cardapio`, responsável por armazenar uma coleção de objetos do tipo `Iguaria`.

A relação entre `Restaurante` e `Cardapio` pode ser tratada como composição, pois o cardápio pertence ao restaurante e faz parte da sua estrutura. Já a relação entre `Cardapio` e `Iguaria` pode ser tratada como agregação, pois uma iguaria pode existir independentemente de um cardápio específico e pode até aparecer em diferentes cardápios.

Também é útil criar uma classe `Pedido`, que represente um conjunto de iguarias solicitadas por um cliente. Essa classe facilita a representação dos métodos utilizados pelo garçom e pelo chefe de cozinha.

Assim, uma possível organização seria:

- um `Restaurante` possui um `Cardapio`;
- um `Cardapio` contém várias `Iguaria`;
- um `Garçom` cria ou registra um `Pedido`;
- um `Pedido` contém uma ou mais `Iguaria`;
- um `Chefe de Cozinha` recebe um `Pedido` para preparar seus itens.

## Questão 3 - Tipos dos argumentos

### argumento1 - `Garçom.anotar_pedido(argumento1)`

O `argumento1` pode ser do tipo `Cardapio`.

O garçom precisa conhecer as opções disponíveis no restaurante para registrar o que foi solicitado pelo cliente. A partir do cardápio, o método pode selecionar as iguarias desejadas e produzir um objeto do tipo `Pedido`.

Portanto, uma assinatura possível seria:

```python
anotar_pedido(cardapio: Cardapio) -> Pedido
```

### argumento2 - `ChefeDeCozinha.preparar(argumento2)`

O `argumento2` pode ser do tipo `Pedido`.

O chefe de cozinha precisa receber as informações sobre os itens que devem ser preparados. Como o pedido reúne as iguarias solicitadas, ele é uma representação adequada para esse argumento.

Uma assinatura possível seria:

```python
preparar(pedido: Pedido)
```

### argumento3 - `Gerente.demitir(argumento3)`

O `argumento3` deve ser do tipo `Funcionário`.

O método representa a demissão de uma pessoa que trabalha no restaurante. Como `Garçom`, `Chefe de Cozinha` e outros funcionários são subclasses de `Funcionário`, o uso do tipo base permite que o método receba qualquer uma dessas subclasses.

Uma assinatura possível seria:

```python
demitir(funcionario: Funcionario)
```
