---
layout: page
title: Widgets
permalink: /widgets
---

# Widgets
![]({{ site.baseurl }}/assets/img/wiki-gui-00.jpg)

O BGForce provê um poderoso sistema de interfaces de usuário altamente customizável. Esta seção visa detalhar o uso dessas funcionalidades.

## Conceito
Os widgets de interface de usuário do BGForce são baseados no uso de bibliotecas do Blender (linked libraries).
Uma vez que os grupos dos widgets são instanciados no arquivo blend desejado é possível adicionar propriedades
para customizar o comportamento dos widgets. Existem vários widgets para diversos fins e com diversas opções de customização disponíveis.

## Como Usar
Para utilizar um widget do BGForce:

- Crie um novo arquivo blend na raiz do projeto (na mesma pasta em que está o arquivo `LibBgf.blend`)
- Dentro deste blend selecione a opção `File` > `Link`
  - Selecione o arquivo `LibBgf.blend`
  - Selecione `Group`
  - Selecione algum widget desejado
  - Clique duas vezes ou no botão `Link from Library`

Com isso será instanciado no blend atual o widget selecionado. Nesta instância é possível adicionar propriedades para
personalizar o widget de acordo com a necessidade.

## Personalização
Abaixo estão definidos os arquivos que permitem a personalização do sistema de GUI do BGForce.

### database/Bgf.json
O arquivo `database/Bgf.json` contém, entre outras configurações globais, as
definições padrão de todos os widgets disponíveis, e apesar de encorajarmos
você a não alterar os valores, este arquivo pode ser personalizado para definir
os valores padrão dos widgets.

### database/Styles.json
O arquivo `database/Styles.json` contém definições de estilos personalizados.
O conceito de estilos no BGForce é semelhante ao conceito de classes em CSS,
portanto vários widgets podem compartilhar um único estilo.

#### Exemplo
Cinco widgets de texto tem o objetivo de serem títulos, e devido a isso, eles terão tamanhos e cores diferentes
do padrão, mas semelhantes entre si. Neste caso:

- Defina um estilo de título em `database/Styles.json`:

```json
"Título" : {
    "LabelColor" : [1.0, 1.0, 0.0, 1.0],
    "LabelSize" : 1.0,
    "Justify" : "Center"
}
```

- Adicione em todos os widgets de texto que deverão ter esse estilo uma propriedade com a classe criada:

![]({{ site.baseurl }}/assets/img/wiki-gui-01.jpg)

### fonts
A pasta `fonts` contém as fontes `.ttf` utilizadas por cada widget específico. Substituir as fontes padrão por
novas fontes irá resultar na alteração das fontes dos widgets.

### textures/gui
A pasta `textures/gui` contém as texturas de todos os widgets. Substituir as texturas padrão por novas texturas
irá resultar na alteração do tema visual dos widgets. A resolução e proporção das texturas podem ser alteradas,
mas é necessário manter a mesma quantidade de tiles e suas distâncias em cada textura.

## Propriedades
Todos os widgets possuem as seguintes propriedades em comum, todas disponíveis para edição em suas
respectivas instâncias,`database/Styles.json`.

### Enabled
- Se o widget está ativado. Isso afeta diversas funcionalidades, desde sua aparência até a possibilidade de ser clicado (caso seja um widget clicável).
    - Pode ser um booleano literal ou uma string com uma expressão em Python. Por exemplo: `config["Fullscreen"] == True`.
    - Não tem efeito se adicionado em `database/Styles.json`, apenas funciona caso adicionado como propriedade na instância do widget.
- **Tipo:** bool ou str

### Group
- Nome do grupo de widgets ao qual essa instância pertence. Pode ser qualquer valor em string.
    - É usado pelo operador `UpdateGui` para atualizar apenas widgets que pertencem a determinado grupo.
    - Não tem efeito se adicionado em `database/Styles.json`, apenas funciona caso adicionado como propriedade na instância do widget.
- **Tipo:** str

### Transition
- Permite adicionar uma animação ao solicitar a atualização dos widgets através do operador `UpdateGui`.
As animações disponíveis são: `SlideL`, `SlideR`, `ScaleV`, `ScaleH` e `Arc`.
- **Tipo:** str

### TransitionSpeed
- Multiplicador de velocidade de animação de transição do widget.
- **Tipo:** float

### Update
- Intervalo de atualização da lógica do widget em quadros. Quanto maior o valor, maior o tempo entre cada atualização. Por exemplo: um valor de `60` fará o widget atualizar sua lógica a cada 60 quadros (1 segundo).
    - É diferente da propriedade `UpdateFrequency`, pois tem prioridade sobre esta e atualiza os textos do widget independentemente da transição. **Útil em labels que precisam ser atualizadas em tempo real**.
    - Não tem efeito se adicionado em `database/Styles.json`, apenas funciona caso adicionado como propriedade na instância do widget.
- **Tipo:** int

### Style
- Nome do estilo em [database/Styles.json]({{ site.baseurl }}/database/styles) que será aplicado neste widget.
- **Tipo:** str

### UpdateFrequency
- Intervalo de atualização da lógica do widget em quadros. Quanto maior o valor, maior o tempo entre cada atualização. Por exemplo: um valor de `60` fará o widget atualizar sua lógica a cada 60 quadros (1 segundo).
- **Tipo:** int
