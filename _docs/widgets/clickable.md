---
layout: page
title: Widgets Clicáveis
---

# Widgets Clicáveis
Um **widget clicável** é um controle que permite a execução de comandos ao ser clicado.
Todos os widgets, com exceção da [GuiLabel](https://github.com/bgempire/bgforce/wiki/GuiLabel), 
são clicáveis, e isso inclui:

- [GuiButton](https://github.com/bgempire/bgforce/wiki/GuiButton)
- [GuiIconButton](https://github.com/bgempire/bgforce/wiki/GuiIconButton)
- [GuiMeshButton](https://github.com/bgempire/bgforce/wiki/GuiMeshButton)
- [GuiCheckbox](https://github.com/bgempire/bgforce/wiki/GuiCheckbox)
- [GuiList](https://github.com/bgempire/bgforce/wiki/GuiList)
- [GuiInput](https://github.com/bgempire/bgforce/wiki/GuiInput)

## Comandos

Widgets clicáveis podem conter propriedades iniciando com o nome `Command` (por exemplo: `Command`, `Command1`, `Command2`, etc). 
Essas propriedades contém comandos que serão executados ao clicar no widget em questão. As propriedades serão colocadas em ordem 
alfabética e serão executadas uma após a outra (a menos que um modificador `!` seja usado).

### Modificador Instantâneo: `!`

O comando será executado no período intermediário entre o fim da transição de saída e o início da transição de 
entrada do widget, portanto ele não é executado imediatamente. Para executar o comando imediatamente ao clicar 
no widget, utilize o prefixo `!` no valor do comando. Por exemplo:

![](https://github.com/bgempire/bgforce/raw/gh-pages/img/wiki-referencia-instant.png)

### Tipos de Comandos
Existem três tipos de comandos, que serão explicados a seguir.

#### Comando de Mensagem
Um comando com um valor qualquer de texto será interpretado como uma mensagem. Usando um `:` no meio da expressão 
resultará no envio de uma mensagem com assunto e corpo divididos. Por exemplo: o commando com o valor 
`Assunto:Corpo` é o equivalente a enviar uma mensagem com `bge.logic.sendMessage("Assunto", "Corpo")`.

![](https://github.com/bgempire/bgforce/raw/gh-pages/img/wiki-referencia-command-message.png)

#### Comando Python: `>`
Um comando com um valor iniciado com o caractere `>` será interpretado como uma expressão em Python. Qualquer 
código Python é válido nesta expressão.

![](https://github.com/bgempire/bgforce/raw/gh-pages/img/wiki-referencia-command-python.png)

#### Comando de Posição de Câmera: `[x, y]`
Uma rotina comum em interfaces de usuário é mudar a posição da câmera para mostrar layouts de widgets diferentes. 
Um comando com um valor iniciado com `[` ou `(` será interpretado como uma coordenada, e transportará a câmera da 
cena do widget em questão para a posição `[x, y]` definida.

![](https://github.com/bgempire/bgforce/raw/gh-pages/img/wiki-referencia-command-camera.png)

## Propriedades
Abaixo estão listadas as propriedade comuns entre os widgets clicáveis.

### ColorClick
- Cor `[r, g, b, a]` do elemento clicável quando o mouse está clicando neste. Por exemplo, verde é: `[0.0, 1.0, 0.0, 1.0]`.
- **Tipo:** [float, float, float, float]

### ColorDisabled
- Cor `[r, g, b, a]` do elemento clicável quando a propriedade `Enabled` do widget é falsa. Por exemplo, branco meio transparente é: `[1.0, 1.0, 1.0, 0.5]`.
- **Tipo:** [float, float, float, float]

### ColorHover
- Cor `[r, g, b, a]` do elemento clicável quando o mouse está por cima deste. Por exemplo, azul é: `[0.0, 0.0, 1.0, 1.0]`.
- **Tipo:** [float, float, float, float]

### ColorNormal
- Cor `[r, g, b, a]` do elemento clicável quando o mouse não está por cima deste. Por exemplo, vermelho é: `[1.0, 0.0, 0.0, 1.0]`.
- **Tipo:** [float, float, float, float]

### Offset
- Deslocamento `[x, y]` do elemento clicável em relação ao centro da instância. Exemplo: `[0.5, -0.5]`.
- **Tipo:** [float, float]

### Size
- Fator de escala `[x, y]` do elemento clicável. Exemplo: `[1.5, 2.0]`.
- **Tipo:** [float, float]

### TransitionOnClick
- Especifica se o widget deve disparar as animações de transição ao ser clicado.
- **Tipo:** bool
