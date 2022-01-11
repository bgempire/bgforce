---
title: Resolutions
description: 
---

# Resolutions
O arquivo `database/Resolutions.json` contém uma lista de resoluções que estarão 
disponíveis para uso no jogo.

- A propriedade `"Resolution"` de [`Config.json`]({{ site.baseurl }}/structure#configjson) 
deve ser um dos valores contidos nesta lista, e esta resolução será aplicada ao disparar 
o operador [`ApplyConfig`]({{ site.baseurl }}/operators/default#applyconfig).

- Os valores devem manter o padrão `"HxV"`, por exemplo `"1280x720"`, com exceção do 
valor `"Native"`, que representa a resolução nativa.

## Exemplo
Um exemplo básico da da lista de resoluções está demonstrado a seguir:

```json
[
    "Native",
    "960x540",
    "1024x576",
    "1280x720",
    "1366x768",
    "1920x1080"
]
```