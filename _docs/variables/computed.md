---
title: Variáveis Computadas
description: 
---

# Variáveis Computadas
Os widgets podem exibir ou verificar uma informação dinâmica através de uma expressão em Python, 
porém uma única linha de Python pode não ser suficiente para processar essa informação em alguns casos. 
O script `scripts/computed.py` possui definições de funções que retornam informações dinâmicas, 
e podem ser usadas nos widgets em qualquer propriedade que utilize uma expressão de Python através do 
valor com prefixo `$`.

## Exemplo

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