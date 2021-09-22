---
title: Operadores Customizados
description: 
---

# Operadores Customizados
Os operadores customizados são funções que o usuário desenvolve por conta própria e configura para serem executadas 
através do disparo de uma mensagem, semelhante ao uso dos [operadores padrão](https://github.com/bgempire/bgforce/wiki/Operadores-Padrão).

**Importante:** Todos os operadores customizados necessitam do componente 
[`ScnManager`][1] ativo no jogo para serem executados.

## Criando Um Operador Customizado
O script `scripts/operators.py` contém as definições de operadores customizados. A estrutura básica deste script inclui 
declarações de funções e declaração de operadores.

### Declarações de funções
A estrutura mínima de uma função de operador é a seguinte:

```python
def funcaoDoOperador(cont, args=""):
    pass # Lógica do operador
```

- `funcaoDoOperador`: Função que executará a lógica do operador. Pode ter qualquer nome.
- `cont`: Referência para o controlador do componente [`ScnManager`][1].
- `args`: Argumento opcional que receberá o corpo da mensagem do operador.

O usuário pode criar quantas funções desejar para seus operadores, e não está limitado a criá-las apenas neste mesmo script: 
caso deseje, pode criá-las em outros scripts e importá-las em `scripts/operators.py` para declará-las na constante `OPERATORS`.

### Declaração de Operadores
A declaração de operadores nada mais é do que um dicionário que deve estar ao final do script 
`scripts/operators.py` contendo a seguinte estrutura:

```python
OPERATORS = {
    "OperadorCustom1" : funcaoDoOperador,
    "OperadorCustom2" : outraFuncaoDoOperador,
    # etc
}
```

- `OPERATORS`: Nome da constante em que os operadores estão declarados. **Deve ter esse nome obrigatoriamente**.
- `"OperadorCustom1"` e `"OperadorCustom2"`: Nomes dos operadores que servirão como assuntos das mensagens. Exemplos:
    - `bge.logic.sendMessage("OperadorCustom1")`
    - `bge.logic.sendMessage("OperadorCustom1:ValorDeArgumento")`
    - `bge.logic.sendMessage("OperadorCustom2", "ValorDeArgumento")`
- `funcaoDoOperador` e `outraFuncaoDoOperador`: Objetos de função que serão executadas quando seus respectivos operadores forem invocados.

O usuário pode adicionar quantas funções desejar a esta constante, e então poderá invocar seus próprios operadores através de mensagens.

[1]: https://github.com/bgempire/bgforce/wiki/Componentes