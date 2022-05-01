---
title: "Cursor do Mouse: ScnMouseCursor"
description:
---

# {{ page.title }}

![]({{ site.baseurl }}/assets/img/wiki-components-01.png)

A cena `ScnMouseCursor` é um componente opcional de cursor do mouse customizável.
O cursor do mouse pode ser personalizado de algumas formas:

- Editando sua textura em `textures/gui/MouseCursor.png`
- Adicionando um item `"MouseCursor"` em `database/Styles.json` e adicionando as propriedades desejadas.

**Nota:** Também é possível editar as propriedades de `"MouseCursor"` em `database/Bgf.json`
na seção `"Gui"`, mas adicionar um estilo personalizado é preferível para evitar
editar os dados padrão do BGForce.

## Propriedades
As propriedades de `"MouseCursor"` abaixo podem ser editadas para alterarem o
visual do cursor, desde sua cor de acordo com o seu estado até o seu tamanho e posição.

### `CanvasSize`
- Tamanho do objeto de canvas do fundo do cursor.

- **Tipo:** list[float]

### `ColorClick`
- Cor RGBA do cursor enquanto estiver clicando.

- **Tipo:** list[float]

### `ColorDisabled`
- Cor RGBA do cursor enquanto estiver por cima de algum widget desabilitado.

- **Tipo:** list[float]

### `ColorHover`
- Cor RGBA do cursor enquanto estiver por cima de algum widget.

- **Tipo:** list[float]

### `ColorNormal`
- Cor RGBA do cursor em seu estado normal.

- **Tipo:** list[float]

### `Offset`
- Posição do cursor em relação ao seu centro nos eixos X e Y.

- **Tipo:** list[float]

### `Size`
- Multiplicador de tamanho do cursor nos eixos X e Y.

- **Tipo:** list[float]
