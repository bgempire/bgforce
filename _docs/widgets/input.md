---
title: GuiInput
description: 
---

# GuiInput
![]({{ site.baseurl }}/assets/img/wiki-input-00.png)

**GuiInputs** são entradas de texto digitado que alteram o valor de um alvo. 
Eles tem suporte a ações de copiar e colar enquanto o cursor estiver ativo utilizando 
os atalhos <kbd>Ctrl</kbd> + <kbd>C</kbd> e <kbd>Ctrl</kbd> + <kbd>V</kbd> respectivamente.

## Propriedades
Abaixo estão listadas as propriedades únicas deste widget. Este widget é 
composto por outros widgets, portanto consulte as seguintes páginas para 
referência de outras propriedades que este widget suporta.

- [Widgets Clicáveis]({{ site.baseurl }}/widgets/clickable#propriedades) 
- [GuiLabel]({{ site.baseurl }}/widgets/label#propriedades)

### Target
- Expressão representando o alvo que este widget deve alterar. Por exemplo: uma propriedade `Target` com valor 
`state["Usuario"]` guardará o nome digitado no widget.
A propriedade `Target` suporta o modificador `!` como prefixo, assegurando que o alvo será criado caso este 
não exista. Por exemplo, uma propriedade `Target` com valor `!config["NovoValor"]` criará a propriedade `NovoValor` 
caso esta já não exista em `config`.
- **Tipo:** str