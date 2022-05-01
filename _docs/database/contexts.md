---
title: Contexts
description: "Contextos no BGForce são definições de cenas e configurações que
serão usadas para alterar grupos de cenas, músicas e ainda fará transições
suaves ao alterar tais elementos, entre outras funcionalidades."
---

# {{ page.title }}

Jogos costumam ter diversas telas diferentes como: título, menu inicial, jogo, loja, etc. Cada uma dessas telas
é formada por diversos elementos que trabalham em conjunto para entregar o resultado como um todo, e isso inclui:

- Música do jogo
- Cenas desenhadas acima de todas as outras (como interfaces de usuário)
- Cenas com a mecânica principal do jogo (como um jogo de corrida ou luta)
- Cenas desenhadas abaixo de todas as outras (como planos de fundo de menus ou skyboxes)

Dessa forma, quando o jogo passa da tela título para o menu inicial, temos uma troca de diversas cenas que são
removidas do jogo para dar lugar às novas cenas, a música de fundo é alterada para uma nova e o estado do jogo
é alterado como um todo neste processo. Além disso, o jogador pode precisar pausar o jogo em algum momento, e
a pausa do jogo é um processo que pode mexer com algumas cenas e não mexer com outras. Gerenciar todos esses
elementos pode acabar sendo uma experiência trabalhosa, e pensando neste problema foi desenvolvido o sistema
de contextos do BGForce.

## Conceito
{{ page.description }}
Todas essas funcionalidades são executadas com o disparo de um operador [`SetContext`]({{ site.baseurl }}/operators/default#setcontext).
O arquivo que contém todas as definições de contextos do jogo é [`database/Contexts.json`]({{ site.baseurl }}/database/contexts).

Abaixo está o modelo comum da definição de um contexto:

```json
"Game": {
    "Default": true,
    "Bgm": "SomedayCoyoteHearing",
    "Loading": "ScnLoading",
    "Scenes": [
        {
            "Name": "ScnGameMap",
            "Pausable": false
        },
        {
            "Name": "ScnGame",
            "Pausable": true
        }
    ]
}
```

Vamos destrinchar cada elemento da definição:

- `"Game"`: Nome desse contexto. O framework trocará para esse contexto caso o operador `SetContext:Game` seja disparado.
    - `"Default"`: Indica que esse será o contexto inicial do jogo.
    - `"Bgm"`: Nome da música de fundo que será tocada quando esse contexto iniciar. Não precisa da extensão de arquivo.
    - `"Loading"`: Nome da cena de carregamento que será mostrada enquanto as outras cenas do contexto são carregadas no jogo.
    - `"Scenes"`: Lista contendo as definições das cenas que compõem o contexto. Serão adicionadas de cima para baixo, isto é, cenas do início da lista se mostrarão acima das cenas do fim da lista.
        - `"Name"`: Nome da cena a ser adicionada.
        - `"Pausable"`: Se esta cena será pausada caso o operador `PauseGame` seja disparado.

Nem todas as propriedades são obrigatórias nas definições de contexto:
- Caso `"Bgm"` não seja definida, o contexto não tocará nenhuma música.
- Caso `"Loading"` não seja definida, o contexto será alterado sem uma cena de intermediária de carregamento.
- Caso `"Default"` seja definida e verdadeira, este será o contexto inicial do jogo. Note que, apesar de ser opcional, essa propriedade é obrigatória em um dos contextos, caso contrário, o framework não saberá em qual contexto o jogo deverá iniciar.
