## 1. Relações de herança entre as classes

As relações de herança identificadas são:

* `Funcionario` herda de `Pessoa`.
* `Garcom` herda de `Funcionario`.
* `ChefeDeCozinha` herda de `Funcionario`.
* `Gerente` herda de `Funcionario`.
* `Pizza` herda de `Iguaria`.
* `Bolo` herda de `Iguaria`.
* `Pizzaria` herda de `Restaurante`.

A classe `Pessoa` é uma classe base porque representa características comuns a uma pessoa, como nome e idade. `Funcionario` é uma classe base intermediária, pois herda de `Pessoa` e serve de base para os diferentes cargos do restaurante.

As classes `Garcom`, `ChefeDeCozinha` e `Gerente` são subclasses de `Funcionario`. Elas herdam nome, idade, salário e carga horária, além de possuírem seus próprios métodos.

A classe `Iguaria` é uma classe base para os alimentos. As classes `Pizza` e `Bolo` herdam seus atributos nome e preço e acrescentam características específicas, como borda recheada e formato.

Por fim, `Restaurante` é a classe base para estabelecimentos de alimentação, e `Pizzaria` é uma especialização que herda seus atributos e acrescenta o atributo `rodizio`.




## 2. Relação entre Restaurante e Iguaria

A relação entre `Restaurante` e `Iguaria` pode ser modelada como uma agregação, pois um restaurante possui um conjunto de iguarias em seu cardápio.

Em UML, essa relação seria representada por um losango branco no lado de `Restaurante`, com multiplicidade `0..*` no lado de `Iguaria`. Isso significa que um restaurante pode possuir zero ou várias iguarias.

A classe `Restaurante` poderia possuir um atributo:

cardapio: List[Iguaria]


Esse atributo armazenaria as iguarias oferecidas pelo restaurante. Também poderia existir um método `adicionar_iguaria(iguaria: Iguaria)` para adicionar novos itens ao cardápio.

A agregação é adequada porque uma iguaria pode existir independentemente de um restaurante. Por exemplo, uma pizza pode ser criada e depois adicionada ao cardápio de um restaurante.

As classes `Pizza` e `Bolo` seriam subclasses de `Iguaria`, podendo ser armazenadas na mesma lista devido ao polimorfismo.




## 3. Tipos dos argumentos

Os tipos sugeridos para os argumentos são:

* argumento1: `List[Iguaria]`.
* argumento2: `Iguaria`.
* argumento3: `Funcionario`.

O argumento1 é utilizado no método `anotar_pedido()` da classe `Garcom`. Como um pedido pode conter várias comidas, é adequado utilizar uma lista de objetos `Iguaria`. Essa lista pode conter instâncias de `Pizza`, `Bolo` ou outras subclasses de `Iguaria`.

O argumento2 é utilizado no método `preparar()` da classe `ChefeDeCozinha`. O tipo `Iguaria` é apropriado porque o chefe prepara comidas. Utilizar a classe base permite que o método receba diferentes tipos de iguaria por meio de polimorfismo.

O argumento3 é utilizado no método `demitir()` da classe `Gerente`. Como o gerente demite funcionários, o tipo apropriado é `Funcionario`. Dessa forma, o método pode receber qualquer funcionário, incluindo objetos das subclasses `Garcom`, `ChefeDeCozinha` e `Gerente`.

Esses tipos são mais adequados do que utilizar tipos primitivos, como `str` ou `int`, pois os métodos trabalham com objetos que possuem atributos e comportamentos próprios.

