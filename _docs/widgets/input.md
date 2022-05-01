---
title: GuiInput
description: "**GuiInputs** são entradas de texto digitado que alteram o valor de um alvo."
---

# GuiInput
![]({{ site.baseurl }}/assets/img/wiki-input-00.png)

{{ page.description }}
Eles tem suporte a ações de copiar e colar enquanto o cursor estiver ativo utilizando
os atalhos <kbd>Ctrl</kbd> + <kbd>C</kbd> e <kbd>Ctrl</kbd> + <kbd>V</kbd> respectivamente.

## Propriedades
Abaixo estão listadas as propriedades únicas deste widget. Este widget é
composto por outros widgets, portanto consulte as seguintes páginas para
referência de outras propriedades que este widget suporta.

- [Widgets Clicáveis]({{ site.baseurl }}/widgets/clickable#propriedades)
- [GuiLabel]({{ site.baseurl }}/widgets/label#propriedades)

### CharsAllowed
- Tipos de caracteres que poderão ser digitados neste input. Pode ter como valores alguma das strings (case insensitive):
  - `"All"`: Qualquer caractere
  - `"Alphabetic"`: Apenas letras de A-Z (maiúsculas e minúsculas)
  - `"AlphaNumericNoSpace"`: Apenas letras de A-Z e números de 0-9 (sem espaços)
  - `"AlphaNumeric"`: Letras de A-Z, números de 0-9 e espaços
  - `"Numeric"`: Apenas números de 0-9
  - `"Printable"`: Letras, números, espaços, sinais e pontuações
- Se uma string vazia for passada `"All"` será usado como padrão.
- Uma string como uma lista de caracteres pode ser passada caso apenas caracteres específicos devam ser permitidos (por exemplo, a string `"abcd"` apenas permitirá as letras contidas).
- **Tipo:** str

### CharsLimit
- Limite em número de caracteres que o usuário está permitido a digitar neste widget (por exemplo: `15`)
- **Tipo:** int

### CursorCharacter
- Caractere que será usado para representar o cursor piscante do widget (por exemplo: `"|"`).
- **Tipo:** str

### CursorSpeed
- Intervalo em que o `"CursorCharacter"` irá piscar em segundos (por exemplo, para piscar a cada 200 milissegundos: `0.2`).
- **Tipo:** float

### PasswordCharacter
- Caractere que será mostrado no lugar dos caracteres reais do texto, útil para ocultar senhas (por exemplo: `"*"`). Caso uma string vazia seja usada (padrão), o texto real será mostrado.
- **Tipo:** str

### PlaceholderColor
- Cor `[r, g, b, a]` do texto de placeholder do widget. Por exemplo, vermelho é: `[1.0, 0.0, 0.0, 1.0]`.
- **Tipo:** [float, float, float, float]

### PlaceholderColorDisabled
- Cor `[r, g, b, a]` do texto de placeholder quando a propriedade `Enabled` do widget é falsa. Por exemplo, verde é: `[0.0, 1.0, 0.0, 1.0]`.
- **Tipo:** [float, float, float, float]

### PlaceholderShadowColor
- Cor `[r, g, b, a]` da sombra do texto de placeholder do widget. Por exemplo, azul é: `[0.0, 0.0, 1.0, 1.0]`.
- **Tipo:** [float, float, float, float]

### PlaceholderShadowColorDisabled
- Cor `[r, g, b, a]` da sombra do texto de placeholder quando a propriedade `Enabled` do widget é falsa. Por exemplo, branco meio transparente é: `[1.0, 1.0, 1.0, 0.5]`.
- **Tipo:** [float, float, float, float]

### Target
- Expressão representando o alvo que este widget deve alterar. Por exemplo: uma propriedade `Target` com valor
`state["Usuario"]` guardará o nome digitado no widget.
A propriedade `Target` suporta o modificador `!` como prefixo, assegurando que o alvo será criado caso este
não exista. Por exemplo, uma propriedade `Target` com valor `!config["NovoValor"]` criará a propriedade `NovoValor`
caso esta já não exista em `config`.
- **Tipo:** str
