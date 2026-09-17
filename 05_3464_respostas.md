# AULA 5

## Questão 1: Identifique relações de herança entre as classes.

A relação de herança entre essas classes segue uma lógica de encaixamento simples e relacionado com a vida real. Veja que um funcionário, por exemplo, sempre é uma pessoa, então a __Classe__ __Funcionário__ herda de __Pessoa__. Além disso, todas as profissões como __Garçom__, __Chefe de cozinha__ ou __Gerente__ herdam de __Funcionário__, pois todos trabalham. Além disso, garçons e chefes de cozinhas só podem existir em um restaurante, portanto __Garçom__ e __Chefe de cozinha__ são classes contidas em __Restaurante__.

Da mesma forma, toda pizzaria é um restaurante, portanto __Pizzaria herda de Restaurante__. Além disso, pizza é obviamente uma comida, e só existe (a princípio) em uma pizzaria, portanto __Pizza__ deve ser uma __subclasse__ de __Iguaria__, pois é uma comida, e deve pertencer à classe __Pizzaria__. Temos, finalmente, __Bolo__, que é uma __subclasse__ de __Iguaria__, que é uma classe separada que pode ser implementada em cada __Restaurante__. 

## Questão 2: Como você modelaria a relação entre a classe Restaurante e a classe Iguaria?

Para implementar essa relação, acredito que a maneira mais simples seja tratar __Iguaria__ como uma classe separada. Dessa maneira poderemos implementar quantas iguarias quisermos em cada __Restaurante__; acredito que a forma mais simples de fazer isso seja usando uma __lista__ em __Restaurante__ que englobe cada __Iguaria__. Assim teríamos algo como um cardápio.

Para uma implementação mais robusta, poderíamos então criar uma classe __Cardápio__, que seria uma subclasse de __Restaurante__. Então, ao inicializar a classe __Restaurante__, deveríamos incluir as comidas no __Cardápio__, que seria uma lista de __Iguarias__. Fazendo dessa forma, temos uma maneira dinâmica de implementar mudanças no restaurante.

## Questão 3: Indique os tipos que você atribuiria para os argumentos: argumento1, argumento2, argumento3.

Eu faria isso da seguinte forma:

* _argumento1_: __[Iguaria]__;
* _argumento2_: __Iguaria__;
* _argumento3_: __Funcionário__;
  
O _argumento1_ seria feito pensando na implementação de que __todo pedido é essencialmente uma lista de comidas__, e __toda comida__, como bolo ou pizza, __é uma Iguaria ou herda de Iguaria__. Dessa forma, como a classe __Iguaria__ possui os atributos __nome__ e __preço__, o garçom já tem os dados necessários para realizar o pedido.

O ___argumento2___ seria feito pensando com raciocínio simular ao ___argumento1___: O __Chefe de cozinha só precisa saber qual comida/prato deve preparar__, então só precisa do __atributo nome__, que está contido em __Iguaria__. Como um restaurante poderia ter mais de um chefe, acredito que a implementação adequada deve atribuir à sua maneira as comidas nos pedidos para os diferentes chefes do restaurante. Sendo feito assim, um mesmo pedido poderia ser concluído mais rápido por ser feito por vários chefes.

O ___argumento3___ tem o princípio de que o __Gerente só pode demitir Funcionários__. Como todo gerente é essencialmente um funcionário, gerentes poderiam demitir eles mesmos, então isso deveria permitido ou proibido de acordo com o problema.

