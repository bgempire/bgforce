---
title: GuiMeshButton
description: "**GuiMeshButtons** são widgets clicáveis capazes de executar comandos."
---

# GuiMeshButton
![]({{ site.baseurl }}/assets/img/wiki-meshbutton-00.png)

{{ page.description }}
São semelhantes aos [GuiButtons][2], com o adicional de terem uma propriedade
que permite a alteração de sua malha, que pode ser qualquer uma presente na
mesma cena do widget em questão. Eles são compostos por um [widget clicável][1],
sendo personalizáveis em suas propriedades.

## Propriedades
Abaixo está listada a propriedade única deste widget. Este widget é composto
por outros widgets, portanto consulte as seguintes páginas para referência de
outras propriedades que este widget suporta.

- [Widgets Clicáveis]({{ site.baseurl }}/widgets/clickable#propriedades)
- [GuiLabel]({{ site.baseurl }}/widgets/label#propriedades)

### Mesh
- Nome da malha que será definida para este widget. A malha deve estar
presente na mesma cena que este widget, podendo estar em um objeto numa
camada oculta ou não.

- **Tipo:** str

[1]: {{ site.baseurl }}/widgets/clickable
[2]: {{ site.baseurl }}/widgets/button