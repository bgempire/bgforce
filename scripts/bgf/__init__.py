import bge
import aud

from pathlib import Path


# Constants
DEBUG = True
VARIABLE_PREFIX = "$"


# Helper variables
curPath = Path(__file__).parent.parent.resolve()


# Global variables
config = {} # type: dict[str, object]
database = {} # type: dict[str, dict | list]
lang = {} # type: dict[str, dict[str, str]]
state = {} # type: dict[str, object]
cache = {} # type: dict[str, object]
sounds = {} # type: dict[str, dict[str, str]]
requests = {} # type: dict[str, object]


def __loadFramework():
    # type: () -> None
    """Main function called at start."""
    
    from ast import literal_eval
    global DEBUG, config, database, lang, state, cache, sounds, requests, curPath
    
    if DEBUG: print("\n> Initializing framework")
    
    curPath = Path(bge.logic.expandPath("//")).resolve()
    config = bge.logic.__config = loadFile(curPath / "Config")
    database = bge.logic.__database = loadFiles(curPath / "database")
    lang = bge.logic.__lang = loadFiles(curPath / "lang")
    state = bge.logic.__state = literal_eval(str(database["State"]))
    requests = bge.logic.__requests = {}
    sounds = bge.logic.__sounds = {
        "Sfx" : getFilePaths(curPath / "sounds/sfx"),
        "Bgm" : getFilePaths(curPath / "sounds/bgm")
    }
    
    # Get numeric definitions of resolutions
    bge.logic.__resolutions = getResolutions()
    
    # Remove outdated keys from config
    configKeys = tuple(config.keys())
    
    for key in configKeys:
        if not key in database["Config"].keys():
            del config[key]
    
    # Add to config new keys from database
    for key in database["Config"].keys():
        if not key in config.keys():
            config[key] = database["Config"][key]
    
    database["Keys"] = getGameKeys()
    
    bge.render.showMouse(database["Global"]["MouseNative"])
    processExitKey(database["Global"]["ExitKey"])
    if DEBUG: print("> Framework initializated\n")
    DEBUG = database["Global"]["Debug"]


def processExitKey(key):
    # type: (str | int) -> None
    
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
        if i and not i.startswith(("//", "#")):
            fileData.append(i.strip())
            
    return "".join(fileData)


def __replaceDictVariables(target, variables=None):
    # type: (dict, dict) -> None
    """Replaces all variable values from dict recursively."""
    
    from ast import literal_eval
        
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


def loadFile(_file):
    # type: (Path) -> dict
    """Load file from given path and return its content as a dict."""
    
    import json
    import zlib
    from ast import literal_eval
                
    if not _file.exists() and _file.parent.exists():
        for f in _file.parent.iterdir():
            if f.stem == _file.stem:
                _file = f
                break
    
    data = {}
    relativePath = _file.as_posix().replace(curPath.as_posix(), "")[1:]
    loaded = False
    isDict = True
        
    if _file.suffix in (".json", ".jsonc"):
        with open(_file.as_posix(), "r", encoding="utf-8") as openedFile:
            dataRaw = __getJsonNoComments(openedFile.read())
            isDict = dataRaw.startswith("{")
            
            try:
                data = json.loads(dataRaw)
                loaded = True
            except Exception as e:
                if DEBUG: print(e)
                try:
                    data = literal_eval(openedFile.read())
                    loaded = True
                except:
                    if DEBUG: print("X Could not load file:", relativePath)
                    
        # Process variables
        if isDict: __replaceDictVariables(data)
            
    elif _file.suffix == ".dat":
        with open(_file.as_posix(), "rb") as openedFile:
            data = json.loads(__getJsonNoComments(zlib.decompress(openedFile.read()).decode(encoding="utf-8")))
            loaded = True
            
    if loaded:
        if DEBUG: print("> File loaded:", relativePath)
            
    return data


def loadFiles(directory, pattern=""):
    # type: (Path, str) -> dict
    """Get all files from given directory recursively, 
    load their content and return data as dict."""
    
    from fnmatch import filter
    if DEBUG: print("> Loading files from:", directory.as_posix().replace(curPath.as_posix(), "")[1:])
    data = {}
    
    for _file in directory.iterdir():
        
        if _file.is_dir():
            data[_file.name] = loadFiles(_file, pattern=pattern)
            
        elif _file.suffix in (".json", ".jsonc", ".dat"):
            if not pattern or filter([_file.name], pattern):
                data[_file.stem] = loadFile(_file)
            
    return data


def saveFile(_file, data, ext=None):
    # type: (Path, object, str) -> None
    
    import json
    import zlib
    from pprint import pformat
    
    saved = False
    
    if ext is None:
        ext = _file.suffix
    else:
        _file = _file.with_suffix(ext)
    
    if ext in (".json", ".jsonc"):
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
            print("> Saved file to:", relativePath)


def getFilePaths(directory):
    # type: (Path) -> dict
    """Get all files from given directory and return dict with name : path relations."""
    
    relativePath = directory.as_posix().replace(curPath.as_posix(), "")[1:]
    if DEBUG: print("> Getting files from:", relativePath)
    data = {}

    if directory.exists():
        for _file in directory.iterdir():
            data[_file.stem] = _file.as_posix()
            if DEBUG:
                print("> File get:", _file.as_posix().replace(curPath.as_posix(), "")[1:])
                    
    else:
        directory.mkdir(parents=True)
        
    return data


def getGameKeys():
    # type: () -> dict[str, dict]
    
    keys = {
        "NameCode" : {},
        "CodeName" : {},
    }
    
    for alias in dir(bge.events):
        if alias.isupper():
            code = eval("bge.events." + alias)
            keys["NameCode"][alias] = code
            keys["CodeName"][code] = alias
            
    return keys


def getResolutions():
    # type: () -> dict[str, list]
    
    resolutions = {}
    displayDimensions = list(bge.render.getDisplayDimensions())
    
    for resolution in database["Resolutions"]:
        resolution = str(resolution)
        
        if resolution:
            if not resolution[0].isnumeric():
                resolutions[resolution] = displayDimensions
                
            else:
                resolutionList = resolution.lower().split("x")
                resolutionList = [int(r) for r in resolutionList]
                
                if resolutionList[0] <= displayDimensions[0] \
                and resolutionList[1] <= displayDimensions[1]:
                    resolutions[resolution] = resolutionList
                else:
                    resolutions[resolution] = displayDimensions
            
    return resolutions


def isKeyPressed(key, status=bge.logic.KX_INPUT_ACTIVE):
    # type: (str | int, int) -> bool
    
    def _checkInputStatus(key, status):
        # type: (bge.types.SCA_InputEvent, int) -> bool
            
        if status == bge.logic.KX_INPUT_NONE:
            return key.inactive
            
        elif status == bge.logic.KX_INPUT_JUST_ACTIVATED:
            return key.activated
        
        elif status == bge.logic.KX_INPUT_ACTIVE:
            return key.active
            
        elif status == bge.logic.KX_INPUT_JUST_RELEASED:
            return key.released
    
    _keyboard = bge.logic.keyboard # type: bge.types.SCA_PythonKeyboard
    _mouse = bge.logic.mouse # type: bge.types.SCA_PythonMouse
    
    # Get key code
    if type(key) == str:
        if not key.endswith("KEY"):
            key += "KEY"
            
        key = database["Keys"]["NameCode"].get(key) # type: int
        
    elif type(key) != int:
        return
    
    if key:
        
        # Check UPBGE inputs
        if hasattr(bge.app, "upbge_version_string"):
            keyPressed = _mouse.inputs.get(key) # type: bge.types.SCA_InputEvent
            
            if keyPressed != None:
                return _checkInputStatus(keyPressed, status=status)
                
            else:
                keyPressed = _keyboard.inputs.get(key) # type: bge.types.SCA_InputEvent
                
                if keyPressed != None:
                    return _checkInputStatus(keyPressed, status=status)
            
        # Check BGE events
        else:
            keyPressed = _mouse.events.get(key)
            
            if keyPressed != None:
                return keyPressed == status
            else:
                return _keyboard.events.get(key) == status


def playSound(sound, origin=None):
    # type: (str, bge.types.KX_GameObject) -> aud.Handle
    """Play specific sound."""
    
    if sound.startswith("./"):
        sound = curPath / sound if (curPath / sound).exists() else None
    else:
        sound = sounds["Sfx"].get(sound) # type: str
        sound = Path(sound) if sound else None # type: Path
        
    if sound:
        device = aud.device() # type: aud.Device
        factory = aud.Factory.file(sound.as_posix())
        handle = device.play(factory) # type: aud.Handle
        handle.volume = config["SfxVol"]
        
        if origin:
            device.distance_model = aud.AUD_DISTANCE_MODEL_LINEAR
            device.listener_location = origin.scene.active_camera.worldPosition
            device.listener_orientation = origin.scene.active_camera.worldOrientation.to_quaternion()
            device.listener_velocity = origin.scene.active_camera.getLinearVelocity()
            
            handle.relative = False
            handle.location = origin.worldPosition
            handle.velocity = origin.getLinearVelocity()
            handle.distance_maximum = 50
            handle.distance_reference = 1
        
        return handle


def _(key):
    # type: (str) -> str
    """Get translation of provided key from current language set in config."""
    
    curLang = lang[config["Lang"]] # type: dict[str, str]
    
    if key in curLang.keys():
        return lang[config["Lang"]][key]
    else:
        return ""


def dump(obj, file="dump.py"):
    # type: (object, str) -> None
    """ Dump to file the object content. """
    
    from pprint import pformat
    file = curPath / file # type: Path
    
    with open(file.as_posix(), "w") as _file:
        _file.write(pformat(obj))
        print("> Dumped object to", file.as_posix())

try:
    __loadFramework()
except Exception as exc:
    print(exc)
