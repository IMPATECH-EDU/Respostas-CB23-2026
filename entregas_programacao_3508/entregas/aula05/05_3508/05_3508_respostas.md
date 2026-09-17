# Aula 5 - Respostas

## Questão 1

Uma organização possível para as classes é a seguinte:

- `Funcionario` herda de `Pessoa`. Assim, um funcionário também possui `nome` e `idade`, além de seus próprios atributos `salario` e `carga_horaria`.
- `Garcom`, `Chefe de cozinha` e `Gerente` herdam de `Funcionario`. Dessa forma, todos eles recebem os atributos de `Pessoa` e `Funcionario` e acrescentam seus próprios métodos.
- `Pizza` e `Bolo` herdam de `Iguaria`, pois são tipos específicos de comida. Eles herdam `nome` e `preco` e acrescentam seus atributos particulares.
- `Pizzaria` herda de `Restaurante`, pois é um tipo específico de restaurante. Ela herda `nome`, `endereco` e `telefone` e acrescenta o atributo `rodizio`.

## Questão 2

Eu modelaria a relação entre `Restaurante` e `Iguaria` como uma agregação. Um restaurante possui um cardápio formado por várias iguarias, mas uma iguaria pode existir independentemente de um restaurante específico.

Uma forma simples de implementar isso seria adicionar em `Restaurante` um atributo:

```python
cardapio: list[Iguaria]
```

Assim, o restaurante poderia armazenar as iguarias que oferece sem precisar criar uma classe diferente para cada item do cardápio.

## Questão 3

- `argumento1`, em `Garcom.anotar_pedido(argumento1)`: eu usaria `list[Iguaria]`, pois um pedido pode conter uma ou mais iguarias.
- `argumento2`, em `ChefeDeCozinha.preparar(argumento2)`: eu usaria `Iguaria`, pois o chefe prepara uma comida específica.
- `argumento3`, em `Gerente.demitir(argumento3)`: eu usaria `Funcionario`, pois o gerente demite um funcionário do restaurante.
