---
layout: page
title: GuiIconButton
---

# GuiIconButton
![]({{ site.baseurl }}/assets/img/wiki-iconbutton-00.png)

**GuiIconButtons** são widgets clicáveis capazes de executar comandos. São semelhantes aos [**GuiButtons**][3],
com o adicional de terem propriedades que permite a alteração de seu ícone
(definido na textura `textures/gui/IconButtonIcons.png`). Eles são compostos por um [widget clicável][1] e um
elemento de [GuiLabel][2], sendo ambos personalizáveis em suas respectivas propriedades.

## Propriedades
Abaixo está listada a propriedade única deste widget. Este widget é composto por outros widgets, portanto consulte
as seguintes páginas para referência de outras propriedades que este widget suporta.
- [Widgets Clicáveis]({{ site.baseurl }}/widgets/clickable#propriedades)
- [GuiLabel]({{ site.baseurl }}/widgets/label#propriedades)

### Icon
- Número de índice que representa um ícone presente na textura `textures/gui/IconButtonIcons.png`.
- **Tipo:** int (de 1 a 25)

### IconColor
- Cor `[r, g, b, a]` do elemento de ícone. Por exemplo, vermelho é: `[1.0, 0.0, 0.0, 1.0]`.
- **Tipo:** [float, float, float, float]

### IconRotation
- Rotação do ícone em graus.
- **Tipo:** int

### IconOffset
- Deslocamento `[x, y]` do elemento de ícone em relação ao centro da instância. Exemplo: `[0.5, -0.5]`.
- **Tipo:** [float, float]

### IconSize
- Fator de escala `[x, y]` do elemento de ícone. Exemplo: `[1.5, 2.0]`.
- **Tipo:** [float, float]

[1]: {{ site.baseurl }}/widgets/clickable
[2]: {{ site.baseurl }}/widgets/label
[3]: {{ site.baseurl }}/widgets/button