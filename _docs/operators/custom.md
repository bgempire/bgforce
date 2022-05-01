---
title: Operadores Customizados
description: "Os operadores customizados são funções que o usuário desenvolve por
conta própria e configura para serem executadas através do disparo de uma mensagem."
---

# {{ page.title }}

{{ page.description }}
Esta funcionalidade é semelhante ao uso dos [operadores padrão]({{ site.baseurl }}/operators/default).

**Importante:** Todos os operadores customizados necessitam do componente
[`ScnManager`][1] ativo no jogo para serem executados.

## Criando Um Operador Customizado
O script `scripts/operators.py` contém as definições de operadores customizados. A estrutura básica deste script inclui
declarações de funções com os nomes dos operadores que recebam dois argumentos.

### Declarações de funções
A estrutura mínima de uma função de operador é a seguinte:

```python
def funcaoDoOperador(cont, args=""):
    pass # Lógica do operador
```

- `funcaoDoOperador`: Função que executará a lógica do operador. Seu nome representa o nome do operador.
- `cont`: Referência para o controlador do componente [`ScnManager`][1].
- `args`: Argumento opcional que receberá o corpo da mensagem do operador.

O usuário pode criar quantas funções desejar para seus operadores, e não está limitado a criá-las apenas neste mesmo script:
caso deseje, pode criá-las em outros scripts e importá-las em `scripts/operators.py` para tê-las disponíveis no jogo.

Uma vez que as funções de operadores customizados estejam definidas neste script, o usuário poderá disparar os
operadores em questão apenas enviando mensagens com os nomes dos operadores. **Nota:** a primeira letra do operador
na mensagem deverá ser **maiúscula** independentemente se o nome da função começar com letra minúscula.

Por exemplo, dada a função `funcaoDoOperador` declarada acima, para disparar este operador no jogo basta enviar
qualquer uma das mensagens:

- `bge.logic.sendMessage("FuncaoDoOperador")` (operador sem argumentos)
- `bge.logic.sendMessage("FuncaoDoOperador:ValorDeArgumento")` (operador com argumentos, mensagem com apenas assunto)
- `bge.logic.sendMessage("FuncaoDoOperador", "ValorDeArgumento")` (operador com argumentos, mensagem com assunto e corpo)

[1]: {{ site.baseurl }}/components