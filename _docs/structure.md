---
title: Estrutura
description: 
---

# {{ page.title }}

A estrutura de arquivos do BGForce possui um padrão conciso e otimizado para o uso com o Blender Game Engine e UPBGE.
A seguir será explicado o objetivo de cada pasta e arquivo relevante do framework.

## database
A pasta `database` contém definições de estruturas de dados utilizadas pelo framework. Veja mais em [Database]({{ site.baseurl }}/database).

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

### scripts/\_\_init\_\_.py
O script `scripts/__init__.py` roda a inicialização do framework. O usuário está livre para editar este arquivo à vontade 
**contanto que não remova a linha 1** (onde há a importação do módulo `scripts/bgf`).

### scripts/computed.py
O script `scripts/computed.py` possui definições de funções que retornam informações dinâmicas, 
e podem ser usadas nos widgets em qualquer propriedade que utilize uma expressão em Python. Veja mais em 
[Variáveis Computadas]({{ site.baseurl }}/variables/computed).

### scripts/operators.py
O script `scripts/operators.py` permite que funções sejam facilmente executadas através de mensagens. O usuário está livre para editar este script à vontade. 
Uma vez que uma função que receba dois argumentos seja definida (`def nomeDaFuncao(cont, args="")`) será possível 
executar as funções através de uma mensagem como `NomeDaFuncao:Argumentos`. Veja mais em 
[Operadores Customizados]({{ site.baseurl }}/operators/custom).

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

- Grupos de [widgets]({{ site.baseurl }}/widgets) de interface de usuário
- Cenas de [componentes]({{ site.baseurl }}/components)
    - ScnManager (gerenciador do BGForce)
    - ScnMouseCursor (cursor do mouse personalizável)

Basta linkar (`File` > `Link`) os dados a partir de outro arquivo blend para utilizar suas funcionalidades.

## Config.json
O arquivo `Config.json` contém as configurações de usuário salvas do jogo. Este arquivo é criado com base no arquivo de 
definições padrão [`database/Config.json`]({{ site.baseurl }}/database/config), que é seu modelo. Desta forma, este arquivo 
é atualizado sempre as configurações de usuário são salvos, diferente de seu modelo que é estático. Este arquivo pode 
não existir enquanto o usuário não solicitar o salvamento de configurações através do operador 
[`SaveConfig`]({{ site.baseurl }}/operators/default#saveconfig).

Os dados podem ser acessados como um dicionário ao importar a variável `config` do módulo `scripts/bgf`.

#### Exemplo
Levando em conta um script qualquer que esteja dentro da pasta `scripts`, para importar `config` use o código:

```python
from .bgf import config

# Obter propriedade lida de Config.json
volSfx = config["VolSfx"]
```