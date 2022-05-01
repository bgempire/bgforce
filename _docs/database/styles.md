---
title: Styles
description: "BGForce suporta em seus widgets a funcionalidade de estilos,
que emula a ideia das classes de CSS, isto é, um estilo pode ser definido
com um nome específico e pode ser usado de forma compartilhada em diversos
widgets diferentes."
---

# {{ page.title }}

{{ page.description }}

Semelhante às classes de CSS, os estilos não necessitam que todas as
propriedades de determinado widget sejam especificadas, apenas aquelas que
se deseja personalizar.

## Criando Um Estilo
Para criar um estilo personalizado, simplesmente adicione um novo dicionário em
`database/Styles.json` sob qualquer nome que desejar e adicione as propriedades
que deseja estilizar neste dicionário.
Por exemplo, caso desejemos criar dois estilos, um para títulos e outro para
textos centralizados, adicionamos o seguinte em `database/Styles.json`:

```json
{
    "Title" : {
        "LineSize" : 28,
        "LabelSize" : 1.0,
        "LabelColor": [1.0, 1.0, 0.3, 1.0],
        "Justify" : "Center"
    },
    "TextCentered": {
        "LineSize" : 40,
        "LabelSize" : 0.7,
        "Justify" : "Center"
    }
}
```

Em seguida, adicionamos nos respectivos widgets que desejamos aplicar
os estilos a propriedade `Style` contendo os nomes dos respectivos estilos.
Neste caso, temos as propriedades do widget que será o título:

![]({{ site.baseurl }}/assets/img/styles-example-props-title.png)

E temos as propriedades do widget que será o texto centralizado:

![]({{ site.baseurl }}/assets/img/styles-example-props-textcentered.png)

E por fim, teremos como resultado cada widget com seus respectivos estilos aplicados:

![]({{ site.baseurl }}/assets/img/styles-example-result.png)

Desta forma, todos os widgets futuros que também venham ser títulos ou textos
centralizados só precisarão conter a propriedade `Style` referenciando seus
respectivos estilos, assim permitindo a reusabilidade de estilos e facilitando
a manutenção do projeto, uma vez que para alterar o visual de todos os títulos
do jogo basta alterar um único estilo.
