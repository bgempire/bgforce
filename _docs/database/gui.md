---
title: Gui
description: 
---

# {{ page.title }}

O arquivo `database/Gui.json` contém as definições de estilos e comportamento padrão dos 
widgets de interface de usuário do framework. Os dados podem ser editados à vontade, 
porém **nenhum deles pode ser removido**, uma vez que eles são parte do núcleo de funcionamento 
dos widgets.

Alterar as definições deste arquivo afetará o visual e comportamento dos widgets 
de forma **global** no projeto. Caso seu intuito seja estilizar e personalizar os widgets de interface de usuário 
sem alterá-los globalmente, crie estilos personalizados em [`database/Styles.json`]({{ site.baseurl }}/database/styles).

## Propriedades
- Para referência de propriedades dos widgets, veja suas respectivas propriedades em [`Widgets`]({{ site.baseurl }}/widgets).
- Para referência de propriedades do cursor do mouse, veja suas respectivas propriedades em [`ScnMouseCursor`]({{ site.baseurl }}/components/mousecursor).