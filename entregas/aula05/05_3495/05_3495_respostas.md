#Aula 05

**Questão 1**

Gerente, Garçom e Chefe de Cozinha são subclasses de Funcionário e herdam dessa classe base os atributos salário e carga_horaria. Além disso, Funcionário é uma subclasse de Pessoa, então Funcionário herda os atributos nome e idade da classe base Pessoa. Vale ressaltar que, como Gerente, Garçom e Chefe de Cozinha são subclasses de Funcionário, o qual é subclasse de Pessoa, eles herdam os atributos de Pessoa (nome e idade).
Pizzaria é uma subclasse da classe base Restaurante e herda dessa última os atributos nome, endereço e telefone.
Pizza e Bolo são subclasses da classe base Iguaria e herdam dessa última os atributos nome e preco.

**Questão 2**

Eu modelaria a relação entre as classes Restaurante e Iguaria da seguinte forma: A classe Restaurante pode ter um método chamado 'cardapio' que retorna uma lista, cujos itens são instâncias de Iguaria, representando quais comidas certo restaurante possui em seu cardápio.

**Questão 3**

O argumento1 seria uma lista na qual cada item seria uma instância da classe iguaria. Analisando o cenário, o argumento1 está como argumento do método anotar_pedido da classe garçom, então entende-se que o argumento seriam as informações de um pedido de algum cliente ao garçom. Considerando que um pedido de um cliente pode conter mais de um item e que os pedidos são apenas de iguarias, ou comidas, então, conclui-se que o argumento1 pode ser uma lista na qual cada item é uma instância da classe iguaria. 

O argumento2 seria uma instância da classe iguaria. Porque é argumento do método preparar que pertece a classe Chefe de cozinha, considerando que o método preparar seria para determinar o preparo de determinada iguaria e que cada iguaria tem um preparo diferente, conclui-se que o argumento seria apenas uma instância da classe iguaria.

O argumento3 seria uma instância da classe funcionário. Porque é argumento do método demitir da classe Gerente, então entende-se que esso método é para demitir alguém, e considerando que se demite uma pessoa por vez e que as pessoas sujeitas a serem demitidas são os funcionários, então o argumento3 pode ser uma instância da classe funcionário. 
