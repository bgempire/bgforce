---
title: Operadores Padrão
description: 
---

# {{ page.title }}

Os operadores padrão são aqueles que já estão disponíveis para uso no BGForce. 

**Importante:** Com exceção do operador `UpdateGui`, todos os outros operadores necessitam do componente 
[`ScnManager`]({{ site.baseurl }}/components) ativo no jogo para serem executados.

## Referência

### ApplyConfig
Aplica as configurações de vídeo no jogo.

**Exemplo:**
- `bge.logic.sendMessage("ApplyConfig")`

### ExitGame
Toca uma transição e sai do jogo.

**Exemplo:**
- `bge.logic.sendMessage("ExitGame")`

### HideMouseCursor
Oculta o cursor do mouse do componente `ScnMouseCursor`.

**Exemplo:**
- `bge.logic.sendMessage("HideMouseCursor")`

### LoadState
Carrega os dados salvos do [`state`][1] a partir de `save.dat` ou `save/*.dat`, onde `*` é o nome de arquivo passado como argumento.

**Argumentos:**
- `NomeDoArquivo`: Nome do arquivo de estado a se carregar (opcional)

**Exemplos:**
- `bge.logic.sendMessage("LoadState")` carregará `save.dat` para o estado
- `bge.logic.sendMessage("LoadState", "slot1")` carregará `save/slot1.dat` para o estado

### PauseContext
Pausa todas as cenas do contexto atual. Apenas cenas com a propriedade `"Pausable": true` em `database/Contexts.json` serão afetadas.

**Exemplo:**
- `bge.logic.sendMessage("PauseContext")`

### PlayBgm
Toca uma música específica da pasta `sounds/bgm`, também tocando a respectiva transição. 
O argumento passado não deve conter a extensão do arquivo de som.

**Argumentos:**
- `NomeDoArquivo`: Nome do arquivo sem extensão

**Exemplo:**
Para tocar a música `sounds/bgm/WriteYouJoeyPecoraro.ogg`:

- `bge.logic.sendMessage("PlayBgm", "WriteYouJoeyPecoraro")`

### PlaySfx
Toca um efeito sonoro específico da pasta `sounds/sfx`. O argumento passado não deve conter a extensão do arquivo de som.

**Argumentos:**
- `NomeDoArquivo`: Nome do arquivo sem extensão

**Exemplo:**
Para tocar o som `sounds/sfx/Jump.wav`:

- `bge.logic.sendMessage("PlaySfx", "Jump")`

### ResumeContext
Resume todas as cenas do contexto atual. Apenas cenas com a propriedade `"Pausable": true` em `database/Contexts.json` serão afetadas.

**Exemplo:**
- `bge.logic.sendMessage("ResumeContext")`

### SaveConfig
Salva as configurações de usuário atuais no arquivo `Config.json`.

**Exemplo:**
- `bge.logic.sendMessage("SaveConfig")`

### SaveState
Salva os dados do [`state`][1] no arquivo `save.dat` ou `save/*.dat`, onde `*` é o nome de arquivo passado como argumento.

**Argumentos:**
- `NomeDoArquivo`: Nome do arquivo a se salvar (opcional)

**Exemplos:**
- `bge.logic.sendMessage("SaveState")` salvará o estado em `save.dat`
- `bge.logic.sendMessage("SaveState", "slot1")` salvará o estado em `save/slot1.dat`

### SetContext
Altera o contexto do jogo, substituindo o grupo de cenas atual pelo grupo de cenas definido no contexto especificado, e a música (caso especificada 
nas definições do contexto).

**Argumentos:**
- `NomeDoContexto`: Contexto alvo

**Exemplo:**
- `bge.logic.sendMessage("SetContext", "MainMenu")` mudará do contexto atual para o contexto `MainMenu` especificado em `database/Contexts.json`.

### ShowMouseCursor
Exibe o cursor do mouse do componente `ScnMouseCursor`.

**Exemplo:**
- `bge.logic.sendMessage("ShowMouseCursor")`

### StopBgm
Para de tocar a música atual, também tocando a respectiva transição.

**Exemplo:**
- `bge.logic.sendMessage("StopBgm")`

### UpdateGui
Solicita atualização dos widgets da interface de usuário, disparando as respectivas transições e atualizando seus textos.

**Argumentos:**
- Nenhum argumento: Atualiza todos os widgets
- `NomeDoGrupo`: Atualiza apenas os widgets que tenham a propriedade `Group` com os valores definidos neste argumento. 
Múltiplos grupos de widgets podem ser passados ao separá-los por vírgula.
- `PosicaoDaCamera`: Toca a transição dos widgets e move a câmera para a posição especificada.

**Exemplos:**
- `bge.logic.sendMessage("UpdateGui")` atualizará todos os widgets.
- `bge.logic.sendMessage("UpdateGui", "MenuDePausa")` atualizará todos os widgets com a propriedade `Group` com o valor `MenuDePausa`.
- `bge.logic.sendMessage("UpdateGui", "MenuDePausa,Hud,Outros")` atualizará todos os widgets com a propriedade `Group` com os valores `MenuDePausa`, `Hud` ou `Outros`.
- `bge.logic.sendMessage("UpdateGui", "[50, 0]")` atualizará todos os widgets e moverá a câmera para a posição `x = 50` e `y = 0`.


[1]: {{ site.baseurl }}/api/variables#bgfstate