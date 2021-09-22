---
layout: page
title: GuiLabel
---

# GuiLabel
![](https://github.com/bgempire/bgforce/raw/gh-pages/img/wiki-label-00.png)

**GuiLabels** são rótulos de texto dinâmicos que permitem a exibição de textos a partir de diversas fontes, sejam elas:

- Textos estáticos
- Textos dinâmicos
- Traduções

A principal propriedade para uma GuiLabel é a propriedade `Label`, que terá um texto estático ou uma referência para um texto dinâmico.

## Textos Estáticos

![](https://github.com/bgempire/bgforce/raw/gh-pages/img/wiki-label-01.png)

Os textos estáticos são simplesmente um texto simples definido para a propriedade `Label`.

## Textos Dinâmicos

![](https://github.com/bgempire/bgforce/raw/gh-pages/img/wiki-label-02.png)

Os textos dinâmicos são um valor obtido através de uma expressão de Python. É possível obter resultados de chamadas de funções, 
valores de listas ou qualquer outra expressão que esteja disponível no escopo.

Os textos dinâmicos utilizam um caractere `>` antes da expressão.

## Traduções

![](https://github.com/bgempire/bgforce/raw/gh-pages/img/wiki-label-03.png)

Traduções são um tipo especial de texto dinâmico que variam de acordo com a linguagem definida no `Config.json` na raiz do projeto.

As traduções utilizam um caractere `#` seguido de uma palavra chave que deve estar disponível nos arquivos de linguagem 
na pasta `lang`. Por exemplo:

- Definir a propriedade `Label` para `#Yes`
- Em `lang/English.json`
    - `"Yes" : "Yes"`
- Em `lang/Portugues.json`
    - `"Yes" : "Sim"`

Neste caso, a GuiLabel mostrará `"Yes"` caso a linguagem definida em `Config.json` for `"English"`, e mostrará `"Sim"` caso a linguagem definida em `Config.json` for `"Portugues"`.

**Observação:** A sintaxe de tradução nada mais é do que um atalho para a expressão de texto dinâmico:
- `lang[config["Lang"]]["PalavraChave"]`.

## Propriedades
Abaixo estão listadas as propriedades comuns entre os widgets com labels.

### Justify
- Alinhamento do texto. Pode ser `Left`, `Center` ou `Right`.
- **Tipo:** str

### LabelColor
- Cor `[r, g, b, a]` do texto. Por exemplo, vermelho é: `[1.0, 0.0, 0.0, 1.0]`.
- **Tipo:** [float, float, float, float]

### LabelColorDisabled
- Cor `[r, g, b, a]` do texto quando a propriedade `Enabled` do widget é falsa. Por exemplo, verde é: `[0.0, 1.0, 0.0, 1.0]`.
- **Tipo:** [float, float, float, float]

### LabelOffset
- Deslocamento `[x, y]` do texto em relação ao centro da instância. Exemplo: `[0.5, -0.5]`.
- **Tipo:** [float, float]

### LabelSize
- Fator de escala do texto, também afeta o tamanho da sombra. Exemplo: `0.65`.
- **Tipo:** float

### LineSize
- Especifica o número de caracteres que cada linha de texto terá antes de sua quebra. Também afeta o comportamento da propriedade `Justify`.
- **Tipo:** int

### ShadowColor
- Cor `[r, g, b, a]` da sombra do texto. Por exemplo, azul é: `[0.0, 0.0, 1.0, 1.0]`.
- **Tipo:** [float, float, float, float]

### ShadowColorDisabled
- Cor `[r, g, b, a]` da sombra do texto quando a propriedade `Enabled` do widget é falsa. Por exemplo, branco meio transparente é: `[1.0, 1.0, 1.0, 0.5]`.
- **Tipo:** [float, float, float, float]

### ShadowEnable
- Especifica a sombra será visível.
- **Tipo:** bool

### ShadowOffset
- Deslocamento `[x, y]` da sombra do texto em relação ao centro da instância. Exemplo: `[0.5, -0.5]`.
- **Tipo:** [float, float]
