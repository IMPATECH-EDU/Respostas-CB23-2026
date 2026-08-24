# Questão 1

As classes podem ser organizadas de forma que as subclasses também possam ser classificadas como a classe base, por exempo, um funcionário também é uma pessoa, portanto existe uma relação de hereança entre essas duas classes.

Como dito no exemplo, podemos ter como a primeira classe base a classe **Pessoa**:
classe base: **Pessoa**
subclasse: **Funcionário**, que herda de **Pessoa** 'nome: str' e 'idade: int'
subclasses de **Funcionário**: **Gerente**, **Chefe De Cozinha** e **Garçom**, que herdam de Funcionário 'salario: float' e 'carga_horaria: int', além dos atributos da classe base Pesssoa.

Para a segunda classe base temos **Iguaria (comida)**:
classe base: **Iguaria (comida)**
subclasses: **Pizza** e **Bolo**, que herdam os atributos 'nome: str' e 'preco: float'

Para a ultima classe base Restaurante:
classe base: **Restaurante**
subclasse: **Pizzaria**, herdando 'nome: str', 'endereço: str' e 'telefone: str'

# Questão 2

Uma forma de estabelecer uma relação entre as classes ***Restaurante** e **Iguaria** seria criando outra classe intermediária **Cardápio**, no qual, **Cardápio** seria uma subclasse da classe base **Restaurante** e **Iguaria** uma subclasse de Cardápio, com o atributo sendo uma lista de iguarias.


# Questão 3

Para o argumento1 da classe **Garçom** o mais apropriado seria uma lista, pois é a ferramenta que melhor auxilia a anotar pedidos das iguarias. Para o argumento2 a escolha correta é uma instancia da classe **Iguaria** para que o chefe de cozinha acesse diretamente o que será preparado. Para o argumento3 seria também uma instancia da classse **Funcionário** que acessaria diretamente os dados de funcionários para uma demissão.

