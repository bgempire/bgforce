---
title: GuiInput
description: 
---

# GuiInput
Em progresso...

## Propriedades
Abaixo estão listadas as propriedades únicas deste widget. Este widget é composto por outros widgets, portanto consulte 
as seguintes páginas para referência de outras propriedades que este widget suporta.
- [Widgets Clicáveis](https://github.com/bgempire/bgforce/wiki/Widgets-Clicáveis#propriedades) 
- [GuiLabel](https://github.com/bgempire/bgforce/wiki/GuiLabel#propriedades)

### Target
- Expressão representando o alvo que este widget deve alterar. Por exemplo: uma propriedade `Target` com valor 
`state["Usuario"]` guardará o nome digitado no widget.
A propriedade `Target` suporta o modificador `!` como prefixo, assegurando que o alvo será criado caso este 
não exista. Por exemplo, uma propriedade `Target` com valor `!config["NovoValor"]` criará a propriedade `NovoValor` 
caso esta já não exista em `config`.
- **Tipo:** str