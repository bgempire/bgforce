---
title: Variáveis
description: 
---

# Variáveis

### `bgf.curPath`
- Caminho da pasta raiz do projeto como um objeto 
[`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path).

- **Tipo:** [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)

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
