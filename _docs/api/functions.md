---
title: Funções
description: 
---

# Funções

### `bgf._(key)`
- Retorna a tradução de `key` com base na linguagem atual definida em 
[`bgf.config["Lang"]`]({{ site.baseurl }}/api/variables#config).

**Parâmetros:**
- `key` (str) - Palavra chave da tradução

**Retorna:** str


### `bgf.dump(obj, file="dump.py")`
- Salva a representação em string de um objeto de Python em um arquivo. Útil 
para fins de depuração.

**Parâmetros:**
- `obj` (object) - Objeto em Python, pode ser string, dict, list ou qualquer outro tipo
- `file` (str) - Nome do arquivo onde salvará o conteúdo (opcional)


### `bgf.getFilePaths(directory)`
- Retorna um dicionário contendo todos os caminhos de arquivo de uma pasta no padrão 
`{"Arquivo" : "Caminho/Para/Arquivo.txt"}`. As chaves não possuem extensão do nome do arquivo.

**Parâmetros:**
- `directory` (str) - Caminho da pasta

**Retorna:** dict


### `bgf.isKeyPressed(key, status=bge.logic.KX_INPUT_ACTIVE)`
- Retorna se uma tecla específica está sendo pressionada.

**Parâmetros:**
- `key` (str ou int) - Nome ou código da tecla ([ver constantes][1])
- `status` (int) - Status de pressionamento da tecla ([ver constantes][2])

**Retorna:** bool


### `bgf.loadFile(file)`
- Carrega um arquivo `file` e retorna seu conteúdo como um dicionário. Suporta 
JSON, JSONC e JSON codificado com [zlib](https://docs.python.org/3/library/zlib.html).

**Parâmetros:**
- `directory` ([Path][3]) - Caminho do arquivo

**Retorna:** dict


### `bgf.loadFiles(directory, pattern="")`
- Carrega todos os arquivos de `directory` e retorna seu conteúdo como um dicionário. 
Suporta JSON, JSONC e JSON codificado com [zlib][4].
Caso `pattern` seja 

**Parâmetros:**
- `directory` ([Path][3]) - Caminho do diretório
- `pattern` (str) - Padrão [glob](https://docs.python.org/3/library/fnmatch.html) para filtrar arquivos por nome (opcional)

**Retorna:** dict


### `bgf.playSound(sound, origin=None)`
- Executa um som de nome `sound` da pasta `sounds/sfx` (sem extensão). Caso um 
objeto `origin` seja fornecido, executará o som como 3D usando as coordenadas deste.

**Parâmetros:**
- `sound` (str) - Nome do som
- `origin` ([KX_GameObject](https://docs.blender.org/api/2.79/bge.types.KX_GameObject.html)) - Objeto de referência para executar o som como 3D (opcional)

**Retorna:** dict


### `bgf.saveFile(file, data, ext=None)`
- Salva no caminho de `file` os dados de `data` como JSON. Caso `ext` seja fornecida, 
usará esta como extensão de arquivo.

**Parâmetros:**
- `file` ([Path][3]) - Caminho do arquivo a ser salvo
- `data` (dict) - Dado a ser salvo
- `ext` (str) - Extensão a ser usada no arquivo, suporta `".json"`, `".jsonc"` e `".dat"` (JSON 
codificado com [zlib][4])

**Retorna:** dict


[1]: https://docs.blender.org/api/2.79/bge.events.html#keys-constants
[2]: https://docs.blender.org/api/2.79/bge.logic.html#id5
[3]: https://docs.python.org/3/library/pathlib.html#pathlib.Path
[4]: https://docs.python.org/3/library/zlib.html