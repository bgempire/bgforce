---
title: Global
description: 
---

# Global
O arquivo `database/Global.json` contém configurações gerais que são aplicadas de 
forma global ao jogo.

## Propriedades
Abaixo estão listadas as propriedades válidas deste arquivo.

### BgmFadeSpeed
- Velocidade da transição entre músicas.

- **Tipo:** bool

### Cache
- Ativar cache de arquivos.

- **Tipo:** bool

### ContextFadeSpeed
- Velocidade da transição da troca de contextos.

- **Tipo:** float

### Debug
- Ativar mensagens de debug no console.

- **Tipo:** bool

### ExitKey
- Tecla de saída do jogo. Exemplos: `"F12"`, `"Esc"`, `0` (desativar).

- **Tipo:** str ou int

### MouseNative
- Mostrar o cursor do mouse nativo do sistema operacional.

- **Tipo:** bool

### StartupOperators
- Lista de operadores que deverão ser executados automaticamente ao iniciar o jogo.

- **Tipo:** list[str]

