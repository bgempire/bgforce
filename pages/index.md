---
layout: page
title: Home
permalink: /
description: "Bem vindo ao manual do BGForce! Aqui você encontrará o manual e as definições
do framework, além de dicas de como usar as features."
---

# BGForce

{{ page.description }}

Você pode fazer o download do último release do framework
[aqui](https://github.com/bgempire/bgforce/releases).

## Índice

{%- for section in site.data.toc %}
- [{{ section.title }}]({{ section.url }})
{%- if section.links %}
    {%- for link in section.links %}
    - [{{ link.title }}]({{ link.url }})
    {%- endfor %}
{%- endif %}
{%- endfor %}