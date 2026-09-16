### 1.

As classes poderiam ser organizadas na seguinte hierarquia de herança:

* Pessoa

  * Funcionário

    * Gerente
    * Chefe de Cozinha
    * Garçom
* Restaurante

  * Pizzaria
* Iguaria

  * Bolo
  * Pizza

A classe Funcionário herda os atributos nome e idade de Pessoa. Por sua vez, Gerente, Chefe de Cozinha e Garçom herdam de Funcionário atributos como salário e carga horária, além dos atributos que Funcionário já herdou de Pessoa.

A classe Pizzaria herda de Restaurante atributos como nome, endereço e telefone.

Por fim, Bolo e Pizza herdam de Iguaria atributos como nome e preço.

### 2.

Eu modelaria a relação entre Restaurante e Iguaria por meio de uma agregação, pois uma iguaria pode existir independentemente de um restaurante.

A classe Restaurante poderia possuir um atributo que armazena uma coleção de referências para objetos do tipo Iguaria, representando as opções oferecidas pelo restaurante. Dessa forma, um restaurante poderia possuir várias iguarias e a mesma iguaria poderia estar associada a diferentes restaurantes.

Caso fosse necessário armazenar informações específicas da relação, como o preço de determinada iguaria em cada restaurante, poderia ser criada uma classe intermediária, como ItemCardapio, relacionando um Restaurante a uma Iguaria e armazenando essas informações adicionais.

## 3.

- argumento1: list[Iguaria]
- argumento2: Iguaria
- argumento3: Funcionario

O argumento1 do método anotar_pedido() poderia ser uma lista de objetos da classe Iguaria, pois um pedido pode conter uma ou mais comidas.

O argumento2 do método preparar() seria uma instância de Iguaria, já que o chefe de cozinha prepara uma determinada comida.

O argumento3 do método demitir() seria uma instância de Funcionario, pois o gerente deve receber como argumento o funcionário que será demitido. Como Garçom e Chefe de Cozinha são subclasses de Funcionario, objetos dessas classes também poderiam ser passados para o método.