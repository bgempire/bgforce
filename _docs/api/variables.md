---
title: Variáveis
description: "O módulo `scripts/bgf` dá acesso à variáveis que podem ser
utilizadas na programação de jogos no BGForce.
O uso de algumas dessas variáveis é essencial para uma boa lógica de jogo,
em especial o seu uso dentro de widgets."
---

# {{ page.title }}

{{ page.description }}

Todas as variáveis estão disponíveis nos escopos dos widgets, portanto é possível utilizá-las em comandos de
widgets clicáveis e em referências de dados fonte / alvo de listas, inputs e checkboxes. Caso deseje importar
essas variáveis no seu próprio script (dado um script na raiz da pasta `scripts`, por exemplo: `scripts/meuscript.py`):

```python
from .bgf import config
from .bgf import database
from .bgf import lang
from .bgf import sounds
from .bgf import state
```

## Referência
Abaixo estão listadas as variáveis disponíveis para uso no BGForce.

### `bgf.curPath`
- Caminho da pasta raiz do projeto como um objeto
[`pathlib.Path`][1].

- **Tipo:** [Path][1]

### `bgf.config`
- Configurações atuais do jogo. Pode ter seus dados alterados para personalizar
as configurações do jogo.
Veja sobre o arquivo de configuração padrão em [Config]({{ site.baseurl }}/database/config).

- **Tipo:** dict

```json
{
    "Lang" : "English",
    "BgmVol" : 0.8,
    "SfxVol" : 1.0,
    "BgmEnable" : true,
    "SfxEnable" : true
    ...
}
```

### `bgf.database`
- Base de dados do projeto. Contém o conteúdo de todos os arquivos na pasta
`database` carregados como dicionários.
Veja sobre a pasta da base de dados em [Database]({{ site.baseurl }}/database).

- **Tipo:** dict

```json
{
    "Config": {...},
    "Contexts": {...},
}
```

### `bgf.lang`
- Textos de tradução do projeto. Contém o conteúdo de todos os arquivos na pasta
`lang` carregados como dicionários.
Veja sobre a pasta de traduções em [Estrutura]({{ site.baseurl }}/structure#lang).

- **Tipo:** dict

```json
{
    "English": {
        "Cheering": "What's up, doc?"
    },
    "Portuguese": {
        "Cheering": "O que é que há, velhinho?"
    }
}
```

### `bgf.sounds`
- Caminhos de arquivo dos sons do jogo. Contém dois dicionários identificados
pelas palavras chave `"Bgm"` e `"Sfx"`, e esses dois dicionários contém de fato
os caminhos dos arquivos de som do jogo com seus respectivos nomes sem extensão.
Veja sobre as pastas de sons em [Estrutura]({{ site.baseurl }}/structure#sounds).

- **Tipo:** dict

```json
{
    "Bgm": {
        "SomedayCoyoteHearing": "/home/bgempire/bgforce/sounds/bgm/SomedayCoyoteHearing.ogg",
        "WriteYouJoeyPecoraro": "/home/bgempire/bgforce/sounds/bgm/WriteYouJoeyPecoraro.ogg"
    },
    "Sfx": {
        "Jump": "/home/bgempire/bgforce/sounds/sfx/Jump.wav",
        "Shoot": "/home/bgempire/bgforce/sounds/sfx/Shoot.wav"
    }
}
```

### `bgf.state`
- Estado atual do jogo. Permite armazenar pontuações, inventário, vida ou qualquer
dado que seja relevante de se manter durante o jogo e possa ser salvo. Defina o
estado inicial em [State]({{ site.baseurl }}/database/state).

- **Tipo:** dict

```json
{
    "Points": 355,
    "Lives": 2,
    "Scores": [512, 99, 477]
}
```

[1]: https://docs.python.org/3/library/pathlib.html#pathlib.Path
