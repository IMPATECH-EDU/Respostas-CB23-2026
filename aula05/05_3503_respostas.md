1) Identifique relações de herança entre as classes. Explique como as classes poderiam ser organizadas em uma hierarquia de herança, indicando quais classes seriam classes base e quais seriam subclasses, e descreva o que seria herdado em cada caso.
-> Veja que todo funcionário é uma pessoa e recebe seus atributos . Funcionário herda (nome e idade) de Pessoa.
Cada uma das classes Gerente, Chefe de Cozinha e Garçom herda e recebe seus atributos. Herdam (salário e carga horária) de Funcionário. Ainda, cada um deles trabalha em um resturante (ou não, no caso dos gerentes), logo herdam o endereço de trabalho de Restaurante, e o telefone de onde trabalho.
Ainda, Pizzaria é um tipo de restaurante, então recebe atributos de Restaurante. Pizzaria herda nome, endereço e telefone de Restaurante.
Restaurantes vendem iguarias, pelo que Iguaria herda (nome,endereço e telefone) de Restaurantes (o preço de uma iguaria varia dependendo do restaurante). Bolo é um tipo de Iguaria, logo Bolo herda (nome e preço) de Iguaria. 
Pizza é vendida em pizzarias e é uma iguaria, logo herda Pizza herda (a qualidade de ser pizza de rodizio ou nao) Pizzaria e (nome e preço) de Iguaria.

2) Como você modelaria a relação entre a classe Restaurante e a classe Iguaria?
Explique como essa relação seria implementada. Se necessário, sugira a criação de novos atributos ou até mesmo de novas classes para representar essa relação de forma eficiente.
-> Restaurantes vendem iguarias (por isso temos um atributo chamado +preço:float), assim, Iguaria deve herdar de Restaurante. Iguarias variam de preço dependendo do restaurante, então é preciso dizer qual o restaurante que está vendendo a certa iguaria.
Poderia ser criada uma nova classe Item para armazenar os itens do cardápio, cada item podendo ser do tipo Iguaria, para criar uma relação mais suave entre Restaurante e Iguaria.

3) Indique os tipos que você atribuiria para os argumentos: argumento1, argumento2, argumento3.
Explique quais seriam os tipos apropriados para cada argumento com base no seu uso e na função em que são empregados. Considere se eles seriam, por exemplo, tipos primitivos, instâncias de classes, ou listas, e justifique sua escolha.
-> O garçom anota os pedidos dos restaurantes, que são as iguarias, logo o argumento1 deve ser do tipo Iguaria.
O chefe de cozinha prepara os pedidos dos restaurantes, que são as iguas=rias também, logo argumento2 deve ser do tipo Iguaria.
O gerente demite funcionários, não sabemos se garçons ou chefes de cozinha, mas temos certeza que deve ser um funcionário, logo argumento3 deve ser do tipo Funcionário.