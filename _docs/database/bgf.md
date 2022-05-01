---
title: Bgf
description:
---

# {{ page.title }}

O arquivo `database/Bgf.json` contém configurações globais do framework, desde
configurações gerais até definições de propriedades de interface usuário.


## Global
O objeto `"Global"` contém configurações gerais que são aplicadas de forma global ao jogo.

### Propriedades
Abaixo estão listadas as propriedades válidas deste arquivo.

#### BgmFadeSpeed
- Velocidade da transição entre músicas.

- **Tipo:** bool

#### Cache
- Ativar cache de arquivos.

- **Tipo:** bool

#### ContextFadeSpeed
- Velocidade da transição da troca de contextos.

- **Tipo:** float

#### Debug
- Ativar mensagens de debug no console.

- **Tipo:** bool

#### ExitKey
- Tecla de saída do jogo. Exemplos: `"F12"`, `"Esc"`, `0` (desativar).

- **Tipo:** str ou int

#### MouseNative
- Mostrar o cursor do mouse nativo do sistema operacional.

- **Tipo:** bool

#### StartupOperators
- Lista de operadores que deverão ser executados automaticamente ao iniciar o jogo.

- **Tipo:** list[str]


## Gui
O objeto `"Gui"` contém as definições de estilos e comportamento padrão dos
widgets de interface de usuário do framework. Os dados podem ser editados à
vontade, porém não encorajamos esta alteração e **nenhum deles pode ser removido**,
uma vez que eles são parte do núcleo de funcionamento dos widgets.

Alterar as definições deste arquivo afetará o visual e comportamento dos
widgets de forma **global** no projeto. Caso seu intuito seja estilizar e
personalizar os widgets de interface de usuário sem alterá-los globalmente,
crie estilos personalizados em [`database/Styles.json`]({{ site.baseurl }}/database/styles).

### Propriedades
- Para referência de propriedades dos widgets, veja suas respectivas propriedades em
    [`Widgets`]({{ site.baseurl }}/widgets).
- Para referência de propriedades do cursor do mouse, veja suas respectivas propriedades em
    [`ScnMouseCursor`]({{ site.baseurl }}/components/mousecursor).
