---
title: State
description: 
---

# State
O arquivo `database/State.json` contém o estado inicial padrão do jogo.
O objetivo de state é ser um substituto ao `bge.logic.globalDict`, armazenando 
o estado do jogo como pontuação, fase atual, inventário ou qualquer outro dado 
relevante para o jogo, e assim pode salvo e carregado do disco.
O estado pode conter qualquer tipo de dado, uma vez que varia de jogo para jogo.

## Exemplo
Um exemplo básico do estado de um jogo como Space Invaders está demonstrado a seguir:

```json
{
    "Score": 0,
    "Lives": 3,
    "Scores": []
}
```

Neste exemplo, `"Score"` e `"Lives"` seriam respectivamente a pontuação e as vidas 
do jogador durante uma fase do jogo, e uma vez que o jogador perdesse todas as vidas, 
a `"Score"` seria adicionada à lista de `"Scores"`, e ambas `"Score"` e `"Lives"` 
seria resetadas aos seus estados iniciais para iniciar a fase novamente.
Tendo essa lógica, o estado poderia ser salvo para guardar permanentemente as 
pontuações das partidas anteriores.