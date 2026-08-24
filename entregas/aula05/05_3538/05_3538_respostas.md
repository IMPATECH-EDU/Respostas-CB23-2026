# Respostas da Atividade Prática 5

## 1. Identificação de relações de herança entre as classes

A hierarquia do sistema divide-se da seguinte forma:

*   **Pessoas e Funcionários:** A classe base é `Pessoa`. A classe `Funcionário` é uma subclasse de `Pessoa` e herda os atributos genéricos `nome` e `idade`.
*   **Cargos:** A classe `Funcionário` atua como classe base para `Garçom`, `Chefe de cozinha` e `Gerente`. Essas três subclasses herdam os atributos `salario` e `carga_horaria` de `Funcionário`, além de herdarem indiretamente `nome` e `idade` de `Pessoa`.
*   **Estabelecimentos:** A classe base é `Restaurante`. A classe `Pizzaria` é uma subclasse de `Restaurante`. A `Pizzaria` herda os atributos `nome`, `endereco` e `telefone`, implementando o seu próprio atributo exclusivo chamado `rodizio`.
*   **Alimentos (Iguarias):** A classe base é `Iguaria (comida)`. As classes `Pizza` e `Bolo` são subclasses diretas de `Iguaria`. Ambas herdam os atributos `nome` e `preco`. Adicionalmente, a `Pizza` introduz o atributo `borda_rechada`, e o `Bolo` introduz o atributo `formato`.

## 2. Modelagem da relação entre Restaurante e Iguaria

A relação entre a classe `Restaurante` e a classe `Iguaria` deve ser modelada através de uma **Agregação**.

A agregação é o modelo ideal porque uma `Iguaria` (o conceito de uma receita, como uma pizza ou um bolo) tem existência independente do `Restaurante`. Se o restaurante falir ou fechar as portas, o prato continua existindo conceitualmente no mundo real.

Essa relação seria implementada através da criação de um novo atributo na classe `Restaurante`. Esse atributo poderia ser chamado de `cardapio` e seria do tipo lista, responsável por armazenar múltiplas instâncias da classe base `Iguaria`. Devido ao polimorfismo, essa lista poderia conter simultaneamente instâncias tanto de `Pizza` quanto de `Bolo`.

## 3. Tipagem dos argumentos

*   **`argumento1` (método `anotar_pedido` da classe `Garçom`):** O tipo mais apropriado seria uma **lista de instâncias da classe `Iguaria`** (exemplo: `list[Iguaria]`). O garçom anota pedidos que frequentemente são compostos por mais de um prato. Alternativamente, poderia ser uma instância de uma nova classe agregadora chamada `Pedido`.
*   **`argumento2` (método `preparar` da classe `Chefe de cozinha`):** O tipo apropriado seria uma **instância da classe `Iguaria`**. O método precisa receber a referência exata do objeto-comida (seja uma pizza ou um bolo) que deve ser manipulado e preparado na cozinha.
*   **`argumento3` (método `demitir` da classe `Gerente`):** O tipo apropriado seria uma **instância da classe `Funcionário`**. Para executar a ação de demissão, o gerente precisa atuar sobre o objeto específico do funcionário (seja ele um garçom, um chefe de cozinha ou outro gerente) que terá seu vínculo desfeito no sistema.