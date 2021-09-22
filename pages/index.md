---
layout: page
title: BGForce
permalink: /
---

# BGForce

Bem vindo ao manual do BGForce! Aqui você encontrará o manual e as definições do 
framework, além de dicas de como usar as features. Utilize o menu de navegação 
para achar o que procura.

## Índice

{%- for section in site.data.toc %}
- [{{ section.title }}]({{ section.url }})
{%- if section.links %}
    {%- for link in section.links %}
    - [{{ link.title }}]({{ link.url }})
    {%- endfor %}
{%- endif %}
{%- endfor %}