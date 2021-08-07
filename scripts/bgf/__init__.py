import bge
import json
import zlib

from bge.logic import globalDict
from ast import literal_eval
from pathlib import Path
from pprint import pformat


# Constants
DEBUG = True
VARIABLE_PREFIX = "$"


# Helper variables
curPath = Path(bge.logic.expandPath("//")).resolve()


# Global variables
config = {}
database = {}
lang = {}
state = {}
cache = {}
sounds = {}
requests = {}


def loadFramework():
    # type: () -> None
    """Main function called at start."""
    
    global DEBUG, config, database, lang, state, cache, sounds, requests
    
    if DEBUG: print("\n> Initializing framework")
    
    config = bge.logic.__config = loadFile(curPath / "Config")
    database = bge.logic.__database = loadFiles(curPath / "database")
    lang = bge.logic.__lang = loadFiles(curPath / "lang")
    state = bge.logic.__state = literal_eval(str(database["State"]))
    cache = bge.logic.__cache = getFilePaths(curPath / ".cache")
    requests = bge.logic.__requests = {}
    sounds = bge.logic.__sounds = {
        "Sfx" : getFilePaths(curPath / "sounds/sfx"),
        "Bgm" : getFilePaths(curPath / "sounds/bgm")
    }
    
    bge.render.showMouse(database["Global"]["MouseNative"])
    processExitKey(database["Global"]["ExitKey"])
    if DEBUG: print("> Framework initializated\n")
    DEBUG = database["Global"]["Debug"]


def processExitKey(key):
    keyCode = bge.events.ESCKEY
    
    # Get int constant from str key
    if type(key) == str:
        key = key.upper()
        
        if hasattr(bge.events, key):
            keyCode = eval("bge.events." + key)
            
        elif hasattr(bge.events, key + "KEY"):
            keyCode = eval("bge.events." + key + "KEY")
            
    # Validate int key
    elif type(key) == int:
        for k in dir(bge.events):
            if k.isupper():
                curKeyCode = eval("bge.events." + k)
                if key == curKeyCode:
                    keyCode = key
                    break
    
    bge.logic.setExitKey(keyCode)


def __getJsonNoComments(fileContent):
    # type: (str) -> str
    
    fileData = []
    
    for i in fileContent.splitlines():
        i = i.strip()
        if i and not i.startswith("//"):
            fileData.append(i.strip())
            
    return "".join(fileData)


def __replaceDictVariables(target, variables=None):
    # type: (dict, dict) -> None
    """Replaces all variable values from dict recursively."""
        
    # Move all variables from top level to its own dict
    if variables is None:
        variables = {}
        
        for key in target.keys():
            if key.startswith(VARIABLE_PREFIX):
                variables[key] = str(target[key])
                
        for key in variables.keys():
            del target[key]
    
    for key in target.keys():
        
        # Replace variables with respective values
        if type(target[key]) == str and target[key] in variables.keys():
            value = variables[target[key]]
            
            try:
                value = literal_eval(value)
            except:
                pass
            
            target[key] = value
            
        # Do replacement recursively
        elif type(target[key]) == dict:
            __replaceDictVariables(target[key], variables)


def loadFile(_file, debugIndent=0):
    # type: (Path, int) -> dict
    """Load file from given path and return its content as a dict."""
                
    if not _file.exists() and _file.parent.exists():
        for f in _file.parent.iterdir():
            if f.stem == _file.stem:
                _file = f
                break
    
    data = {}
    relativePath = _file.as_posix().replace(curPath.as_posix(), "")[1:]
    loaded = False
        
    if _file.suffix == ".json":
        with open(_file.as_posix(), "r", encoding="utf-8") as openedFile:
            try:
                data = json.loads(__getJsonNoComments(openedFile.read()))
                loaded = True
            except Exception as e:
                if DEBUG: print(e)
                try:
                    data = literal_eval(openedFile.read())
                    loaded = True
                except:
                    if DEBUG: print((debugIndent * " ") + "X Could not load file:", relativePath)
                    
        # Process variables
        __replaceDictVariables(data)
            
    elif _file.suffix == ".dat":
        with open(_file.as_posix(), "rb") as openedFile:
            data = json.loads(__getJsonNoComments(zlib.decompress(openedFile.read()).decode(encoding="utf-8")))
            loaded = True
            
    if loaded:
        if DEBUG: print((debugIndent * " ") + "> File loaded:", relativePath)
            
    return data


def loadFiles(directory, debugIndent=0):
    # type: (Path, int) -> dict
    """Get all files from given directory, load their content and return data as dict."""
    
    relativePath = directory.as_posix().replace(curPath.as_posix(), "")[1:]
    if DEBUG: print((debugIndent * " ") + "> Loading files from:", relativePath)
    data = {}

    for _file in directory.iterdir():
        if _file.suffix in (".json", ".dat"):
            data[_file.stem] = loadFile(_file, debugIndent=debugIndent + 2)
            
    return data


def saveFile(_file, data, ext=None, debugIndent=0):
    # type: (Path, object, str, int) -> None
    saved = False
    
    if ext is None:
        ext = _file.suffix
    else:
        _file = _file.with_suffix(ext)
    
    if ext == ".json":
        with open(_file.as_posix(), "w", encoding="utf-8") as openedFile:
            try:
                openedFile.write(json.dumps(data, indent=4))
            except Exception as e:
                if DEBUG: print(e)
                openedFile.write(pformat(data, indent=4))
            finally:
                saved = True
    
    elif ext == ".dat":
        with open(_file.as_posix(), "wb") as openedFile:
            openedFile.write(zlib.compress(json.dumps(data).encode(encoding="utf-8")))
            saved = True
            
    if saved:
        if DEBUG:
            relativePath = _file.as_posix().replace(curPath.as_posix(), "")[1:]
            print((debugIndent * " ") + "> Saved file to:", relativePath)


def getFilePaths(directory, debugIndent=0):
    # type: (Path, int) -> dict
    """Get all files from given directory and return dict with name : path relations."""
    
    relativePath = directory.as_posix().replace(curPath.as_posix(), "")[1:]
    if DEBUG: print((debugIndent * " ") + "> Getting files from:", relativePath)
    data = {}

    if directory.exists():
        for _file in directory.iterdir():
            data[_file.stem] = _file.as_posix()
            if DEBUG:
                print(((debugIndent + 2) * " ") + "> File get:", 
                    _file.as_posix().replace(curPath.as_posix(), "")[1:])
                    
    else:
        directory.mkdir(parents=True)
        
    return data


loadFramework()