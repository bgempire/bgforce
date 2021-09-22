---
title: GuiCheckbox
description: 
---

# GuiCheckbox
Em progresso...

## Propriedades
Abaixo estão listadas as propriedades únicas deste widget. Este widget é composto por outros widgets, portanto consulte 
as seguintes páginas para referência de outras propriedades que este widget suporta.
- [Widgets Clicáveis](https://github.com/bgempire/bgforce/wiki/Widgets-Clicáveis#propriedades) 
- [GuiLabel](https://github.com/bgempire/bgforce/wiki/GuiLabel#propriedades)

### Target
- Expressão representando o alvo que este widget deve alterar. Por exemplo: uma propriedade `Target` com valor 
`config["Fullscreen"]` irá mostrar se a propriedade de tela cheia das configurações está ativada ou não, e 
alterará esta mesma propriedade caso o widget for clicado.

- **Tipo:** str

### Value
- Caso fornecido, o widget se comportará como um radio button, alterando o `Target` apenas para o valor de `Value` 
ao invés de alternar entre verdadeiro e falso. Este valor pode ser de qualquer tipo, e será avaliado como tal, isto é, 
um `Value` do tipo inteiro irá guardar em `Target` um inteiro.

- **Tipo:** any