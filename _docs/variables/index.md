---
title: Variáveis
description: 
---

# Variáveis
O módulo `scripts/bgf` dá acesso à variáveis que podem ser utilizadas na programação de jogos no BGForce. 
O uso de algumas dessas variáveis é essencial para uma boa lógica de jogo, em especial o seu uso dentro de widgets.

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
Abaixo estão listadas as variáveis disponíveis para uso no BGForce. Todas elas são dicionários que são 
carregados dos respectivos arquivos de definições.

#### config
Configuração do jogo carregada de `Config.json`.

#### database
Base de dados do BGForce, contendo todos os dados lidos da pasta `database`. Os dados podem ser acessados 
a partir de múltiplos níveis, dependendo de como o arquivo lido foi estruturado.

#### lang
Dados de tradução utilizados por widgets com textos. Contém todos os dados dos arquivos lidos da pasta `lang`.

#### sounds
Contém os caminhos e definições de músicas e efeitos sonoros carregados das pastas `sounds/bgm` e `sounds/sfx`.

#### state
Contém o estado de dados do jogo. É um substituto ao 
[`bge.logic.globalDict`](https://docs.blender.org/api/2.79/bge.logic.html#bge.logic.globalDict). 
Sua diferença para o `globalDict` é que seus dados podem ter um estado inicial logo ao iniciar o jogo pela 
primeira vez, estado esse que pode ser alterado em `database/State.json`.