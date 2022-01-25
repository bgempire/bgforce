---
title: Componentes
description: 
---

# {{ page.title }}

![]({{ site.baseurl }}/assets/img/wiki-components-00.png)

A cena `ScnManager` é o gerenciador principal do BGForce. Apenas através do uso dela que podemos 
utilizar os recursos de:

- [Execução de operadores]({{ site.baseurl }}/operators)
- [Troca de contextos]({{ site.baseurl }}/database/contexts)
- Reprodução de música e efeitos sonoros
- Transição de fade in/out de música e cenas

A cena `ScnManager` **deve ser a cena ativa no arquivo blend principal do jogo**, e a partir dela as definições 
de contextos do jogo serão obedecidas, adicionando e removendo outras cenas automaticamente e podendo executar 
as mais diversas ações por meio dos operadores.
