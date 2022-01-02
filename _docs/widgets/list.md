---
title: GuiList
description: 
---

# GuiList
![]({{ site.baseurl }}/assets/img/wiki-list-00.png)

Em progresso...

## Propriedades
Abaixo estão listadas as propriedades únicas deste widget. Este widget é 
composto por outros widgets, portanto consulte as seguintes páginas para 
referência de outras propriedades que este widget suporta.

- [Widgets Clicáveis]({{ site.baseurl }}/widgets/clickable#propriedades) 
- [GuiLabel]({{ site.baseurl }}/widgets/label#propriedades)

### List
- Expressão apontando a lista fonte que o widget deve percorrer. Por ser uma expressão em Python, a lista também pode ser gerada ao invés de ser uma referência.
- **Tipo:** list

**Exemplos:**
- `['Yes', 'No']`: Lista literal.
- `database["Resolutions"]`: Referência para uma lista da database.
- `[i/10 for i in range(0, 11)]`: Lista com 10 valores de `0.0` a `1.0` gerada programaticamente.

### Sort
- Por padrão, as listas serão exibidas em sua ordem original. Caso `Sort` seja verdadeiro, organiza a lista alfabeticamente.
- **Tipo:** bool

### Target
- Expressão representando o alvo que este widget deve alterar. Por exemplo: uma propriedade `Target` com valor 
`config["Resolution"]` irá alterar a resolução nas configurações a cada clique de acordo com o valor mostrado. 
A propriedade `Target` suporta o modificador `!` como prefixo, assegurando que o alvo será criado caso este 
não exista. Por exemplo, uma propriedade `Target` com valor `!config["NovoValor"]` criará a propriedade `NovoValor` 
caso esta já não exista em `config`.
- **Tipo:** str

### Translate
- Caso seja verdadeiro, tenta traduzir o valor selecionado de acordo com a configuração da linguagem atual. Caso 
não haja uma tradução, mostra o valor original. Vale notar que esta é apenas uma opção visual: o valor mostrado 
será traduzido, mas o valor guardado em `Target` continuará sendo o valor original obtido de `List`.
- **Tipo:** bool

### Value
- Caso fornecido, o widget se comportará como um radio button, alterando o `Target` apenas para o valor de `Value` 
ao invés de alternar entre verdadeiro e falso. Este valor pode ser de qualquer tipo, e será avaliado como tal, isto é, 
um `Value` do tipo inteiro irá guardar em `Target` um inteiro.
- **Tipo:** any