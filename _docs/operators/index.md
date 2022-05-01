---
title: Operadores
description: "Operadores são mensagens específicas que podem ser enviadas e
recebidas por widgets ou pelo gerenciador do BGForce, e a partir disso podem
executar uma função pré-determinada. O BGForce provê alguns operadores padrão
e dá ao usuário a possibilidade de criar operadores customizados."
---

# {{ page.title }}

{{ page.description }}

## Conceito
Operadores são disparados através de mensagens a partir de qualquer objeto, seja por blocos de lógica, Python
ou a partir de commandos de [widgets clicáveis]({{ site.baseurl }}/widgets/clickable).
Com isso, o padrão de mensagens para disparar operadores é:

- Mensagens sem corpo
    - `NomeDoOperador` como assunto (caso o operador não precise de argumentos)
    - `NomeDoOperador:Argumentos` como assunto (caso o operador aceite argumentos)
- Mensagens com corpo
    - `NomeDoOperador` como assunto e `Argumentos` como corpo (caso o operador aceite argumentos)

**Exemplos:**

```python
# Operador sem argumentos
bge.logic.sendMessage("UpdateGui")

# Operador com argumentos passados junto ao assunto
bge.logic.sendMessage("UpdateGui:Formulario")

# Operador com argumentos passados no corpo da mensagem
bge.logic.sendMessage("UpdateGui", "Formulario")
```

O operador `UpdateGui` é recebido apenas por widgets de interface de usuário, já todos os outros operadores
(sejam eles padrão ou customizados) **precisam da cena de gerenciador [`ScnManager`]({{ site.baseurl }}/components)
para funcionarem**.

## Índice

{%- for section in site.data.toc %}
{%- if section.url == "operators" %}
{%- for link in section.links %}
- [{{ link.title }}]({{ site.baseurl }}/{{ link.url }})
{%- endfor %}
{%- endif %}
{%- endfor %}