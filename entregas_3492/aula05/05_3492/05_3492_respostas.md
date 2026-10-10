Respostas
Questão 1

As classes Pizza e Bolo devem ser subclasses de Iguaria (comida), herdando os atributos nome e preco (pois é preciso o nome para saber o tipo da pizza, por exemplo calabresa, e do bolo, por exemplo chocolate ou cenoura, e é claro, o quanto custa. Além disso, pizza e bolo são comidas).

A classe Funcionário é subclasse da classe Pessoa e herda nome e idade (Funcionário é uma pessoa com nome e idade, embora idade talvez não seja muito útil além de servir para garantir que não seja um menor de idade ou verificar quando se tem uma idade mínima para determinada função na empresa).

As classes Garçom, Chefe de cozinha e Gerente são subclasses de Funcionário e herdam nome, idade, salario e carga_horaria (nome e idade vêm da herança da "classe avó" Pessoa, enquanto salario é herdado pois o garçom, o chefe de cozinha e o gerente não aceitam trabalhar de graça, enquanto carga_horaria é herdada pois o dono do restaurante não aceita pagar os funcionários citados sem que tenham trabalhado).

A classe Pizzaria é subclasse de Restaurante e herda os atributos nome, endereço e telefone (toda pizzaria é um restaurante e precisa de um nome, como "Pizza by Alfredo", endereço, como "Baker Street 221B", e telefone para ligar para a pizzaria, já que o iFood coloca taxa).

Questão 2

Por meio da criação de um atributo de Restaurante chamado registro, que seria um dicionário onde as chaves são instâncias da classe Comida e o valor da chave é o número de vezes que essa comida foi pedida no restaurante (pelo menos naquele dia).

Para complementar, poderia ser criado um método de Restaurante chamado lucro, que percorresse todas as chaves do dicionário registro e retornasse o produto da quantidade vendida pelo atributo preco da chave, retornando, assim, a quantidade de dinheiro que o restaurante ganhou.

Também seria possível ter um atributo chamado disponiveis, que seria uma lista com objetos da classe Comida. Essa lista conteria todas as comidas disponíveis no restaurante. Uma comida seria removida quando os ingredientes acabassem e adicionada quando eles voltassem.

Isso permitiria a criação de um método chamado cardapio, que mostraria todos os alimentos disponíveis e seus respectivos preços.

Questão 3
argumento1

A função deve ser do tipo que tem um * no argumento ao ter sido criada no def, pois assim ela pode receber quantos argumentos forem dados. Dessa forma, o cliente pode fazer um ou mais pedidos de uma vez.

Os argumentos seriam instâncias das classes Bolo, Pizza e Comida (nos casos em que não é bolo nem pizza). Dessa forma, a função anotar_pedido terá os pedidos em suas respectivas classes.

argumento2

A função deve ser do tipo que tem um * no argumento ao ter sido criada no def, pois assim ela pode receber quantos argumentos forem dados. Dessa forma, o cliente pode fazer um ou mais pedidos de uma vez.

Os argumentos seriam instâncias das classes Bolo, Pizza e Comida (nos casos em que não é bolo nem pizza). Dessa forma, a função preparar terá os pedidos em suas respectivas classes que deve preparar.

argumento3

A função deve ser do tipo que tem um * no argumento ao ter sido criada no def, pois assim ela pode receber quantos argumentos forem dados. Dessa forma, o gerente pode demitir um ou mais funcionários de uma vez.

Os argumentos seriam instâncias da classe Funcionário (tanto Garçom como Chefe de cozinha são funcionários). Nesse caso, não precisa especificar a função, apenas demitir o objeto da classe Funcionário. Dessa forma, o gerente já recebe diretamente o funcionário que vai defenestrar.