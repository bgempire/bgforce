---
title: Config
description: 
---

# Config
O arquivo `database/Config.json` contém as definições de configurações padrão do jogo.
O usuário pode adicionar novas configurações ao jogo (como teclas de controles, 
dificuldade do jogo, etc), mas **não deve remover as configurações existentes** ainda que 
não as utilize no jogo.

## Propriedades
Abaixo estão listadas as propriedades válidas deste arquivo.

### Lang
- Linguagem do jogo, deve ser o nome de um dos arquivos em `lang` (sem extensão).

- **Tipo:** str

### BgmVol
- Volume da música. Tem efeito na música tocada por [contextos]({{ site.baseurl }}/database/contexts) 
ou pelo operador [`PlayBgm`]({{ site.baseurl }}/operators/default#playbgm).

- **Tipo:** float

### BgmEnable
- Se a reprodução de música está ativada. Tem efeito na música tocada por 
[contextos]({{ site.baseurl }}/database/contexts) ou pelo operador 
[`PlayBgm`]({{ site.baseurl }}/operators/default#playbgm).

- **Tipo:** bool

### SfxVol
- Volume dos efeitos sonoros. Tem efeito nos sons tocados pelo operador 
[`PlaySfx`]({{ site.baseurl }}/operators/default#playsfx).

- **Tipo:** float

### SfxEnable
- Se a reprodução de efeitos sonoros está ativada. Tem efeito nos sons tocados 
pelo operador [`PlaySfx`]({{ site.baseurl }}/operators/default#playsfx).

- **Tipo:** bool

### Resolution
- Resolução de tela. Tem efeito caso aplicada com o operador 
[`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- **Tipo:** str
- **Exemplo:** `"1280x720"`

### Fullscreen
- Se o jogo deve rodar em tela cheia. Tem efeito caso aplicado com o operador 
[`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- **Tipo:** bool

### AnisotropicFiltering
- Nível da filtragem anisotrópica. Tem efeito caso aplicado com o operador 
[`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- **Tipo:** int
- **Valores:** `1`, `2`, `4`, `8` ou `16`

### Mipmaps
- Tipo de mipmapping. Tem efeito caso aplicado com o operador 
[`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- **Tipo:** str
- **Valores:** `"None"`, `"Nearest"` ou `"Linear"`

### MotionBlur
- Nível do desfoque de movimento. Tem efeito caso aplicado com o operador 
[`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- **Tipo:** float (`0.0` a `1.0`)

### Vsync
- Ativar sincronização vertical. Tem efeito caso aplicado com o operador 
[`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- **Tipo:** bool

### Lights
- Ativar luzes. Tem efeito caso aplicado com o operador 
[`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- **Tipo:** bool

### Shaders
- Ativar shaders. Tem efeito caso aplicado com o operador 
[`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- **Tipo:** bool

### Shadows
- Ativar sombras. Tem efeito caso aplicado com o operador 
[`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- **Tipo:** bool

### Ramps
- Ativar ramps de materiais. Tem efeito caso aplicado com o operador 
[`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- **Tipo:** bool

### Nodes
- Ativar nós de materiais. Tem efeito caso aplicado com o operador 
[`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- **Tipo:** bool

### ExtraTextures
- Ativar texturas extras (normal maps, specular maps, etc). Tem efeito caso 
aplicado com o operador [`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- **Tipo:** bool

