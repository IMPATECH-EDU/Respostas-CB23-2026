Aula 05
Respostas:

Questão 1 - Relações de herança
Pra achar as heranças eu fui testando a frase "X é um Y" entre as classes. Quando ela faz sentido (garçom é um funcionário, pizza é uma iguaria) usei herança. Quando não faz (cardápio não é um restaurante, 
pizza não é uma pizzaria, apesar do nome parecido) a relação é de outro tipo, que é o que aparece na questão 2. Com isso as classes ficaram divididas em três hierarquias.

Pessoa → Funcionário → Garçom, Chefe de cozinha e Gerente
Pessoa é a classe base, com nome e idade. Todo funcionário é uma pessoa, então Funcionario herda esses dois atributos e acrescenta o que é específico de quem trabalha no restaurante: salario e carga_horaria.

Garçom, chefe de cozinha e gerente são tipos de funcionário, então os três herdam de Funcionario. Assim cada um já tem nome, idade, salario e carga_horaria (os dois primeiros vêm da Pessoa, 
passando pelo Funcionario) e só precisa definir o próprio método: anotar_pedido no garçom, preparar no chefe e demitir no gerente. Ou seja, 
Funcionario é subclasse de Pessoa e ao mesmo tempo classe base dos três cargos.

Restaurante → Pizzaria
Uma pizzaria é um restaurante com uma informação a mais, que é se tem rodízio ou não. Então Pizzaria herda nome, endereco e telefone de Restaurante e acrescenta rodizio. 
Como na minha modelagem o restaurante também tem cardápio e lista de funcionários (questão 2), a pizzaria herda isso junto sem precisar escrever nada a mais.

Iguaria → Pizza e Bolo
Iguaria representa uma comida qualquer, com nome e preco. Pizza e bolo são comidas, então herdam esses dois atributos e cada uma adiciona o seu: borda_recheada na pizza e formato no bolo. 
Pensei em deixar Iguaria como classe abstrata, mas acabei deixando como classe normal, porque o restaurante pode vender alguma coisa que não é nem pizza nem bolo (uma salada, por exemplo) 
e aí dá pra usar a própria Iguaria.

Em python a ideia fica assim (no código tirei os acentos dos nomes das classes):

class Pessoa:
    def __init__(self, nome: str, idade: int):
        self.nome = nome
        self.idade = idade


class Funcionario(Pessoa):
    def __init__(self, nome: str, idade: int, salario: float, carga_horaria: int):
        super().__init__(nome, idade)  # nome e idade ficam por conta da Pessoa
        self.salario = salario
        self.carga_horaria = carga_horaria


class Garcom(Funcionario):
    # nao tem atributo novo, entao nem precisa de __init__, usa o do Funcionario
    def anotar_pedido(self, argumento1):
        pass

ChefeDeCozinha e Gerente seguem o mesmo modelo do Garcom. As outras duas hierarquias (Pizza(Iguaria), Bolo(Iguaria) e Pizzaria(Restaurante)) são parecidas com a do Funcionario: chamam super().__init__(...) 
e depois guardam o atributo novo.

Questão 2 - Relação entre Restaurante e Iguaria
A primeira ideia seria colocar direto uma lista de iguarias dentro do restaurante. Funciona, mas preferi criar uma classe nova no meio das duas, o Cardapio:

o Restaurante tem um Cardapio (composição)

o Cardapio tem várias iguarias (agregação)

Restaurante e Cardápio: composição. O cardápio pertence a um restaurante só e não faz sentido sem ele. Se o restaurante deixar de existir, o cardápio vai junto. 
Por isso o próprio restaurante cria o cardápio dentro do __init__, ninguém passa um cardápio pronto de fora. No diagrama ficou 1 dos dois lados.

Cardápio e Iguaria: agregação. A iguaria existe independente do cardápio. Dá pra criar a pizza antes, colocar no cardápio, tirar depois, e ela continua existindo. 
Também dá pra mesma iguaria estar em mais de um cardápio (por exemplo, duas unidades da mesma pizzaria). Então as iguarias são criadas fora e só adicionadas no cardápio, 
por isso a multiplicidade 0..* dos dois lados.

Separar o cardápio também deixa o Restaurante mais limpo, já que tudo que é de mexer com comida (adicionar, remover e, se precisar, buscar) fica numa classe só. Usei lista porque é o jeito mais simples, 
mas se o cardápio fosse grande e precisasse buscar prato pelo nome toda hora, dava pra trocar por um dict[str, Iguaria], que faz a busca em O(1) em média em vez de O(n).

class Cardapio:
    def __init__(self):
        self.itens: list[Iguaria] = []

    def adicionar(self, iguaria: Iguaria):
        self.itens.append(iguaria)

    def remover(self, iguaria: Iguaria):
        self.itens.remove(iguaria)


class Restaurante:
    def __init__(self, nome: str, endereco: str, telefone: str):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.cardapio = Cardapio()  # composicao: o restaurante cria o proprio cardapio
        self.funcionarios: list[Funcionario] = []  # agregacao: os funcionarios vem de fora

Exemplo de uso (com Pizza e Pizzaria feitas do jeito que falei na questão 1):

calabresa = Pizza("Calabresa", 45.0, borda_recheada=True)

centro = Pizzaria("Pizzaria Bella", "Rua A, 10", "(21) 2222-1111", rodizio=True)
tijuca = Pizzaria("Pizzaria Bella", "Rua B, 20", "(21) 2222-2222", rodizio=False)

centro.cardapio.adicionar(calabresa)
tijuca.cardapio.adicionar(calabresa)  # a mesma pizza nos dois cardapios

del centro  # o cardapio do centro some junto, mas a calabresa continua existindo

Uma coisa que vale comentar é que em Python a linguagem não obriga um objeto a "morrer junto" com outro. O coletor de lixo apaga o objeto quando ninguém mais aponta pra ele, 
então a diferença entre composição e agregação aparece na forma como o código é organizado: quem cria o objeto e quem mais guarda referência pra ele.

Um problema que eu percebi nessa modelagem: o preco fica na Iguaria, então se a mesma pizza estiver nas duas unidades ela tem o mesmo preço nas duas. Pra essa atividade deixei assim, 
mas se precisasse de preço diferente por restaurante dava pra guardar o preço no cardápio (tipo um dict de iguaria pra preço).

Aproveitei e também liguei o Restaurante ao Funcionario, com a lista funcionarios. Aqui usei agregação e não composição 
(no rascunho do diagrama eu tinha colocado composição, mas troquei). O funcionário é uma pessoa, então existe por conta própria: se ele for demitido ou se o restaurante fechar, 
ele continua existindo e pode ir trabalhar em outro lugar. Por isso no diagrama ficou 0..1 do lado do restaurante (o funcionário pode estar sem emprego) e 0..* do lado do funcionário.

Questão 3 - Tipos dos argumentos
argumento1 (anotar_pedido do Garçom): list[Iguaria]

Um pedido normalmente tem mais de uma coisa (uma pizza e um bolo, por exemplo), então faz sentido o garçom receber uma lista. E é uma lista de objetos Iguaria, 
não de strings com o nome do prato: com o objeto já vêm o nome e o preço juntos (dá pra calcular a conta depois) e não tem o risco de anotar um prato que não existe por erro de digitação. 
Como Pizza e Bolo herdam de Iguaria, a mesma lista aceita os dois. Se precisar de quantidade dá pra repetir o item na lista ou usar um dict[Iguaria, int], mas deixei a lista por ser mais simples.

argumento2 (preparar do Chefe de cozinha): Iguaria

O chefe prepara um prato de cada vez, então recebe uma instância de Iguaria. Aqui a herança ajuda bastante: como o tipo é a classe base, o mesmo método serve pra Pizza, 
pra Bolo e pra qualquer comida nova que for criada depois, sem precisar de um preparar_pizza e um preparar_bolo. Se o pedido tiver vários itens, é só chamar preparar pra cada item da lista que o garçom anotou.

argumento3 (demitir do Gerente): Funcionario

Quem é demitido é um funcionário, então o argumento é uma instância de Funcionario. Não usei Pessoa porque aí daria pra passar qualquer pessoa, até um cliente, 
e não faz sentido demitir alguém que nem trabalha lá. Também não usei uma str com o nome, porque dois funcionários podem ter o mesmo nome e não daria pra saber qual demitir.
Passando o próprio objeto não tem essa ambiguidade. E de novo, por causa da herança, o método aceita Garcom, ChefeDeCozinha e até outro Gerente.

No fim, nenhum dos três é tipo primitivo: dois são instâncias de classes do próprio modelo e um é uma lista de instâncias. 
Com as anotações de tipo fica assim (num código de verdade eu usaria nomes melhores, tipo itens, iguaria e funcionario, mas deixei argumento1/2/3 pra bater com o enunciado):

class Garcom(Funcionario):
    def anotar_pedido(self, argumento1: list[Iguaria]):
        pass


class ChefeDeCozinha(Funcionario):
    def preparar(self, argumento2: Iguaria):
        pass


class Gerente(Funcionario):
    def demitir(self, argumento3: Funcionario):
        pass