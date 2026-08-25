# Respostas - Aula 5 (24/08) - Programação 2

## Questão 1: Relações de Herança entre as Classes
### 1. Pessoa
- **Classe Base (Superclasse):** `Pessoa`
  - **Atributos Herdados:** `nome: str`, `idade: int`
- **Subclasses:**
  - `Funcionário`: Herda `nome` e `idade` de `Pessoa` e adiciona os atributos próprios `salario: float` e `carga_horaria: int`.

### 2. Funcionario
- **Classe Base (Superclasse):** `Funcionário`
  - **Atributos Herdados:** `nome: str`, `idade: int`, `salario: float`, `carga_horaria: int`
- **Subclasses:**
  - `Garçom`: Herda `nome` e `idade` de `Pessoa`, `salario` e `carga_horario` de `Funcionario` e adiciona o método próprio `anotar_pedido`.
  - `Chefe de cozinha`: Herda `nome` e `idade` de `Pessoa`, `salario` e `carga_horario` de `Funcionario` e adiciona o método próprio `preparar`.
  - `Gerente`: Herda `nome` e `idade` de `Pessoa`, `salario` e `carga_horario` de `Funcionario` e adiciona o método próprio `demitir`.

### 3. Iguaria
- **Classe Base (Superclasse):** `Iguaria (comida)`
  - **Atributos Herdados:** `nome: str`, `preco: float`
- **Subclasses:**
  - `Pizza`: Herda `nome` e `preco` de `Iguaria` e adiciona o atributo próprio `borda_recheada: bool`.
  - `Bolo`: Herda `nome` e `preco` de `Iguaria` e adiciona o atributo próprio `formato: str`.

### 4. Restaurante
- **Classe Base (Superclasse):** `Restaurante`
  - **Atributos Herdados:** `nome: str`, `endereco: str`, `telefone: str`
- **Subclasses:**
  - `Pizzaria`: Herda `nome`, `endereco` e `telefone` de `Restaurante` e adiciona o atributo próprio `rodizio: bool`.

---

## Questão 2: Modelagem da Relação entre Restaurante e Iguaria

### 1. Tipo de Relacionamento
A relação entre **Restaurante** e **Iguaria** é uma **Associação / Agregação** ("Tem-um"): um *Restaurante* possui um cardápio com várias *Iguarias*.

### 2. Implementação Sugerida
- **Atributo na classe `Restaurante`:** `cardapio: list[Iguaria]` (uma lista contendo instâncias de subclasses  de `Iguaria`, como `Pizza` e `Bolo`).

---

## Questão 3: Tipagem dos Argumentos (`argumento1`, `argumento2`, `argumento3`)

### 1. `argumento1` (método `anotar_pedido` da classe `Garçom`)
- **Tipo:** `list[Iguaria]`.
- **Justificativa:** O garçom precisa registrar os itens pedidos pelo cliente. Recebe uma lista de objetos de subclasses de `Iguaria`.

### 2. `argumento2` (método `preparar` da classe `Chefe de cozinha`)
- **Tipo:** `Iguaria`.
- **Justificativa:** O chefe precisa saber exatamente qual prato deve preparar, acessando seus atributos (como o formato do bolo ou se a pizza tem borda recheda). Recebe um objeto de uma subclasse de `Iguaria`.

### 3. `argumento3` (método `demitir` da classe `Gerente`)
- **Tipo:** `Funcionario`.
- **Justificativa:** O gerente precisa especificar qual funcionário (Garçom ou Chefe de cozinha) vai demitir. Recebe um objeto de uma subclasse de `Funcionário`.