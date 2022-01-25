---
title: API
description: 
---

# {{ page.title }}

A seguir está apresentada a referência da API pública do BGForce. Ela contém variáveis 
e funções úteis nos mais diversos casos, desde salvamento e carregamento de arquivos, 
detecção de controles até reprodução de sons.

{%- for section in site.data.toc %}
{%- if section.url == "api" %}
{%- for link in section.links %}
- [{{ link.title }}]({{ site.baseurl }}/{{ link.url }})
{%- endfor %}
{%- endif %}
{%- endfor %}