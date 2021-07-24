import bge
import json
import pathlib
import zlib

from bge.logic import globalDict
from ast import literal_eval
from pathlib import Path
from pprint import pprint, pformat

# Constants
DEBUG = 1
DEBUG_INDENT = 2

# Global variables
curPath = Path(bge.logic.expandPath("//")).resolve()


def loadFramework():
    if DEBUG: print("\n> Initializing framework")
    
    globalDict["Config"] = loadFile(curPath / "Config", debugIndent=DEBUG_INDENT)
    globalDict["Database"] = loadFiles(curPath / "database", debugIndent=DEBUG_INDENT)
    globalDict["Locale"] = loadFiles(curPath / "locale", debugIndent=DEBUG_INDENT)
    
    globalDict["Sounds"] = {
        "Sfx" : getFilePaths(curPath / "sounds/sfx", debugIndent=DEBUG_INDENT),
        "Bgm" : getFilePaths(curPath / "sounds/bgm", debugIndent=DEBUG_INDENT)
    }
    
    if DEBUG:
        # saveFile(curPath / "GlobalDictDump.json", globalDict, debugIndent=DEBUG_INDENT)
        print("> Framework initializated\n")


def loadFile(_file, debugIndent=0):
    # type: (Path, int) -> dict
    """Load file from given path and return its content as a dict."""
    
    def replaceVariables(target, variables):
        # type: (dict, dict) -> None
        
        for key in target.keys():
            if type(target[key]) == str and target[key] in variables.keys():
                value = variables[target[key]]
                try:
                    value = literal_eval(value)
                except:
                    pass
                target[key] = value
                
            elif type(target[key]) == dict:
                replaceVariables(target[key], variables)
                
                
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
                fileData = []
                for i in openedFile.read().splitlines():
                    i = i.strip()
                    if i and not i.startswith("//"):
                        fileData.append(i.strip())
                        
                data = json.loads("".join(fileData))
                loaded = True
            except Exception as e:
                if DEBUG: print(e)
                try:
                    data = literal_eval(openedFile.read())
                    loaded = True
                except:
                    if DEBUG: print((debugIndent * " ") + "X Could not load file:", relativePath)
                    
        # Process variables
        variables = {}
        
        for key in data.keys():
            if key.startswith("$"):
                variables[key] = str(data[key])
                
        for key in variables.keys():
            del data[key]
            
        replaceVariables(data, variables)

    elif _file.suffix in [".cfg", ".ini"]:
        
        with open(_file.as_posix(), "r", encoding="utf-8") as openedFile:
            fileData = []
                        
            for line in openedFile.read().split("\n"):
                if line != "" and not line.startswith("#") and not line.isspace():
                    fileData.append(line.strip())
                
            curSection = None
            variables = {}
            
            for item in fileData:
                
                if item.startswith("["):
                    item = item.replace("[", "").replace("]", "").strip()
                    curSection = item
                    data[item] = {}
                    
                else:
                    item = [i.strip() for i in item.split("=", 1)] # type: list[str]
                    
                    if len(item) == 2:
                        itemKey = item[0]
                        itemVal = variables[item[1]] if item[1] in variables.keys() else item[1]
                        
                        try:
                            itemVal = literal_eval(itemVal)
                        except:
                            pass
                            
                        if itemKey.startswith("$"):
                            variables[itemKey] = itemVal
                        elif curSection is not None:
                            data[curSection][itemKey] = itemVal
                        else:
                            data[itemKey] = itemVal
                        
            loaded = True
            
    elif _file.suffix == ".dat":
        with open(_file.as_posix(), "rb") as openedFile:
            data = json.loads(zlib.decompress(openedFile.read()).decode(encoding="utf-8"))
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
        if _file.suffix in (".json", ".ini", ".cfg", ".dat"):
            data[_file.stem] = loadFile(_file, debugIndent=debugIndent + DEBUG_INDENT)
            
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
            openedFile.write(zlib.compress(str(data).encode()))
            saved = True
    
    elif ext in (".cfg", ".ini"):
        with open(_file.as_posix(), "w", encoding="utf-8") as openedFile:
            fileContentTop = ""
            fileContent = ""
            if hasattr(data, "keys"):
                for key in data.keys():
                    if not hasattr(data[key], "keys"):
                        fileContentTop += str(key) + "=" + str(data[key]) + "\n"
                    elif hasattr(data[key], "keys"):
                        fileContent += "\n[" + str(key) + "]\n"
                        for subKey in data[key].keys():
                            fileContent += str(subKey) + "=" + str(data[key][subKey]) + "\n"
            openedFile.write(fileContentTop + fileContent)
                    
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
                print(((debugIndent + DEBUG_INDENT) * " ") + "> File get:", 
                    _file.as_posix().replace(curPath.as_posix(), "")[1:])
                    
    else:
        directory.mkdir(parents=True)
        
    return data


loadFramework()