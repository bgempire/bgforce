---
title: Operadores Padrão
description: 
---

# Operadores Padrão
Os operadores padrão são aqueles que já estão disponíveis para uso no BGForce. 

**Importante:** Com exceção do operador `UpdateGui`, todos os outros operadores necessitam do componente 
[`ScnManager`](https://github.com/bgempire/bgforce/wiki/Componentes) ativo no jogo para serem executados.

## Referência

### SaveConfig
Salva as configurações de usuário atuais no arquivo `Config.json`.

**Exemplo:**
- `bge.logic.sendMessage("SaveConfig")`

### SetContext
Altera o contexto do jogo, substituindo o grupo de cenas atual pelo grupo de cenas definido no contexto especificado, e a música (caso especificada 
nas definições do contexto).

**Argumentos:**
- `NomeDoContexto`: Contexto alvo

**Exemplo:**
- `bge.logic.sendMessage("SetContext", "MainMenu")` mudará do contexto atual para o contexto `MainMenu` especificado em `database/Contexts.json`.

### UpdateGui
Solicita atualização dos widgets da interface de usuário, disparando as respectivas transições e atualizando seus textos.

**Argumentos:**
- Nenhum argumento: Atualiza todos os widgets
- `NomeDoGrupo`: Atualiza apenas os widgets que tenham a propriedade `Group` com os valores definidos neste argumento. 
Múltiplos grupos de widgets podem ser passados ao separá-los por vírgula.

**Exemplos:**
- `bge.logic.sendMessage("UpdateGui")` atualizará todos os widgets.
- `bge.logic.sendMessage("UpdateGui", "MenuDePausa")` atualizará todos os widgets com a propriedade `Group` com o valor `MenuDePausa`.
- `bge.logic.sendMessage("UpdateGui", "MenuDePausa,Hud,Outros")` atualizará todos os widgets com a propriedade `Group` com os valores `MenuDePausa`, `Hud` ou `Outros`.