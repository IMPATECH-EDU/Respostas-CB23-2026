# Respostas da Atividade 05

## Questão-01: 
Veja que gerente, garçom e chefe de cozinha são pessoas, mas também são funcionários. Isso nos diz, nesse contexto, que Pessoa é a classe base de todas elas, em seguida na ordem de hierarquia vem a classe funcionários que é subclasse apenas de Pessoa. Ou seja, A classe Pessoa é classe base da Funcionário, esta, por sua vez, é classe base de Garçom, Gerente e Chefe de Cozinha. Com isso, é evidente que a classe Funcionário herdaria apenas os atributos da classe Pessoa, e as outras herdariam os atributos tanto desta quanto dessa. Nessa situação, a classe Funcionário herdaria nome (valor: str) e idade (valor: int) da classe Pessoa, e as demais classes herdariam os atributos salário (valor: sttr) e carga_horária (valor: int) 

Na mesma ideia, note que a classe Restaurante seria a classe base de Pizzaria, em que esta herdaria os atributos (sendo eles, endereço, nome e telefone, todos do tipo str) dessa e teria seu próprio atributo "rodízio", que seria um valor do tipo booleano (True ou False).

Analogamente, observe que a classe Iguaria seria classe base das suas subclasses Pizza e Bolo, já que estas devem ter nome e preço, cujos são os atributos (tipo: str) que a classe Iguaria cria.

## Questão-02:
Dado que iguaria é um prato vendido em um restaurante, deveria ser implementado um novo atributo em Restaurante, no qual ele seria uma lista das iguarias que esse tipo de restaurante venderia. Essa ideia seria posta no "def__init__()" da classe Restaurante, da forma: "self.iguarias=[ iguaria() ]", onde a lista seria composta por elementos do tipo "iguaria".

Portanto, a relação seria de atributo (Iguaria) e classe (Restaurante).

## Questão-03:
Para o "_argumentos 1_" e o "_argumento 2_" tem-se que eles seriam do tipo "_iguaria_",com o primeirso sendo uma lista de "_iguaria_" (tendo em vista que eles seriam os pedidos de um restaurante, utilizando no código "self.iguarias", da classe Restaurante) e o segundo sendo qual "_iguaria_" o Chefe de Cozinha deverá preparar. No tocante ao "_argumento 3_", ele seria do tipo Funcionário, já que o Gerente pode apenas demitir objetos dessa classe.
