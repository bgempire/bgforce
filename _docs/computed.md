---
title: Variáveis Computadas
description: "Os widgets podem exibir ou verificar uma informação dinâmica
através de uma expressão em Python, porém uma única linha de Python pode não
ser suficiente para processar essa informação em alguns casos.
O script `scripts/computed.py` possui definições de funções que retornam
informações dinâmicas, e podem ser usadas nos widgets em qualquer propriedade
que utilize uma expressão de Python através do valor com prefixo `$`."
---

# {{ page.title }}

{{ page.description }}

### Exemplo

Por exemplo, caso queiramos mostrar num widget [GuiLabel]({{ site.baseurl }}/widgets/label) a data de hoje
corretamente formatada, podemos utilizar uma propriedade computada. Desta forma, no script
`scripts/computed.py` definimos uma função que nos retornará a string formatada com a data de hoje:

```python
def dataDeHojeFormatada():
    from datetime import datetime
    return datetime.today().strftime('%d/%m/%Y')
```

E por fim, adicione o nome da função com o prefixo `$` na propriedade `Label` da instância da `GuiLabel`.

![]({{ site.baseurl }}/assets/img/computed-0.png)

Isso resultará no valor de retorno da função sendo mostrado no texto da `GuiLabel`.

![]({{ site.baseurl }}/assets/img/computed-1.png)

As propriedades computadas não estão limitadas a apenas textos: qualquer expressão de Python que possa ser
inserida em um widget (como a propriedade `Enabled`) pode ser uma propriedade computada.

## Parâmetro

Opcionalmente, as variáveis computadas podem receber um parâmetro que pode ser passado
para sua função fonte. Para isso, utilize o caractere `:` para definir o argumento que
deverá ser passado para a função. Por exemplo: `$nomeDaFuncao:Parametro`.

No exemplo mostrado anteriormente, poderíamos atualizar nossa função da seguinte forma:

```python
def dataDeHojeFormatada(formato=""):
    from datetime import datetime
    date = datetime.today()

    if formato == "Extenso":
        return date.strftime('%A, %d de %B de %Y')
    else:
        return date.strftime('%d/%m/%Y')
```

Adicionando uma nova label, podemos adicionar a mesma propriedade computada, porém
passando um parâmetro adicional após o caractere `:`:

![]({{ site.baseurl }}/assets/img/computed-2.png)

Teremos então duas labels com a mesma propriedade computada, mas que se comportam
de formas diferentes devido ao parâmetro passado ou a ausência deste.

![]({{ site.baseurl }}/assets/img/computed-3.png)

