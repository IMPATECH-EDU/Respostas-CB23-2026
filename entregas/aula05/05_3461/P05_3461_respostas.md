## Resposta da Questão 1

Baseado nas características em comum das classes, podemos estruturar:

- **Pessoa** seria uma classe base. Ela possui os atributos `nome` e `idade`.
  - **Funcionario** seria uma subclasse de `Pessoa`, herdando os atributos `nome` e `idade` e acrescentando `salario` e `carga_horaria`.
    - **Garçom** seria uma subclasse de `Funcionario`, herdando `nome`, `idade`, `salario` e `carga_horaria`. Além disso, possui o método `anotar_pedido()`.
    - **Chefe de cozinha** seria uma subclasse de `Funcionario`, herdando `nome`, `idade`, `salario` e `carga_horaria`. Além disso, possui o método `preparar()`.
    - **Gerente** seria uma subclasse de `Funcionario`, herdando `nome`, `idade`, `salario` e `carga_horaria`. Além disso, possui o método `demitir()`.

- **Restaurante** seria uma classe base, possuindo os atributos `nome`, `endereco` e `telefone`.
  - **Pizzaria** seria uma subclasse de `Restaurante`, herdando esses três atributos e acrescentando o atributo `rodizio`.

- **Iguaria (comida)** seria uma classe base, possuindo os atributos `nome` e `preco`.
  - **Pizza** seria uma subclasse de `Iguaria`, herdando `nome` e `preco` e acrescentando o atributo `borda_recheada`.
  - **Bolo** seria uma subclasse de `Iguaria`, herdando `nome` e `preco` e acrescentando o atributo `formato`.

Assim, as principais hierarquias de herança seriam:

**Pessoa → Funcionario → Garçom / Chefe de cozinha / Gerente**

**Restaurante → Pizzaria**

**Iguaria → Pizza / Bolo**

## Resposta da Questão 2

A relação natural entre `Restaurante` e `Iguaria` pode ser moldada por meio de uma nova classe **Cardápio**.

A classe `Cardápio` teria um atributo, por exemplo, `itens: list[Iguaria]`, responsável por armazenar as iguarias oferecidas pelo restaurante. Dessa forma, o `Restaurante` poderia possuir um `Cardápio`, e o `Cardápio` manteria uma coleção de objetos da classe `Iguaria`.

Essa solução evita criar uma relação direta entre `Restaurante` e cada tipo específico de comida e permite que o mesmo modelo seja utilizado para diferentes restaurantes.

A relação entre `Restaurante` e `Cardápio` deve ser representada como uma **composição opcional**, pois um restaurante pode possuir um cardápio, mas a quantidade de cardápios associados poderia ser zero ou um, dependendo da modelagem adotada (restaurantes que só vendem comida no peso).

Já a relação entre `Cardápio` e `Iguaria` seria melhor representada como uma **associação ou agregação**, pois uma iguaria pode existir independentemente de um determinado cardápio. Por exemplo, uma `Pizza` pode ser cadastrada como uma iguaria e posteriormente ser incluída em um ou mais cardápios.

Em geral, a estrutura seria:

- `Restaurante` → possui um `Cardápio`;
- `Cardápio` → possui uma lista de `Iguaria`;
- `Iguaria` → possui como subclasses `Pizza` e `Bolo`.

## Resposta da Questão 3

Os tipos dos argumentos podem ser definidos de acordo com a função de cada método:

- `argumento1: list[Iguaria]` — utilizado pelo método `anotar_pedido()` da classe `Garçom`. Um pedido pode conter uma ou mais iguarias, como pizzas e bolos, portanto uma lista de objetos `Iguaria` é adequada para representar os itens do pedido.

- `argumento2: Iguaria` — utilizado pelo método `preparar()` da classe `Chefe de cozinha`. O método representa a preparação de uma iguaria específica, que pode ser uma instância de `Pizza`, `Bolo` ou outra futura subclasse de `Iguaria`.

- `argumento3: Funcionario` — utilizado pelo método `demitir()` da classe `Gerente`. O gerente deve receber como argumento um funcionário que será demitido. Como `Garçom`, `Chefe de cozinha` e `Gerente` são subclasses de `Funcionario`, o argumento pode receber uma instância dessas classes, conforme as regras do sistema.