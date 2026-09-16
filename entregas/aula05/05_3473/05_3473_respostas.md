## Exercício 1: Relações de Herança

* **Hierarquia de Pessoas/Funcionários:**
  * A classe `Pessoa` é a **classe base** para a subclasse `Funcionário`, pois todo funcionário é uma pessoa. Consequentemente, `Funcionário` herda todos os atributos de `Pessoa`.
  * A classe `Funcionário`, por sua vez, atua como **classe base** para as subclasses `Chefe de cozinha`, `Garçom` e `Gerente`, pois todas essas classes representam tipos específicos de funcionários. Com isso, elas herdam todos os atributos e métodos de `Funcionário` (e, por extensão, de `Pessoa`).

* **Hierarquia de Comidas:**
  * A classe `Iguaria` é a **classe base** para as subclasses `Bolo` e `Pizza`. Ou seja, tanto `Bolo` quanto `Pizza` herdam todos os atributos definidos em `Iguaria`.

* **Hierarquia de Estabelecimentos:**
  * A classe `Restaurante` é a **classe base** para a subclasse `Pizzaria`. Assim, `Pizzaria` herda todos os atributos de `Restaurante`.

---

## Exercício 2: Relação entre Restaurante e Iguaria

* **Tipo de Relação:** A relação entre `Restaurante` e `Iguaria` é uma **Agregação**. Isso ocorre porque as iguarias são independentes e continuam a existir logicamente mesmo caso a instância da classe `Restaurante` deixe de existir.
* **Implementação e Justificativa:** A minha sugestão é criar um novo atributo do tipo lista, chamado `pratos`, dentro da classe `Restaurante`. Dessa forma, as instâncias de `Iguaria` poderiam ser armazenadas dentro dessa lista. Escolhi usar esse atributo pelo fato de ser uma solução simples e que mantém o código mais limpo, evitando a necessidade e a complexidade de criar uma classe separada (como `Cardápio`, por exemplo) apenas para esse agrupamento.

---

## Exercício 3: Tipagem dos Argumentos

* **Argumento 1:**
  * **Tipo:** Lista de instâncias da classe `Iguaria`.
  * **Justificativa:** O tipo apropriado seria uma lista, pois o garçom vai anotar um pedido que pode conter um ou mais pratos simultaneamente.

* **Argumento 2:**
  * **Tipo:** Lista de instâncias da classe `Iguaria`.
  * **Justificativa:** O tipo apropriado seria uma lista, pois o chefe de cozinha vai preparar os pratos que foram solicitados pelos clientes no pedido.

* **Argumento 3:**
  * **Tipo:** Instância da classe `Funcionário`.
  * **Justificativa:** O tipo apropriado seria uma instância direta da classe `Funcionário`, pois a ação de demitir recai sobre um objeto específico que representa o funcionário a ser desligado.





