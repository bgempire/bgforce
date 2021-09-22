---
title: Estrutura
description: 
---

# Estrutura
A estrutura de arquivos do BGForce possui um padrão conciso e otimizado para o uso com o Blender Game Engine e UPBGE.
A seguir será explicado o objetivo de cada pasta e arquivo relevante do framework.

## database
A pasta `database` contém definições de estruturas de dados utilizadas pelo framework. O usuário está livre para 
adicionar novos arquivos à esta pasta e editar os arquivos existentes **contanto que não remova nenhum dos arquivos padrão**.

Os dados podem ser acessados como dicionários ao importar a variável `database` do módulo `scripts/bgf`.

#### Exemplo
Levando em conta um script qualquer que esteja dentro da pasta `scripts`, para importar `database` use o código:

```python
from .bgf import database

# Obter propriedade lida de database/Global.json
contextFadeSpeed = database["Global"]["ContextFadeSpeed"]
```

## fonts
A pasta `fonts` contém as fontes utilizadas pelos widgets de interface de usuário do framework. Basta substituir 
os arquivos de fontes existentes para alterar as fontes padrão da interface de usuário.

## lang
A pasta `lang` contém os arquivos de tradução usados pelos widgets com suporte a texto. O modelo dos arquivos de 
tradução segue o padrão: `"PalavraChave" : "Tradução"`, onde a palavra chave deve existir e ser igual em todos 
os arquivos da pasta `lang`, e a tradução deve conter o texto traduzido de fato.

Os dados podem ser acessados como dicionários ao importar a variável `lang` do módulo `scripts/bgf` (porém raramente 
isso será necessário, uma vez que os widgets de interface de usuário automatizam o processo de tradução).

#### Exemplo
Levando em conta um script qualquer que esteja dentro da pasta `scripts`, para importar `lang` use o código:

```python
from .bgf import lang

# Obter a propriedade lida de lang/English.json
langPrevious = lang["English"]["Previous"]
```

## scripts
A pasta `scripts` contém os scripts da lógica de programação do jogo. Em geral, o usuário está livre para adicionar seus 
próprios scripts à esta pasta.

**Observação:** Recomendamos que não altere o conteúdo da pasta `scripts/bgf` e nem remova a 
linha 1 do script `scripts/__init__.py` (onde há a importação do `scripts/bgf`), pois através destes intermediários que 
o framework carregará os dados e funcionará corretamente.

### scripts/bgf
O módulo `scripts/bgf` contém toda a lógica do framework. **Recomendamos que não altere o seu conteúdo.**

### scripts/__init__.py
O script `scripts/__init__.py` roda a inicialização do framework. O usuário está livre para editar este arquivo à vontade 
**contanto que não remova a linha 1** (onde há a importação do módulo `scripts/bgf`).

### scripts/operators.py
O script `scripts/operators.py` permite que funções sejam facilmente executadas através de mensagens. O usuário está 
livre para editar este arquivo à vontade **contanto que não remova a declaração do dicionário `OPERATORS`**. 
O dicionário `OPERATORS` deve conter o padrão `"NomeDoOperador" : funcaoEmPython`, e a partir disso será possível 
executar as funções através de uma mensagem como `NomeDoOperador:Argumentos`. Veja mais em 
[Operadores Customizados](https://github.com/bgempire/bgforce/wiki/Operadores-Customizados).

## sounds
A pasta `sounds` contém os sons utilizados no jogo. Ao iniciar o jogo, a lista de todos os sons dentro 
desta pasta será carregada, e permitirá ao framework reproduzir estes sons através de mensagens 
específicas para esse fim. Ela contém duas subpastas.

### sounds/bgm
A pasta `sounds/bgm` contém as músicas que serão tocadas no jogo. O usuário está livre para excluir 
as músicas de exemplo existentes nesta pasta e adicionar suas próprias músicas, que poderão ser 
facilmente reproduzidas através de uma mensagem `PlayBgm:NomeDaMusica` ou definindo a música para uma 
propriedade `"Bgm"` em algum contexto em `database/Contexts.json`.

### sounds/sfx
A pasta `sounds/sfx` contém os efeitos sonoros que serão tocados no jogo. O usuário está livre para excluir 
os sons de exemplo existentes nesta pasta e adicionar seus próprios sons, que poderão ser 
facilmente reproduzidos através de uma mensagem `PlaySfx:NomeDoSom`.

## textures
A pasta `textures` contém as texturas do jogo. Em geral, o usuário está livre para adicionar suas próprias texturas 
nesta pasta conforme a necessidade.

### textures/gui
A pasta `textures/gui` contém as texturas dos widgets de interface de usuário. O usuário está livre para personalizar 
as texturas existentes para criar seu próprio tema de interface de usuário.

## LibBgf.blend
O arquivo `LibBgf.blend` contém todos os grupos e componentes (cenas) necessários para o funcionamento do framework. Nele se encontram:

- Grupos de [widgets](https://github.com/bgempire/bgforce/wiki/Widgets) de interface de usuário
- Cenas de [componentes](https://github.com/bgempire/bgforce/wiki/Componentes)
    - ScnManager (gerenciador do BGForce)
    - ScnMouseCursor (cursor do mouse personalizável)

Basta linkar (`File` > `Link`) os dados a partir de outro arquivo blend para utilizar suas funcionalidades.

## Config.json
O arquivo `Config.json` contém as configurações de usuário do jogo. O usuário está livre para adicionar novas 
configurações a este arquivo **contanto que não remova as configurações existentes**.

Os dados podem ser acessados como um dicionário ao importar a variável `config` do módulo `scripts/bgf`.

#### Exemplo
Levando em conta um script qualquer que esteja dentro da pasta `scripts`, para importar `config` use o código:

```python
from .bgf import config

# Obter propriedade lida de Config.json
volSfx = config["VolSfx"]
```