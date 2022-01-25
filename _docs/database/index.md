---
title: Database
description: 
---

# {{ page.title }}

A pasta `database` contém definições de estruturas de dados utilizadas pelo framework. O usuário está livre para 
**adicionar** novos arquivos à esta pasta e editar os arquivos existentes **contanto que não remova nenhum dos arquivos padrão**.

Os dados podem ser acessados como dicionários ao importar a variável `database` do módulo `scripts/bgf`. 

#### Exemplo
Levando em conta um script qualquer que esteja dentro da pasta `scripts`, para importar `database` use o código:

```python
from .bgf import database

# Obter propriedade lida de database/Global.json
contextFadeSpeed = database["Global"]["ContextFadeSpeed"]
```

## Variáveis
Para facilitar o reuso de dados, os arquivos JSON do BGForce suportam a funcionalidade de variáveis. Para utilizá-las, 
crie uma propriedade com o prefixo `$` e atribua um valor a esta, e então use o nome desta propriedade onde quiser que seu 
valor seja utilizado. Por exemplo:

```json
{
    "$CorPrincipal": [1.0, 0.0, 0.0, 1.0],
    "$CorSecundária": [0.0, 1.0, 0.0, 1.0],
    
    "CorDoJogador": "$CorPrincipal",
    "CorDoPet": "$CorPrincipal",
    "CorDoInimigo": "$CorSecundária",
    "CorDoChefe": "$CorSecundária",
}
```

Ao acessar `"CorDoJogador"` ou `"CorDoPet"` dentro do jogo, seus valores serão o mesmo que `"$CorPrincipal"`, ou seja, 
a cor vermelha `[1.0, 0.0, 0.0, 1.0]`. Dessa forma, caso precisemos alterar a `"CorDoJogador"` e `"CorDoPet"` ao mesmo tempo 
só precisaremos alterar `"$CorPrincipal"`, então as demais também se alterarão. O uso de variáveis no JSON não é obrigatório e em 
dados mais simples sequer é necessário, mas em árvores de dados que contém muitos valores pode facilitar muito a nossa vida 
(veja o arquivo [`database/Gui.json`]({{ site.baseurl }}/database/gui) como exemplo de um caso desses) .

**Nota:** As variáveis não existem durante a execução do jogo, portanto no exemplo acima será impossível acessar `"$CorPrincipal"` 
como uma propriedade desta árvore de dados.

## Arquivos
Os arquivos de definições do framework possuem particularidades relacionadas às suas funcionalidades, e estas estão 
descritas em suas respectivas páginas.

{%- for section in site.data.toc %}
{%- if section.url == "database" %}
{%- for link in section.links %}
- [{{ link.title }}]({{ site.baseurl }}/{{ link.url }})
{%- endfor %}
{%- endif %}
{%- endfor %}