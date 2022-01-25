---
title: "Cursor do Mouse: ScnMouseCursor"
description: 
---

# {{ page.title }}

![]({{ site.baseurl }}/assets/img/wiki-components-01.png)

A cena `ScnMouseCursor` é um componente opcional de cursor do mouse customizável.
O cursor do mouse pode ser personalizado de duas formas:

- Editando sua textura em `textures/gui/MouseCursor.png`
- Editando as propriedades de `"MouseCursor"` em `database/Gui.json`

## Propriedades
As propriedades de `"MouseCursor"` em `database/Gui.json` podem ser editadas para 
alterarem o visual do cursor, desde sua cor de acordo com o seu estado até o seu 
tamanho e posição.

```json
"MouseCursor" : {
    "Size" : [0.8, 0.8],
    "Offset" : [0.0, 0.0],
    "CanvasSize" : [100, 100],
    "ColorNormal" : [1, 1, 1, 1],
    "ColorClick" : [1, 1, 1, 1],
    "ColorHover" : [1, 1, 1, 1],
    "ColorDisabled" : [1, 1, 1, 1]
}
```

### `Size`
- Multiplicador de tamanho do cursor nos eixos X e Y.

- **Tipo:** list[float]

### `Offset`
- Posição do cursor em relação ao seu centro nos eixos X e Y.

- **Tipo:** list[float]

### `CanvasSize`
- Tamanho do objeto de canvas do fundo do cursor.

- **Tipo:** list[float]

### `ColorNormal`
- Cor RGBA do cursor em seu estado normal.

- **Tipo:** list[float]

### `ColorClick`
- Cor RGBA do cursor enquanto estiver clicando.

- **Tipo:** list[float]

### `ColorHover`
- Cor RGBA do cursor enquanto estiver por cima de algum widget.

- **Tipo:** list[float]

### `ColorDisabled`
- Cor RGBA do cursor enquanto estiver por cima de algum widget desabilitado.

- **Tipo:** list[float]