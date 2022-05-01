---
title: Componentes
description: "BGForce contém alguns componentes que podem ser adicionados ao jogo.
Estes componentes estão no formato de cenas dentro do arquivo **`LibBgf.blend`**,
e podem ser linkadas (`File` > `Link`) no arquivo blend principal do jogo para uso."
---

# {{ page.title }}

{{ page.description }}

## Índice
Abaixo estão listados os componentes disponíveis para uso no BGForce.

{%- for section in site.data.toc %}
{%- if section.url == "components" %}
{%- for link in section.links %}
- [{{ link.title }}]({{ site.baseurl }}/{{ link.url }})
{%- endfor %}
{%- endif %}
{%- endfor %}